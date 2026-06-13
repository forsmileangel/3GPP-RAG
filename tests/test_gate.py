"""Unit tests for the evidence gate (src/retrieval/gate.py).

Pure-logic tests use SimpleNamespace fakes (no DB / model). The orchestrator
test uses a throwaway in-memory SQLite, mirroring test_rerank.py, to prove
gate_for_hits scores the FULL chunk text rather than the 240-char preview.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models import Base, Chunk, Section, Spec
from src.retrieval.gate import (
    GateDecision,
    GateOutcome,
    GateSignals,
    GateThresholds,
    extract_query_terms,
    gate_for_hits,
    make_gate_decision,
    normalize_top_score,
    section_consistency,
    term_coverage,
)


# --------------------------------------------------- extract_query_terms

def test_extract_keeps_numbers_units_sections_acronyms():
    terms = extract_query_terms(
        "What is the minimum output power for PC3 at -40 dBm in §6.3.1?"
    )
    assert "-40" in terms
    assert "dbm" in terms
    assert "pc3" in terms
    assert "§6.3.1" in terms
    assert "minimum" in terms
    assert "the" not in terms      # stopword
    assert "is" not in terms       # stopword


def test_extract_dedupes_preserving_order():
    assert extract_query_terms("power power MPR mpr") == ["power", "mpr"]


def test_extract_keeps_short_domain_units():
    terms = extract_query_terms("measured in dB and ms")
    assert "db" in terms
    assert "ms" in terms
    assert "in" not in terms       # stopword + too short


def test_extract_empty():
    assert extract_query_terms("the is of for") == []
    assert extract_query_terms("") == []


# ---------------------------------------------------- normalize_top_score

def test_normalize_rerank_score_sigmoid():
    assert normalize_top_score(SimpleNamespace(rerank_score=10.0)) > 0.99
    assert normalize_top_score(SimpleNamespace(rerank_score=-10.0)) < 0.01
    assert normalize_top_score(SimpleNamespace(rerank_score=0.0)) == pytest.approx(0.5)


def test_normalize_rrf_score_larger_better_and_saturates():
    low = normalize_top_score(SimpleNamespace(rrf_score=0.005))
    high = normalize_top_score(SimpleNamespace(rrf_score=0.033))
    assert 0.0 < low < high <= 1.0
    assert normalize_top_score(SimpleNamespace(rrf_score=0.1)) == 1.0


def test_normalize_distance_smaller_better_clamped():
    assert normalize_top_score(SimpleNamespace(distance=0.0)) == 1.0
    assert normalize_top_score(SimpleNamespace(distance=0.2)) == pytest.approx(0.8)
    assert normalize_top_score(SimpleNamespace(distance=1.5)) == 0.0


def test_normalize_bm25_negative_magnitude():
    weak = normalize_top_score(SimpleNamespace(bm25_score=-1.2))
    strong = normalize_top_score(SimpleNamespace(bm25_score=-12.0))
    assert 0.0 < weak < strong <= 1.0
    assert strong == 1.0


def test_normalize_prefers_rerank_over_rrf():
    # A RerankedHit carries BOTH; rerank_score (what ordered the row) must win.
    hit = SimpleNamespace(rerank_score=10.0, rrf_score=0.001)
    assert normalize_top_score(hit) > 0.99   # sigmoid(10), not the rrf path


def test_normalize_no_score_attr_is_none():
    assert normalize_top_score(SimpleNamespace(chunk_id=1)) is None


# ---------------------------------------------------- section_consistency

def test_section_consistency_all_same_clause():
    frac, dom = section_consistency(["6.3.4.2", "6.3.4.3", "6.3.4.4"])
    assert frac == 1.0
    assert dom == "6.3.4"


def test_section_consistency_scattered():
    frac, _ = section_consistency(
        ["6.2.1", "6.3.4.2", "6.2.2", "6.5.1", "6.2.4"]
    )
    assert frac < 0.5


def test_section_consistency_single():
    assert section_consistency(["6.2.1.5"]) == (1.0, "6.2.1")


def test_section_consistency_empty():
    assert section_consistency([]) == (0.0, None)


def test_section_consistency_respects_top_n():
    frac, dom = section_consistency(["6.2.1", "6.2.1", "9.9.9"], top_n=2)
    assert frac == 1.0
    assert dom == "6.2.1"


# -------------------------------------------------------- term_coverage

def test_term_coverage_full_partial_zero():
    texts = ["the minimum output power is -40 dBm"]
    assert term_coverage(["minimum", "-40"], texts) == 1.0
    assert term_coverage(["minimum", "absent"], texts) == 0.5
    assert term_coverage(["absent"], texts) == 0.0


def test_term_coverage_case_insensitive():
    assert term_coverage(["dbm"], ["Output is 23 DBM"]) == 1.0


def test_term_coverage_empty_terms():
    assert term_coverage([], ["anything"]) == 0.0


# ----------------------------------------------------- make_gate_decision

def _signals(**overrides) -> GateSignals:
    base = dict(
        result_count=10, top_score_norm=0.9, section_consistency=1.0,
        term_coverage=1.0, dominant_section="6.3.4", backend="hybrid",
    )
    base.update(overrides)
    return GateSignals(**base)


# Fixed thresholds for band-logic tests — decoupled from the CALIBRATED config
# in src/config.py so recalibration (M4+) can never break these pure-logic
# tests. Mirrors the original balanced shape (weights 0.5/0.25/0.25).
_FIXED = GateThresholds(
    min_results=2, min_top_score=0.30, strong_score=0.55,
    answer_floor=0.50, low_floor=0.30,
    w_score=0.5, w_consist=0.25, w_cover=0.25,
)


def test_decision_no_results_refuses():
    d = make_gate_decision(_signals(result_count=0, top_score_norm=None))
    assert d.outcome is GateOutcome.REFUSE
    assert d.confidence == 1.0
    assert "no retrieval results" in d.reason


def test_decision_strong_answers():
    d = make_gate_decision(_signals(), thresholds=_FIXED)
    assert d.outcome is GateOutcome.ANSWER
    assert "answer_floor" in d.reason


def test_decision_weak_top_score_refuses():
    d = make_gate_decision(_signals(top_score_norm=0.05), thresholds=_FIXED)
    assert d.outcome is GateOutcome.REFUSE
    assert "floor" in d.reason


def test_decision_mid_evidence_low_confidence():
    # _FIXED: evidence = .5*.5 + .25*.2 + .25*.2 = 0.35 -> in [0.3, 0.5)
    d = make_gate_decision(
        _signals(top_score_norm=0.5, section_consistency=0.2, term_coverage=0.2),
        thresholds=_FIXED,
    )
    assert d.outcome is GateOutcome.LOW_CONFIDENCE


def test_decision_weak_evidence_refuses():
    # score clears min_top_score (0.3) but evidence 0.175 < low_floor 0.3
    d = make_gate_decision(
        _signals(top_score_norm=0.35, section_consistency=0.0, term_coverage=0.0),
        thresholds=_FIXED,
    )
    assert d.outcome is GateOutcome.REFUSE
    assert "low_floor" in d.reason


def test_decision_too_few_and_weak_refuses():
    d = make_gate_decision(
        _signals(result_count=1, top_score_norm=0.4), thresholds=_FIXED,
    )
    assert d.outcome is GateOutcome.REFUSE
    assert "result(s)" in d.reason


def test_decision_few_but_strong_does_not_trip_rule2():
    d = make_gate_decision(
        _signals(result_count=1, top_score_norm=0.9), thresholds=_FIXED,
    )
    assert d.outcome is GateOutcome.ANSWER


def test_decision_mode_monotonicity_same_signals_flip():
    sig = _signals(top_score_norm=0.45, section_consistency=0.4, term_coverage=0.4)
    assert make_gate_decision(sig, mode="permissive").outcome is GateOutcome.ANSWER
    assert make_gate_decision(sig, mode="strict").outcome is not GateOutcome.ANSWER


def test_decision_signals_roundtrip():
    d = make_gate_decision(_signals(top_score_norm=0.7))
    assert d.signals["top_score_norm"] == 0.7
    assert d.signals["backend"] == "hybrid"
    assert d.signals["dominant_section"] == "6.3.4"


# ----------------------------------------------------- GateThresholds

def test_for_mode_unknown_raises():
    with pytest.raises(ValueError, match="unknown gate mode"):
        GateThresholds.for_mode("bogus")


def test_for_mode_strict_raises_floors():
    base = GateThresholds.for_mode("balanced")
    strict = GateThresholds.for_mode("strict")
    assert strict.answer_floor > base.answer_floor
    assert strict.min_top_score > base.min_top_score


# ----------------------------------------------------- gate_for_hits (DB)

def _db_session() -> Session:
    engine = create_engine("sqlite://", future=True)
    Base.metadata.create_all(engine)
    return Session(engine)


def test_gate_for_hits_scores_full_text_not_preview():
    session = _db_session()
    spec = Spec(
        name="38.521-1", version="i00", source_file="x.md",
        source_format="tspec_md",
    )
    session.add(spec)
    session.flush()
    sec = Section(
        spec_id=spec.spec_id, section_number="6.3.4.2",
        title="Absolute power tolerance", level=4, page_start=1,
    )
    session.add(sec)
    session.flush()
    # "gap larger than 20ms" sits PAST char 240 — only a full-text fetch finds
    # it; the 240-char preview would undercount coverage.
    head = "Absolute power tolerance applies under normal conditions. "
    long_text = head + ("x" * 220) + " The transmission gap is larger than 20ms."
    chunk = Chunk(
        section_id=sec.section_id, text=long_text, page=0, char_offset=0,
        source_format="tspec_md",
    )
    session.add(chunk)
    session.flush()

    hits = [SimpleNamespace(
        chunk_id=chunk.chunk_id, section_number="6.3.4.2",
        rrf_score=0.033, text_preview=long_text[:240],
    )]
    decision = gate_for_hits(
        session,
        "absolute power tolerance gap larger than 20ms",
        hits, backend="hybrid",
    )
    assert isinstance(decision, GateDecision)
    # all six query terms appear in the FULL text -> coverage 1.0
    # (preview alone, missing gap/larger/20ms, would give 0.5)
    assert decision.signals["term_coverage"] == 1.0
    assert decision.outcome is GateOutcome.ANSWER


def test_gate_for_hits_empty_refuses():
    session = _db_session()
    d = gate_for_hits(session, "anything", [], backend="hybrid")
    assert d.outcome is GateOutcome.REFUSE
    assert d.signals["result_count"] == 0


def test_gate_for_hits_falls_back_to_preview_when_text_missing():
    session = _db_session()  # empty DB: fetch_full_texts returns {}
    hits = [SimpleNamespace(
        chunk_id=999, section_number="6.2.1", rrf_score=0.02,
        text_preview="minimum output power -40 dBm",
    )]
    d = gate_for_hits(session, "minimum output power", hits, backend="hybrid")
    assert d.signals["term_coverage"] > 0.0   # preview fallback still scores
