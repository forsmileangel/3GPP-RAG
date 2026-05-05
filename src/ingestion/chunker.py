"""Section-aware deterministic chunker for 3GPP PDFs.

Week 2 (v2.1 precision upgrade) goal: take the section tree written by
ingest_toc.py and produce chunks that retain the metadata needed for
hybrid retrieval, fact-layer extraction, and PDF jump-to-page later.

Per-chunk metadata preserved:
  - section_id          (FK to sections row)
  - parent_section_id   (denormalized — chunks belonging to §6.2.1 carry
                         §6.2's section_id so filtering by parent is fast)
  - page                (1-indexed PDF page where chunk starts)
  - char_offset         (offset within the section's concatenated text)
  - chunk_type          (prose | table | table_row | heading | list)
  - table_id / row_index (only when chunk_type indicates a table)

What this chunker DOES NOT do (deferred to Week 2 stretch / Week 3):
  - Embedding (separate Embedder writes vector_id + embedding_model)
  - Smart table parsing (this version detects table headings via regex
    and emits one TABLE chunk per detected table block; table-row
    splitting becomes meaningful only once unstructured.io is wired in)
  - Fact extraction

Determinism: same input PDF + same section list = same chunks (no LLM
calls, no randomness). Required so retrieval benchmarks are reproducible.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import fitz
from sqlalchemy.orm import Session

from src.ingestion.toc_extractor import extract_pages_text
from src.models import Chunk, ChunkType, Section


# Heuristic: a "Table X.Y.Z-N" caption marks the start of a table block.
# 3GPP's convention is rigid enough that this hits with very low false
# positives. The block ends at the next section heading OR the next
# Table caption OR a blank-line gap (>=2 blank lines).
_TABLE_CAPTION_RE = re.compile(
    r"^\s*Table\s+([0-9]+(?:\.[0-9A-Z]+)*-[0-9]+)\b",
    re.MULTILINE,
)
# Section heading at start-of-line: "6.2", "6.2.1", "6.2A", "Annex B" etc.
# Conservative — must be followed by whitespace + capitalized word.
_SECTION_HEADING_RE = re.compile(
    r"^\s*([0-9]+(?:\.[0-9A-Z]+)+)\s+[A-Z]",
    re.MULTILINE,
)


@dataclass
class ChunkSpec:
    """In-memory chunk before persisting."""
    section_id: int
    parent_section_id: int | None
    text: str
    page: int
    char_offset: int
    chunk_type: ChunkType
    table_id: str | None = None
    row_index: int | None = None


def _offset_to_page(offset: int, page_offsets: list[int], page_start_1idx: int) -> int:
    """Map a char offset within the section's concatenated text back to
    the 1-indexed PDF page where that offset lives."""
    last = 0
    for i, off in enumerate(page_offsets):
        if off > offset:
            break
        last = i
    return page_start_1idx + last


def _split_into_blocks(
    text: str,
    page_offsets: list[int],
    page_start_1idx: int,
) -> list[tuple[str, int, int, ChunkType, str | None]]:
    """First pass: scan text, split at table-caption boundaries.

    Returns list of (block_text, char_offset, page, chunk_type, table_id).
    Tables get chunk_type=TABLE; everything else PROSE.
    """
    table_matches = list(_TABLE_CAPTION_RE.finditer(text))
    if not table_matches:
        # No tables detected; whole thing is prose.
        if text.strip():
            return [(
                text.strip(),
                0,
                _offset_to_page(0, page_offsets, page_start_1idx),
                ChunkType.PROSE,
                None,
            )]
        return []

    blocks: list[tuple[str, int, int, ChunkType, str | None]] = []
    cursor = 0
    for i, m in enumerate(table_matches):
        # Prose before this table caption (if any)
        if m.start() > cursor:
            prose = text[cursor:m.start()]
            if prose.strip():
                blocks.append((
                    prose.strip(),
                    cursor,
                    _offset_to_page(cursor, page_offsets, page_start_1idx),
                    ChunkType.PROSE,
                    None,
                ))

        # Table block runs from this caption to start of next caption OR
        # to next section heading OR to end of section text.
        next_table_start = (
            table_matches[i + 1].start()
            if i + 1 < len(table_matches)
            else len(text)
        )
        # Look for a section heading inside the table-candidate window
        heading_in_window = _SECTION_HEADING_RE.search(text, m.start(), next_table_start)
        end = (
            heading_in_window.start()
            if heading_in_window
            else next_table_start
        )

        block_text = text[m.start():end].strip()
        if block_text:
            blocks.append((
                block_text,
                m.start(),
                _offset_to_page(m.start(), page_offsets, page_start_1idx),
                ChunkType.TABLE,
                m.group(1),  # the captured table_id, e.g. "6.2.1.5-1"
            ))
        cursor = end

    # Trailing prose after last table block
    if cursor < len(text):
        tail = text[cursor:]
        if tail.strip():
            blocks.append((
                tail.strip(),
                cursor,
                _offset_to_page(cursor, page_offsets, page_start_1idx),
                ChunkType.PROSE,
                None,
            ))

    return blocks


# Prose chunk size. Mid-range value: small enough that a chunk usually
# centers on one idea, large enough that BGE-M3 has context. Tables are
# never split on this boundary — they go in whole.
PROSE_CHUNK_CHARS = 1200
PROSE_CHUNK_OVERLAP = 200


def _chunk_prose(
    text: str,
    base_offset: int,
    page_offsets: list[int],
    page_start_1idx: int,
) -> list[tuple[str, int, int]]:
    """Split a long prose block into overlapping windows. Each window
    keeps its char_offset (relative to the section's text) and page
    number. Returns (text, abs_char_offset, page) per window."""
    out: list[tuple[str, int, int]] = []
    n = len(text)
    if n <= PROSE_CHUNK_CHARS:
        out.append((
            text,
            base_offset,
            _offset_to_page(base_offset, page_offsets, page_start_1idx),
        ))
        return out

    i = 0
    while i < n:
        end = min(i + PROSE_CHUNK_CHARS, n)
        body = text[i:end].strip()
        if body:
            abs_off = base_offset + i
            out.append((
                body,
                abs_off,
                _offset_to_page(abs_off, page_offsets, page_start_1idx),
            ))
        if end >= n:
            break
        i = end - PROSE_CHUNK_OVERLAP
    return out


def chunk_section(
    doc: fitz.Document,
    section: Section,
) -> list[ChunkSpec]:
    """Produce ChunkSpec list for one section. Whole-table blocks become
    one TABLE chunk each; prose blocks are split into overlapping windows."""
    if section.page_start is None or section.page_end is None:
        return []

    text, page_offsets = extract_pages_text(
        doc, section.page_start - 1, section.page_end - 1
    )
    if not text.strip():
        return []

    blocks = _split_into_blocks(text, page_offsets, section.page_start)

    specs: list[ChunkSpec] = []
    for block_text, char_offset, page, chunk_type, table_id in blocks:
        if chunk_type == ChunkType.TABLE:
            specs.append(ChunkSpec(
                section_id=section.section_id,
                parent_section_id=section.parent_id,
                text=block_text,
                page=page,
                char_offset=char_offset,
                chunk_type=ChunkType.TABLE,
                table_id=table_id,
                row_index=None,  # whole-table chunk; row split is Week 3+ work
            ))
        else:
            for body, abs_off, p in _chunk_prose(
                block_text, char_offset, page_offsets, section.page_start,
            ):
                specs.append(ChunkSpec(
                    section_id=section.section_id,
                    parent_section_id=section.parent_id,
                    text=body,
                    page=p,
                    char_offset=abs_off,
                    chunk_type=ChunkType.PROSE,
                ))
    return specs


def persist_chunks(session: Session, specs: list[ChunkSpec]) -> int:
    """Insert ChunkSpec rows; FTS5 triggers keep chunks_fts in sync."""
    rows = [
        Chunk(
            section_id=s.section_id,
            parent_section_id=s.parent_section_id,
            text=s.text,
            page=s.page,
            char_offset=s.char_offset,
            chunk_type=s.chunk_type,
            table_id=s.table_id,
            row_index=s.row_index,
        )
        for s in specs
    ]
    session.add_all(rows)
    session.flush()
    return len(rows)


def chunk_spec_pdf(
    session: Session,
    pdf_path: Path,
    sections: list[Section],
    *,
    skip_already_indexed: bool = True,
) -> dict[int, int]:
    """Chunk every section in `sections` and persist. Returns
    {section_id: chunk_count}. Marks each section's is_indexed=True
    after successful chunk write."""
    counts: dict[int, int] = {}
    with fitz.open(pdf_path) as doc:
        for sec in sections:
            if skip_already_indexed and sec.is_indexed:
                counts[sec.section_id] = 0
                continue
            specs = chunk_section(doc, sec)
            n = persist_chunks(session, specs)
            sec.is_indexed = True
            counts[sec.section_id] = n
    return counts
