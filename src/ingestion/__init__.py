"""Ingestion pipeline: PDF -> sections -> chunks -> facts.

Public surface:
    extract_sections    — TOC bookmark walker (multi-section, sibling-aware)
    extract_pages_text  — page text + offset map (used by the chunker)
"""

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
    "SectionEntry",
    "SectionNotFoundError",
    "TOCEmptyError",
    "TOCEntry",
    "compute_section_tree",
    "extract_pages_text",
    "extract_sections",
    "parse_toc",
]
