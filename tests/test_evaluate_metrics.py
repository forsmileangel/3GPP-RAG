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
