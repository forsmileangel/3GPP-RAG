"""Stage 1 ingestion: register a spec and its selected section tree.

This is *only* the TOC step — it walks the PDF bookmarks, picks the
requested sections (plus all their descendants), and writes rows to the
`specs` and `sections` tables. Each section starts with `is_indexed=False`
because the chunker / embedder runs in a later stage (Week 2).

Idempotent on (spec_name, version): re-running with the same PDF either
short-circuits (default) or refreshes the section tree (--refresh).

Examples:
    .venv/Scripts/python.exe scripts/ingest_toc.py \
        --pdf data/raw/ts_138521-01_v17_05_00.pdf \
        --sections 6.2,6.3

    .venv/Scripts/python.exe scripts/ingest_toc.py --pdf ... --sections 6.2 \
        --spec-name 38.521-1 --version 17.5.0 --generation 5G
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Allow running from repo root without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import fitz  # PyMuPDF
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.config import settings
from src.ingestion import (
    SectionEntry,
    SectionNotFoundError,
    TOCEmptyError,
    extract_sections,
)
from src.models import Section, Spec


# Best-effort spec name + version inference from common 3GPP filename
# patterns: "ts_138521-01_v17_05_00.pdf" -> ("38.521-1", "17.5.0").
# Pattern walk-through:
#   ts_ : literal prefix, case-insensitive
#   1?(\d{2})(\d{3}) : optional leading '1' (3GPP doc-id quirk on TS 138521),
#                     then 2-digit family + 3-digit doc number
#   (?:-(\d+))? : optional '-NN' subdoc
#   _v(\d+)_(\d+)_(\d+) : version major/minor/patch
_FILENAME_RE = re.compile(
    r"ts_1?(\d{2})(\d{3})(?:-(\d+))?_v(\d+)_(\d+)_(\d+)",
    re.IGNORECASE,
)


def _infer_spec_meta(pdf_path: Path) -> tuple[str | None, str | None, str | None]:
    """Return (spec_name, version, generation) inferred from the filename."""
    m = _FILENAME_RE.search(pdf_path.name)
    if not m:
        return None, None, None
    fam, doc, sub, vmaj, vmin, vpat = m.groups()
    name = f"{fam}.{doc}"
    if sub:
        # Strip leading zeros: "01" -> "1" (3GPP citation form is "38.521-1").
        name += f"-{int(sub)}"
    version = f"{int(vmaj)}.{int(vmin)}.{int(vpat)}"
    # Generation hint: 38.xxx = 5G NR, 36.xxx = LTE, 25.xxx = UMTS, 45.xxx = GSM.
    gen_hint = {"38": "5G", "36": "4G", "25": "3G", "45": "2G"}.get(fam)
    return name, version, gen_hint


def parse_section_list(raw: str) -> list[str]:
    """Comma-separated section numbers; whitespace is forgiving."""
    items = [p.strip() for p in raw.split(",") if p.strip()]
    if not items:
        raise argparse.ArgumentTypeError("--sections must list at least one section")
    return items


def _ensure_spec(
    session: Session,
    *,
    name: str,
    version: str,
    pdf_path: Path,
    page_count: int,
    generation: str | None,
    release: str | None,
) -> Spec:
    spec = session.execute(
        select(Spec).where(Spec.name == name, Spec.version == version)
    ).scalar_one_or_none()

    if spec is None:
        spec = Spec(
            name=name,
            version=version,
            release=release,
            generation=generation,
            source_file=str(pdf_path.resolve()),
            page_count=page_count,
        )
        session.add(spec)
        session.flush()
        print(f"[spec] CREATE {name} v{version} (spec_id={spec.spec_id})")
    else:
        # Don't silently change source_file — the user might be re-running
        # against the same canonical PDF in a different mount path. Just
        # log if the path differs.
        new_path = str(pdf_path.resolve())
        if spec.source_file != new_path:
            print(
                f"[spec] WARN: source_file differs ({spec.source_file!r} -> "
                f"{new_path!r}); keeping existing on row"
            )
        print(f"[spec] EXISTS {name} v{version} (spec_id={spec.spec_id})")
    return spec


def _write_sections(
    session: Session,
    spec: Spec,
    entries: list[SectionEntry],
    *,
    refresh: bool,
) -> tuple[int, int]:
    """Insert (or refresh) sections rows. Returns (created, skipped)."""
    if refresh:
        # Delete current sections for this spec — cascades into chunks.
        existing = session.execute(
            select(Section).where(Section.spec_id == spec.spec_id)
        ).scalars().all()
        if existing:
            for row in existing:
                session.delete(row)
            session.flush()
            print(f"[sections] --refresh: removed {len(existing)} prior rows")

    # Build in TOC order so parents are flushed before children look them up.
    by_number: dict[str, Section] = {}
    created = 0
    skipped = 0

    for entry in entries:
        existing = session.execute(
            select(Section).where(
                Section.spec_id == spec.spec_id,
                Section.section_number == entry.section_number,
            )
        ).scalar_one_or_none()
        if existing:
            by_number[entry.section_number] = existing
            skipped += 1
            continue

        parent = (
            by_number.get(entry.parent_number)
            if entry.parent_number
            else None
        )
        # If the parent wasn't in this batch but exists in DB (from earlier
        # ingest of an overlapping selection), look it up.
        if parent is None and entry.parent_number:
            parent = session.execute(
                select(Section).where(
                    Section.spec_id == spec.spec_id,
                    Section.section_number == entry.parent_number,
                )
            ).scalar_one_or_none()

        row = Section(
            spec_id=spec.spec_id,
            parent_id=parent.section_id if parent else None,
            section_number=entry.section_number,
            title=entry.title or entry.full_title,
            level=entry.level,
            page_start=entry.page_start,
            page_end=entry.page_end,
            is_indexed=False,
        )
        session.add(row)
        session.flush()  # populate row.section_id for child wiring
        by_number[entry.section_number] = row
        created += 1

    return created, skipped


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True, type=Path, help="Path to source PDF")
    parser.add_argument(
        "--sections",
        required=True,
        type=parse_section_list,
        help="Comma-separated section numbers, e.g. '6.2,6.3'",
    )
    parser.add_argument("--spec-name", help="Override inferred spec name (e.g. '38.521-1')")
    parser.add_argument("--version", help="Override inferred version (e.g. '17.5.0')")
    parser.add_argument("--generation", help="Override inferred generation (e.g. '5G')")
    parser.add_argument("--release", help="3GPP release label, optional (e.g. 'Rel-17')")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Drop existing sections (and their chunks) for this spec before re-ingesting",
    )
    args = parser.parse_args()

    pdf_path: Path = args.pdf
    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    inferred_name, inferred_version, inferred_gen = _infer_spec_meta(pdf_path)
    spec_name = args.spec_name or inferred_name
    version = args.version or inferred_version
    generation = args.generation or inferred_gen

    if not spec_name or not version:
        print(
            "ERROR: could not infer spec_name/version from filename — "
            "pass --spec-name and --version explicitly.",
            file=sys.stderr,
        )
        return 1

    print(f"[input] PDF={pdf_path.name}  spec={spec_name} v{version}  gen={generation}")
    print(f"[input] requested sections: {args.sections}")

    # Read page_count up-front; extract_sections re-opens the PDF internally.
    with fitz.open(pdf_path) as doc:
        page_count = doc.page_count
    print(f"[input] page_count={page_count}")

    try:
        entries = extract_sections(pdf_path, args.sections)
    except TOCEmptyError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    except SectionNotFoundError as e:
        print(f"ERROR: section not in TOC: {e}", file=sys.stderr)
        return 2

    print(
        f"[toc] selected {len(entries)} section rows "
        f"({sum(1 for x in entries if x.requested)} requested, "
        f"{sum(1 for x in entries if not x.requested)} pulled in as descendants)"
    )

    settings.db_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(settings.db_url, future=True)
    with Session(engine) as session, session.begin():
        spec = _ensure_spec(
            session,
            name=spec_name,
            version=version,
            pdf_path=pdf_path,
            page_count=page_count,
            generation=generation,
            release=args.release,
        )
        created, skipped = _write_sections(session, spec, entries, refresh=args.refresh)

    print(f"[sections] created={created}  skipped(existing)={skipped}")
    print("OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
