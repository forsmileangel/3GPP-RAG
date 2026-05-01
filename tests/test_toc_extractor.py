"""Unit tests for the TOC extractor — cover sibling vs child handling,
multi-section requests, page-end computation, and error paths.

These tests use synthetic TOCs (no real PDF) to exercise the pure logic
in `compute_section_tree` and `parse_toc`.
"""

from __future__ import annotations

import pytest

from src.ingestion.toc_extractor import (
    SectionNotFoundError,
    TOCEmptyError,
    compute_section_tree,
    parse_toc,
)


# Fragment of a realistic TS 38.521-1 TOC with §6.2 / §6.2A siblings and
# §6.3 sibling-of-§6.2. Levels: 1 = chapter, 2 = section, 3..n = subsections.
SAMPLE_TOC_RAW = [
    [1, "6 Transmitter characteristics", 90],
    [2, "6.2 Transmitter power", 92],
    [3, "6.2.1 UE maximum output power", 92],
    [4, "6.2.1.5 Maximum output power", 93],
    [4, "6.2.1.6 Test requirement", 96],
    [3, "6.2.2 UE maximum output power reduction", 98],
    [3, "6.2.3 UE additional MPR (A-MPR)", 123],
    [3, "6.2.4 Configured transmitted power", 273],
    [2, "6.2A Transmitter power for CA", 280],
    [3, "6.2A.1 UE maximum output power for CA", 280],
    [2, "6.2B Transmitter power for DC", 410],
    [2, "6.3 Output power dynamics", 541],
    [3, "6.3.1 Minimum output power", 541],
    [4, "6.3.1.1 Test purpose", 541],
    [3, "6.3.2 Transmit OFF power", 544],
    [4, "6.3.2.1 Test purpose", 544],
    [2, "6.4 Receiver characteristics", 600],
]
TOTAL_PAGES = 700


@pytest.fixture
def toc():
    return parse_toc(SAMPLE_TOC_RAW, TOTAL_PAGES)


def test_parse_toc_splits_section_number(toc):
    assert toc[0].section_number == "6"
    assert toc[0].title == "Transmitter characteristics"
    assert toc[1].section_number == "6.2"
    assert toc[1].title == "Transmitter power"
    assert toc[8].section_number == "6.2A"


def test_parse_toc_clamps_pages():
    raw = [[1, "1 Foo", 0], [1, "2 Bar", 99999]]
    parsed = parse_toc(raw, total_pages=10)
    assert parsed[0].page_1idx == 1
    assert parsed[1].page_1idx == 10


def test_request_62_excludes_62A(toc):
    """The Phase 0 lesson: §6.2A is sibling not child of §6.2."""
    result = compute_section_tree(toc, TOTAL_PAGES, ["6.2"])
    section_nums = [s.section_number for s in result]
    assert "6.2" in section_nums
    assert "6.2.1" in section_nums
    assert "6.2.1.5" in section_nums
    assert "6.2.4" in section_nums
    # The whole point of this test:
    assert "6.2A" not in section_nums
    assert "6.2B" not in section_nums
    assert "6.3" not in section_nums


def test_request_62_page_end_stops_before_62A(toc):
    """§6.2 ends on the page before §6.2A starts."""
    result = compute_section_tree(toc, TOTAL_PAGES, ["6.2"])
    sec_62 = next(s for s in result if s.section_number == "6.2")
    assert sec_62.page_start == 92
    assert sec_62.page_end == 279  # §6.2A starts at 280, so §6.2 ends at 279


def test_multi_section_request_62_and_63(toc):
    result = compute_section_tree(toc, TOTAL_PAGES, ["6.2", "6.3"])
    section_nums = {s.section_number for s in result}
    # both branches included
    assert {"6.2", "6.2.1", "6.3", "6.3.1", "6.3.2"} <= section_nums
    # siblings still excluded
    assert "6.2A" not in section_nums
    assert "6.4" not in section_nums


def test_explicit_request_for_sibling_includes_it(toc):
    """User can opt in to §6.2A by asking for it directly."""
    result = compute_section_tree(toc, TOTAL_PAGES, ["6.2", "6.2A"])
    section_nums = {s.section_number for s in result}
    assert "6.2A" in section_nums
    assert "6.2A.1" in section_nums  # its descendant
    assert "6.2B" not in section_nums  # still excluded


def test_parent_number_set_only_within_selection(toc):
    result = compute_section_tree(toc, TOTAL_PAGES, ["6.2"])
    by_num = {s.section_number: s for s in result}
    # 6.2 was requested, no parent in selection (we didn't request "6")
    assert by_num["6.2"].parent_number is None
    # 6.2.1 is a child of 6.2 (which IS in selection)
    assert by_num["6.2.1"].parent_number == "6.2"
    # 6.2.1.5 -> 6.2.1
    assert by_num["6.2.1.5"].parent_number == "6.2.1"
    # 6.2.2 is sibling of 6.2.1, parent is 6.2
    assert by_num["6.2.2"].parent_number == "6.2"


def test_children_list_populated(toc):
    result = compute_section_tree(toc, TOTAL_PAGES, ["6.2"])
    by_num = {s.section_number: s for s in result}
    # 6.2 has 4 direct subsection children: 6.2.1 .. 6.2.4
    assert set(by_num["6.2"].children) == {"6.2.1", "6.2.2", "6.2.3", "6.2.4"}
    assert set(by_num["6.2.1"].children) == {"6.2.1.5", "6.2.1.6"}


def test_requested_flag_distinguishes_user_pick_from_pulled_in(toc):
    result = compute_section_tree(toc, TOTAL_PAGES, ["6.2"])
    by_num = {s.section_number: s for s in result}
    assert by_num["6.2"].requested is True
    assert by_num["6.2.1"].requested is False  # pulled in as descendant


def test_unknown_section_raises():
    toc = parse_toc(SAMPLE_TOC_RAW, TOTAL_PAGES)
    with pytest.raises(SectionNotFoundError):
        compute_section_tree(toc, TOTAL_PAGES, ["9.99"])


def test_empty_toc_raises():
    with pytest.raises(TOCEmptyError):
        compute_section_tree([], TOTAL_PAGES, ["6.2"])


def test_last_section_page_end_runs_to_doc_end(toc):
    """The last subsection of the requested branch covers up to the doc end
    when nothing comes after it at the same or shallower level."""
    # Request §6.4 which is the final TOC entry
    result = compute_section_tree(toc, TOTAL_PAGES, ["6.4"])
    sec = next(s for s in result if s.section_number == "6.4")
    assert sec.page_start == 600
    assert sec.page_end == TOTAL_PAGES
