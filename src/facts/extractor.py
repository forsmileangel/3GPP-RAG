"""Pure rule-based fact extraction from a TABLE chunk (Step 6).

Row-centric by design (chosen after inspecting the real §6.2/6.3 md tables,
which are ragged + pivoted): the row label is column 0, and every data cell
that contains a digit becomes a table-cell fact. Column labels are best-effort
from the header. value_num distinguishes a matchable number from a
formula/range cell (which is stored verbatim but not value-matchable).

md (tspec_md) → grid extraction. pdf_pymupdf → [] : PyMuPDF linearizes tables
to one-token-per-line with no recoverable column structure (0/302 chunks carry
a delimiter — verified), and the linearization scrambles value↔row pairing, so
rule-based extraction would emit wrong facts. Returning nothing is the honest
position; that gap is itself a measurement input for the LLM decision.
No DB, no I/O.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.models import Confidence, FactType
from src.source_formats import SOURCE_FORMAT_TSPEC_MD

from ._grid import (
    col_label,
    detect_header_rows,
    is_well_formed,
    split_rendered_grid,
)
from ._tokens import extract_value_unit, find_unit


@dataclass(frozen=True)
class ChunkView:
    """The subset of a Chunk the pure extractor needs (keeps it DB-free)."""
    chunk_id: int
    section_id: int
    text: str
    table_id: str | None
    page: int
    source_format: str


@dataclass(frozen=True)
class FactRecord:
    """An in-memory fact before persisting (mirrors ChunkSpec's role)."""
    section_id: int
    source_chunk_id: int
    fact_type: FactType
    fact_data: dict
    page: int | None
    table_id: str | None
    extracted_by: str
    confidence: Confidence


def _has_digit(s: str) -> bool:
    return any(ch.isdigit() for ch in s)


def extract_facts_from_chunk(chunk: ChunkView) -> list[FactRecord]:
    """Dispatch on source_format. md → grid; pdf → [] (see module docstring)."""
    if chunk.source_format == SOURCE_FORMAT_TSPEC_MD:
        return _extract_grid(chunk)
    return []


def _extract_grid(chunk: ChunkView) -> list[FactRecord]:
    rows = split_rendered_grid(chunk.text)
    if not is_well_formed(rows):
        return []
    header_rows = detect_header_rows(rows)

    facts: list[FactRecord] = []
    for r in range(header_rows, len(rows)):
        row = rows[r]
        if not row:
            continue
        row_label = row[0].strip()
        if not row_label:
            continue
        for c in range(1, len(row)):
            cell = row[c].strip()
            if not cell or not _has_digit(cell):
                continue  # skip empty + purely-textual (label-like) cells
            clabel = col_label(rows, header_rows, c)
            tok = extract_value_unit(cell, header_unit=find_unit(clabel))
            fact_data: dict = {
                "table_id": chunk.table_id,
                "row_label": row_label,
                "col_label": clabel,
                "value": tok.raw,
            }
            if tok.value_num is not None:
                fact_data["value_num"] = tok.value_num
            if tok.unit:
                fact_data["unit"] = tok.unit
            facts.append(FactRecord(
                section_id=chunk.section_id,
                source_chunk_id=chunk.chunk_id,
                fact_type=FactType.NUMERIC,
                fact_data=fact_data,
                page=chunk.page or None,
                table_id=chunk.table_id,
                extracted_by="rule/table_v1",
                confidence=Confidence.CONFIRMED,
            ))
    return facts


def fact_to_text(fact_data: dict) -> str:
    """Flatten fact_data into one searchable string for facts_fts (M5). Keys
    in a stable order; missing keys skipped."""
    parts = [
        str(fact_data.get(k, ""))
        for k in ("row_label", "col_label", "value", "unit", "table_id")
    ]
    return " ".join(p for p in parts if p)
