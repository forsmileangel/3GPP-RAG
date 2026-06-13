"""Unit tests for the pure metric functions in scripts/evaluate.py.

scripts/ is intentionally not a package (no __init__.py), so the module is
loaded by file path via importlib. These tests exercise only the pure
metric math — no DB, no Chroma, no embedding model.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location(
    "evaluate_module", REPO_ROOT / "scripts" / "evaluate.py"
)
evaluate = importlib.util.module_from_spec(_spec)
# Must register before exec: @dataclass resolves cls.__module__ through
# sys.modules, and an unregistered module makes that lookup return None.
sys.modules["evaluate_module"] = evaluate
_spec.loader.exec_module(evaluate)


# ---------------------------------------------------------------- hit_at_k

def test_hit_at_k_rank1():
    ranked = ["6.2.1", "6.2.3", "6.3.1"]
    expected = {"6.2.1"}
    assert evaluate.hit_at_k(ranked, expected, 1)
    assert evaluate.hit_at_k(ranked, expected, 3)
    assert evaluate.hit_at_k(ranked, expected, 5)


def test_hit_at_k_rank5_only():
    ranked = ["6.2.3", "6.2.4", "6.3.2", "6.3.3.4", "6.2.1"]
    expected = {"6.2.1"}
    assert not evaluate.hit_at_k(ranked, expected, 1)
    assert not evaluate.hit_at_k(ranked, expected, 3)
    assert evaluate.hit_at_k(ranked, expected, 5)


def test_hit_at_k_rank4_boundary():
    # Guards the off-by-one: a rank-4 hit is inside @5 but outside @3.
    ranked = ["a", "b", "c", "6.2.1", "d"]
    expected = {"6.2.1"}
    assert not evaluate.hit_at_k(ranked, expected, 3)
    assert evaluate.hit_at_k(ranked, expected, 4)
    assert evaluate.hit_at_k(ranked, expected, 5)


def test_hit_at_k_no_hit():
    ranked = ["6.2.2"] * 10
    assert not evaluate.hit_at_k(ranked, {"6.2.1"}, 10)


def test_hit_at_k_empty():
    assert not evaluate.hit_at_k([], {"6.2.1"}, 5)


# --------------------------------------------------------- reciprocal_rank

def test_reciprocal_rank_rank1():
    assert evaluate.reciprocal_rank(["6.2.1", "x"], {"6.2.1"}) == 1.0


def test_reciprocal_rank_rank3():
    rr = evaluate.reciprocal_rank(["a", "b", "6.2.1"], {"6.2.1"})
    assert abs(rr - 1 / 3) < 1e-9


def test_reciprocal_rank_beyond_cap():
    # First match at rank 11 with cap=10 -> counts as no hit.
    ranked = ["x"] * 10 + ["6.2.1"]
    assert evaluate.reciprocal_rank(ranked, {"6.2.1"}, cap=10) == 0.0


def test_reciprocal_rank_no_hit():
    assert evaluate.reciprocal_rank(["a", "b"], {"6.2.1"}) == 0.0


def test_reciprocal_rank_empty():
    assert evaluate.reciprocal_rank([], {"6.2.1"}) == 0.0


def test_subtree_match():
    # Expected subtree as produced by _build_section_subtree: parent plus
    # descendants. A child hit at rank 2 must count for the parent question.
    expected = {"6.3.4", "6.3.4.2", "6.3.4.3"}
    ranked = ["6.2.1", "6.3.4.2", "x"]
    assert not evaluate.hit_at_k(ranked, expected, 1)
    assert evaluate.hit_at_k(ranked, expected, 3)
    assert evaluate.reciprocal_rank(ranked, expected) == 0.5


# ------------------------------------------------------------- _hit_score

def test_hit_score_attribute_chain():
    class Rrf:
        rrf_score = 0.05

    class Dense:
        distance = 0.0   # must NOT fall through (old `or` chain bug)

    class Sparse:
        bm25_score = -12.5

    class Bare:
        pass

    assert evaluate._hit_score(Rrf()) == 0.05
    assert evaluate._hit_score(Dense()) == 0.0
    assert evaluate._hit_score(Sparse()) == -12.5
    assert evaluate._hit_score(Bare()) == 0.0


# ------------------------------------------------------- aggregate_metrics

def _qm(**overrides):
    defaults = dict(
        qid="qx",
        backend="sparse",
        question_type="numeric",
        hit_at_1=False,
        hit_at_3=False,
        hit_at_5=False,
        rr_at_10=0.0,
        keyword_coverage=0.0,
        keywords_found=[],
        keywords_missing=[],
        top1_section=None,
        top1_page=None,
        top1_table_id=None,
        top_chunk_summaries=[],
    )
    defaults.update(overrides)
    return evaluate.QuestionMetrics(**defaults)


def test_aggregate_metrics_empty():
    agg = evaluate.aggregate_metrics([])
    assert agg == {
        "hit@1": 0.0, "hit@3": 0.0, "hit@5": 0.0, "mrr@10": 0.0, "coverage": 0.0,
    }


def test_aggregate_metrics_mixed():
    ms = [
        _qm(hit_at_1=True, hit_at_3=True, hit_at_5=True, rr_at_10=1.0,
            keyword_coverage=1.0),
        _qm(hit_at_1=False, hit_at_3=False, hit_at_5=True, rr_at_10=0.25,
            keyword_coverage=0.5),
    ]
    agg = evaluate.aggregate_metrics(ms)
    assert agg["hit@1"] == 0.5
    assert agg["hit@3"] == 0.5
    assert agg["hit@5"] == 1.0
    assert abs(agg["mrr@10"] - 0.625) < 1e-9
    assert abs(agg["coverage"] - 0.75) < 1e-9


# ------------------------------------------ _build_section_subtree (DB-backed)

def test_build_section_subtree_isolates_by_source_format():
    """Two specs sharing section_numbers (the same spec ingested as both
    pdf_pymupdf and tspec_md) must not let one source's subtree overwrite the
    other's. The map is keyed by bare section_number, so the scorer filters by
    --source-format to build the tree from the corpus the run retrieves from."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    from src.models import Base, Section, Spec

    engine = create_engine("sqlite://", future=True)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        # pdf spec: 6.2.1 (parent) + 6.2.1.5 (child) — shallow tree
        pdf = Spec(name="38.521-1", version="17.5.0",
                   source_file="x.pdf", source_format="pdf_pymupdf")
        session.add(pdf)
        session.flush()
        pdf_parent = Section(spec_id=pdf.spec_id, section_number="6.2.1",
                             title="Max power", level=2, page_start=1)
        session.add(pdf_parent)
        session.flush()
        session.add(Section(spec_id=pdf.spec_id, parent_id=pdf_parent.section_id,
                            section_number="6.2.1.5", title="Test req",
                            level=3, page_start=2))
        # md spec: 6.2.1 (parent) + 6.2.1.4 + 6.2.1.4.1 — deeper, different
        md = Spec(name="38.521-1", version="i00",
                  source_file="x.md", source_format="tspec_md")
        session.add(md)
        session.flush()
        md_parent = Section(spec_id=md.spec_id, section_number="6.2.1",
                            title="Max power", level=2, page_start=1)
        session.add(md_parent)
        session.flush()
        md_mid = Section(spec_id=md.spec_id, parent_id=md_parent.section_id,
                         section_number="6.2.1.4", title="Conformance",
                         level=3, page_start=2)
        session.add(md_mid)
        session.flush()
        session.add(Section(spec_id=md.spec_id, parent_id=md_mid.section_id,
                            section_number="6.2.1.4.1", title="Deeper",
                            level=4, page_start=3))
        session.commit()

        pdf_tree = evaluate._build_section_subtree(
            session, source_format="pdf_pymupdf")
        assert pdf_tree["6.2.1"] == {"6.2.1", "6.2.1.5"}
        # the deep md node must not bleed into the pdf-filtered map at all
        assert "6.2.1.4.1" not in pdf_tree

        md_tree = evaluate._build_section_subtree(
            session, source_format="tspec_md")
        assert md_tree["6.2.1"] == {"6.2.1", "6.2.1.4", "6.2.1.4.1"}


# ----------------------------------------------------- gate scoring helpers

def _gr(**overrides):
    base = dict(
        qid="qx", answerability="answerable", oos_kind=None, outcome="answer",
        confidence=0.9, reason="", hit_correct=True, coverage=1.0,
        classification="TN",
    )
    base.update(overrides)
    return evaluate.GateQuestionResult(**base)


def test_classify_gate_four_cells():
    # REFUSE is the positive class.
    assert evaluate.classify_gate(answerability="out_of_scope", outcome="refuse") == "TP"
    assert evaluate.classify_gate(answerability="out_of_scope", outcome="answer") == "FN"
    assert evaluate.classify_gate(answerability="answerable", outcome="answer") == "TN"
    assert evaluate.classify_gate(answerability="answerable", outcome="refuse") == "FP"


def test_classify_gate_lowconf_default_is_answer():
    assert evaluate.classify_gate(
        answerability="answerable", outcome="low_confidence"
    ) == "TN"
    assert evaluate.classify_gate(
        answerability="out_of_scope", outcome="low_confidence"
    ) == "FN"


def test_classify_gate_lowconf_as_refuse_flips():
    assert evaluate.classify_gate(
        answerability="out_of_scope", outcome="low_confidence",
        lowconf_as_refuse=True,
    ) == "TP"
    assert evaluate.classify_gate(
        answerability="answerable", outcome="low_confidence",
        lowconf_as_refuse=True,
    ) == "FP"


def test_gate_confusion_precision_recall_f1():
    results = [
        _gr(classification="TP"), _gr(classification="TP"),
        _gr(classification="FP"),
        _gr(classification="FN"),
        _gr(classification="TN"), _gr(classification="TN"),
    ]
    cm = evaluate.gate_confusion(results)
    assert (cm["TP"], cm["FP"], cm["TN"], cm["FN"]) == (2, 1, 2, 1)
    assert abs(cm["precision"] - 2 / 3) < 1e-9
    assert abs(cm["recall"] - 2 / 3) < 1e-9
    assert abs(cm["f1"] - 2 / 3) < 1e-9


def test_gate_confusion_empty_zeros():
    cm = evaluate.gate_confusion([])
    assert cm == {
        "TP": 0, "FP": 0, "TN": 0, "FN": 0,
        "precision": 0.0, "recall": 0.0, "f1": 0.0,
    }


def test_citation_accuracy_over_answered_only():
    results = [
        _gr(classification="TN", hit_correct=True),
        _gr(classification="TN", hit_correct=False),
        _gr(classification="FP", hit_correct=False),   # refused -> excluded
        _gr(classification="TP", hit_correct=False),   # out-of-scope -> excluded
    ]
    assert evaluate.citation_accuracy(results) == 0.5


def test_citation_accuracy_empty_zero():
    assert evaluate.citation_accuracy([_gr(classification="FP")]) == 0.0


def test_gate_mean_coverage_over_answered():
    results = [
        _gr(classification="TN", coverage=1.0),
        _gr(classification="TN", coverage=0.5),
        _gr(classification="TP", coverage=None),   # out-of-scope -> excluded
    ]
    assert abs(evaluate.gate_mean_coverage(results) - 0.75) < 1e-9
