"""Retrieval-only benchmark over the test bank.

For every question in data/eval/test_questions.yaml:
  - run sparse (FTS5) retrieval
  - run dense (BGE-M3 → Chroma) retrieval
  - run hybrid (RRF fusion of sparse + dense, k=60)
  - optionally run reranked (cross-encoder over the hybrid top-30; pick the
    model with --reranker jina|bge, reported as "reranked:<model>")
  - retrieve ONCE at k = max(10, --top-k), then score by slicing that single
    ranked list:
      hit@1 / hit@3 / hit@5 — does any chunk in the first k live in
                              expected_section's subtree?
      RR@10     — reciprocal rank of the first subtree hit, 0.0 if the
                  subtree never appears in the top 10; aggregated as MRR@10
      coverage  — fraction of expected_keywords found in the top-5 chunks
                  (window kept at 5 for comparability with earlier reports)
  - emit a markdown report to data/eval/last_eval.md (also stdout)

Gate (ratio-based so it survives test-bank growth):
  - hit@5 ratio ≥ 0.8 per backend (sparse & dense independently)
  - hit@1 and MRR@10 are REPORTED, NOT gated — they are the improvement
    targets for the upcoming RRF / reranker steps

--top-k only controls how many detail rows each question shows in the
report; scoring always uses the k=10 window described above.

Usage:
    .venv/Scripts/python.exe scripts/evaluate.py
    .venv/Scripts/python.exe scripts/evaluate.py --top-k 10
    .venv/Scripts/python.exe scripts/evaluate.py --backend sparse,dense
    .venv/Scripts/python.exe scripts/evaluate.py --backend reranked --reranker bge
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dataclasses import dataclass

import yaml
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.config import settings
from src.models import Section, Spec
from src.retrieval import (
    gate_for_hits,
    search_dense,
    search_hybrid,
    search_reranked,
    search_sparse,
)


# Scoring window: hit@1/3/5 slices and the RR cap all live inside the first
# SCORING_CAP hits, so one retrieval call per (question, backend) suffices.
SCORING_CAP = 10
GATE_THRESHOLD = 0.8  # hit@5 ratio each backend must clear

# Evidence-gate (Step 5) acceptance targets, reported only under --gate.
GATE_CITATION_TARGET = 0.9   # of ANSWERED answerable, fraction with correct top-1
GATE_COVERAGE_TARGET = 0.7   # mean keyword coverage over answered answerable


@dataclass
class QuestionMetrics:
    qid: str
    backend: str
    question_type: str            # mirrors the bank's question_type taxonomy
    hit_at_1: bool
    hit_at_3: bool
    hit_at_5: bool
    rr_at_10: float               # reciprocal rank; 0.0 if no hit in top 10
    keyword_coverage: float       # 0..1, over the top-5 window
    keywords_found: list[str]
    keywords_missing: list[str]
    top1_section: str | None
    top1_page: int | None
    top1_table_id: str | None
    top_chunk_summaries: list[str]


def _hit_score(hit) -> float:
    """Score for the report's detail rows. Backends use different attribute
    names AND sign conventions (rerank_score / rrf_score: larger = better;
    distance / bm25_score: smaller = better) — this only labels rows, never
    ranks. rerank_score comes first: RerankedHit also carries rrf_score as
    provenance, but the rerank score is what ordered the row."""
    for attr in ("rerank_score", "rrf_score", "distance", "bm25_score"):
        value = getattr(hit, attr, None)
        if value is not None:
            return float(value)
    return 0.0


def hit_at_k(ranked_sections: list[str], expected: set[str], k: int) -> bool:
    """True if any of the first k ranked sections is in the expected subtree."""
    return any(s in expected for s in ranked_sections[:k])


def reciprocal_rank(
    ranked_sections: list[str], expected: set[str], cap: int = SCORING_CAP
) -> float:
    """1/rank (1-indexed) of the first expected-subtree section, scanning at
    most `cap` positions. 0.0 when the subtree never appears in that window."""
    for rank, section in enumerate(ranked_sections[:cap], start=1):
        if section in expected:
            return 1.0 / rank
    return 0.0


def aggregate_metrics(ms: list[QuestionMetrics]) -> dict[str, float]:
    """Mean hit@1/3/5, MRR@10 and keyword coverage over per-question metrics.
    Empty input -> all zeros (small question_type groups must not raise)."""
    n = len(ms)
    if n == 0:
        return {"hit@1": 0.0, "hit@3": 0.0, "hit@5": 0.0, "mrr@10": 0.0, "coverage": 0.0}
    return {
        "hit@1": sum(1 for m in ms if m.hit_at_1) / n,
        "hit@3": sum(1 for m in ms if m.hit_at_3) / n,
        "hit@5": sum(1 for m in ms if m.hit_at_5) / n,
        "mrr@10": sum(m.rr_at_10 for m in ms) / n,
        "coverage": sum(m.keyword_coverage for m in ms) / n,
    }


@dataclass
class GateQuestionResult:
    """One question's evidence-gate outcome + its confusion-matrix cell."""
    qid: str
    answerability: str           # "answerable" | "out_of_scope"
    oos_kind: str | None
    outcome: str                 # answer | low_confidence | refuse
    confidence: float
    reason: str
    hit_correct: bool            # answerable only: top-1 section correct
    coverage: float | None       # answerable only: keyword coverage
    classification: str          # TP | FP | TN | FN (REFUSE = positive class)


def classify_gate(
    *, answerability: str, outcome: str, lowconf_as_refuse: bool = False,
) -> str:
    """2x2 confusion with REFUSE as the positive class (the gate's job is to
    refuse the unanswerable):
        out_of_scope + refuse -> TP        answerable + answer -> TN
        out_of_scope + answer -> FN        answerable + refuse -> FP
    LOW_CONFIDENCE counts as ANSWER unless lowconf_as_refuse is set."""
    refused = outcome == "refuse" or (
        lowconf_as_refuse and outcome == "low_confidence"
    )
    if answerability == "out_of_scope":
        return "TP" if refused else "FN"
    return "FP" if refused else "TN"


def gate_confusion(results: list[GateQuestionResult]) -> dict[str, float]:
    """Confusion counts + refusal precision / recall / F1. Empty -> zeros."""
    tp = sum(1 for r in results if r.classification == "TP")
    fp = sum(1 for r in results if r.classification == "FP")
    tn = sum(1 for r in results if r.classification == "TN")
    fn = sum(1 for r in results if r.classification == "FN")
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) else 0.0
    )
    return {
        "TP": tp, "FP": fp, "TN": tn, "FN": fn,
        "precision": precision, "recall": recall, "f1": f1,
    }


def citation_accuracy(results: list[GateQuestionResult]) -> float:
    """Among answerable questions the gate chose to ANSWER (classification TN),
    fraction whose top-1 retrieved section is correct — when we answer, is the
    citation trustworthy? Empty -> 0.0."""
    answered = [r for r in results if r.classification == "TN"]
    if not answered:
        return 0.0
    return sum(1 for r in answered if r.hit_correct) / len(answered)


def gate_mean_coverage(results: list[GateQuestionResult]) -> float:
    """Mean keyword coverage over answered answerable questions. Empty -> 0.0."""
    covs = [
        r.coverage for r in results
        if r.classification == "TN" and r.coverage is not None
    ]
    return sum(covs) / len(covs) if covs else 0.0


def _build_section_subtree(
    session: Session, *, source_format: str | None = None
) -> dict[str, set[str]]:
    """Map section_number -> set of section_numbers that are it OR its
    descendants. Used to score 'is this hit in the expected subtree?'.

    When source_format is set, only sections of specs with that source are
    included. The DB can hold the same spec under two sources (e.g. 38.521-1
    as both pdf_pymupdf and tspec_md) with shared section_numbers; without
    this filter the map (keyed by bare section_number) would let whichever
    spec is iterated last silently overwrite the other's subtree. Build it
    from the same corpus the run actually retrieves from.
    """
    stmt = select(Section)
    if source_format is not None:
        stmt = stmt.join(Spec, Spec.spec_id == Section.spec_id).where(
            Spec.source_format == source_format
        )
    sections = list(session.execute(stmt).scalars())
    by_id = {s.section_id: s for s in sections}

    descendants: dict[int, set[int]] = {s.section_id: {s.section_id} for s in sections}
    # Bottom-up roll-up: for each section, walk parents adding self.
    for s in sections:
        cur = s
        while cur.parent_id is not None:
            descendants[cur.parent_id].add(s.section_id)
            cur = by_id.get(cur.parent_id)
            if cur is None:
                break

    return {
        s.section_number: {by_id[d].section_number for d in descendants[s.section_id]}
        for s in sections
    }


def _evaluate_question(
    *,
    question: dict,
    hits: list,  # SparseHit or DenseHit
    subtree: dict[str, set[str]],
    backend: str,
    session: Session,
) -> QuestionMetrics:
    expected_subtree = subtree.get(question["expected_section"], {question["expected_section"]})
    expected_kws = [k.lower() for k in question["expected_keywords"]]

    ranked = [h.section_number for h in hits]

    # keyword coverage — query the FULL chunk text from SQL (the hit's
    # text_preview is truncated to 240 chars; matching against preview
    # under-counts coverage when the keyword appears later in a long chunk).
    # Window stays at top-5 even though scoring sees top-10, so coverage
    # numbers remain comparable with reports from before the multi-K upgrade.
    from src.models import Chunk

    chunk_ids = [h.chunk_id for h in hits[:5]]
    full_texts = []
    if chunk_ids:
        rows = session.execute(
            select(Chunk.text).where(Chunk.chunk_id.in_(chunk_ids))
        ).scalars().all()
        full_texts = [t.lower() for t in rows]
    all_text = " ".join(full_texts)
    found = [k for k in expected_kws if k in all_text]
    missing = [k for k in expected_kws if k not in all_text]
    coverage = len(found) / len(expected_kws) if expected_kws else 0.0

    top1 = hits[0] if hits else None

    summaries = [
        f"#{i + 1} sec={h.section_number} page={h.page} table={h.table_id or '-'} "
        f"score={_hit_score(h):.3f}"
        for i, h in enumerate(hits)
    ]

    return QuestionMetrics(
        qid=question["qid"],
        backend=backend,
        question_type=question["question_type"],
        hit_at_1=hit_at_k(ranked, expected_subtree, 1),
        hit_at_3=hit_at_k(ranked, expected_subtree, 3),
        hit_at_5=hit_at_k(ranked, expected_subtree, 5),
        rr_at_10=reciprocal_rank(ranked, expected_subtree),
        keyword_coverage=coverage,
        keywords_found=found,
        keywords_missing=missing,
        top1_section=top1.section_number if top1 else None,
        top1_page=top1.page if top1 else None,
        top1_table_id=top1.table_id if top1 else None,
        top_chunk_summaries=summaries,
    )


def _format_report(
    *,
    backend_metrics: dict[str, list[QuestionMetrics]],
    questions: list[dict],
    top_k: int,
    source_format: str | None = None,
) -> str:
    lines: list[str] = []
    lines.append("# Retrieval Benchmark\n")
    source_label = source_format or "mixed"
    lines.append(
        f"_scored at k={SCORING_CAP} (hit@1/3/5, MRR@10); "
        f"detail rows show top {top_k}; "
        f"source_format = {source_label}; "
        f"backends = {', '.join(backend_metrics.keys())}_\n"
    )

    # Aggregate header
    lines.append("## Aggregate\n")
    lines.append("| backend | hit@1 | hit@3 | hit@5 | MRR@10 | mean coverage |")
    lines.append("|---|---|---|---|---|---|")
    for backend, ms in backend_metrics.items():
        n = len(ms)
        h1 = sum(1 for m in ms if m.hit_at_1)
        h3 = sum(1 for m in ms if m.hit_at_3)
        h5 = sum(1 for m in ms if m.hit_at_5)
        agg = aggregate_metrics(ms)
        lines.append(
            f"| {backend} | {h1}/{n} | {h3}/{n} | {h5}/{n} "
            f"| {agg['mrr@10']:.2f} | {agg['coverage']:.0%} |"
        )
    lines.append("")

    # Per-question_type breakdown — shows which category drags a backend
    # down. n is displayed so small groups aren't over-interpreted.
    lines.append("## By question type\n")
    lines.append("| backend | type | n | hit@1 | hit@3 | hit@5 | MRR@10 | coverage |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for backend, ms in backend_metrics.items():
        for qtype in sorted({m.question_type for m in ms}):
            group = [m for m in ms if m.question_type == qtype]
            agg = aggregate_metrics(group)
            lines.append(
                f"| {backend} | {qtype} | {len(group)} "
                f"| {agg['hit@1']:.0%} | {agg['hit@3']:.0%} | {agg['hit@5']:.0%} "
                f"| {agg['mrr@10']:.2f} | {agg['coverage']:.0%} |"
            )
    lines.append("")

    # Per-question detail
    by_qid = {q["qid"]: q for q in questions}
    qids = [q["qid"] for q in questions]
    for qid in qids:
        q = by_qid[qid]
        lines.append(f"## {qid} — {q['question']}")
        lines.append(
            f"_expected_section = §{q['expected_section']} · "
            f"type = {q['question_type']} · "
            f"difficulty = {q['difficulty']}_\n"
        )
        for backend, ms in backend_metrics.items():
            m = next(x for x in ms if x.qid == qid)
            flags = (
                f"hit@1={'Y' if m.hit_at_1 else 'N'} "
                f"hit@3={'Y' if m.hit_at_3 else 'N'} "
                f"hit@5={'Y' if m.hit_at_5 else 'N'} "
                f"RR@10={m.rr_at_10:.2f}"
            )
            lines.append(
                f"**{backend}** — {flags} · "
                f"coverage = {len(m.keywords_found)}/{len(m.keywords_found) + len(m.keywords_missing)} "
                f"({m.keyword_coverage:.0%}) · "
                f"top-1 = §{m.top1_section} p{m.top1_page} table={m.top1_table_id or '-'}"
            )
            if m.keywords_missing:
                lines.append(f"  missing keywords: {m.keywords_missing}")
            for s in m.top_chunk_summaries[:top_k]:
                lines.append(f"    {s}")
            lines.append("")

    return "\n".join(lines)


def _retrieve(
    session: Session, backend: str, query: str, *,
    k: int, source_format: str | None, reranker: str,
) -> list:
    """Dispatch to a backend's search function. Shared by the metric loop and
    the gate pass so both retrieve identically for a given backend."""
    if backend == "sparse":
        return search_sparse(session, query, top_k=k, source_format=source_format)
    if backend == "dense":
        return search_dense(session, query, top_k=k, source_format=source_format)
    if backend == "hybrid":
        return search_hybrid(session, query, top_k=k, source_format=source_format)
    return search_reranked(
        session, query, top_k=k, reranker_model=reranker,
        source_format=source_format,
    )


def _format_gate_report(
    *, results: list[GateQuestionResult], gate_label: str, mode: str,
    source_format: str | None,
) -> str:
    cm = gate_confusion(results)
    cite = citation_accuracy(results)
    cov = gate_mean_coverage(results)
    n_oos = sum(1 for r in results if r.answerability == "out_of_scope")
    n_ans = sum(1 for r in results if r.answerability == "answerable")
    source_label = source_format or "mixed"

    lines: list[str] = []
    lines.append("# Evidence Gate\n")
    lines.append(
        f"_backend = {gate_label}; mode = {mode}; "
        f"source_format = {source_label}; {n_ans} answerable + {n_oos} "
        f"out-of-scope; REFUSE = positive class_\n"
    )

    lines.append("## Confusion matrix\n")
    lines.append("| | gate REFUSE | gate ANSWER |")
    lines.append("|---|---|---|")
    lines.append(
        f"| out_of_scope (should refuse) | {cm['TP']} (TP) | {cm['FN']} (FN) |"
    )
    lines.append(
        f"| answerable (should answer) | {cm['FP']} (FP) | {cm['TN']} (TN) |"
    )
    lines.append("")
    lines.append(
        f"refusal precision = {cm['precision']:.0%} · "
        f"refusal recall = {cm['recall']:.0%} · F1 = {cm['f1']:.2f}\n"
    )

    lines.append("## Acceptance\n")
    lines.append(
        f"- out-of-scope refusal correctness (recall) = {cm['recall']:.0%} "
        f"({cm['TP']}/{cm['TP'] + cm['FN']} OOS refused)"
    )
    lines.append(
        f"- citation accuracy = {cite:.0%} "
        f"({'PASS' if cite >= GATE_CITATION_TARGET else 'FAIL'} "
        f"vs >= {GATE_CITATION_TARGET:.0%})"
    )
    lines.append(
        f"- mean coverage (answered) = {cov:.0%} "
        f"({'PASS' if cov >= GATE_COVERAGE_TARGET else 'FAIL'} "
        f"vs >= {GATE_COVERAGE_TARGET:.0%})\n"
    )

    lines.append("## Out-of-scope refusal by kind\n")
    lines.append("| oos_kind | n | refused | refusal rate |")
    lines.append("|---|---|---|---|")
    for kind in ("hard", "scope_boundary"):
        group = [r for r in results if r.oos_kind == kind]
        refused = sum(1 for r in group if r.classification == "TP")
        rate = refused / len(group) if group else 0.0
        lines.append(f"| {kind} | {len(group)} | {refused} | {rate:.0%} |")
    lines.append("")

    lines.append("## Gate detail\n")
    for r in results:
        tag = r.answerability + (f"/{r.oos_kind}" if r.oos_kind else "")
        lines.append(
            f"- **{r.qid}** [{tag}] [{r.classification}] "
            f"{r.outcome} (conf {r.confidence:.2f}) — {r.reason}"
        )
    lines.append("")
    return "\n".join(lines)


def _print_gate_summary(
    results: list[GateQuestionResult], gate_label: str,
) -> None:
    cm = gate_confusion(results)
    cite = citation_accuracy(results)
    cov = gate_mean_coverage(results)
    print(f"\n=== GATE (evidence) — {gate_label} ===")
    print(
        f"  refusal precision={cm['precision']:.0%}  recall={cm['recall']:.0%}  "
        f"F1={cm['f1']:.2f}  (TP={cm['TP']} FP={cm['FP']} "
        f"TN={cm['TN']} FN={cm['FN']})"
    )
    print(
        f"  citation accuracy={cite:.0%} (target {GATE_CITATION_TARGET:.0%})  "
        f"mean coverage={cov:.0%} (target {GATE_COVERAGE_TARGET:.0%})"
    )
    ok = cite >= GATE_CITATION_TARGET and cov >= GATE_COVERAGE_TARGET
    print(
        f"  GATE(evidence) {'OK' if ok else 'FAIL'} "
        f"(citation + coverage targets; refusal precision/recall reported)"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="detail rows per question in the report; scoring always uses "
        f"k={SCORING_CAP} for hit@1/3/5 + MRR@10",
    )
    parser.add_argument(
        "--backend",
        default="sparse,dense,hybrid",
        help="Comma-separated subset of {sparse, dense, hybrid, reranked}",
    )
    parser.add_argument(
        "--reranker",
        choices=["jina", "bge"],
        default="jina",
        help="Cross-encoder used by the 'reranked' backend; the report "
        "labels the run as 'reranked:<model>' so A/B runs stay distinct",
    )
    parser.add_argument(
        "--source-format",
        choices=["pdf_pymupdf", "tspec_md"],
        default=None,
        help="Restrict retrieval to one corpus for source A/B runs; "
        "default None searches the mixed collection",
    )
    parser.add_argument(
        "--questions",
        type=Path,
        default=settings.eval_dir / "test_questions.yaml",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=settings.eval_dir / "last_eval.md",
    )
    parser.add_argument(
        "--gate",
        action="store_true",
        help="ALSO run the evidence-gate eval (ANSWER/REFUSE per question + "
        "confusion matrix over the out-of-scope questions). Off by default so "
        "the retrieval report stays byte-identical to committed baselines; "
        "on writes a SEPARATE --gate-report.",
    )
    parser.add_argument(
        "--gate-mode",
        choices=["strict", "balanced", "permissive"],
        default="balanced",
    )
    parser.add_argument(
        "--gate-backend",
        choices=["sparse", "dense", "hybrid", "reranked"],
        default="hybrid",
        help="Retrieval backend the gate scores over (default hybrid).",
    )
    parser.add_argument(
        "--gate-report",
        type=Path,
        default=settings.eval_dir / "gate_eval.md",
    )
    parser.add_argument(
        "--gate-lowconf-as-refuse",
        action="store_true",
        help="Count LOW_CONFIDENCE as a refusal in the confusion matrix.",
    )
    args = parser.parse_args()

    backends = [b.strip() for b in args.backend.split(",") if b.strip()]
    valid = {"sparse", "dense", "hybrid", "reranked"}
    bad = set(backends) - valid
    if bad:
        print(f"ERROR: unknown backend(s) {bad}; valid: {valid}", file=sys.stderr)
        return 2

    if not args.questions.exists():
        print(f"ERROR: questions file not found: {args.questions}", file=sys.stderr)
        return 1

    # Pre-flight check: dense (and hybrid/reranked, which call dense
    # internally) requires the Chroma collection to exist and
    # chunks.vector_id to be populated. Bail early with a clear message if
    # the user runs evaluate.py before embed_chunks.py completes.
    dense_users = set(backends) | ({args.gate_backend} if args.gate else set())
    if {"dense", "hybrid", "reranked"} & dense_users:
        engine_pre = create_engine(settings.db_url, future=True)
        with Session(engine_pre) as s:
            from src.models import Chunk

            unembedded = s.execute(
                select(Chunk).where(Chunk.vector_id.is_(None)).limit(1)
            ).scalar_one_or_none()
            embedded_count = s.execute(
                select(Chunk).where(Chunk.vector_id.is_not(None)).limit(1)
            ).scalar_one_or_none()
        if embedded_count is None:
            print(
                "ERROR: dense backend requested but no chunks have vector_id set. "
                "Run scripts/embed_chunks.py first.",
                file=sys.stderr,
            )
            return 1
        if unembedded is not None:
            print(
                "WARN: some chunks still have vector_id=NULL — dense retrieval "
                "will only see the partially-embedded subset.",
                file=sys.stderr,
            )

    with args.questions.open(encoding="utf-8") as f:
        questions = yaml.safe_load(f)

    # Retrieval metrics run over ANSWERABLE questions only — out-of-scope
    # questions carry no expected_section. The answerable set + order match
    # the pre-OOS bank, so existing reports stay byte-identical. OOS questions
    # are consumed only by the --gate pass below.
    answerable = [
        q for q in questions
        if q.get("answerability", "answerable") == "answerable"
    ]

    engine = create_engine(settings.db_url, future=True)

    # Report/gate label: the reranked backend embeds the model id so A/B
    # runs ("reranked:jina" vs "reranked:bge") stay distinct everywhere.
    backend_labels = {
        b: (f"reranked:{args.reranker}" if b == "reranked" else b)
        for b in backends
    }
    backend_metrics: dict[str, list[QuestionMetrics]] = {
        backend_labels[b]: [] for b in backends
    }

    # Retrieve once per (question, backend) at a depth that covers both the
    # report detail rows and the fixed scoring window.
    k_retrieve = max(SCORING_CAP, args.top_k)

    with Session(engine) as session:
        subtree = _build_section_subtree(session, source_format=args.source_format)

        for q in answerable:
            print(f"[eval] {q['qid']}: {q['question']}")
            for backend in backends:
                hits = _retrieve(
                    session, backend, q["question"],
                    k=k_retrieve, source_format=args.source_format,
                    reranker=args.reranker,
                )
                label = backend_labels[backend]
                m = _evaluate_question(
                    question=q,
                    hits=hits,
                    subtree=subtree,
                    backend=label,
                    session=session,
                )
                backend_metrics[label].append(m)
                print(
                    f"  [{label:13s}] "
                    f"h1={'Y' if m.hit_at_1 else 'N'} "
                    f"h5={'Y' if m.hit_at_5 else 'N'} "
                    f"rr={m.rr_at_10:.2f}  cov={m.keyword_coverage:.0%}  "
                    f"top-1=§{m.top1_section} p{m.top1_page}"
                )

    report = _format_report(
        backend_metrics=backend_metrics,
        questions=answerable,
        top_k=args.top_k,
        source_format=args.source_format,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")
    print(f"\n[eval] Report written to {args.report}")

    # Aggregate summary at end
    print("\n=== AGGREGATE ===")
    for backend, ms in backend_metrics.items():
        n = len(ms)
        h1 = sum(1 for m in ms if m.hit_at_1)
        h3 = sum(1 for m in ms if m.hit_at_3)
        h5 = sum(1 for m in ms if m.hit_at_5)
        agg = aggregate_metrics(ms)
        print(
            f"  {backend:13s}  hit@1={h1}/{n}  hit@3={h3}/{n}  hit@5={h5}/{n}  "
            f"MRR@10={agg['mrr@10']:.2f}  mean_coverage={agg['coverage']:.0%}"
        )

    # Gate: BOTH backends must clear hit@5 ratio >= GATE_THRESHOLD. Ratio-based
    # (not an absolute count) so the gate keeps meaning as the bank grows.
    gate_ok = True
    for backend, ms in backend_metrics.items():
        ratio = aggregate_metrics(ms)["hit@5"]
        if ratio < GATE_THRESHOLD:
            print(
                f"\n  GATE FAIL  {backend} hit@5 = {ratio:.0%} "
                f"(< {GATE_THRESHOLD:.0%} required)"
            )
            gate_ok = False
    if gate_ok:
        print(f"\n  GATE OK  hit@5 >= {GATE_THRESHOLD:.0%} for all backends")
    print("  (hit@1 / MRR@10 reported, not gated — RRF/reranker targets)")

    # Evidence gate (Step 5) — opt-in, separate report, never perturbs the
    # retrieval numbers above. Runs over ALL questions (answerable + OOS) on a
    # single backend, fresh retrieval so the metric path is untouched.
    if args.gate:
        gate_label = (
            f"reranked:{args.reranker}"
            if args.gate_backend == "reranked" else args.gate_backend
        )
        gate_results: list[GateQuestionResult] = []
        with Session(engine) as gate_session:
            for q in questions:  # answerable + out-of-scope
                answerability = q.get("answerability", "answerable")
                hits = _retrieve(
                    gate_session, args.gate_backend, q["question"],
                    k=k_retrieve, source_format=args.source_format,
                    reranker=args.reranker,
                )
                decision = gate_for_hits(
                    gate_session, q["question"], hits,
                    backend=gate_label, mode=args.gate_mode,
                )
                if answerability == "answerable":
                    qm = _evaluate_question(
                        question=q, hits=hits, subtree=subtree,
                        backend=gate_label, session=gate_session,
                    )
                    hit_correct, coverage = qm.hit_at_1, qm.keyword_coverage
                else:
                    hit_correct, coverage = False, None
                gate_results.append(GateQuestionResult(
                    qid=q["qid"],
                    answerability=answerability,
                    oos_kind=q.get("oos_kind"),
                    outcome=decision.outcome.value,
                    confidence=decision.confidence,
                    reason=decision.reason,
                    hit_correct=hit_correct,
                    coverage=coverage,
                    classification=classify_gate(
                        answerability=answerability,
                        outcome=decision.outcome.value,
                        lowconf_as_refuse=args.gate_lowconf_as_refuse,
                    ),
                ))
        gate_report = _format_gate_report(
            results=gate_results, gate_label=gate_label,
            mode=args.gate_mode, source_format=args.source_format,
        )
        args.gate_report.parent.mkdir(parents=True, exist_ok=True)
        args.gate_report.write_text(gate_report, encoding="utf-8")
        print(f"\n[eval] Gate report written to {args.gate_report}")
        _print_gate_summary(gate_results, gate_label)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
