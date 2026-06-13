"""Persist rule-based facts into the facts table (Step 6, IO layer).

Idempotent: delete-and-reinsert, scoped to (spec, [sections]). spec_id is
source-specific in this schema (the pdf and md corpora are separate spec
rows), so deleting by spec_id is already per-source — a pdf re-run never
wipes md facts. Writes fact_text so the facts_fts triggers index it. Does
NOT commit — the caller owns the transaction (same contract as
MarkdownAdapter.emit).
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from src.models import Chunk, ChunkType, Fact, Section

from .extractor import ChunkView, extract_facts_from_chunk, fact_to_text


@dataclass(frozen=True)
class FactEmitStats:
    n_chunks_scanned: int
    n_facts: int
    n_chunks_degraded: int    # TABLE chunks that yielded 0 facts


def _in_scope(section_number: str, prefixes: list[str]) -> bool:
    """Dotted-prefix match: '6.2' selects 6.2 and 6.2.x.y (mirrors
    md_parser._filter_selected so fact scope and ingest scope agree)."""
    return any(
        section_number == p or section_number.startswith(p + ".")
        for p in prefixes
    )


def load_table_chunks(
    session: Session, spec_id: int, *, sections_filter: list[str] | None = None,
) -> list[ChunkView]:
    """All TABLE chunks of a spec (optionally scoped to section prefixes),
    as DB-free ChunkViews for the pure extractor."""
    rows = session.execute(
        select(
            Chunk.chunk_id, Chunk.section_id, Chunk.text, Chunk.table_id,
            Chunk.page, Chunk.source_format, Section.section_number,
        )
        .join(Section, Section.section_id == Chunk.section_id)
        .where(Section.spec_id == spec_id, Chunk.chunk_type == ChunkType.TABLE)
    ).all()
    views: list[ChunkView] = []
    for r in rows:
        if sections_filter and not _in_scope(r.section_number, sections_filter):
            continue
        views.append(ChunkView(
            chunk_id=r.chunk_id, section_id=r.section_id, text=r.text,
            table_id=r.table_id, page=r.page or 0, source_format=r.source_format,
        ))
    return views


def emit_facts(
    session: Session, spec_id: int, *, sections_filter: list[str] | None = None,
) -> FactEmitStats:
    """Idempotently (re)extract facts for a spec's TABLE chunks. Deletes the
    spec's existing facts in scope first, then inserts fresh. Does NOT commit."""
    if sections_filter:
        scoped = [
            sid for sid, num in session.execute(
                select(Section.section_id, Section.section_number)
                .where(Section.spec_id == spec_id)
            ).all()
            if _in_scope(num, sections_filter)
        ]
        session.execute(
            delete(Fact).where(
                Fact.spec_id == spec_id, Fact.section_id.in_(scoped)
            )
        )
    else:
        session.execute(delete(Fact).where(Fact.spec_id == spec_id))

    views = load_table_chunks(session, spec_id, sections_filter=sections_filter)
    n_facts = 0
    n_degraded = 0
    for view in views:
        records = extract_facts_from_chunk(view)
        if not records:
            n_degraded += 1
            continue
        for rec in records:
            session.add(Fact(
                spec_id=spec_id,
                section_id=rec.section_id,
                source_chunk_id=rec.source_chunk_id,
                fact_type=rec.fact_type,
                fact_data=rec.fact_data,
                fact_text=fact_to_text(rec.fact_data),
                page=rec.page,
                table_id=rec.table_id,
                extracted_by=rec.extracted_by,
                confidence=rec.confidence,
            ))
            n_facts += 1
    session.flush()
    return FactEmitStats(
        n_chunks_scanned=len(views), n_facts=n_facts, n_chunks_degraded=n_degraded,
    )
