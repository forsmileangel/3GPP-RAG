"""Stage 2 ingestion: produce chunks for sections that ingest_toc.py
already wrote.

Default behavior: chunks LEAF sections only (those without children in
the registered tree). This avoids the double-coverage trap — §6.2's
page range fully contains §6.2.1.5 etc., so chunking §6.2 *and* §6.2.1.5
would index the same text twice. Use --include-non-leaf when you
genuinely want a parent's full range chunked (e.g. §6.2 was registered
without children).

Run after `ingest_toc.py`. Idempotent: only chunks sections where
is_indexed=False (override with --refresh to re-chunk everything,
which deletes prior chunks via cascade).

    .venv/Scripts/python.exe scripts/chunk_sections.py --pdf data/raw/...pdf

Filter to a subset (must include leaves of those subtrees):
    .venv/Scripts/python.exe scripts/chunk_sections.py --pdf ... \
        --sections 6.2,6.3
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.config import settings
from src.ingestion import chunk_spec_pdf
from src.models import Chunk, Section, Spec


def parse_section_list(raw: str) -> list[str]:
    items = [p.strip() for p in raw.split(",") if p.strip()]
    if not items:
        raise argparse.ArgumentTypeError("--sections must list at least one section")
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True, type=Path, help="Path to source PDF")
    parser.add_argument(
        "--sections",
        type=parse_section_list,
        help="Optional comma-separated section_numbers; defaults to all sections of the spec",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Re-chunk even if section.is_indexed=True (existing chunks cascade-deleted)",
    )
    parser.add_argument(
        "--include-non-leaf",
        action="store_true",
        help="Chunk non-leaf sections too (default: skip them to avoid double-coverage)",
    )
    args = parser.parse_args()

    if not args.pdf.exists():
        print(f"ERROR: PDF not found: {args.pdf}", file=sys.stderr)
        return 1

    engine = create_engine(settings.db_url, future=True)
    with Session(engine) as session, session.begin():
        spec = session.execute(
            select(Spec).where(Spec.source_file == str(args.pdf.resolve()))
        ).scalar_one_or_none()
        if spec is None:
            print(
                f"ERROR: no spec row for source_file={args.pdf!s}. "
                "Run scripts/ingest_toc.py first.",
                file=sys.stderr,
            )
            return 2

        q = select(Section).where(Section.spec_id == spec.spec_id).order_by(Section.page_start)
        if args.sections:
            # User restricted to specific section_numbers; expand to include
            # their descendants so leaf filtering still picks up the actual
            # leaves under e.g. "6.2".
            seed_ids = {
                s.section_id
                for s in session.execute(
                    select(Section).where(
                        Section.spec_id == spec.spec_id,
                        Section.section_number.in_(args.sections),
                    )
                ).scalars()
            }
            if not seed_ids:
                print(f"WARN: --sections {args.sections} matched no rows")
                return 0
            # BFS down the parent_id graph to collect all descendants.
            all_ids = set(seed_ids)
            frontier = set(seed_ids)
            while frontier:
                children = session.execute(
                    select(Section).where(Section.parent_id.in_(frontier))
                ).scalars().all()
                next_frontier = {c.section_id for c in children if c.section_id not in all_ids}
                all_ids |= next_frontier
                frontier = next_frontier
            q = q.where(Section.section_id.in_(all_ids))

        sections = list(session.execute(q).scalars())

        if not sections:
            print("WARN: no matching sections found")
            return 0

        if not args.include_non_leaf:
            # Filter to leaves: sections that are not parents of any other
            # section in the current subset.
            parent_ids = {
                s.parent_id for s in sections if s.parent_id is not None
            }
            non_leaves = [s for s in sections if s.section_id in parent_ids]
            sections = [s for s in sections if s.section_id not in parent_ids]
            if non_leaves:
                print(
                    f"[filter] Skipping {len(non_leaves)} non-leaf sections "
                    f"(use --include-non-leaf to chunk them anyway): "
                    f"{[s.section_number for s in non_leaves]}"
                )

        if args.refresh:
            # Cascade delete existing chunks for these sections; FTS triggers
            # propagate the deletion.
            kept_ids = {s.section_id for s in sections}
            existing = session.execute(
                select(Chunk).where(Chunk.section_id.in_(kept_ids))
            ).scalars().all()
            for c in existing:
                session.delete(c)
            for s in sections:
                s.is_indexed = False
            session.flush()
            print(f"[refresh] Removed {len(existing)} prior chunks; reset is_indexed")

        print(f"[chunker] Processing {len(sections)} sections from {spec.name} v{spec.version}")
        counts = chunk_spec_pdf(
            session,
            args.pdf,
            sections,
            source_format=spec.source_format,
            skip_already_indexed=not args.refresh,
        )

    total = sum(counts.values())
    indexed = sum(1 for n in counts.values() if n > 0)
    skipped = sum(1 for n in counts.values() if n == 0)
    print(f"[chunker] indexed={indexed} sections, skipped={skipped}, total chunks={total}")
    print("OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
