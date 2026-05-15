"""IngestionAdapter — common interface for pluggable data sources.

Three-tier disclosure model (workspace-level `../CLAUDE.md` §5):
  - Tier 1 (personal): MarkdownAdapter ingests TSpec-LLM markdown corpus.
  - Tier 2/3 (commercial / shared): future PdfAdapter ingests 3GPP PDFs via
    PyMuPDF, *not* TSpec-LLM derivatives.

Both adapters emit into the same SQLAlchemy schema (see src/models.py); only
the data source layer differs. config.yaml's `data_source` switch (planned
for a follow-up task) chooses which adapter runs at ingest time.

DTOs are intentionally separate from the SQLAlchemy ORM models — adapters
produce these in-memory snapshots, then `emit` translates them into ORM
inserts. Keeping the parsing layer ORM-free makes it easy to unit-test
without a database.

STATUS (2026-05-15): scaffold only. The `source_format` schema blocker is
resolved; concrete `MarkdownAdapter.emit()` is still NOT implemented and
will be filled in by the Day 2 parser/persistence work.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

from sqlalchemy.orm import Session

from src.source_formats import VALID_SOURCE_FORMATS


@dataclass(frozen=True)
class InputUnit:
    """A source-agnostic 'one logical spec part' that an adapter discovered.

    For TSpec-LLM markdown, multiple files (cover + sN-sN ranges + sAnnexes)
    can map to one InputUnit. For PDFs, source_paths typically has one entry.

    Frozen because units are deduplicated via set / used as dict keys when
    grouping discoveries.
    """

    spec_id: str             # canonical "38.521" / "38.331" (no part)
    part: str | None         # "1" | "2" | "3" | "4"; None if spec has no parts
    version: str             # "i00" | "i20" | "h60"
    release: str             # "R18" / "R17"
    source_format: str       # one of SOURCE_FORMAT_* constants
    source_paths: tuple[Path, ...]
    extra: tuple[tuple[str, str], ...] = ()  # adapter-specific key-value pairs

    def __post_init__(self) -> None:
        if self.source_format not in VALID_SOURCE_FORMATS:
            raise ValueError(
                f"Invalid source_format {self.source_format!r}; "
                f"must be one of {sorted(VALID_SOURCE_FORMATS)}"
            )
        if not self.source_paths:
            raise ValueError("source_paths must be non-empty")


@dataclass(frozen=True)
class Heading:
    """A parsed heading with normalised level and extracted anchor.

    `level` is 1..8; the parser may emit H8 (annex top markers in TSpec-LLM)
    and downstream normalises to H1 before persisting.
    """

    level: int               # 1..8
    title: str               # cleaned title text (without {#anchor} attrs)
    anchor: str | None       # e.g. "6.3.1" / "A.2.2.1"; None if not parseable
    pandoc_id: str | None    # raw {#sec-6-3-1 .unnumbered} id, if any
    line_no: int             # 0-indexed line number in the merged source text


@dataclass(frozen=True)
class Table:
    """A parsed table rendered to plain text for indexing.

    `rendered_text` is the final searchable string after cell-internal
    multiline join + LaTeX rendering (see _table_parser). `raw_format`
    distinguishes "grid" (pandoc grid table) from "html" so downstream can
    track per-format error rates if needed.
    """

    rendered_text: str
    raw_format: str          # "grid" | "html"
    n_rows: int
    n_cols: int
    caption_id: str | None = None  # e.g. "Table 6.2.1.5-1" if detected


@dataclass
class Section:
    """One heading-bounded section of a parsed spec.

    `body_text` excludes the heading line itself and excludes table blocks
    (those are in `tables[]`). chunker._chunk_prose() consumes body_text;
    tables become their own chunks (chunk_type=TABLE).
    """

    heading: Heading
    body_text: str
    tables: list[Table] = field(default_factory=list)
    parent_path: list[str] = field(default_factory=list)  # ["6", "6.3", "6.3.1"]


@dataclass
class ParsedSpec:
    """Output of IngestionAdapter.parse() — full structured representation."""

    unit: InputUnit
    sections: list[Section] = field(default_factory=list)
    full_text: str = ""           # debugging / fallback
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class IngestStats:
    """Summary of what emit() wrote to the DB. Used by e2e test acceptance."""

    n_sections: int
    n_chunks: int
    n_tables: int
    n_headings_by_level: dict[int, int]
    elapsed_sec: float


class IngestionAdapter(ABC):
    """Pluggable ingestion source.

    Three lifecycle methods:
      discover_inputs : walk a directory, return logical InputUnits.
      parse           : turn one InputUnit into a ParsedSpec.
      emit            : write a ParsedSpec into the SQLAlchemy session.

    Implementations live in:
      MarkdownAdapter  -> md_parser.py  (Tier 1, TSpec-LLM)
      PdfAdapter       -> pdf_parser.py (Tier 2/3, future task)
    """

    @abstractmethod
    def discover_inputs(self, root: Path) -> list[InputUnit]:
        """Scan `root` for files this adapter can ingest. Return one
        InputUnit per logical spec part (which may span multiple source
        files in the markdown case)."""

    @abstractmethod
    def parse(self, unit: InputUnit) -> ParsedSpec:
        """Read the unit's source files and produce structured DTOs.

        Should be a pure function of `unit` + filesystem state; should not
        touch the DB. Non-fatal issues (level jumps, unknown markup) go
        into ParsedSpec.warnings rather than raising.
        """

    @abstractmethod
    def emit(self, parsed: ParsedSpec, session: Session) -> IngestStats:
        """Persist a ParsedSpec into the SQLAlchemy session.

        Must be idempotent on (Spec.name, Spec.version) — calling twice
        with the same input should leave the DB in the same final state.
        Implementations are expected to commit at end (or let the caller
        commit; document the choice clearly).

        NOTE (2026-05-15): `source_format` columns now exist, so concrete
        implementations can distinguish Tier 1 (tspec_md) from Tier 2
        (pdf_pymupdf) data for the retrieval A/B in Day 4 acceptance.
        """
