"""Tests for MarkdownAdapter.emit (M4) — real throwaway SQLite with the
production FTS5 triggers applied, fake-free except Chroma deletion."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

import src.ingestion.md_parser as md_parser_module
from src.ingestion._base import InputUnit
from src.ingestion.md_parser import MarkdownAdapter
from src.models import Base, Chunk, ChunkType, Section, Spec
from src.source_formats import SOURCE_FORMAT_TSPEC_MD

REPO_ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location(
    "init_db_module", REPO_ROOT / "scripts" / "init_db.py",
)
init_db = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(init_db)


_SPEC_MD = """6 Transmitter characteristics
=============================

6.3.4 Power control
-------------------

### 6.3.4.1 General

The requirements on power control accuracy apply under normal conditions.

### 6.3.4.2 Absolute power tolerance

Tolerance prose for the absolute case.

Table 6.3.4.2-1: Tolerances

  Condition   Tolerance
  ----------- -----------
  Normal      +/- 9.0 dB

### 6.3.4.3 Relative power tolerance

Relative tolerance prose.
"""


def _session(tmp_path) -> Session:
    engine = create_engine(
        f"sqlite:///{(tmp_path / 'emit.sqlite').as_posix()}", future=True,
    )
    Base.metadata.create_all(engine)
    with engine.begin() as conn:
        for ddl in init_db.FTS_DDL:
            conn.exec_driver_sql(ddl)
    return Session(engine)


def _unit(tmp_path) -> InputUnit:
    path = tmp_path / "38521-1-i00_s06-s0602C.md"
    path.write_text(_SPEC_MD, encoding="utf-8")
    return InputUnit(
        spec_id="38.521", part="1", version="i00", release="R18",
        source_format=SOURCE_FORMAT_TSPEC_MD, source_paths=(path,),
    )


def _emit(tmp_path, session, **kwargs):
    adapter = MarkdownAdapter()
    parsed = adapter.parse(_unit(tmp_path))
    return adapter.emit(parsed, session, **kwargs)


def test_emit_writes_spec_sections_chunks_with_source_format(tmp_path):
    session = _session(tmp_path)
    stats = _emit(tmp_path, session)
    session.commit()

    spec = session.execute(select(Spec)).scalar_one()
    assert spec.name == "38.521-1"
    assert spec.version == "i00"
    assert spec.source_format == SOURCE_FORMAT_TSPEC_MD

    sections = session.execute(select(Section)).scalars().all()
    numbers = {s.section_number for s in sections}
    assert numbers == {"6", "6.3.4", "6.3.4.1", "6.3.4.2", "6.3.4.3"}
    assert stats.n_sections == 5

    chunks = session.execute(select(Chunk)).scalars().all()
    assert chunks, "expected chunks"
    assert all(c.source_format == SOURCE_FORMAT_TSPEC_MD for c in chunks)
    assert all(c.page == 0 for c in chunks)
    assert stats.n_chunks == len(chunks)
    assert stats.n_tables == sum(
        1 for c in chunks if c.chunk_type is ChunkType.TABLE
    )


def test_emit_fts_rows_match_chunks(tmp_path):
    session = _session(tmp_path)
    _emit(tmp_path, session)
    session.commit()
    n_chunks = session.execute(
        text("SELECT count(*) FROM chunks")
    ).scalar_one()
    n_fts = session.execute(
        text("SELECT count(*) FROM chunks_fts")
    ).scalar_one()
    assert n_chunks == n_fts > 0
    # Trigger looked up section_number at insert: FTS row carries it.
    row = session.execute(text(
        "SELECT section_number FROM chunks_fts "
        "WHERE text MATCH '\"9.0\"' LIMIT 1"
    )).first()
    assert row is not None and row[0] == "6.3.4.2"


def test_emit_parent_wiring_and_indexed_semantics(tmp_path):
    session = _session(tmp_path)
    _emit(tmp_path, session)
    by_number = {
        s.section_number: s
        for s in session.execute(select(Section)).scalars()
    }
    child = by_number["6.3.4.2"]
    assert child.parent_id == by_number["6.3.4"].section_id
    # P1-B: 6.3.4's synthetic parent "6.3" has no heading in this fixture;
    # it must wire to the nearest PRESENT ancestor ("6"), not orphan (None).
    assert by_number["6.3.4"].parent_id == by_number["6"].section_id
    # md bodies are disjoint: thin parents carry no chunks.
    assert by_number["6"].is_indexed is False
    assert by_number["6.3.4.2"].is_indexed is True
    # line-number bounds keep document order for the subtree roll-up.
    assert by_number["6"].page_start < by_number["6.3.4.1"].page_start


def test_emit_is_idempotent_when_unembedded(tmp_path):
    session = _session(tmp_path)
    first = _emit(tmp_path, session)
    second = _emit(tmp_path, session)
    session.commit()
    assert second.n_sections == first.n_sections
    assert second.n_chunks == first.n_chunks
    assert session.execute(
        text("SELECT count(*) FROM chunks")
    ).scalar_one() == first.n_chunks
    assert session.execute(
        text("SELECT count(*) FROM chunks_fts")
    ).scalar_one() == first.n_chunks
    assert len(session.execute(select(Spec)).scalars().all()) == 1


def test_emit_refuses_embedded_spec_without_force(tmp_path):
    session = _session(tmp_path)
    _emit(tmp_path, session)
    chunk = session.execute(select(Chunk)).scalars().first()
    chunk.vector_id = "v-1"
    session.flush()
    with pytest.raises(RuntimeError, match="force=True"):
        _emit(tmp_path, session)


def test_emit_force_deletes_chroma_vectors(tmp_path, monkeypatch):
    session = _session(tmp_path)
    _emit(tmp_path, session)
    chunk = session.execute(select(Chunk)).scalars().first()
    chunk.vector_id = "v-1"
    session.flush()

    deleted: list[list[str]] = []
    monkeypatch.setattr(
        md_parser_module, "_delete_chroma_vectors",
        lambda ids: deleted.append(list(ids)),
    )
    stats = _emit(tmp_path, session, force=True)
    assert deleted == [["v-1"]]
    assert stats.n_chunks > 0
    assert all(
        c.vector_id is None
        for c in session.execute(select(Chunk)).scalars()
    )


def test_emit_sections_filter_keeps_subtree_only(tmp_path):
    session = _session(tmp_path)
    stats = _emit(tmp_path, session, sections_filter=["6.3.4.2"])
    numbers = {
        s.section_number
        for s in session.execute(select(Section)).scalars()
    }
    assert numbers == {"6.3.4.2"}
    assert stats.n_sections == 1
    assert stats.n_tables == 1


def test_emit_empty_filter_match_raises(tmp_path):
    session = _session(tmp_path)
    with pytest.raises(ValueError, match="matched nothing"):
        _emit(tmp_path, session, sections_filter=["9.9"])
