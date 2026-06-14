"""Unit tests for app/_render.py — pure UI formatting helpers (no streamlit)."""

from __future__ import annotations

from types import SimpleNamespace

from app._render import (
    citation_line,
    format_source_locator,
    gate_badge,
    hit_locator,
)
from src.retrieval import GateOutcome


def test_gate_badge_all_outcomes():
    assert gate_badge("answer") == ("ANSWER", "green")
    assert gate_badge("low_confidence") == ("LOW CONFIDENCE", "orange")
    assert gate_badge("refuse") == ("REFUSE", "red")
    # accepts the StrEnum too (str(GateOutcome.ANSWER) == "answer")
    assert gate_badge(GateOutcome.ANSWER) == ("ANSWER", "green")
    # unknown -> gray
    assert gate_badge("weird") == ("WEIRD", "gray")


def test_format_source_locator():
    assert format_source_locator(section="6.3.1") == "§6.3.1"
    assert (
        format_source_locator(section="6.2.1", table_id="6.2.1.5-1")
        == "§6.2.1, Table 6.2.1.5-1"
    )
    assert format_source_locator(section="6.2.1", page=12) == "§6.2.1, p.12"
    # page 0 (md sentinel) and None both omitted
    assert format_source_locator(section="6.3.1", page=0) == "§6.3.1"
    assert format_source_locator(section="6.3.1", page=None) == "§6.3.1"
    assert (
        format_source_locator(section="6.2.1", table_id="T1", page=5)
        == "§6.2.1, Table T1, p.5"
    )


def test_citation_line():
    c = {"n": 2, "section": "6.2.1", "page": 12, "table_id": "6.2.1.5-1", "chunk_id": 9}
    assert citation_line(c) == "[2] §6.2.1, Table 6.2.1.5-1, p.12"
    # page None tolerated
    c2 = {"n": 1, "section": "6.3.1", "page": None, "table_id": None, "chunk_id": 1}
    assert citation_line(c2) == "[1] §6.3.1"


def test_hit_locator():
    hit = SimpleNamespace(section_number="6.3.1", table_id=None, page=0)
    assert hit_locator(hit) == "§6.3.1"
    hit2 = SimpleNamespace(section_number="6.2.1", table_id="6.2.1.5-1", page=12)
    assert hit_locator(hit2) == "§6.2.1, Table 6.2.1.5-1, p.12"
