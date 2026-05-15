"""Unit tests for the deterministic chunker.

Pure-text tests cover:
  - prose-only sections produce >=1 chunk with correct page mapping
  - table-caption text creates a TABLE chunk with table_id captured
  - long prose splits into overlapping windows (PROSE_CHUNK_CHARS)
  - char_offset is monotonic within a section
  - chunk_type / table_id metadata is preserved correctly
"""

from __future__ import annotations

from src.ingestion.chunker import (
    PROSE_CHUNK_CHARS,
    _split_into_blocks,
    _chunk_prose,
)
from src.models import ChunkType
from src.source_formats import SOURCE_FORMAT_PDF_PYMUPDF, SOURCE_FORMAT_TSPEC_MD


def _page_offsets_for(text: str, pages: list[str]) -> list[int]:
    """Build page_offsets for a synthetic multi-page text."""
    offsets = [0]
    cursor = 0
    for p in pages[:-1]:
        cursor += len(p) + 1
        offsets.append(cursor)
    return offsets


def test_prose_only_no_tables_one_block():
    text = "This is a prose paragraph. It has no table captions at all."
    blocks = _split_into_blocks(text, [0], 100)
    assert len(blocks) == 1
    body, off, page, ctype, tid = blocks[0]
    assert ctype == ChunkType.PROSE
    assert tid is None
    assert off == 0
    assert page == 100


def test_table_caption_creates_table_block():
    text = (
        "Some intro prose about output power.\n"
        "Table 6.2.1.5-1: Maximum output power for PC3 UE\n"
        "Band | Power | Tolerance\n"
        "n78  | 23    | +/- 2\n"
    )
    blocks = _split_into_blocks(text, [0], 93)
    types = [b[3] for b in blocks]
    assert ChunkType.PROSE in types
    assert ChunkType.TABLE in types
    table_block = next(b for b in blocks if b[3] == ChunkType.TABLE)
    assert table_block[4] == "6.2.1.5-1"  # table_id captured


def test_table_block_ends_before_next_section_heading():
    text = (
        "Table 6.2.1.5-1: PC3 power\n"
        "Some rows here\n"
        "6.2.1.6 Test requirement\n"
        "More prose follows.\n"
    )
    blocks = _split_into_blocks(text, [0], 93)
    table_block = next(b for b in blocks if b[3] == ChunkType.TABLE)
    # Table content should NOT include the "6.2.1.6 Test requirement" heading
    assert "6.2.1.6" not in table_block[0]
    # The trailing prose chunk should exist and contain it
    prose_after = [b for b in blocks if b[3] == ChunkType.PROSE and "6.2.1.6" in b[0]]
    assert prose_after


def test_multiple_tables_each_get_own_block():
    text = (
        "Table 6.2.1.5-1: First table\n"
        "row data\n"
        "Table 6.2.1.5-2: Second table\n"
        "more rows\n"
    )
    blocks = _split_into_blocks(text, [0], 93)
    table_blocks = [b for b in blocks if b[3] == ChunkType.TABLE]
    assert len(table_blocks) == 2
    table_ids = {b[4] for b in table_blocks}
    assert table_ids == {"6.2.1.5-1", "6.2.1.5-2"}


def test_long_prose_splits_into_overlapping_windows():
    text = "x " * (PROSE_CHUNK_CHARS * 2)  # 2x the chunk size
    windows = _chunk_prose(text, base_offset=0, page_offsets=[0], page_start_1idx=1)
    assert len(windows) >= 2
    # Verify monotonic offsets
    offs = [w[1] for w in windows]
    assert offs == sorted(offs)
    # Verify overlap: window 2 starts before window 1 ended
    assert offs[1] < len(windows[0][0])


def test_short_prose_single_window():
    text = "Short paragraph."
    windows = _chunk_prose(text, base_offset=0, page_offsets=[0], page_start_1idx=1)
    assert len(windows) == 1
    assert windows[0][0] == text


def test_chunkspec_carries_source_format():
    from src.ingestion.chunker import ChunkSpec

    spec = ChunkSpec(
        section_id=1,
        parent_section_id=None,
        text="body",
        source_format=SOURCE_FORMAT_TSPEC_MD,
        page=1,
        char_offset=0,
        chunk_type=ChunkType.PROSE,
    )
    assert spec.source_format == SOURCE_FORMAT_TSPEC_MD
    assert SOURCE_FORMAT_PDF_PYMUPDF == "pdf_pymupdf"


def test_prose_window_page_mapping_uses_offsets():
    """Page should advance as char offsets cross page boundaries."""
    page_a = "First page text " * 50  # ~800 chars
    page_b = "Second page text " * 50
    full = page_a + "\n" + page_b
    page_offsets = [0, len(page_a) + 1]

    windows = _chunk_prose(full, base_offset=0, page_offsets=page_offsets, page_start_1idx=10)
    pages = [w[2] for w in windows]
    # First window starts at offset 0 -> page 10
    assert pages[0] == 10
    # Some later window should be on page 11
    assert any(p == 11 for p in pages)
