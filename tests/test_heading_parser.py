"""Unit tests for heading detection + anchor extraction (M1).

Fixtures are verbatim cuts from the real TSpec-LLM 38.521-1 R18 corpus —
the setext/ATX mix and the H8 annex marker are exactly what production
parse() will meet.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.ingestion._heading_parser import (
    _is_setext_underline,
    extract_anchor,
    parse_headings,
)

FIXTURES = Path(__file__).parent / "fixtures" / "md"


# ------------------------------------------------------------ extract_anchor

@pytest.mark.parametrize("title,expected_anchor", [
    ("6 Transmitter characteristics", "6"),
    ("6.1 General", "6.1"),
    ("6.3.1 Minimum output power", "6.3.1"),
    ("6.3.4.2 Absolute power tolerance", "6.3.4.2"),
    ("6.3.1.1.1 Test purpose", "6.3.1.1.1"),
    ("6.2A Maximum output power for CA", "6.2A"),
    ("6.3.1A Minimum output power for CA", "6.3.1A"),
    ("A.1 General", "A.1"),
    ("A.2.2.1 DFT-s-OFDM Pi/2-BPSK", "A.2.2.1"),
    ("Annex A (normative): Measurement channels", "A"),
    ("General", None),
    ("Scope", None),
])
def test_extract_anchor_forms(title, expected_anchor):
    anchor, _ = extract_anchor(title)
    assert anchor == expected_anchor


def test_extract_anchor_residual_title():
    anchor, residual = extract_anchor("6.3.2 Transmit OFF power")
    assert anchor == "6.3.2"
    assert residual == "Transmit OFF power"


# --------------------------------------------------- setext disambiguation

def test_setext_underline_accepts_real_heading():
    assert _is_setext_underline("-----------", "6.1 General", "")


def test_setext_underline_rejects_multi_run_table_rule():
    assert not _is_setext_underline(
        "-------- ---------------", "SCS  Active Uplink slots", "",
    )


def test_setext_underline_rejects_column_layout_header():
    # Even a single-run underline under a columnar line is a table rule.
    assert not _is_setext_underline(
        "----------------", "SCS  Active Uplink slots", "",
    )


def test_setext_underline_rejects_non_block_start():
    # Heading line must start a block (blank line or BOF above).
    assert not _is_setext_underline("-----", "continuation text", "prose above")


# ------------------------------------------------------------ parse_headings

def test_parse_setext_atx_mix_fixture():
    text = (FIXTURES / "headings_setext_atx_mix.md").read_text(encoding="utf-8")
    headings, _ = parse_headings(text)
    got = [(h.anchor, h.level) for h in headings]
    assert got == [("6", 1), ("6.1", 2), ("A.2.2.1", 3)]
    # The simple table's rule lines must NOT have produced headings.
    assert all("SCS" not in h.title for h in headings)


def test_parse_annex_h8_fixture():
    text = (FIXTURES / "headings_annex_h8.md").read_text(encoding="utf-8")
    headings, _ = parse_headings(text)
    got = [(h.anchor, h.level) for h in headings]
    assert got == [("A", 8), ("A.1", 1), ("A.2", 1), ("A.2.1", 2)]
    assert headings[0].line_no == 0


def test_line_numbers_index_into_source():
    text = (FIXTURES / "headings_setext_atx_mix.md").read_text(encoding="utf-8")
    lines = text.split("\n")
    headings, _ = parse_headings(text)
    for h in headings:
        assert h.title in lines[h.line_no]


def test_level_jump_warns_not_raises():
    text = "## 6.2 Top\n\n#### 6.2.1.1.1 Deep\n"
    headings, warnings = parse_headings(text)
    assert [h.anchor for h in headings] == ["6.2", "6.2.1.1.1"]
    assert any("level jump" in w for w in warnings)


def test_anchorless_heading_warns():
    text = "### General\n"
    headings, warnings = parse_headings(text)
    assert headings[0].anchor is None
    assert any("without parseable anchor" in w for w in warnings)


def test_pandoc_id_attached_by_line_number():
    text = "6.2.1 UE maximum output power\n-----------------------------\n"
    headings, _ = parse_headings(
        text, anchor_map={0: "ue-maximum-output-power .unnumbered"},
    )
    assert headings[0].pandoc_id == "ue-maximum-output-power .unnumbered"
    assert headings[0].anchor == "6.2.1"
