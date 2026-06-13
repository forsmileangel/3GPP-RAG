"""Initialize the SQLite metadata DB.

Idempotent: safe to run multiple times. `--drop` wipes existing tables.

    uv run python scripts/init_db.py            # create if missing
    uv run python scripts/init_db.py --drop     # drop then create

Builds:
  - 7 SQLAlchemy tables (specs, sections, chunks, facts, personal_notes,
    cross_gen_mapping, share_profiles)
  - chunks_fts FTS5 virtual table mirroring chunks.text (sparse retrieval)
  - 3 sync triggers (insert/update/delete on chunks → keep chunks_fts current)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running this as a top-level script: `python scripts/init_db.py`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine, inspect, text

from src.config import settings
from src.models import Base
from src.source_formats import SOURCE_FORMAT_PDF_PYMUPDF


# FTS5 virtual table — non-contentless so we can store denormalized columns
# (like section_number from sections via trigger lookup) that aren't on
# the chunks table. Storage overhead is minimal at our scale and we get
# straightforward DELETE/UPDATE semantics.
FTS_DDL = [
    """
    CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
        text,
        section_number UNINDEXED,
        table_id UNINDEXED,
        page UNINDEXED,
        tokenize='unicode61 remove_diacritics 2'
    )
    """,
    """
    CREATE TRIGGER IF NOT EXISTS chunks_fts_ai AFTER INSERT ON chunks BEGIN
        INSERT INTO chunks_fts(rowid, text, section_number, table_id, page)
        VALUES (
            new.chunk_id,
            new.text,
            (SELECT section_number FROM sections WHERE section_id = new.section_id),
            new.table_id,
            new.page
        );
    END
    """,
    """
    CREATE TRIGGER IF NOT EXISTS chunks_fts_ad AFTER DELETE ON chunks BEGIN
        DELETE FROM chunks_fts WHERE rowid = old.chunk_id;
    END
    """,
    """
    CREATE TRIGGER IF NOT EXISTS chunks_fts_au AFTER UPDATE ON chunks BEGIN
        DELETE FROM chunks_fts WHERE rowid = old.chunk_id;
        INSERT INTO chunks_fts(rowid, text, section_number, table_id, page)
        VALUES (
            new.chunk_id,
            new.text,
            (SELECT section_number FROM sections WHERE section_id = new.section_id),
            new.table_id,
            new.page
        );
    END
    """,
]


# facts_fts mirrors facts.fact_text the way chunks_fts mirrors chunks.text.
# section_number is looked up via facts.section_id -> sections at trigger time.
FACTS_FTS_DDL = [
    """
    CREATE VIRTUAL TABLE IF NOT EXISTS facts_fts USING fts5(
        fact_text,
        section_number UNINDEXED,
        table_id UNINDEXED,
        page UNINDEXED,
        fact_type UNINDEXED,
        tokenize='unicode61 remove_diacritics 2'
    )
    """,
    """
    CREATE TRIGGER IF NOT EXISTS facts_fts_ai AFTER INSERT ON facts BEGIN
        INSERT INTO facts_fts(rowid, fact_text, section_number, table_id, page, fact_type)
        VALUES (
            new.fact_id,
            new.fact_text,
            (SELECT section_number FROM sections WHERE section_id = new.section_id),
            new.table_id,
            new.page,
            new.fact_type
        );
    END
    """,
    """
    CREATE TRIGGER IF NOT EXISTS facts_fts_ad AFTER DELETE ON facts BEGIN
        DELETE FROM facts_fts WHERE rowid = old.fact_id;
    END
    """,
    """
    CREATE TRIGGER IF NOT EXISTS facts_fts_au AFTER UPDATE ON facts BEGIN
        DELETE FROM facts_fts WHERE rowid = old.fact_id;
        INSERT INTO facts_fts(rowid, fact_text, section_number, table_id, page, fact_type)
        VALUES (
            new.fact_id,
            new.fact_text,
            (SELECT section_number FROM sections WHERE section_id = new.section_id),
            new.table_id,
            new.page,
            new.fact_type
        );
    END
    """,
]


def _has_column(conn, table_name: str, column_name: str) -> bool:
    rows = conn.exec_driver_sql(f"PRAGMA table_info({table_name})").fetchall()
    return any(row[1] == column_name for row in rows)


def _migrate_add_source_format(engine) -> None:
    """Forward migration for DBs created before source_format existed.

    SQLite does not support ADD COLUMN IF NOT EXISTS on all deployed
    versions, so inspect first and then ALTER only when needed.
    """
    with engine.begin() as conn:
        for table_name in ("specs", "chunks"):
            if _has_column(conn, table_name, "source_format"):
                continue
            print(
                f"Migrating {table_name}: add source_format "
                f"DEFAULT {SOURCE_FORMAT_PDF_PYMUPDF!r}"
            )
            conn.exec_driver_sql(
                f"ALTER TABLE {table_name} "
                "ADD COLUMN source_format VARCHAR(16) "
                f"NOT NULL DEFAULT '{SOURCE_FORMAT_PDF_PYMUPDF}'"
            )


def _migrate_add_fact_text(engine) -> None:
    """Forward migration for DBs created before facts.fact_text existed
    (Step 6). Nullable add — existing fact rows (none today) stay valid."""
    with engine.begin() as conn:
        if _has_column(conn, "facts", "fact_text"):
            return
        print("Migrating facts: add fact_text TEXT")
        conn.exec_driver_sql("ALTER TABLE facts ADD COLUMN fact_text TEXT")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--drop", action="store_true", help="Drop all tables before creating")
    args = parser.parse_args()

    settings.db_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"DB path: {settings.db_path}")
    print(f"DB URL:  {settings.db_url}")

    engine = create_engine(settings.db_url, echo=False, future=True)

    if args.drop:
        print("Dropping all tables...")
        with engine.begin() as conn:
            # FTS objects must be dropped before their parent tables.
            for trig in ("facts_fts_au", "facts_fts_ad", "facts_fts_ai"):
                conn.exec_driver_sql(f"DROP TRIGGER IF EXISTS {trig}")
            conn.exec_driver_sql("DROP TABLE IF EXISTS facts_fts")
            conn.exec_driver_sql("DROP TRIGGER IF EXISTS chunks_fts_au")
            conn.exec_driver_sql("DROP TRIGGER IF EXISTS chunks_fts_ad")
            conn.exec_driver_sql("DROP TRIGGER IF EXISTS chunks_fts_ai")
            conn.exec_driver_sql("DROP TABLE IF EXISTS chunks_fts")
        Base.metadata.drop_all(engine)

    print("Creating tables...")
    Base.metadata.create_all(engine)

    print("Applying forward migrations...")
    _migrate_add_source_format(engine)
    _migrate_add_fact_text(engine)

    print("Creating FTS5 virtual tables + sync triggers...")
    with engine.begin() as conn:
        for ddl in (*FTS_DDL, *FACTS_FTS_DDL):
            conn.exec_driver_sql(ddl.strip())

    inspector = inspect(engine)
    tables = sorted(inspector.get_table_names())
    print(f"Tables present: {tables}")

    expected = {
        "specs", "sections", "chunks", "facts",
        "personal_notes", "cross_gen_mapping", "share_profiles",
    }
    missing = expected - set(tables)
    if missing:
        print(f"ERROR: missing tables {missing}", file=sys.stderr)
        return 1

    # Verify FTS table + triggers
    with engine.connect() as conn:
        fts_rows = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='chunks_fts'")
        ).fetchall()
        triggers = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='trigger' "
                "AND name LIKE 'chunks_fts_%' ORDER BY name"
            )
        ).fetchall()

    if not fts_rows:
        print("ERROR: chunks_fts virtual table missing", file=sys.stderr)
        return 1
    expected_triggers = {"chunks_fts_ad", "chunks_fts_ai", "chunks_fts_au"}
    actual_triggers = {row[0] for row in triggers}
    if expected_triggers - actual_triggers:
        print(
            f"ERROR: missing triggers {expected_triggers - actual_triggers}",
            file=sys.stderr,
        )
        return 1
    print(f"FTS5: chunks_fts present, triggers: {sorted(actual_triggers)}")

    # Verify facts_fts table + triggers (Step 6)
    with engine.connect() as conn:
        facts_fts_rows = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='facts_fts'")
        ).fetchall()
        facts_triggers = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='trigger' "
                "AND name LIKE 'facts_fts_%' ORDER BY name"
            )
        ).fetchall()
    if not facts_fts_rows:
        print("ERROR: facts_fts virtual table missing", file=sys.stderr)
        return 1
    expected_facts_triggers = {"facts_fts_ad", "facts_fts_ai", "facts_fts_au"}
    actual_facts_triggers = {row[0] for row in facts_triggers}
    if expected_facts_triggers - actual_facts_triggers:
        print(
            f"ERROR: missing facts triggers "
            f"{expected_facts_triggers - actual_facts_triggers}",
            file=sys.stderr,
        )
        return 1
    print(f"FTS5: facts_fts present, triggers: {sorted(actual_facts_triggers)}")

    print("OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
