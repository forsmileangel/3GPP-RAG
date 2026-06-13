"""Unit tests for the pure helpers in scripts/evaluate_facts.py."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location(
    "evaluate_facts_module", REPO_ROOT / "scripts" / "evaluate_facts.py",
)
ef = importlib.util.module_from_spec(_spec)
# Register before exec: @dataclass resolves cls.__module__ via sys.modules.
sys.modules["evaluate_facts_module"] = ef
_spec.loader.exec_module(ef)


def test_parse_expected_values():
    assert ef.parse_expected_values(
        ["minimum output power", "-40", "9.375"]
    ) == [-40.0, 9.375]
    assert ef.parse_expected_values(["n14", "31", "public safety"]) == [31.0]
    assert ef.parse_expected_values(["inner", "outer", "channel bandwidth"]) == []


def test_value_matches():
    assert ef.value_matches(-40.0, [-40.0, 9.375]) is True
    assert ef.value_matches(23.0, [1.23]) is False     # R8 at the metric layer
    assert ef.value_matches(None, [1.0]) is False
    assert ef.value_matches(9.375, [9.375]) is True


def test_section_matches():
    assert ef.section_matches("6.3.1.3", "6.3.1") is True
    assert ef.section_matches("6.3.1", "6.3.1") is True
    assert ef.section_matches("6.2.1", "6.3.1") is False
    assert ef.section_matches(None, "6.3.1") is False


def _res(**kw):
    base = dict(
        qid="qx", qtype="numeric", expected_section="6.2.1",
        expected_values=[1.0], has_values=True, value_hit_1=True,
        value_hit_k=True, chunk_cite_1=True, factsfirst_cite_1=True,
        top_fact="x",
    )
    base.update(kw)
    return ef.FactQResult(**base)


def test_format_report_decision_pass():
    rep = ef._format_report([_res() for _ in range(10)], source_format="tspec_md")
    assert "UNNECESSARY" in rep


def test_format_report_decision_fail():
    rep = ef._format_report(
        [_res(qid="q1", value_hit_1=False, value_hit_k=False,
              chunk_cite_1=False, factsfirst_cite_1=False, top_fact=None)],
        source_format="tspec_md",
    )
    assert "proceed to the LLM decision" in rep and "q1" in rep
