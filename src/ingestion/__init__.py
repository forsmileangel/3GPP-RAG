"""Ingestion pipeline: PDF -> sections -> chunks -> facts.

Public surface:
    extract_sections    — TOC bookmark walker (multi-section, sibling-aware)
    extract_pages_text  — page text + offset map (used by the chunker)
    chunk_section       — produce ChunkSpec list for one section
    chunk_spec_pdf      — chunk every section in a list and persist
    persist_chunks      — insert ChunkSpec rows (FTS5 syncs via triggers)
"""

from .chunker import (
    ChunkSpec,
    chunk_section,
    chunk_spec_pdf,
    persist_chunks,
)
from .embedder import EmbedResult, embed_pending_chunks
from .toc_extractor import (
    SectionEntry,
    SectionNotFoundError,
    TOCEmptyError,
    TOCEntry,
    compute_section_tree,
    extract_pages_text,
    extract_sections,
    parse_toc,
)

__all__ = [
    "ChunkSpec",
    "EmbedResult",
    "SectionEntry",
    "SectionNotFoundError",
    "TOCEmptyError",
    "TOCEntry",
    "chunk_section",
    "chunk_spec_pdf",
    "compute_section_tree",
    "embed_pending_chunks",
    "extract_pages_text",
    "extract_sections",
    "parse_toc",
    "persist_chunks",
]
