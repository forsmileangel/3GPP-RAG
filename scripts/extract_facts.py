"""Extract rule-based facts from a spec's TABLE chunks into the facts table.

Idempotent (delete-and-reinsert, scoped to the spec [and --sections]). md
tables yield structured table-cell facts; pdf tables yield nothing (PyMuPDF
linearization is not rule-recoverable). Run AFTER ingest + chunking.

    .venv/Scripts/python.exe scripts/extract_facts.py \
        --spec 38.521-1 --source-format tspec_md --sections "6.2,6.3"
    ... --dry-run        # count facts, write nothing
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.config import settings
from src.facts.emit import emit_facts, load_table_chunks
from src.facts.extractor import extract_facts_from_chunk
from src.models import Spec
from src.source_formats import validate_source_format


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, help='spec name, e.g. "38.521-1"')
    parser.add_argument(
        "--source-format", required=True, choices=["pdf_pymupdf", "tspec_md"],
    )
    parser.add_argument("--sections", default=None,
                        help='dotted-prefix filter, e.g. "6.2,6.3"')
    parser.add_argument("--dry-run", action="store_true",
                        help="count facts; write nothing")
    args = parser.parse_args()

    source_format = validate_source_format(args.source_format)
    sections_filter = (
        [s.strip() for s in args.sections.split(",") if s.strip()]
        if args.sections else None
    )

    engine = create_engine(settings.db_url, future=True)
    with Session(engine) as session:
        spec = session.execute(
            select(Spec).where(
                Spec.name == args.spec, Spec.source_format == source_format
            )
        ).scalar_one_or_none()
        if spec is None:
            available = ", ".join(
                f"{s.name}/{s.source_format}@{s.version}"
                for s in session.execute(select(Spec)).scalars()
            )
            print(
                f"ERROR: no spec {args.spec!r} with source_format "
                f"{source_format!r}; have: {available or '(none)'}",
                file=sys.stderr,
            )
            return 1

        if args.dry_run:
            views = load_table_chunks(
                session, spec.spec_id, sections_filter=sections_filter
            )
            counts = [len(extract_facts_from_chunk(v)) for v in views]
            n_facts = sum(counts)
            degraded = sum(1 for c in counts if c == 0)
            print(
                f"[dry-run] {len(views)} TABLE chunks -> {n_facts} facts, "
                f"{degraded} degraded (0 facts); no DB writes"
            )
            return 0

        stats = emit_facts(
            session, spec.spec_id, sections_filter=sections_filter
        )
        session.commit()

    print(
        f"[emit] spec={args.spec}/{source_format} "
        f"chunks={stats.n_chunks_scanned} facts={stats.n_facts} "
        f"degraded={stats.n_chunks_degraded}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
