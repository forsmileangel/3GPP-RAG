"""Evidence gate — decide ANSWER / LOW_CONFIDENCE / REFUSE for a retrieval
result set (Phase A Week 4, Step 5).

The spec's "evidence check before generation": rather than let an answer
layer hallucinate from weak hits, score the retrieval result and refuse
("目前索引資料不足以回答") when the evidence is too thin.

KEY DESIGN POINT: the gate is a RUNTIME mechanism, so it must work from a
bare user query. It CANNOT use a question's expected_section /
expected_keywords — those exist only for benchmark questions and are the
evaluation ORACLE, not gate inputs. Every runtime signal is query-agnostic:

    top_score_norm      strength of the #1 hit, normalized to [0,1]
                        (sign-corrected per backend; see normalize_top_score)
    section_consistency do the top hits concentrate on one clause, or scatter?
    term_coverage       fraction of the query's salient terms present in the
                        retrieved chunk text (FULL text, never the preview)
    result_count        how many candidates retrieval returned at all

Pure decision logic (make_gate_decision) is separated from the one IO step
(gate_for_hits fetches full chunk text), mirroring apply_rerank vs
search_reranked in rerank.py.
"""

from __future__ import annotations

import enum
import math
import re
from collections import Counter
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from typing import Protocol

from sqlalchemy.orm import Session

from src.config import settings

from ._textfetch import fetch_full_texts

# Normalization reference scales — algorithmic constants like RRF_K, tuned in
# M4. rrf_score for a hit ranked #1 by BOTH backends is ~2/(60+1) ≈ 0.033, so
# RRF_REF maps that to ~1.0. A strong FTS5 bm25 magnitude runs ~8-15.
RRF_REF = 0.033
BM25_REF = 12.0
_SCORE_ATTRS = ("rerank_score", "rrf_score", "distance", "bm25_score")

# Group sibling subsections (6.3.4.2 / .3 / .4) under one clause "6.3.4" when
# measuring how concentrated the top hits are.
CLAUSE_DEPTH = 3

# A single scalar per mode scales the score-space thresholds (floors); the
# weights and min_results stay fixed. >1 = stricter (refuse more readily),
# <1 = more permissive (answer / reach more readily).
_MODE_MULTIPLIERS = {"strict": 1.25, "balanced": 1.0, "permissive": 0.6}


class GateOutcome(enum.StrEnum):
    ANSWER = "answer"
    LOW_CONFIDENCE = "low_confidence"
    REFUSE = "refuse"


class _Hit(Protocol):
    """Structural type for a retrieval hit the gate consumes. The relevance
    score lives under a backend-specific attribute (see _SCORE_ATTRS) and is
    read via getattr, so it is not part of the protocol."""
    chunk_id: int
    section_number: str


@dataclass(frozen=True)
class GateSignals:
    """Query-agnostic evidence signals for one retrieval result set."""
    result_count: int
    top_score_norm: float | None   # [0,1]; None when there are no hits
    section_consistency: float     # [0,1] concentration of top hits on one clause
    term_coverage: float           # [0,1] query terms found in chunk text
    dominant_section: str | None   # modal clause prefix among the top hits
    backend: str


@dataclass(frozen=True)
class GateThresholds:
    min_results: int
    min_top_score: float
    strong_score: float
    answer_floor: float
    low_floor: float
    w_score: float
    w_consist: float
    w_cover: float

    @classmethod
    def for_mode(cls, mode: str = "balanced") -> GateThresholds:
        """Build thresholds for a mode. balanced = config defaults; strict
        raises the floors (refuses more readily); permissive lowers them
        (answers / reaches more readily). Modes change only VALUES, never the
        decision logic. Unknown mode raises ValueError."""
        if mode not in _MODE_MULTIPLIERS:
            raise ValueError(
                f"unknown gate mode {mode!r}; valid: {sorted(_MODE_MULTIPLIERS)}"
            )
        mult = _MODE_MULTIPLIERS[mode]
        return cls(
            min_results=settings.gate_min_results,
            min_top_score=min(settings.gate_min_top_score * mult, 1.0),
            strong_score=min(settings.gate_strong_score * mult, 1.0),
            answer_floor=min(settings.gate_answer_floor * mult, 1.0),
            low_floor=min(settings.gate_low_floor * mult, 1.0),
            w_score=settings.gate_w_score,
            w_consist=settings.gate_w_consist,
            w_cover=settings.gate_w_cover,
        )


@dataclass(frozen=True)
class GateDecision:
    outcome: GateOutcome
    confidence: float   # [0,1]: confidence in the action taken
    reason: str         # names the deciding numeric comparison
    signals: dict       # asdict(GateSignals) — for the report / debugging


# ----------------------------------------------------------- pure signals

_QUERY_TOKEN_RE = re.compile(r"[A-Za-z0-9§\-./]+")  # mirrors sparse._TOKEN_RE

# Short domain tokens worth keeping despite the length floor.
_KEEP_SHORT = frozenset({"db", "ms", "hz", "ue", "rb", "nr", "fr"})

# Generic query filler that carries no retrieval signal.
_STOPWORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "of", "for", "to", "in", "on", "at", "and", "or", "but", "by", "as",
    "from", "with", "within", "under", "over", "than", "that", "this",
    "these", "those", "its", "it", "what", "which", "who", "whom", "how",
    "when", "where", "why", "does", "do", "did", "must", "may", "can",
    "define", "given", "value", "values", "used", "use", "apply", "applies",
})


def extract_query_terms(query: str) -> list[str]:
    """Heuristic salient-term extraction (NO NER dependency): keep numeric
    tokens, short domain units, and content words (>=3 chars, non-stopword).
    Lowercased, order-preserving, de-duplicated. Mirrors sparse's tokenizer
    so gate terms and the FTS index agree on token boundaries."""
    terms: list[str] = []
    seen: set[str] = set()
    for tok in _QUERY_TOKEN_RE.findall(query):
        low = tok.lower()
        if low in seen:
            continue
        has_digit = any(ch.isdigit() for ch in low)
        if has_digit or low in _KEEP_SHORT or (
            len(low) >= 3 and low not in _STOPWORDS
        ):
            seen.add(low)
            terms.append(low)
    return terms


def _sigmoid(x: float) -> float:
    x = max(-30.0, min(30.0, x))  # guard math.exp overflow
    return 1.0 / (1.0 + math.exp(-x))


def normalize_top_score(hit: object) -> float | None:
    """Map a hit's native relevance score to [0,1], larger = more confident,
    correcting each backend's sign and scale. Detects which score the hit
    carries the SAME way as evaluate._hit_score (rerank_score -> rrf_score ->
    distance -> bm25_score): a RerankedHit also carries rrf_score, but
    rerank_score is what ordered it. Returns None if no recognized score."""
    for attr in _SCORE_ATTRS:
        value = getattr(hit, attr, None)
        if value is None:
            continue
        value = float(value)
        if attr == "rerank_score":     # cross-encoder logit / relevance
            return _sigmoid(value)
        if attr == "rrf_score":        # larger = better, ~[0, 0.033]
            return min(value / RRF_REF, 1.0)
        if attr == "distance":         # smaller = better (cosine)
            return max(0.0, min(1.0, 1.0 - value))
        if attr == "bm25_score":       # FTS5: negative, smaller = better
            return min(max(-value, 0.0) / BM25_REF, 1.0)
    return None


def _clause(section_number: str, depth: int = CLAUSE_DEPTH) -> str:
    return ".".join(section_number.split(".")[:depth])


def section_consistency(
    sections: Sequence[str], *, top_n: int = 5,
) -> tuple[float, str | None]:
    """How concentrated the top_n hit sections are on a single clause (prefix
    to CLAUSE_DEPTH components). Returns (modal_fraction, dominant_clause).
    Empty -> (0.0, None). Scatter across unrelated clauses gives a low
    fraction — a query-agnostic 'the index isn't sure' signal."""
    considered = [s for s in sections[:top_n] if s]
    if not considered:
        return 0.0, None
    groups = Counter(_clause(s) for s in considered)
    dominant, count = groups.most_common(1)[0]
    return count / len(considered), dominant


def term_coverage(
    query_terms: Sequence[str], chunk_texts: Sequence[str],
) -> float:
    """Fraction of query_terms appearing (case-insensitive substring) in the
    concatenated chunk text. Empty query_terms -> 0.0. Mirrors evaluate.py's
    coverage math but over QUERY terms; caller must pass FULL chunk text."""
    if not query_terms:
        return 0.0
    haystack = " ".join(chunk_texts).lower()
    found = sum(1 for term in query_terms if term in haystack)
    return found / len(query_terms)


# ----------------------------------------------------------- pure decision

def make_gate_decision(
    signals: GateSignals,
    *,
    mode: str = "balanced",
    thresholds: GateThresholds | None = None,
) -> GateDecision:
    """Pure decision from precomputed signals. Precedence: no results ->
    too-few-and-weak -> top-score-below-floor -> weighted evidence band.
    `reason` always embeds the deciding numeric comparison. Pass `thresholds`
    to bypass the per-mode config lookup (used by calibration)."""
    t = thresholds if thresholds is not None else GateThresholds.for_mode(mode)
    record = asdict(signals)
    score = signals.top_score_norm

    if signals.result_count == 0 or score is None:
        return GateDecision(
            GateOutcome.REFUSE, 1.0, "no retrieval results", record,
        )

    if signals.result_count < t.min_results and score < t.strong_score:
        return GateDecision(
            GateOutcome.REFUSE, 1.0 - score,
            f"only {signals.result_count} result(s) and top score "
            f"{score:.3f} < strong {t.strong_score:.3f}",
            record,
        )

    if score < t.min_top_score:
        return GateDecision(
            GateOutcome.REFUSE, 1.0 - score,
            f"top score {score:.3f} < floor {t.min_top_score:.3f}",
            record,
        )

    evidence = (
        t.w_score * score
        + t.w_consist * signals.section_consistency
        + t.w_cover * signals.term_coverage
    )
    if evidence >= t.answer_floor:
        return GateDecision(
            GateOutcome.ANSWER, evidence,
            f"evidence {evidence:.3f} >= answer_floor {t.answer_floor:.3f}",
            record,
        )
    if evidence >= t.low_floor:
        return GateDecision(
            GateOutcome.LOW_CONFIDENCE, evidence,
            f"evidence {evidence:.3f} in "
            f"[{t.low_floor:.3f}, {t.answer_floor:.3f})",
            record,
        )
    return GateDecision(
        GateOutcome.REFUSE, 1.0 - evidence,
        f"evidence {evidence:.3f} < low_floor {t.low_floor:.3f}",
        record,
    )


# ----------------------------------------------------------- orchestrator

def gate_for_hits(
    session: Session,
    query: str,
    hits: Sequence[_Hit],
    *,
    backend: str,
    mode: str = "balanced",
    top_n: int = 5,
) -> GateDecision:
    """Build evidence signals for a retrieved result set and decide. The one
    IO step is fetching FULL chunk text (the 240-char preview would undercount
    term coverage). Mirrors search_reranked (IO) -> apply_rerank (pure)."""
    query_terms = extract_query_terms(query)
    top_hits = list(hits[:top_n])

    if not top_hits:
        signals = GateSignals(
            result_count=len(hits),
            top_score_norm=None,
            section_consistency=0.0,
            term_coverage=0.0,
            dominant_section=None,
            backend=backend,
        )
        return make_gate_decision(signals, mode=mode)

    texts_by_id = fetch_full_texts(session, [h.chunk_id for h in top_hits])
    chunk_texts = [
        texts_by_id.get(h.chunk_id) or getattr(h, "text_preview", "")
        for h in top_hits
    ]
    consistency, dominant = section_consistency(
        [h.section_number for h in top_hits], top_n=top_n,
    )
    signals = GateSignals(
        result_count=len(hits),
        top_score_norm=normalize_top_score(hits[0]),
        section_consistency=consistency,
        term_coverage=term_coverage(query_terms, chunk_texts),
        dominant_section=dominant,
        backend=backend,
    )
    return make_gate_decision(signals, mode=mode)
