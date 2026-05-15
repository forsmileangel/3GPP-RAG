"""Canonical source format identifiers used across ingestion and retrieval."""

from __future__ import annotations

SOURCE_FORMAT_TSPEC_MD = "tspec_md"
SOURCE_FORMAT_PDF_PYMUPDF = "pdf_pymupdf"

VALID_SOURCE_FORMATS = frozenset({
    SOURCE_FORMAT_TSPEC_MD,
    SOURCE_FORMAT_PDF_PYMUPDF,
})


def validate_source_format(source_format: str) -> str:
    """Return `source_format` if valid; raise ValueError otherwise."""
    if source_format not in VALID_SOURCE_FORMATS:
        raise ValueError(
            f"Invalid source_format {source_format!r}; "
            f"must be one of {sorted(VALID_SOURCE_FORMATS)}"
        )
    return source_format
