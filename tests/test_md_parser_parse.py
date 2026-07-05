"""Tests for MarkdownAdapter.discover_inputs + parse (M3 — no DB).

Two layers: synthetic tmp-dir specs (deterministic, CI-safe) and the real
TSpec-LLM corpus under spike/ (e2e-marked, skipped when absent — mirrors
test_question_bank.py's PDF guard).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.ingestion._base import InputUnit
from src.ingestion.md_parser import (
    MarkdownAdapter,
    _merge_duplicate_sections,
    _parent_path_of,
    _release_from_version,
)
from src.source_formats import SOURCE_FORMAT_TSPEC_MD

CORPUS_38 = (
    Path(__file__).resolve().parent.parent
    / "spike" / "tspec_probe_out" / "3GPP-clean" / "Rel-18" / "38_series"
)


# ------------------------------------------------------------------ helpers

def test_release_from_version():
    assert _release_from_version("i00") == "R18"
    assert _release_from_version("h60") == "R17"
    assert _release_from_version("j10") == "R19"


def test_parent_path_of():
    assert _parent_path_of("6.3.4.2") == ["6", "6.3", "6.3.4", "6.3.4.2"]
    assert _parent_path_of("A.2") == ["A", "A.2"]
    assert _parent_path_of("6") == ["6"]
    # band-combination: "_" stays inside its segment, so the subtree nests
    # under 6.2D.1_1 — parallel to (not colliding with) the real 6.2D.1.
    assert _parent_path_of("6.2D.1_1.1") == ["6", "6.2D", "6.2D.1_1", "6.2D.1_1.1"]
    # inserted-clause lowercase variant: sibling of 6.4.2.1, child of 6.4.2.
    assert _parent_path_of("6.4.2.1a") == ["6", "6.4", "6.4.2", "6.4.2.1a"]


def test_merge_duplicate_sections():
    from src.ingestion._base import Heading, Section

    def _sec(anchor: str, line_no: int, body: str) -> Section:
        return Section(
            heading=Heading(level=3, title=f"{anchor} T", anchor=anchor,
                            pandoc_id=None, line_no=line_no),
            body_text=body,
            tables=[],
            parent_path=_parent_path_of(anchor),
        )

    first = _sec("7.6A.4", 10, "first body")
    dup = _sec("7.6A.4", 90, "typo-family body")
    other = _sec("7.6A.5", 200, "unrelated")
    merged, warnings = _merge_duplicate_sections([first, dup, other])

    # duplicate folded into the first occurrence; content preserved; warned
    assert [s.heading.anchor for s in merged] == ["7.6A.4", "7.6A.5"]
    assert "first body" in merged[0].body_text
    assert "typo-family body" in merged[0].body_text
    assert any("merged duplicate section" in w and "7.6A.4" in w
               for w in warnings)
    # no duplicates -> untouched, no warnings
    merged2, warnings2 = _merge_duplicate_sections([other])
    assert merged2 == [other] and warnings2 == []


# ----------------------------------------------------------------- discover

def _write(root: Path, name: str, body: str) -> None:
    (root / name).write_text(body, encoding="utf-8")


def test_discover_groups_multifile_unit(tmp_path):
    # The sanity gate needs >= 100 bytes + a heading; pad realistically.
    pad = "Filler prose so the sanity gate's 100-byte floor is cleared.\n" * 3
    head = f"6 Transmitter characteristics\n====\n\n{pad}"
    _write(tmp_path, "38521-1-i00_cover.md", f"# 3GPP TS 38.521-1 cover\n\n{pad}")
    _write(tmp_path, "38521-1-i00_s06-s0602C.md", head)
    _write(tmp_path, "38521-1-i00_sAnnexes.md", f"######## Annex A\n\n{pad}")
    _write(tmp_path, "38521-2-i00.md", f"# 38.521-2 single file\n\n{pad}")
    _write(tmp_path, "README.md", f"# not a spec\n\n{pad}")

    adapter = MarkdownAdapter()
    units = adapter.discover_inputs(tmp_path)

    assert len(units) == 2
    # The stray README must be skipped but VISIBLY (no silent vanishing).
    assert any("README.md" in issue for issue in adapter.last_discovery_issues)
    unit_p1 = next(u for u in units if u.part == "1")
    assert unit_p1.spec_id == "38.521"
    assert unit_p1.version == "i00"
    assert unit_p1.release == "R18"
    assert unit_p1.source_format == SOURCE_FORMAT_TSPEC_MD
    assert [p.name for p in unit_p1.source_paths] == [
        "38521-1-i00_cover.md",
        "38521-1-i00_s06-s0602C.md",
        "38521-1-i00_sAnnexes.md",
    ]


# -------------------------------------------------------------------- parse

_FILE_ONE = """6 Transmitter characteristics
=============================

6.1 General
-----------

General prose about the transmitter requirements before any subsection.
"""

_FILE_TWO = """6.3.4 Power control
-------------------

### 6.3.4.1 General

The requirements on power control accuracy apply under normal conditions.

### 6.3.4.2 Absolute power tolerance

Tolerance prose with an artifact P~CMAX~ marker.

Table 6.3.4.2-1: Tolerances

  Condition   Tolerance
  ----------- -----------
  Normal      +/- 9.0 dB

### General

Anchorless heading whose text must stay inside 6.3.4.2's body.
"""


def _two_file_unit(tmp_path) -> InputUnit:
    a = tmp_path / "38521-1-i00_s06-s0602C.md"
    b = tmp_path / "38521-1-i00_s0603A-s0604G.md"
    a.write_text(_FILE_ONE, encoding="utf-8")
    b.write_text(_FILE_TWO, encoding="utf-8")
    return InputUnit(
        spec_id="38.521", part="1", version="i00", release="R18",
        source_format=SOURCE_FORMAT_TSPEC_MD, source_paths=(a, b),
    )


def test_parse_merges_files_and_builds_section_tree(tmp_path):
    parsed = MarkdownAdapter().parse(_two_file_unit(tmp_path))

    anchors = [s.heading.anchor for s in parsed.sections]
    assert anchors == ["6", "6.1", "6.3.4", "6.3.4.1", "6.3.4.2"]

    by_anchor = {s.heading.anchor: s for s in parsed.sections}
    assert by_anchor["6.3.4.2"].parent_path == ["6", "6.3", "6.3.4", "6.3.4.2"]

    # Merge proof: the second file's headings live past the first file's
    # line count in the merged text.
    file_one_lines = _FILE_ONE.count("\n")
    assert by_anchor["6.3.4"].heading.line_no >= file_one_lines


def test_parse_splits_tables_out_of_body(tmp_path):
    parsed = MarkdownAdapter().parse(_two_file_unit(tmp_path))
    sec = next(s for s in parsed.sections if s.heading.anchor == "6.3.4.2")

    assert len(sec.tables) == 1
    assert sec.tables[0].caption_id == "6.3.4.2-1"
    assert "+/- 9.0 dB" in sec.tables[0].rendered_text
    assert "+/- 9.0 dB" not in sec.body_text          # excised from prose
    # Cleaned artifact present as searchable text, not pandoc markup.
    assert "P_CMAX" in sec.body_text
    # The anchorless "### General" heading did not open a section; its
    # trailing text stays in 6.3.4.2's body.
    assert "must stay inside" in sec.body_text


def test_parse_records_anchorless_warning(tmp_path):
    parsed = MarkdownAdapter().parse(_two_file_unit(tmp_path))
    assert any("without parseable anchor" in w for w in parsed.warnings)


def test_parse_body_excludes_heading_and_underline(tmp_path):
    parsed = MarkdownAdapter().parse(_two_file_unit(tmp_path))
    sec = next(s for s in parsed.sections if s.heading.anchor == "6.1")
    assert not sec.body_text.startswith("-")
    assert "General prose about the transmitter" in sec.body_text


# ------------------------------------------------------------- real corpus

needs_corpus = pytest.mark.skipif(
    not CORPUS_38.exists(), reason=f"TSpec corpus unavailable: {CORPUS_38}",
)


@pytest.mark.e2e
@needs_corpus
def test_discover_real_corpus_groups_38521_1():
    units = MarkdownAdapter().discover_inputs(CORPUS_38)
    unit = next(
        u for u in units
        if u.spec_id == "38.521" and u.part == "1" and u.version == "i00"
    )
    assert len(unit.source_paths) == 8
    assert unit.source_paths[0].name == "38521-1-i00_cover.md"
    assert unit.source_paths[-1].name == "38521-1-i00_sAnnexes.md"


@pytest.mark.e2e
@needs_corpus
def test_parse_real_38521_1_yields_distinct_634x_sections():
    """The whole point of the markdown path: §6.3.4.1–.4 must come out as
    DISTINCT sections (the PDF flow's shared-page attribution can't keep
    them apart — q13/q17/q28)."""
    adapter = MarkdownAdapter()
    units = adapter.discover_inputs(CORPUS_38)
    unit = next(
        u for u in units
        if u.spec_id == "38.521" and u.part == "1" and u.version == "i00"
    )
    parsed = adapter.parse(unit)

    anchors = {s.heading.anchor for s in parsed.sections}
    for expected in ("6.2.1", "6.3.1", "6.3.2",
                     "6.3.4.1", "6.3.4.2", "6.3.4.3", "6.3.4.4"):
        assert expected in anchors, f"missing section {expected}"

    # Band-combination clauses ("6.2D.1\_1.1") must parse as sections
    # DISTINCT from the real 6.2D.1 (pre-fix they all collapsed onto it).
    for expected in ("6.2D.1", "6.2D.1_1", "6.2D.1_1.1"):
        assert expected in anchors, f"missing band-combo section {expected}"

    # Inserted-clause lowercase variants must be distinct from their parent
    # (pre-fix "6.4.2.1a" truncated to "6.4.2" — nine-way collision).
    for expected in ("6.4.2", "6.4.2.1a", "6.4.2.1a.1"):
        assert expected in anchors, f"missing inserted-clause section {expected}"

    # After duplicate-merge, anchors are unique across the parse — the emit
    # UNIQUE(spec_id, section_number) constraint cannot fire.
    all_anchors = [s.heading.anchor for s in parsed.sections]
    assert len(all_anchors) == len(set(all_anchors))

    # md parses DEEPER than the PDF bookmarks (which stop at level 3): the
    # prose lives in 6.3.2.x / 6.3.4.2.x subsections, the parents stay thin.
    # Assert at subtree granularity, the same way evaluate.py scores.
    by_anchor = {s.heading.anchor: s for s in parsed.sections}
    assert "Transmit OFF power" in by_anchor["6.3.2"].heading.title

    def _subtree_text(prefix: str) -> str:
        chunks: list[str] = []
        for sec in parsed.sections:
            anchor = sec.heading.anchor or ""
            if anchor == prefix or anchor.startswith(prefix + "."):
                chunks.append(sec.body_text)
                chunks.extend(t.rendered_text for t in sec.tables)
        return " ".join(chunks)

    assert "Transmit OFF power" in _subtree_text("6.3.2")
    assert "9.0" in _subtree_text("6.3.4.2")
