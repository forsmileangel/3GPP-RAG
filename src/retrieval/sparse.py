"""Sparse retrieval over chunks_fts (SQLite FTS5).

Phase A Week 2 step 2 of the v2.1 hybrid plan: BM25-style keyword search
that complements BGE-M3 dense retrieval. SQLite FTS5 is the chosen sparse
backend because it ships with SQLite (no extra dependency), supports BM25
ranking out of the box, and can be JOINed back to chunks/sections cheaply.

Query escaping rules baked into _build_match_expr:
  - bare alphanumeric tokens are passed through (FTS5 will AND them)
  - any token containing characters the unicode61 tokenizer treats as
    separators (`-`, `.`, `/`, etc.) is wrapped in "double quotes" so
    FTS5 reads it as a phrase (otherwise "A-MPR" => "A column-MPR-search")
  - column-syntax in user input is rejected to keep the query language
    safe — callers can pass a list of pre-built phrases via `phrases=`
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.source_formats import validate_source_format


@dataclass(frozen=True)
class SparseHit:
    """One row from FTS5 sparse search."""
    chunk_id: int
    section_number: str
    table_id: str | None
    page: int
    bm25_score: float  # smaller = more relevant (FTS5 bm25 returns negative)
    text_preview: str


# Tokens that need to stay together as one FTS5 phrase. unicode61 + the
# default `remove_diacritics 2` treats anything not in the letter+digit
# class as a token boundary. Empirically PC3 dBm § A-MPR / 6.2.1.5-1 etc.
_TOKEN_RE = re.compile(r"[A-Za-z0-9§\-./]+")


def _looks_like_phrase(token: str) -> bool:
    """Return True if the token must be quoted to survive FTS5 parsing
    (contains a separator that unicode61 would split on)."""
    return any(ch in token for ch in "-./§")


def _escape_phrase(token: str) -> str:
    """FTS5 phrase quoting: replace internal " with "" and wrap in "...".
    Internal separators that unicode61 ignores are already fine to leave
    inside the quoted phrase."""
    return '"' + token.replace('"', '""') + '"'


def _build_match_expr(query: str) -> str:
    """Convert a free-text query into an FTS5 MATCH expression.

    Strategy: extract token-like substrings; quote those that contain
    separators; **OR** them so BM25 ranking can rank by which chunks
    contain the rarest / most informative terms. AND-of-everything is
    too strict for natural-language queries that include filler words
    like "Define", "UE", "requirement" — chunks rarely contain all
    such words simultaneously even when they're the right answer.
    """
    tokens = _TOKEN_RE.findall(query)
    if not tokens:
        return ""
    parts: list[str] = []
    for tok in tokens:
        if _looks_like_phrase(tok):
            parts.append(_escape_phrase(tok))
        else:
            parts.append(tok)
    return " OR ".join(parts)


def search_sparse(
    session: Session,
    query: str,
    *,
    top_k: int = 5,
    spec_id: int | None = None,
    source_format: str | None = None,
) -> list[SparseHit]:
    """Run FTS5 BM25 search; return top_k hits ordered by relevance.

    Optional filters let mixed corpora (PDF vs TSpec markdown, multi-spec DBs)
    avoid cross-source contamination.
    """
    match_expr = _build_match_expr(query)
    if not match_expr:
        return []
    if source_format is not None:
        source_format = validate_source_format(source_format)

    where_parts = ["chunks_fts MATCH :q"]
    params: dict[str, object] = {"q": match_expr, "k": top_k}
    if spec_id is not None:
        where_parts.append("sec.spec_id = :spec_id")
        params["spec_id"] = spec_id
    if source_format is not None:
        where_parts.append("c.source_format = :source_format")
        params["source_format"] = source_format

    sql = """
        SELECT
            c.chunk_id,
            sec.section_number,
            c.table_id,
            c.page,
            bm25(chunks_fts) AS score,
            c.text
        FROM chunks_fts
        JOIN chunks c ON c.chunk_id = chunks_fts.rowid
        JOIN sections sec ON sec.section_id = c.section_id
        WHERE {where_clause}
        ORDER BY score
        LIMIT :k
    """.format(where_clause=" AND ".join(where_parts))
    rows = session.execute(text(sql), params).fetchall()
    hits: list[SparseHit] = []
    for r in rows:
        cid, sec_num, table_id, page, score, body = r
        hits.append(SparseHit(
            chunk_id=int(cid),
            section_number=sec_num,
            table_id=table_id,
            page=int(page),
            bm25_score=float(score),
            text_preview=body[:240].replace("\n", " "),
        ))
    return hits
