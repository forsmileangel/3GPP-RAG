"""Fact retrieval over facts_fts (Step 6).

Mirrors src/retrieval/sparse.py: FTS5 BM25 over the flattened fact_text,
JOINed back to facts/sections for citation metadata. Reuses sparse's
_build_match_expr so the fact index and the chunk index agree on token
boundaries. A FactHit satisfies the evidence gate's _Hit protocol (chunk_id +
section_number + a score attribute), so it feeds gate_for_hits unchanged.

Sign convention: bm25_score is SMALLER = more relevant (FTS5), same as
SparseHit — normalize_top_score in the gate already handles it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.models import FactType
from src.retrieval.sparse import _build_match_expr
from src.source_formats import validate_source_format


@dataclass(frozen=True)
class FactHit:
    fact_id: int
    chunk_id: int | None        # source_chunk_id, for citation back to a chunk
    section_number: str
    table_id: str | None
    page: int | None
    bm25_score: float           # smaller = more relevant
    fact_data: dict
    fact_text: str


def search_facts(
    session: Session,
    query: str,
    *,
    top_k: int = 5,
    spec_id: int | None = None,
    source_format: str | None = None,
    fact_types: list[FactType] | None = None,
) -> list[FactHit]:
    """FTS5 BM25 search over facts_fts; return top_k facts best-first.

    Filters: spec_id (sections.spec_id), source_format (via the source chunk),
    fact_types (e.g. only NUMERIC). Empty / tokenless query -> []."""
    match_expr = _build_match_expr(query)
    if not match_expr:
        return []
    if source_format is not None:
        source_format = validate_source_format(source_format)

    joins = [
        "JOIN facts f ON f.fact_id = facts_fts.rowid",
        "JOIN sections sec ON sec.section_id = f.section_id",
    ]
    where = ["facts_fts MATCH :q"]
    params: dict[str, object] = {"q": match_expr, "k": top_k}
    if spec_id is not None:
        where.append("sec.spec_id = :spec_id")
        params["spec_id"] = spec_id
    if source_format is not None:
        joins.append("LEFT JOIN chunks c ON c.chunk_id = f.source_chunk_id")
        where.append("c.source_format = :sf")
        params["sf"] = source_format
    if fact_types:
        names = [ft.name for ft in fact_types]
        placeholders = ",".join(f":ft{i}" for i in range(len(names)))
        where.append(f"f.fact_type IN ({placeholders})")
        for i, name in enumerate(names):
            params[f"ft{i}"] = name

    sql = """
        SELECT
            f.fact_id,
            f.source_chunk_id,
            sec.section_number,
            f.table_id,
            f.page,
            bm25(facts_fts) AS score,
            f.fact_data,
            f.fact_text
        FROM facts_fts
        {joins}
        WHERE {where}
        ORDER BY score
        LIMIT :k
    """.format(joins="\n        ".join(joins), where=" AND ".join(where))

    rows = session.execute(text(sql), params).fetchall()
    hits: list[FactHit] = []
    for fid, cid, sec_num, table_id, page, score, fdata, ftext in rows:
        hits.append(FactHit(
            fact_id=int(fid),
            chunk_id=int(cid) if cid is not None else None,
            section_number=sec_num,
            table_id=table_id,
            page=int(page) if page is not None else None,
            bm25_score=float(score),
            fact_data=json.loads(fdata) if isinstance(fdata, str) else fdata,
            fact_text=ftext or "",
        ))
    return hits
