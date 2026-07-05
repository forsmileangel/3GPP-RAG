"""Ingest a TSpec-LLM markdown spec part — the md path's one-shot CLI.

PDF flow is staged (init_db -> ingest_toc -> chunk_sections); markdown is
discover -> parse -> emit in one command because the adapter already
holds the whole structure in memory.

Usage:
    .venv/Scripts/python.exe scripts/ingest_md.py \
        --root spike/tspec_probe_out/3GPP-clean/Rel-18/38_series \
        --spec 38.521-1 --version i00 --sections "6.2,6.3"
    ... --dry-run         # parse + stats only, no DB writes
    ... --force           # allow re-emit of an already-EMBEDDED spec
                          # (deletes its Chroma vectors first)

After a successful emit, run embed_chunks.py — it picks up the new chunks
automatically (vector_id IS NULL).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.config import settings
from src.ingestion.md_parser import MarkdownAdapter


def parse_spec_arg(spec: str) -> tuple[str, str | None]:
    """"38.521-1" -> ("38.521", "1"); "38.331" -> ("38.331", None)."""
    if "-" in spec:
        spec_id, part = spec.rsplit("-", 1)
        return spec_id, part
    return spec, None


# On a full-spec parse the benign level-jump warnings (band-combination
# subtrees are H3 -> H5 by design) number in the hundreds; a flat
# `warnings[:20]` would bury the STRUCTURAL ones that demand a look
# (duplicate anchors, unparseable anchors). Print structural in full,
# sample the rest.
_LEVEL_JUMP_SAMPLE = 5
_OTHER_SAMPLE = 10


def _print_warnings(warnings: list[str]) -> None:
    structural = [w for w in warnings
                  if "duplicate anchor" in w or "without parseable anchor" in w]
    level_jumps = [w for w in warnings
                   if "level jump" in w and w not in structural]
    other = [w for w in warnings if w not in structural and w not in level_jumps]

    print(f"[parse] warning census: structural={len(structural)} "
          f"level-jump={len(level_jumps)} other={len(other)}")
    for w in structural:
        print(f"  [warn] {w}")
    for w in level_jumps[:_LEVEL_JUMP_SAMPLE]:
        print(f"  [warn] {w}")
    if len(level_jumps) > _LEVEL_JUMP_SAMPLE:
        print(f"  [warn] ... and {len(level_jumps) - _LEVEL_JUMP_SAMPLE} "
              f"more level-jump warnings (benign by design)")
    for w in other[:_OTHER_SAMPLE]:
        print(f"  [warn] {w}")
    if len(other) > _OTHER_SAMPLE:
        print(f"  [warn] ... and {len(other) - _OTHER_SAMPLE} more")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True,
                        help="corpus directory to discover")
    parser.add_argument("--spec", required=True,
                        help='spec selector, e.g. "38.521-1" or "38.331"')
    parser.add_argument("--version", required=True, help='e.g. "i00"')
    parser.add_argument("--sections", default=None,
                        help='dotted-prefix subtree filter, e.g. "6.2,6.3"')
    parser.add_argument("--force", action="store_true",
                        help="re-emit an already-embedded spec (deletes its "
                             "Chroma vectors first)")
    parser.add_argument("--dry-run", action="store_true",
                        help="parse and print stats; write nothing")
    args = parser.parse_args()

    if not args.root.exists():
        print(f"ERROR: root not found: {args.root}", file=sys.stderr)
        return 1

    spec_id, part = parse_spec_arg(args.spec)
    sections_filter = (
        [s.strip() for s in args.sections.split(",") if s.strip()]
        if args.sections else None
    )

    adapter = MarkdownAdapter()
    units = adapter.discover_inputs(args.root)
    for issue in adapter.last_discovery_issues:
        print(f"[discover] {issue}")

    unit = next(
        (u for u in units
         if u.spec_id == spec_id and u.part == part
         and u.version == args.version),
        None,
    )
    if unit is None:
        available = ", ".join(
            f"{u.spec_id}-{u.part or '-'}@{u.version}" for u in units
        )
        print(
            f"ERROR: no unit for {args.spec}@{args.version}; "
            f"discovered: {available or '(none)'}",
            file=sys.stderr,
        )
        return 1

    print(f"[parse] {len(unit.source_paths)} file(s): "
          f"{', '.join(p.name for p in unit.source_paths)}")
    parsed = adapter.parse(unit)
    print(f"[parse] {len(parsed.sections)} sections, "
          f"{len(parsed.warnings)} warning(s)")
    _print_warnings(parsed.warnings)

    if args.dry_run:
        print("[dry-run] no DB writes")
        return 0

    engine = create_engine(settings.db_url, future=True)
    with Session(engine) as session:
        stats = adapter.emit(
            parsed, session,
            sections_filter=sections_filter, force=args.force,
        )
        session.commit()

    print(
        f"[emit] sections={stats.n_sections} chunks={stats.n_chunks} "
        f"tables={stats.n_tables} elapsed={stats.elapsed_sec:.1f}s"
    )
    print("[next] run embed_chunks.py to embed the new chunks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
