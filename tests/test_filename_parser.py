"""Unit tests for the TSpec-LLM filename parser.

Cover:
  - All 6 scope kinds (NONE / COVER / SECTION_RANGE / SINGLE_SECTION /
    ANNEX_RANGE / ANNEXES_ALL)
  - Single-file parts vs multi-file parts
  - 38.521-1 R18 full 8-file sort order
  - 36.521-1 R18 full 13-file sort order (excludes the 0-byte cover)
  - Invalid filenames raise FilenameParseError
  - FileNameInfo is frozen / hashable
"""

from __future__ import annotations

import pytest

from src.ingestion._filename_parser import (
    FilenameParseError,
    ScopeKind,
    parse_filename,
    sort_key,
)


# --------------------------------------------------------------------------
# Single-filename cases
# --------------------------------------------------------------------------

def test_no_part_no_scope():
    """38.331 has no parts and no scope splits."""
    info = parse_filename("38331-h60.md")
    assert info.spec_id == "38.331"
    assert info.part is None
    assert info.version == "h60"
    assert info.scope == ScopeKind.NONE
    assert info.scope_start is None
    assert info.scope_end is None


def test_with_part_no_scope():
    """36521-2 is a single-file part — has part but no scope."""
    info = parse_filename("36521-2-i20.md")
    assert info.spec_id == "36.521"
    assert info.part == "2"
    assert info.scope == ScopeKind.NONE


def test_cover():
    info = parse_filename("38521-1-i00_cover.md")
    assert info.scope == ScopeKind.COVER
    assert info.scope_start is None


def test_section_range():
    info = parse_filename("38521-1-i00_s06-s0602C.md")
    assert info.scope == ScopeKind.SECTION_RANGE
    assert info.scope_start == "s06"
    assert info.scope_end == "s0602C"


def test_section_range_with_letter_suffix():
    info = parse_filename("36521-1-i20_s07ca9-s07d.md")
    assert info.scope == ScopeKind.SECTION_RANGE
    assert info.scope_start == "s07ca9"
    assert info.scope_end == "s07d"


def test_single_section():
    info = parse_filename("38521-1-i00_s0700.md")
    assert info.scope == ScopeKind.SINGLE_SECTION
    assert info.scope_start == "s0700"
    assert info.scope_end == "s0700"


def test_single_section_short():
    info = parse_filename("38521-1-i00_s0605.md")
    assert info.scope == ScopeKind.SINGLE_SECTION
    assert info.scope_start == "s0605"


def test_annex_range():
    info = parse_filename("36521-1-i20_sAnnexA-sAnnexE.md")
    assert info.scope == ScopeKind.ANNEX_RANGE
    assert info.scope_start == "sAnnexA"
    assert info.scope_end == "sAnnexE"


def test_annexes_all():
    info = parse_filename("38521-1-i00_sAnnexes.md")
    assert info.scope == ScopeKind.ANNEXES_ALL
    assert info.scope_start is None


def test_underscore_in_section_id():
    """e.g. s08h-s08_14 — the trailing _14 is part of the end token."""
    info = parse_filename("36521-1-i20_s08h-s08_14.md")
    assert info.scope == ScopeKind.SECTION_RANGE
    assert info.scope_start == "s08h"
    assert info.scope_end == "s08_14"


# --------------------------------------------------------------------------
# Invalid filenames
# --------------------------------------------------------------------------

def test_invalid_random():
    with pytest.raises(FilenameParseError):
        parse_filename("not_a_spec_filename.md")


def test_invalid_short_num():
    with pytest.raises(FilenameParseError):
        parse_filename("38-h60.md")  # num too short


def test_invalid_extension():
    with pytest.raises(FilenameParseError):
        parse_filename("38331-h60.txt")


# --------------------------------------------------------------------------
# Hashability (FileNameInfo frozen)
# --------------------------------------------------------------------------

def test_frozen_filenameinfo_hashable():
    """FileNameInfo should be frozen so it can live in a set."""
    a = parse_filename("38331-h60.md")
    b = parse_filename("38331-h60.md")
    assert a == b
    s = {a, b}
    assert len(s) == 1


# --------------------------------------------------------------------------
# Sort order — full part lists from eval report §(d)
# --------------------------------------------------------------------------

def test_38521_1_r18_full_8_files_sort_order():
    """38.521-1 R18 full file list, intentionally shuffled, must sort to
    cover → s00-s05 → s06-s0602C → s0602D-s060304 → s0603A-s0604G →
    s0605 → s0700 → sAnnexes (per eval report §(d))."""
    raw_files = [
        "38521-1-i00_s0603A-s0604G.md",
        "38521-1-i00_sAnnexes.md",
        "38521-1-i00_cover.md",
        "38521-1-i00_s06-s0602C.md",
        "38521-1-i00_s0605.md",
        "38521-1-i00_s00-s05.md",
        "38521-1-i00_s0700.md",
        "38521-1-i00_s0602D-s060304.md",
    ]
    parsed = [parse_filename(f) for f in raw_files]
    parsed.sort(key=sort_key)

    expected = [
        "38521-1-i00_cover.md",
        "38521-1-i00_s00-s05.md",
        "38521-1-i00_s06-s0602C.md",
        "38521-1-i00_s0602D-s060304.md",
        "38521-1-i00_s0603A-s0604G.md",
        "38521-1-i00_s0605.md",
        "38521-1-i00_s0700.md",
        "38521-1-i00_sAnnexes.md",
    ]
    assert [p.raw for p in parsed] == expected


def test_36521_1_r18_full_13_files_sort_order():
    """36.521-1 R18 file list (excluding the 0-byte cover.md). Tests
    letter-mixed scope IDs (s06b5, s07ca8, s07ca9, s08_14) and that the
    annex range goes after section ranges."""
    raw_files = [
        "36521-1-i20_s09-s14.md",
        "36521-1-i20_s06f3-s06h.md",
        "36521-1-i20_s00-s05.md",
        "36521-1-i20_sAnnexA-sAnnexE.md",
        "36521-1-i20_s06a-s06b4.md",
        "36521-1-i20_s07ca9-s07d.md",
        "36521-1-i20_s06e-s06f2.md",
        "36521-1-i20_s07e-s07j.md",
        "36521-1-i20_s08a-s08g.md",
        "36521-1-i20_s07a-s07ca8.md",
        "36521-1-i20_s06b5-s06d.md",
        "36521-1-i20_s08h-s08_14.md",
        "36521-1-i20_sAnnexF-sAnnexL.md",
    ]
    parsed = [parse_filename(f) for f in raw_files]
    parsed.sort(key=sort_key)

    expected = [
        "36521-1-i20_s00-s05.md",
        "36521-1-i20_s06a-s06b4.md",
        "36521-1-i20_s06b5-s06d.md",
        "36521-1-i20_s06e-s06f2.md",
        "36521-1-i20_s06f3-s06h.md",
        "36521-1-i20_s07a-s07ca8.md",
        "36521-1-i20_s07ca9-s07d.md",
        "36521-1-i20_s07e-s07j.md",
        "36521-1-i20_s08a-s08g.md",
        "36521-1-i20_s08h-s08_14.md",
        "36521-1-i20_s09-s14.md",
        "36521-1-i20_sAnnexA-sAnnexE.md",
        "36521-1-i20_sAnnexF-sAnnexL.md",
    ]
    assert [p.raw for p in parsed] == expected


def test_sort_priority_cover_before_sections_before_annexes():
    """Sanity check: cover < section/single < annex_range < annexes_all."""
    cover = parse_filename("38521-1-i00_cover.md")
    section = parse_filename("38521-1-i00_s06-s0602C.md")
    single = parse_filename("38521-1-i00_s0700.md")
    annex = parse_filename("36521-1-i20_sAnnexA-sAnnexE.md")
    annexes_all = parse_filename("38521-1-i00_sAnnexes.md")

    assert sort_key(cover) < sort_key(section)
    assert sort_key(section) < sort_key(annex)
    assert sort_key(annex) < sort_key(annexes_all)
    # section_range and single_section share priority — sub-order by scope_start
    assert sort_key(section)[0] == sort_key(single)[0]
