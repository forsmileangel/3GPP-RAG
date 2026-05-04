"""End-to-end smoke for Phase A Week 1.

Walks the full Week 1 pipeline against a temporary SQLite DB:
  1. init_db.py creates 7 tables + chunks_fts + 3 triggers
  2. ingest_toc.py registers spec + section tree from the real PDF
  3. SQL invariants hold (counts, sibling exclusion, parent tree, is_indexed)
  4. FTS5 triggers stay in sync on INSERT / UPDATE / DELETE of chunks

Marked `e2e` because it touches the real PDF; can be deselected with
`pytest -m "not e2e"` once the suite grows.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.orm import Session


REPO_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = REPO_ROOT / "data" / "raw" / "ts_138521-01_v17_05_00.pdf"
PYTHON = REPO_ROOT / ".venv" / "Scripts" / "python.exe"


pytestmark = pytest.mark.e2e


@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    """Point DB_PATH at a tmp file so init_db / ingest_toc don't clobber
    the dev DB. The CHROMA_PATH override keeps Chroma I/O isolated too,
    though Week 1 doesn't actually write Chroma yet."""
    db_file = tmp_path / "metadata.sqlite"
    monkeypatch.setenv("DB_PATH", str(db_file))
    monkeypatch.setenv("CHROMA_PATH", str(tmp_path / "chroma"))
    return db_file


def _run(script: str, *args: str) -> subprocess.CompletedProcess:
    """Run a script with the same DB_PATH the fixture set."""
    cmd = [str(PYTHON), str(REPO_ROOT / "scripts" / script), *args]
    return subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env={**os.environ},
        timeout=120,
    )


@pytest.fixture
def initialized_db(tmp_db):
    result = _run("init_db.py")
    assert result.returncode == 0, (
        f"init_db.py failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "OK." in result.stdout
    return tmp_db


@pytest.fixture
def ingested_db(initialized_db):
    if not PDF_PATH.exists():
        pytest.skip(f"PDF unavailable: {PDF_PATH}")
    result = _run(
        "ingest_toc.py",
        "--pdf", str(PDF_PATH),
        "--sections", "6.2,6.3",
    )
    assert result.returncode == 0, (
        f"ingest_toc.py failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "OK." in result.stdout
    return initialized_db


def test_init_db_creates_all_tables_and_fts(initialized_db):
    engine = create_engine(f"sqlite:///{initialized_db.as_posix()}", future=True)
    with engine.connect() as conn:
        tables = {
            row[0] for row in conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table'")
            )
        }
    assert {
        "specs", "sections", "chunks", "facts",
        "personal_notes", "cross_gen_mapping", "share_profiles",
        "chunks_fts",
    }.issubset(tables)


def test_ingest_writes_expected_invariants(ingested_db):
    """Re-asserts the 23-section / sibling-exclusion / parent-tree
    invariants that we manually checked, but in an automated test."""
    from src.models import Section, Spec

    engine = create_engine(f"sqlite:///{ingested_db.as_posix()}", future=True)
    with Session(engine) as s:
        spec = s.execute(select(Spec)).scalar_one()
        assert spec.name == "38.521-1"
        assert spec.version == "17.5.0"
        assert spec.generation == "5G"

        sec_count = s.execute(select(func.count(Section.section_id))).scalar()
        assert sec_count == 23, f"expected 23 sections, got {sec_count}"

        # §6.2A is a sibling of §6.2 — must NOT be present (Phase 0 lesson).
        leaked = s.execute(
            select(Section).where(Section.section_number == "6.2A")
        ).scalar_one_or_none()
        assert leaked is None, "§6.2A leaked into selection"

        # §6.3.2 (Transmit OFF) IS a child of §6.3 — must be present.
        target = s.execute(
            select(Section).where(Section.section_number == "6.3.2")
        ).scalar_one()
        assert target.title == "Transmit OFF power"

        # Parent tree is wired up.
        sec_62 = s.execute(
            select(Section).where(Section.section_number == "6.2")
        ).scalar_one()
        sec_621 = s.execute(
            select(Section).where(Section.section_number == "6.2.1")
        ).scalar_one()
        assert sec_621.parent_id == sec_62.section_id

        # Nothing is indexed yet (Week 1 only writes the TOC tree).
        indexed = s.execute(
            select(func.count(Section.section_id)).where(Section.is_indexed.is_(True))
        ).scalar()
        assert indexed == 0


def test_fts5_triggers_stay_in_sync(ingested_db):
    """INSERT / UPDATE / DELETE on chunks must propagate to chunks_fts."""
    from src.models import Chunk, ChunkType, Section

    engine = create_engine(f"sqlite:///{ingested_db.as_posix()}", future=True)
    with Session(engine) as s:
        sec = s.execute(
            select(Section).where(Section.section_number == "6.2.1")
        ).scalar_one()

        c1 = Chunk(
            section_id=sec.section_id,
            text="FR1 PC3 UE maximum output power 23 dBm with tolerance",
            page=93,
            char_offset=0,
            chunk_type=ChunkType.TABLE_ROW,
            table_id="Table 6.2.1.5-1",
            row_index=2,
        )
        s.add(c1)
        s.commit()

        # FTS reflects the insert AND the trigger pulled section_number from sections.
        rows = s.execute(
            text(
                "SELECT rowid, section_number, table_id, page FROM chunks_fts "
                "WHERE chunks_fts MATCH 'PC3 dBm'"
            )
        ).fetchall()
        assert rows, "FTS5 did not see INSERT"
        assert rows[0][1] == "6.2.1"
        assert rows[0][2] == "Table 6.2.1.5-1"

        # UPDATE
        s.execute(
            text("UPDATE chunks SET text=:t WHERE chunk_id=:cid"),
            {"t": "REPLACED tolerance line for FR1 PC3", "cid": c1.chunk_id},
        )
        s.commit()
        rows = s.execute(
            text("SELECT rowid FROM chunks_fts WHERE chunks_fts MATCH 'REPLACED'")
        ).fetchall()
        assert rows, "FTS5 did not see UPDATE (new text)"
        rows = s.execute(
            text("SELECT rowid FROM chunks_fts WHERE chunks_fts MATCH 'maximum'")
        ).fetchall()
        assert not rows, "FTS5 still has old text after UPDATE"

        # DELETE
        s.execute(text("DELETE FROM chunks WHERE chunk_id=:cid"), {"cid": c1.chunk_id})
        s.commit()
        rows = s.execute(
            text("SELECT rowid FROM chunks_fts WHERE chunks_fts MATCH 'REPLACED'")
        ).fetchall()
        assert not rows, "FTS5 retained row after DELETE"


def test_idempotent_reingest_doesnt_duplicate(ingested_db):
    """Running ingest_toc.py twice on the same input shouldn't double rows."""
    from src.models import Section, Spec

    # Re-run; should report 'EXISTS' on spec and skip all sections.
    result = _run(
        "ingest_toc.py",
        "--pdf", str(PDF_PATH),
        "--sections", "6.2,6.3",
    )
    assert result.returncode == 0
    assert "EXISTS" in result.stdout
    assert "skipped(existing)=23" in result.stdout

    engine = create_engine(f"sqlite:///{ingested_db.as_posix()}", future=True)
    with Session(engine) as s:
        spec_count = s.execute(select(func.count(Spec.spec_id))).scalar()
        assert spec_count == 1
        sec_count = s.execute(select(func.count(Section.section_id))).scalar()
        assert sec_count == 23
