"""Tests for src/facts/emit.py — real throwaway SQLite with the production
FTS5 triggers (chunks_fts + facts_fts) applied, mirroring test_md_emit.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from src.facts.emit import emit_facts
from src.models import Base, Chunk, ChunkType, Fact, Section, Spec

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
_MIS_SLICED = (  # pandoc simple-table sliced mid-token -> degrades to 0 facts
    "P_CMAX (dBm) T | olerance (dB)\n"
    "23 < P ≤ 33 | 2 | .0\n"
    "21 ≤ P ≤ 23 | 2 | .0\n"
)


def _session(tmp_path) -> Session:
    engine = create_engine(
        f"sqlite:///{(tmp_path / 'facts.sqlite').as_posix()}", future=True,
    )
    Base.metadata.create_all(engine)
    with engine.begin() as conn:
        for ddl in (*init_db.FTS_DDL, *init_db.FACTS_FTS_DDL):
            conn.exec_driver_sql(ddl)
    return Session(engine)


def _add_spec(session, *, version="i00") -> Spec:
    spec = Spec(
        name="38.521-1", version=version, source_file="x.md",
        source_format="tspec_md",
    )
    session.add(spec)
    session.flush()
    return spec


def _add_table(session, spec, section_number, body, *, table_id="6.3.1.3-1"):
    sec = Section(
        spec_id=spec.spec_id, section_number=section_number, title="t",
        level=len(section_number.split(".")), page_start=1,
    )
    session.add(sec)
    session.flush()
    session.add(Chunk(
        section_id=sec.section_id, text=body, page=0, char_offset=0,
        source_format="tspec_md", chunk_type=ChunkType.TABLE, table_id=table_id,
    ))
    session.flush()
    return sec


def test_emit_writes_facts_and_syncs_fts(tmp_path):
    session = _session(tmp_path)
    spec = _add_spec(session)
    _add_table(session, spec, "6.3.1.3", _GRID)
    stats = emit_facts(session, spec.spec_id)
    session.commit()

    facts = session.execute(select(Fact)).scalars().all()
    assert facts and stats.n_facts == len(facts)
    assert all(f.fact_text for f in facts)                # fact_text populated
    assert all(f.extracted_by == "rule/table_v1" for f in facts)
    # -40 extracted under the right row label, in the right section
    assert any(
        f.fact_data["row_label"] == "Minimum output power"
        and f.fact_data.get("value_num") == -40.0
        for f in facts
    )
    # facts_fts kept in sync by the trigger
    n_fts = session.execute(text("SELECT count(*) FROM facts_fts")).scalar_one()
    assert n_fts == len(facts)
    row = session.execute(text(
        "SELECT section_number FROM facts_fts WHERE fact_text MATCH 'minimum' LIMIT 1"
    )).first()
    assert row is not None and row[0] == "6.3.1.3"


def test_emit_is_idempotent(tmp_path):
    session = _session(tmp_path)
    spec = _add_spec(session)
    _add_table(session, spec, "6.3.1.3", _GRID)
    first = emit_facts(session, spec.spec_id)
    second = emit_facts(session, spec.spec_id)
    session.commit()
    assert second.n_facts == first.n_facts
    n_facts = session.execute(text("SELECT count(*) FROM facts")).scalar_one()
    n_fts = session.execute(text("SELECT count(*) FROM facts_fts")).scalar_one()
    assert n_facts == n_fts == first.n_facts


def test_emit_mis_sliced_degrades(tmp_path):
    session = _session(tmp_path)
    spec = _add_spec(session)
    _add_table(session, spec, "6.2.4.3", _MIS_SLICED, table_id="6.2.4.3-2")
    stats = emit_facts(session, spec.spec_id)
    session.commit()
    assert stats.n_chunks_scanned == 1
    assert stats.n_chunks_degraded == 1
    assert stats.n_facts == 0


def test_emit_section_scoped_delete(tmp_path):
    session = _session(tmp_path)
    spec = _add_spec(session)
    _add_table(session, spec, "6.2.1.3", _GRID, table_id="6.2.1.3-1")
    _add_table(session, spec, "6.3.1.3", _GRID, table_id="6.3.1.3-1")
    # emit only 6.3 scope
    emit_facts(session, spec.spec_id, sections_filter=["6.3"])
    session.commit()
    secs = {
        f.fact_data["table_id"]
        for f in session.execute(select(Fact)).scalars()
    }
    assert secs == {"6.3.1.3-1"}    # 6.2 not extracted
    # re-emit 6.3 scope: must not require/disturb 6.2 (still absent), stable
    emit_facts(session, spec.spec_id, sections_filter=["6.3"])
    session.commit()
    assert session.execute(text("SELECT count(*) FROM facts")).scalar_one() > 0
