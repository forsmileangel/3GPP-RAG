"""Snapshot the local databases into a timestamped archive (Step 9d).

Implements portability rule #4 (CLAUDE.md §6): back up `data/db/` (SQLite
metadata + Chroma vectors — the expensive-to-regenerate state) into
`snapshots/YYYY-MM-DD.tar.gz`. Python instead of the originally-planned
bash so it runs unchanged on Windows and Linux. `snapshots/` is gitignored.

    .venv/Scripts/python.exe scripts/backup.py            # create snapshot
    ... --list                                            # show existing ones

Idempotence: a second run on the same day gets an _HHMMSS suffix rather
than overwriting the earlier snapshot.
"""

from __future__ import annotations

import argparse
import sys
import tarfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import settings

SNAPSHOT_DIR = settings.repo_root / "snapshots"


def _target_path(now: datetime) -> Path:
    base = SNAPSHOT_DIR / f"{now:%Y-%m-%d}.tar.gz"
    if not base.exists():
        return base
    return SNAPSHOT_DIR / f"{now:%Y-%m-%d}_{now:%H%M%S}.tar.gz"


def create_snapshot() -> int:
    db_dir = settings.db_path.parent  # data/db — holds SQLite + Chroma
    if not db_dir.is_dir():
        print(f"ERROR: nothing to back up — {db_dir} does not exist",
              file=sys.stderr)
        return 1

    SNAPSHOT_DIR.mkdir(exist_ok=True)
    target = _target_path(datetime.now())
    with tarfile.open(target, "w:gz") as tar:
        tar.add(db_dir, arcname=db_dir.name)

    size_mb = target.stat().st_size / (1024 * 1024)
    print(f"[backup] {db_dir} -> {target} ({size_mb:.1f} MB)")
    return 0


def list_snapshots() -> int:
    if not SNAPSHOT_DIR.is_dir():
        print("(no snapshots yet)")
        return 0
    entries = sorted(SNAPSHOT_DIR.glob("*.tar.gz"))
    if not entries:
        print("(no snapshots yet)")
        return 0
    for p in entries:
        print(f"{p.name}  {p.stat().st_size / (1024 * 1024):.1f} MB")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true",
                        help="list existing snapshots instead of creating one")
    args = parser.parse_args()
    return list_snapshots() if args.list else create_snapshot()


if __name__ == "__main__":
    raise SystemExit(main())
