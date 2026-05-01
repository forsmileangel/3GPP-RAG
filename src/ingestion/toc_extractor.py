"""TOC-driven section locator for 3GPP PDFs.

Phase 0 (spike) used a single hard-coded TARGET_SECTION. Phase A needs:
  - **Multi-section** ingestion (e.g. ["6.2", "6.3"] in one call) so the
    common §6.2 / §6.3 split (q01..q03 vs q04..q05 in the test bank) is
    handled by a single pipeline run.
  - **Sibling vs child distinction**: 3GPP releases bake CA / DC / SUL
    variants in as siblings — §6.2A, §6.2B, §6.2C live next to §6.2 at the
    same TOC depth, NOT under it. Selecting "6.2" must NOT silently include
    "6.2A" (Phase 0 lesson — see reality_check.md, "Mistake 3").
  - Bookmark-only locating. Body-text regex on "6.2" matches the
    table-of-contents page entry, not the real heading (Phase 0 lesson —
    "Mistake 1"). PyMuPDF's get_toc() is the only reliable source.

The pure section-tree computation is split out from the fitz I/O so it
can be unit-tested with synthetic TOCs — see tests/test_toc_extractor.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import fitz  # PyMuPDF


class TOCEmptyError(RuntimeError):
    """PDF has no bookmark TOC. Refuse to fall back to body regex."""


class SectionNotFoundError(KeyError):
    """A requested section_number was not found among TOC bookmarks."""


@dataclass(frozen=True)
class TOCEntry:
    """One row from PyMuPDF's get_toc() with the section number split out."""
    level: int
    section_number: str  # "6.2" / "6.2.1" / "6.2A" / "Annex A.3" etc.
    title: str           # title with the section number stripped
    full_title: str      # raw TOC title ("6.2  Transmitter power")
    page_1idx: int


@dataclass
class SectionEntry:
    """A section selected for ingestion, with computed page range."""
    section_number: str
    title: str
    full_title: str
    level: int
    page_start: int        # 1-indexed inclusive
    page_end: int          # 1-indexed inclusive
    parent_number: str | None  # parent section_number, only if parent is also in the selection
    requested: bool        # True if user asked for this directly; False if pulled in as a child
    children: list[str] = field(default_factory=list)  # section_numbers of direct children in the selection


# --------------------------------------------------------------------------
# Pure logic — testable without a real PDF
# --------------------------------------------------------------------------

def _split_section_token(title: str) -> tuple[str, str]:
    """Return (section_number, rest_of_title).

    Splits on the first whitespace run. The leading token is treated as the
    section number even if it doesn't look numeric — 3GPP TOCs sometimes
    have entries like "Annex A (informative)" where the section_number is
    "Annex" by this rule, but those won't be requestable anyway.
    """
    parts = title.strip().split(maxsplit=1)
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[1].strip()


def parse_toc(raw_toc: list[list], total_pages: int) -> list[TOCEntry]:
    """Convert PyMuPDF's get_toc() output into TOCEntry rows.

    PyMuPDF returns [[level, title, page], ...]. Pages are 1-indexed.
    """
    entries: list[TOCEntry] = []
    for row in raw_toc:
        if len(row) < 3:
            continue
        level, full_title, page = row[0], row[1], row[2]
        sec_num, rest = _split_section_token(full_title)
        if not sec_num:
            continue
        page_clamped = max(1, min(int(page), total_pages))
        entries.append(TOCEntry(
            level=int(level),
            section_number=sec_num,
            title=rest,
            full_title=full_title.strip(),
            page_1idx=page_clamped,
        ))
    return entries


def _compute_page_end(entries: list[TOCEntry], idx: int, total_pages: int) -> int:
    """Last 1-indexed page covered by entries[idx], inclusive.

    The end is the page just before the next TOC entry whose level is <=
    entries[idx].level. If no such entry exists, the section runs to the
    final page of the document.
    """
    target_level = entries[idx].level
    target_page = entries[idx].page_1idx
    for nxt in entries[idx + 1:]:
        if nxt.level <= target_level:
            end = nxt.page_1idx - 1
            return max(end, target_page)
    return total_pages


def compute_section_tree(
    toc: list[TOCEntry],
    total_pages: int,
    requested: list[str],
) -> list[SectionEntry]:
    """Build a flat list of SectionEntry covering each requested section
    plus all of its descendants in the TOC.

    Sibling exclusion: if user asks for "6.2" and the TOC has "6.2", "6.2A",
    "6.2B" all at the same level, only "6.2" and its true children are
    returned. "6.2A" is a sibling — user must request it explicitly.
    """
    if not toc:
        raise TOCEmptyError("TOC is empty")

    # Locate each requested section in the TOC (first occurrence wins).
    requested_indices: dict[str, int] = {}
    for sec_num in requested:
        for i, entry in enumerate(toc):
            if entry.section_number == sec_num:
                requested_indices[sec_num] = i
                break
        else:
            raise SectionNotFoundError(sec_num)

    # Walk forward from each requested index, collecting until we hit an
    # entry at the same or shallower level (= boundary).
    selected: dict[int, SectionEntry] = {}  # toc_index -> entry
    requested_set = set(requested)

    for sec_num in requested:
        idx = requested_indices[sec_num]
        target_level = toc[idx].level
        # Collect [idx .. next-sibling-or-shallower)
        for j in range(idx, len(toc)):
            if j > idx and toc[j].level <= target_level:
                break
            if j in selected:
                continue
            entry = toc[j]
            page_end = _compute_page_end(toc, j, total_pages)
            selected[j] = SectionEntry(
                section_number=entry.section_number,
                title=entry.title,
                full_title=entry.full_title,
                level=entry.level,
                page_start=entry.page_1idx,
                page_end=page_end,
                parent_number=None,  # filled in below
                requested=(entry.section_number in requested_set),
            )

    # Wire up parent_number: nearest ancestor in the selection (by walking
    # backward in TOC order to a strictly shallower level).
    ordered_indices = sorted(selected.keys())
    for i in ordered_indices:
        cur = selected[i]
        for j in reversed([k for k in ordered_indices if k < i]):
            if selected[j].level < cur.level:
                cur.parent_number = selected[j].section_number
                selected[j].children.append(cur.section_number)
                break

    return [selected[i] for i in ordered_indices]


# --------------------------------------------------------------------------
# Public API — opens the PDF
# --------------------------------------------------------------------------

def extract_sections(pdf_path: Path, requested: list[str]) -> list[SectionEntry]:
    """Open a PDF, read its bookmark TOC, and return the SectionEntry list
    covering each requested section_number plus all its descendants."""
    if not requested:
        raise ValueError("requested section list must be non-empty")

    doc = fitz.open(pdf_path)
    try:
        raw_toc = doc.get_toc()
        total_pages = doc.page_count
    finally:
        doc.close()

    if not raw_toc:
        raise TOCEmptyError(
            f"PDF has no bookmark TOC: {pdf_path}. "
            "Refusing to fall back to body-text regex (Phase 0 lesson)."
        )

    toc = parse_toc(raw_toc, total_pages)
    return compute_section_tree(toc, total_pages, requested)


def extract_pages_text(
    doc: fitz.Document,
    start_page_0idx: int,
    end_page_0idx: int,
) -> tuple[str, list[int]]:
    """Concatenate text from pages [start..end] (both 0-indexed, inclusive).

    Returns (full_text, page_offsets) where page_offsets[i] is the char
    offset of the i-th included page's start within full_text. Used by the
    chunker (Week 2) to map a chunk back to its page number.
    """
    if start_page_0idx > end_page_0idx:
        raise ValueError(f"start_page > end_page ({start_page_0idx} > {end_page_0idx})")

    parts: list[str] = []
    page_offsets: list[int] = []
    cursor = 0
    for p_idx in range(start_page_0idx, end_page_0idx + 1):
        page = doc[p_idx]
        text = page.get_text("text")
        page_offsets.append(cursor)
        parts.append(text)
        cursor += len(text) + 1  # +1 accounts for the joining "\n"
    return "\n".join(parts), page_offsets
