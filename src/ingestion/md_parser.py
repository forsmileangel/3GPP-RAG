"""MarkdownAdapter — TSpec-LLM markdown ingestion (Tier 1).

Lifecycle (contract in _base.IngestionAdapter):
  discover_inputs : sanity-gate the directory, parse filenames, group the
                    multi-file spec parts (cover + sNN ranges + annexes)
                    into one InputUnit each, source_paths in reading order.
  parse           : merge the unit's files into one text, clean pandoc
                    artifacts, parse headings, slice heading-bounded
                    sections, split tables out of each body. Pure — no DB.
  emit            : M4 (not yet implemented).

Section identity comes from the heading ANCHOR (the dotted number parsed
out of the title), never from markdown heading levels — levels in this
corpus are presentation (setext top sections, ATX deeper, H8 annex
markers) while the dotted number is authoritative structure. Headings
without a parseable anchor do NOT open a section; their text stays in the
enclosing section's body (and parse() records a warning).
"""

from __future__ import annotations

import re
import time
from collections import defaultdict
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.ingestion.chunker import chunk_section_text, persist_chunks
from src.models import Chunk, ChunkType, Section, Spec
from src.source_formats import SOURCE_FORMAT_TSPEC_MD

from ._artifact_cleaner import clean_body, strip_pandoc_anchors
from ._base import (
    Heading,
    IngestionAdapter,
    IngestStats,
    InputUnit,
    ParsedSpec,
)
from ._base import Section as ParsedSection
from ._filename_parser import FilenameParseError, parse_filename, sort_key
from ._heading_parser import extract_anchor, parse_headings
from ._sanity_gate import gate_directory
from ._table_parser import parse_tables

_SETEXT_UNDERLINE_RE = re.compile(r"^(=+|-+)\s*$")


def _release_from_version(version: str) -> str:
    """TSpec version letter encodes the 3GPP release: h=R17, i=R18, j=R19
    (letters run a=10 upward)."""
    letter = version[0].lower()
    if not letter.isalpha():
        return "R?"
    return f"R{ord(letter) - ord('a') + 10}"


def _parent_path_of(anchor: str) -> list[str]:
    """Dotted anchor -> ancestor chain including self.

    "6.3.4.2" -> ["6", "6.3", "6.3.4", "6.3.4.2"]; "A.2" -> ["A", "A.2"].
    """
    segments = anchor.split(".")
    return [".".join(segments[: i + 1]) for i in range(len(segments))]


class MarkdownAdapter(IngestionAdapter):
    """TSpec-LLM markdown -> ParsedSpec (Tier 1 data source).

    discover_inputs also fills `last_discovery_issues` (sanity-gate
    failures + readable .md files whose names don't parse) so callers —
    the ingest CLI in particular — can surface what was skipped instead
    of files vanishing silently.
    """

    def __init__(self) -> None:
        self.last_discovery_issues: list[str] = []

    def discover_inputs(self, root: Path) -> list[InputUnit]:
        self.last_discovery_issues = []
        valid, failed = gate_directory(root)
        self.last_discovery_issues.extend(
            f"sanity gate rejected {path.name}: {reason}"
            for path, reason in failed
        )

        groups: dict[tuple[str, str | None, str], list[Path]] = defaultdict(list)
        for path in valid:
            try:
                info = parse_filename(path.name)
            except FilenameParseError:
                # README-style strays are expected; record them so a
                # typo'd SPEC filename can't disappear without trace.
                self.last_discovery_issues.append(
                    f"unrecognised filename skipped: {path.name}"
                )
                continue
            groups[(info.spec_id, info.part, info.version)].append(path)

        units: list[InputUnit] = []
        # None-safe sort key: a partless and a parted entry under the SAME
        # spec_id would otherwise make the tuple sort compare None to str.
        for (spec_id, part, version), paths in sorted(
            groups.items(), key=lambda kv: (kv[0][0], kv[0][1] or "", kv[0][2]),
        ):
            ordered = sorted(paths, key=lambda p: sort_key(parse_filename(p.name)))
            units.append(InputUnit(
                spec_id=spec_id,
                part=part,
                version=version,
                release=_release_from_version(version),
                source_format=SOURCE_FORMAT_TSPEC_MD,
                source_paths=tuple(ordered),
            ))
        return units

    # ------------------------------------------------------------- parse

    def parse(self, unit: InputUnit) -> ParsedSpec:
        merged, seam_warnings = _merge_sources(unit.source_paths)
        stripped, anchor_map = strip_pandoc_anchors(merged)
        cleaned = clean_body(stripped)

        headings, heading_warnings = parse_headings(cleaned, anchor_map)
        sections, section_warnings = _build_sections(cleaned, headings)

        return ParsedSpec(
            unit=unit,
            sections=sections,
            full_text=cleaned,
            warnings=[*seam_warnings, *heading_warnings, *section_warnings],
        )

    def emit(
        self,
        parsed: ParsedSpec,
        session: Session,
        *,
        sections_filter: list[str] | None = None,
        force: bool = False,
    ) -> IngestStats:
        """Persist a ParsedSpec: Spec -> Sections (flushed before chunks so
        the FTS insert trigger can look up section_number) -> chunks.

        Idempotent on (Spec.name, Spec.version): an existing un-embedded
        spec is delete-and-reinserted (ORM cascade fires the FTS delete
        triggers). An EMBEDDED spec is refused unless force=True, which
        first deletes its Chroma vectors so no orphans remain.

        Unlike the PDF path's leaf-only chunking (page ranges overlap
        parent/child), md section bodies are DISJOINT by construction —
        every section with content gets chunks; is_indexed marks exactly
        the sections that produced chunks.

        Does NOT commit — the caller owns the transaction.
        """
        started = time.perf_counter()
        unit = parsed.unit
        spec_name = (
            f"{unit.spec_id}-{unit.part}" if unit.part else unit.spec_id
        )

        ordered = _with_line_bounds(parsed.sections, parsed.full_text)
        selected = _filter_selected(ordered, sections_filter)
        if not selected:
            raise ValueError(
                f"sections_filter {sections_filter!r} matched nothing"
            )

        spec = self._fresh_spec_row(session, unit, spec_name, force=force)

        by_anchor: dict[str, Section] = {}
        n_chunks = 0
        n_tables = 0
        headings_by_level: dict[int, int] = {}
        for parsed_sec, line_start, line_end in selected:
            anchor = parsed_sec.heading.anchor
            _, residual_title = extract_anchor(parsed_sec.heading.title)
            # Wire to the nearest ANCESTOR that actually exists as a section.
            # parent_path is the synthetic dotted chain (6.3.4.2 ->
            # ["6","6.3","6.3.4","6.3.4.2"]); an intermediate level (e.g.
            # "6.3") may have no heading, so [-2] alone can orphan the node.
            # Walk parents nearest-first and take the first one present.
            parent = next(
                (
                    by_anchor[a]
                    for a in reversed(parsed_sec.parent_path[:-1])
                    if a in by_anchor
                ),
                None,
            )
            row = Section(
                spec_id=spec.spec_id,
                parent_id=parent.section_id if parent else None,
                section_number=anchor,
                title=residual_title or parsed_sec.heading.title,
                level=len(parsed_sec.parent_path),
                page_start=line_start,
                page_end=line_end,
                is_indexed=False,
            )
            session.add(row)
            session.flush()  # section_id needed by chunks + FTS trigger
            by_anchor[anchor] = row

            level = parsed_sec.heading.level
            headings_by_level[level] = headings_by_level.get(level, 0) + 1

            specs = chunk_section_text(
                section_id=row.section_id,
                parent_section_id=row.parent_id,
                body_text=parsed_sec.body_text,
                tables=[
                    (t.rendered_text, t.caption_id) for t in parsed_sec.tables
                ],
                source_format=unit.source_format,
            )
            if specs:
                n_chunks += persist_chunks(session, specs)
                n_tables += sum(
                    1 for s in specs if s.chunk_type is ChunkType.TABLE
                )
                row.is_indexed = True

        return IngestStats(
            n_sections=len(selected),
            n_chunks=n_chunks,
            n_tables=n_tables,
            n_headings_by_level=headings_by_level,
            elapsed_sec=time.perf_counter() - started,
        )

    def _fresh_spec_row(
        self, session: Session, unit: InputUnit, spec_name: str, *, force: bool,
    ) -> Spec:
        """Idempotency: reuse the Spec row, wiping its sections/chunks.
        Refuse to wipe embedded chunks unless force (Chroma orphan guard)."""
        existing = session.execute(
            select(Spec).where(
                Spec.name == spec_name, Spec.version == unit.version,
            )
        ).scalar_one_or_none()
        if existing is None:
            spec = Spec(
                name=spec_name,
                version=unit.version,
                release=unit.release,
                source_file=unit.source_paths[0].name,
                source_format=unit.source_format,
            )
            session.add(spec)
            session.flush()
            return spec

        embedded_ids = session.execute(
            select(Chunk.vector_id)
            .join(Section, Chunk.section_id == Section.section_id)
            .where(
                Section.spec_id == existing.spec_id,
                Chunk.vector_id.is_not(None),
            )
        ).scalars().all()
        if embedded_ids:
            if not force:
                raise RuntimeError(
                    f"{spec_name} {unit.version} already has "
                    f"{len(embedded_ids)} embedded chunks; re-emitting would "
                    "orphan their Chroma vectors. Pass force=True to delete "
                    "them and re-ingest."
                )
            _delete_chroma_vectors(embedded_ids)

        for row in session.execute(
            select(Section).where(Section.spec_id == existing.spec_id)
        ).scalars():
            session.delete(row)  # cascades chunks; FTS delete trigger fires
        session.flush()
        return existing


def _merge_sources(source_paths: tuple[Path, ...]) -> tuple[str, list[str]]:
    """Read the unit's files in order into ONE text with stable line
    numbers: newlines normalised to \\n and every file terminated with a
    BLANK line — a setext heading at the top of the next file needs a
    blank line above it or _is_setext_underline rejects it as mid-block
    (the merge-seam failure mode the Step 4 plan flagged)."""
    parts: list[str] = []
    warnings: list[str] = []
    for path in source_paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
            warnings.append(f"{path.name}: undecodable bytes replaced")
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        parts.append(text.rstrip("\n") + "\n\n")
    return "".join(parts), warnings


def _body_start_line(heading: Heading, lines: list[str]) -> int:
    """First body line after a heading: skip the setext underline when the
    heading was setext-style (ATX headings occupy a single line)."""
    nxt = heading.line_no + 1
    if nxt < len(lines) and _SETEXT_UNDERLINE_RE.match(lines[nxt]):
        return nxt + 1
    return nxt


def _build_sections(
    cleaned: str, headings: list[Heading],
) -> tuple[list[ParsedSection], list[str]]:
    """Slice heading-bounded bodies; anchored headings open sections,
    anchorless ones stay inside the enclosing body. Tables are split out
    of each body into Section.tables."""
    lines = cleaned.split("\n")
    anchored = [h for h in headings if h.anchor]
    sections: list[ParsedSection] = []
    warnings: list[str] = []

    for idx, heading in enumerate(anchored):
        body_start = _body_start_line(heading, lines)
        body_end = (
            anchored[idx + 1].line_no if idx + 1 < len(anchored) else len(lines)
        )
        body_raw = "\n".join(lines[body_start:body_end])
        tables, body_text, table_warnings = parse_tables(body_raw)
        warnings.extend(
            f"§{heading.anchor}: {w}" for w in table_warnings
        )
        sections.append(ParsedSection(
            heading=heading,
            body_text=body_text.strip("\n"),
            tables=tables,
            parent_path=_parent_path_of(heading.anchor),
        ))
    return sections, warnings


def _with_line_bounds(
    sections: list[ParsedSection], full_text: str,
) -> list[tuple[ParsedSection, int, int]]:
    """Pair each parsed section with its (line_start, line_end) in the
    merged text — these fill Section.page_start/page_end for md sources
    (line numbers keep document ordering, which evaluate's subtree
    roll-up implicitly relies on)."""
    total_lines = full_text.count("\n")
    out: list[tuple[ParsedSection, int, int]] = []
    for idx, sec in enumerate(sections):
        start = sec.heading.line_no
        end = (
            sections[idx + 1].heading.line_no - 1
            if idx + 1 < len(sections) else total_lines
        )
        out.append((sec, start, max(start, end)))
    return out


def _filter_selected(
    bounded: list[tuple[ParsedSection, int, int]],
    sections_filter: list[str] | None,
) -> list[tuple[ParsedSection, int, int]]:
    """Dotted-prefix subtree filter: keep a section when its anchor IS one
    of the filters or descends from one ("6.2" keeps 6.2, 6.2.1, 6.2A...)."""
    if not sections_filter:
        return bounded
    wanted = [f.strip() for f in sections_filter if f.strip()]

    def _match(anchor: str) -> bool:
        return any(
            anchor == f or anchor.startswith(f + ".") for f in wanted
        )

    return [item for item in bounded if _match(item[0].heading.anchor or "")]


def _delete_chroma_vectors(vector_ids: list[str]) -> None:
    """force-re-emit path: remove the spec's embedded vectors so the
    shared Chroma collection holds no orphans pointing at deleted chunks."""
    import chromadb
    from chromadb.config import Settings as ChromaSettings

    from src.config import settings
    from src.ingestion.embedder import DEFAULT_COLLECTION

    client = chromadb.PersistentClient(
        path=str(settings.chroma_path),
        settings=ChromaSettings(anonymized_telemetry=False),
    )
    collection = client.get_collection(DEFAULT_COLLECTION)
    collection.delete(ids=list(vector_ids))
