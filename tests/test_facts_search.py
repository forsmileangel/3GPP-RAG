"""Tests for src/facts/search.py — FTS-backed fact retrieval (real SQLite)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.facts.emit import emit_facts
from src.facts.search import FactHit, search_facts
from src.models import Base, Chunk, ChunkType, FactType, Section, Spec
from src.retrieval.gate import GateDecision, gate_for_hits

REPO_ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location(
    "init_db_module", REPO_ROOT / "scripts" / "init_db.py",
)
init_db = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(init_db)

_GRID = (
    "Minimum output power | (dBm) | -40 | -39\n"
    "Maximum output power | (dBm) | 23 | 24\n"
)


def _populated(tmp_path) -> Session:
    engine = create_engine(
        f"sqlite:///{(tmp_path / 's.sqlite').as_posix()}", future=True,
    )
    Base.metadata.create_all(engine)
    with engine.begin() as conn:
        for ddl in (*init_db.FTS_DDL, *init_db.FACTS_FTS_DDL):
            conn.exec_driver_sql(ddl)
    session = Session(engine)
    spec = Spec(
        name="38.521-1", version="i00", source_file="x.md",
        source_format="tspec_md",
    )
    session.add(spec)
    session.flush()
    sec = Section(
        spec_id=spec.spec_id, section_number="6.3.1.3", title="t",
        level=4, page_start=1,
    )
    session.add(sec)
    session.flush()
    session.add(Chunk(
        section_id=sec.section_id, text=_GRID, page=0, char_offset=0,
        source_format="tspec_md", chunk_type=ChunkType.TABLE,
        table_id="6.3.1.3-1",
    ))
    session.flush()
    emit_facts(session, spec.spec_id)
    session.commit()
    return session


def test_search_returns_relevant_fact(tmp_path):
    session = _populated(tmp_path)
    hits = search_facts(session, "minimum output power", top_k=5)
    assert hits and isinstance(hits[0], FactHit)
    assert any(h.fact_data.get("row_label") == "Minimum output power" for h in hits)
    assert all(h.section_number == "6.3.1.3" for h in hits)


def test_search_empty_query_returns_empty(tmp_path):
    session = _populated(tmp_path)
    assert search_facts(session, "???") == []


def test_search_source_format_filter(tmp_path):
    session = _populated(tmp_path)
    assert search_facts(session, "minimum output power", source_format="tspec_md")
    assert search_facts(
        session, "minimum output power", source_format="pdf_pymupdf"
    ) == []


def test_search_fact_type_filter(tmp_path):
    session = _populated(tmp_path)
    assert search_facts(
        session, "minimum output power", fact_types=[FactType.NUMERIC]
    )
    assert search_facts(
        session, "minimum output power", fact_types=[FactType.PROCEDURE]
    ) == []


def test_facthit_feeds_gate_unchanged(tmp_path):
    session = _populated(tmp_path)
    hits = search_facts(session, "minimum output power", top_k=5)
    decision = gate_for_hits(session, "minimum output power", hits, backend="facts")
    assert isinstance(decision, GateDecision)
    assert decision.signals["result_count"] == len(hits)
    assert decision.signals["backend"] == "facts"
