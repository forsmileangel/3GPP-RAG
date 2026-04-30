"""Initialize the SQLite metadata DB.

Idempotent: safe to run multiple times. `--drop` wipes existing tables.

    uv run python scripts/init_db.py            # create if missing
    uv run python scripts/init_db.py --drop     # drop then create
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running this as a top-level script: `python scripts/init_db.py`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine, inspect

from src.config import settings
from src.models import Base


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
        Base.metadata.drop_all(engine)

    print("Creating tables...")
    Base.metadata.create_all(engine)

    inspector = inspect(engine)
    tables = sorted(inspector.get_table_names())
    print(f"Tables present: {tables}")

    expected = {"specs", "sections", "chunks", "personal_notes", "cross_gen_mapping", "share_profiles"}
    missing = expected - set(tables)
    if missing:
        print(f"ERROR: missing tables {missing}", file=sys.stderr)
        return 1

    print("OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
