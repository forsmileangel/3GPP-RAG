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
            # FTS objects must be dropped before chunks (parent table)
            conn.exec_driver_sql("DROP TRIGGER IF EXISTS chunks_fts_au")
            conn.exec_driver_sql("DROP TRIGGER IF EXISTS chunks_fts_ad")
            conn.exec_driver_sql("DROP TRIGGER IF EXISTS chunks_fts_ai")
            conn.exec_driver_sql("DROP TABLE IF EXISTS chunks_fts")
        Base.metadata.drop_all(engine)

    print("Creating tables...")
    Base.metadata.create_all(engine)

    print("Creating FTS5 virtual table + sync triggers...")
    with engine.begin() as conn:
        for ddl in FTS_DDL:
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

    print("OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
