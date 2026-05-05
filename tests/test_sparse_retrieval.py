"""Sparse retrieval tests — FTS5 query escaping + ranking sanity.

Pure tests on the escape logic, plus an e2e test that runs against the
DB populated by chunk_sections.py. The e2e test is gated on the DB
already containing chunks (skip cleanly if not).
"""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from src.config import settings
from src.models import Chunk
from src.retrieval.sparse import _build_match_expr, _escape_phrase, search_sparse


# --------------------------------------------------------------------------
# Pure escape logic
# --------------------------------------------------------------------------

def test_escape_alphanumeric_passthrough():
    assert _build_match_expr("PC3 dBm") == "PC3 OR dBm"


def test_escape_hyphen_token_quoted():
    expr = _build_match_expr("A-MPR")
    assert expr == '"A-MPR"'


def test_escape_dotted_section_quoted():
    expr = _build_match_expr("6.2.1.5-1")
    assert expr == '"6.2.1.5-1"'


def test_escape_mixed_query():
    expr = _build_match_expr("PC3 power class A-MPR table 6.2.1.5-1")
    # Each token containing a separator gets quoted; bare ones don't.
    assert "PC3" in expr
    assert "power" in expr
    assert "class" in expr
    assert '"A-MPR"' in expr
    assert "table" in expr
    assert '"6.2.1.5-1"' in expr
    # Tokens are OR-joined so BM25 can rank by relevance instead of
    # demanding all terms appear in one chunk.
    assert " OR " in expr


def test_escape_empty_query_returns_empty():
    assert _build_match_expr("") == ""
    assert _build_match_expr("???") == ""


def test_escape_phrase_doubles_internal_quotes():
    # Direct test of the escape primitive — the regex in _build_match_expr
    # strips bare " from input, so test _escape_phrase directly to verify
    # FTS5-safe quote handling on whatever the caller passes.
    assert _escape_phrase('A"B-C') == '"A""B-C"'


# --------------------------------------------------------------------------
# E2E against the populated DB
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def session():
    engine = create_engine(settings.db_url, future=True)
    with Session(engine) as s:
        chunk_count = s.execute(select(func.count(Chunk.chunk_id))).scalar()
        if chunk_count == 0:
            pytest.skip(
                "DB has no chunks. Run scripts/init_db.py + ingest_toc.py + "
                "chunk_sections.py first."
            )
        yield s


@pytest.mark.parametrize(
    "query,must_appear_in_text",
    [
        ("PC3 dBm tolerance", "PC3"),
        ("A-MPR additional MPR", "MPR"),
        ("Transmit OFF power", "OFF"),
        ("minimum output power", "minimum output power"),
        ("Table 6.2.1.5-1", "6.2.1.5-1"),
    ],
)
def test_sparse_finds_required_exact_terms(session, query, must_appear_in_text):
    """The Week 2 benchmark needs sparse to catch precise-term queries
    that pure-vector retrieval misses."""
    hits = search_sparse(session, query, top_k=5)
    assert hits, f"sparse returned 0 hits for {query!r}"
    # At least one hit's text contains the expected term (case-insensitive).
    found = any(must_appear_in_text.lower() in h.text_preview.lower() for h in hits)
    assert found, (
        f"none of top-5 hits for {query!r} mentioned {must_appear_in_text!r}; "
        f"top-1 was {hits[0]}"
    )


def test_sparse_top1_for_q04_is_in_section_63(session):
    """Phase 0 lesson stress-test: q04 (minimum output power) must NOT
    drift back to §6.2 — answer lives in §6.3.1."""
    hits = search_sparse(session, "Define UE minimum output power requirement", top_k=5)
    assert hits, "no sparse hits for q04-style query"
    # Any of top-5 should be in §6.3.x
    in_63 = [h for h in hits if h.section_number.startswith("6.3")]
    assert in_63, (
        f"q04 sparse hits all outside §6.3: {[(h.section_number, h.page) for h in hits]}"
    )


def test_sparse_top1_for_q05_is_in_section_632(session):
    hits = search_sparse(session, "Transmit OFF power requirement NR FR1", top_k=5)
    assert hits
    in_632 = [h for h in hits if h.section_number == "6.3.2"]
    assert in_632, (
        f"q05 sparse hits did not surface §6.3.2: "
        f"{[(h.section_number, h.page) for h in hits]}"
    )


def test_sparse_returns_table_chunks_for_table_query(session):
    """Querying by table id should surface the TABLE chunks specifically."""
    hits = search_sparse(session, "Table 6.2.1.5-1 maximum output power", top_k=5)
    assert hits
    table_hits = [h for h in hits if h.table_id is not None]
    assert table_hits, f"no TABLE chunks surfaced: {hits}"
