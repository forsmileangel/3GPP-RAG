"""SQLAlchemy 2.0 schema for the 3GPP RAG project.

Seven tables, mirroring the original plan with refinements from Phase 0
and the v2.1 precision upgrade (2026-05-01):
  - specs            — one row per ingested spec (PDF / docx)
  - sections         — TOC tree per spec (parent_id self-reference, supports
                       3GPP's §X.YA / §X.YB / §X.YC siblings)
  - chunks           — text chunks with table-awareness (table_id, row_index,
                       parent_section_id); metadata.vector_id mirrors Chroma id
  - facts            — structured facts extracted from tables/paragraphs; the
                       fact layer that numeric questions hit before chunks
  - personal_notes   — user notes with confidence + extensible metadata JSON
  - cross_gen_mapping — generic from/to section relation (LTE↔NR, NR↔future)
  - share_profiles   — visibility filter sets (for future shared deployments)

Design notes:
  - SQLAlchemy 2.0 declarative style (Mapped[T] + mapped_column)
  - SQLite-friendly types (TEXT, INTEGER, REAL, JSON via TypeEngine)
  - personal_notes.metadata is JSON-typed so future fields don't require ALTER
  - All FKs are nullable=False where the relationship is required to make
    sense; deletes use ON DELETE CASCADE for sections/chunks (deleting a spec
    cleans its tree)
"""

from __future__ import annotations

import enum
from datetime import datetime, timezone

from sqlalchemy import (
    JSON,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.source_formats import SOURCE_FORMAT_PDF_PYMUPDF


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Visibility(enum.StrEnum):
    PRIVATE = "private"
    SHARED = "shared"
    PUBLIC = "public"


class Importance(enum.StrEnum):
    CORE = "core"
    SUPPLEMENTARY = "supplementary"
    APPENDIX = "appendix"
    SKIP = "skip"


class Confidence(enum.StrEnum):
    CONFIRMED = "confirmed"
    LIKELY = "likely"
    NEEDS_VALIDATION = "needs_validation"


# --------------------------------------------------------------------------
# specs
# --------------------------------------------------------------------------

class Spec(Base):
    __tablename__ = "specs"

    spec_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    release: Mapped[str | None] = mapped_column(String(16))
    generation: Mapped[str | None] = mapped_column(String(8))
    source_file: Mapped[str] = mapped_column(String, nullable=False)
    source_format: Mapped[str] = mapped_column(
        String(16),
        default=SOURCE_FORMAT_PDF_PYMUPDF,
        server_default=SOURCE_FORMAT_PDF_PYMUPDF,
        nullable=False,
    )
    page_count: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)

    sections: Mapped[list[Section]] = relationship(
        back_populates="spec",
        cascade="all, delete-orphan",
        order_by="Section.page_start",
    )

    __table_args__ = (
        UniqueConstraint("name", "version", name="uq_spec_name_version"),
    )


# --------------------------------------------------------------------------
# sections (TOC tree)
# --------------------------------------------------------------------------

class Section(Base):
    __tablename__ = "sections"

    section_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    spec_id: Mapped[int] = mapped_column(
        ForeignKey("specs.spec_id", ondelete="CASCADE"), nullable=False
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("sections.section_id", ondelete="CASCADE")
    )
    section_number: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    page_start: Mapped[int] = mapped_column(Integer, nullable=False)
    page_end: Mapped[int | None] = mapped_column(Integer)
    importance_tag: Mapped[Importance] = mapped_column(
        Enum(Importance, native_enum=False, length=16),
        default=Importance.SUPPLEMENTARY,
        nullable=False,
    )
    is_indexed: Mapped[bool] = mapped_column(default=False, nullable=False)

    spec: Mapped[Spec] = relationship(back_populates="sections")
    children: Mapped[list[Section]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan",
    )
    parent: Mapped[Section | None] = relationship(
        back_populates="children",
        remote_side="Section.section_id",
    )
    chunks: Mapped[list[Chunk]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan",
        order_by="Chunk.char_offset",
        foreign_keys="Chunk.section_id",
    )

    __table_args__ = (
        UniqueConstraint("spec_id", "section_number", name="uq_section_per_spec"),
    )


# --------------------------------------------------------------------------
# chunks
# --------------------------------------------------------------------------

class ChunkType(enum.StrEnum):
    PROSE = "prose"          # narrative paragraphs
    TABLE = "table"          # entire table as one chunk
    TABLE_ROW = "table_row"  # single row from a table
    HEADING = "heading"      # section/subsection heading
    LIST = "list"            # bullet/numbered list


class Chunk(Base):
    __tablename__ = "chunks"

    chunk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    section_id: Mapped[int] = mapped_column(
        ForeignKey("sections.section_id", ondelete="CASCADE"), nullable=False
    )
    # Denormalized parent for hybrid queries that filter by parent (e.g. all
    # chunks in §6.2.x). Populated by ingestion from sections.parent_id.
    parent_section_id: Mapped[int | None] = mapped_column(
        ForeignKey("sections.section_id", ondelete="SET NULL")
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    source_format: Mapped[str] = mapped_column(
        String(16),
        default=SOURCE_FORMAT_PDF_PYMUPDF,
        server_default=SOURCE_FORMAT_PDF_PYMUPDF,
        nullable=False,
    )
    page: Mapped[int] = mapped_column(Integer, nullable=False)
    char_offset: Mapped[int] = mapped_column(Integer, nullable=False)
    token_count: Mapped[int | None] = mapped_column(Integer)

    # Table-awareness (v2.1): for chunks that come from a 3GPP table, capture
    # the table identifier and row index so retrieval can keep tables intact
    # and the fact layer can cite "Table 6.2.1.5-1, row 3".
    chunk_type: Mapped[ChunkType] = mapped_column(
        Enum(ChunkType, native_enum=False, length=16),
        default=ChunkType.PROSE,
        nullable=False,
    )
    table_id: Mapped[str | None] = mapped_column(String(64))   # e.g. "Table 6.2.1.5-1"
    row_index: Mapped[int | None] = mapped_column(Integer)     # NULL for table=whole-table chunks

    # Mirrors Chroma collection ID (often == "c{chunk_id:06d}"); kept as a
    # nullable string so we can populate after Chroma write completes.
    vector_id: Mapped[str | None] = mapped_column(String(64), unique=True)
    embedding_model: Mapped[str | None] = mapped_column(String(128))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)

    section: Mapped[Section] = relationship(
        back_populates="chunks", foreign_keys=[section_id]
    )
    parent_section: Mapped[Section | None] = relationship(
        foreign_keys=[parent_section_id]
    )


# --------------------------------------------------------------------------
# facts (v2.1 — structured fact layer)
# --------------------------------------------------------------------------

class FactType(enum.StrEnum):
    NUMERIC = "numeric"          # "PC3 max power = 23 dBm ±2"
    PROCEDURE = "procedure"      # ordered test steps
    REFERENCE = "reference"      # cross-spec / cross-section pointer
    DEFINITION = "definition"    # term → meaning
    REQUIREMENT = "requirement"  # MUST/SHOULD-style normative text
    CATEGORICAL = "categorical"  # enum-like (e.g. modulation schemes for a band)


class Fact(Base):
    __tablename__ = "facts"

    fact_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    spec_id: Mapped[int] = mapped_column(
        ForeignKey("specs.spec_id", ondelete="CASCADE"), nullable=False
    )
    section_id: Mapped[int] = mapped_column(
        ForeignKey("sections.section_id", ondelete="CASCADE"), nullable=False
    )
    source_chunk_id: Mapped[int | None] = mapped_column(
        ForeignKey("chunks.chunk_id", ondelete="SET NULL")
    )
    fact_type: Mapped[FactType] = mapped_column(
        Enum(FactType, native_enum=False, length=16), nullable=False
    )

    # Free-form structured payload. Schema varies by fact_type; validated at
    # the app layer (e.g. NUMERIC requires {parameter, value, unit}).
    fact_data: Mapped[dict] = mapped_column(JSON, nullable=False)

    # Page + table_id duplicated from chunks for fast citation lookup.
    page: Mapped[int | None] = mapped_column(Integer)
    table_id: Mapped[str | None] = mapped_column(String(64))

    extracted_by: Mapped[str | None] = mapped_column(String(128))  # e.g. "claude-haiku-4.5/extract-v1"
    confidence: Mapped[Confidence] = mapped_column(
        Enum(Confidence, native_enum=False, length=24),
        default=Confidence.LIKELY,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)


# --------------------------------------------------------------------------
# personal_notes
# --------------------------------------------------------------------------

class PersonalNote(Base):
    __tablename__ = "personal_notes"

    note_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[Confidence] = mapped_column(
        Enum(Confidence, native_enum=False, length=24),
        default=Confidence.LIKELY,
        nullable=False,
    )
    visibility: Mapped[Visibility] = mapped_column(
        Enum(Visibility, native_enum=False, length=12),
        default=Visibility.PRIVATE,
        nullable=False,
    )

    related_section_id: Mapped[int | None] = mapped_column(
        ForeignKey("sections.section_id", ondelete="SET NULL")
    )

    # Extensible JSON column — tags, validated_in, expires_at, private_link,
    # etc. live here so we don't ALTER the table for every new field.
    extra: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    vector_id: Mapped[str | None] = mapped_column(String(64), unique=True)
    embedding_model: Mapped[str | None] = mapped_column(String(128))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=_utcnow, onupdate=_utcnow, nullable=False
    )

    related_section: Mapped[Section | None] = relationship()


# --------------------------------------------------------------------------
# cross_gen_mapping (generic — not LTE-specific)
# --------------------------------------------------------------------------

class CrossGenMapping(Base):
    __tablename__ = "cross_gen_mapping"

    mapping_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_section_id: Mapped[int] = mapped_column(
        ForeignKey("sections.section_id", ondelete="CASCADE"), nullable=False
    )
    to_section_id: Mapped[int] = mapped_column(
        ForeignKey("sections.section_id", ondelete="CASCADE"), nullable=False
    )
    relation_type: Mapped[str] = mapped_column(String(32), nullable=False)  # evolved_to / replaced_by / related_to / split_into
    topic: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    extra: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)


# --------------------------------------------------------------------------
# share_profiles
# --------------------------------------------------------------------------

class ShareProfile(Base):
    __tablename__ = "share_profiles"

    profile_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    # Stored as JSON arrays so SQLite stays fine. Validated at app layer.
    allowed_visibilities: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    allowed_section_ids: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)
