"""TSpec-LLM filename parser — extract spec / part / version / scope.

TSpec-LLM organises spec files under `<release>/<series>_series/` with
filenames following the convention:

    <num>(-<part>)?-<version>(_<scope>)?.md

Examples (from R18 download):
    36521-1-i20_cover.md           — cover page
    36521-1-i20_s06a-s06b4.md      — section range
    36521-1-i20_sAnnexA-sAnnexE.md — annex range
    38521-1-i00_sAnnexes.md        — combined annexes (38521 convention)
    36521-2-i20.md                 — single-file part (no scope)
    38331-h60.md                   — no parts, no scope (NR RRC)

`spec_id` is reconstructed from `<num>` by inserting a dot after the 2-digit
series prefix (36521 → "36.521", 38521 → "38.521"). The result is the
canonical 3GPP spec name without the part number — `part` lives in its own
field.

The `sort_key` function returns a tuple suitable for `sorted(..., key=...)`
that orders files within a part as: cover → section ranges → annex ranges →
combined annexes. The ordering is *not* a simple lex-sort on raw filenames,
to avoid relying on the `-` (0x2D) < `0` (0x30) ASCII edge case (B0 spike
reviewer flagged this as risk #8 in the eval report).
"""

from __future__ import annotations

import enum
import re
from dataclasses import dataclass


class ScopeKind(enum.StrEnum):
    NONE = "none"                # whole-part single file (e.g. 36521-2-i20.md)
    COVER = "cover"              # cover page
    SECTION_RANGE = "section_range"    # "s06-s0602C" (start may equal end)
    SINGLE_SECTION = "single_section"  # "s0700"
    ANNEX_RANGE = "annex_range"        # "sAnnexA-sAnnexE" or single "sAnnexA"
    ANNEXES_ALL = "annexes_all"        # "sAnnexes" (38521 convention)


class FilenameParseError(ValueError):
    """Filename did not match the TSpec-LLM convention."""


@dataclass(frozen=True)
class FileNameInfo:
    """Parsed components of a TSpec-LLM markdown filename."""

    spec_id: str             # canonical "38.521" / "38.331" (no part)
    part: str | None         # "1" | "2" | None
    version: str             # "i00" | "i20" | "h60"
    scope: ScopeKind
    scope_start: str | None  # e.g. "s06" / "sAnnexA"; None for NONE/COVER/ANNEXES_ALL
    scope_end: str | None    # e.g. "s0602C" / "sAnnexE"; None unless RANGE
    raw: str                 # original filename


_FILENAME_RE = re.compile(
    r"^(?P<num>\d{4,5})"
    r"(?:-(?P<part>\d+))?"
    r"-(?P<version>[a-z]\d+)"
    r"(?:_(?P<scope>.+))?"
    r"\.md$"
)


def _split_scope(scope_raw: str) -> tuple[ScopeKind, str | None, str | None]:
    """Return (kind, start, end) for the scope suffix string."""
    if scope_raw == "cover":
        return ScopeKind.COVER, None, None
    if scope_raw == "sAnnexes":
        return ScopeKind.ANNEXES_ALL, None, None
    # Range: "s06-s0602C" or "sAnnexA-sAnnexE"
    if "-" in scope_raw:
        start, end = scope_raw.split("-", 1)
        kind = (
            ScopeKind.ANNEX_RANGE
            if start.lower().startswith("sannex")
            else ScopeKind.SECTION_RANGE
        )
        return kind, start, end
    # Single (no range)
    if scope_raw.lower().startswith("sannex"):
        # e.g. "sAnnexA" alone — treat as single-annex range
        return ScopeKind.ANNEX_RANGE, scope_raw, scope_raw
    # "sNN" / "sNNNN" single section (e.g. "s0605" / "s0700")
    return ScopeKind.SINGLE_SECTION, scope_raw, scope_raw


def _format_spec_id(num: str) -> str:
    """Insert dot after the 2-digit series prefix (36521 → '36.521').

    3GPP TS series numbers are 4-5 digits: first two digits are the series
    (36 / 37 / 38 / ...), remaining digits are the spec number.
    """
    if len(num) < 4:
        raise FilenameParseError(f"spec number too short: {num!r}")
    return f"{num[:2]}.{num[2:]}"


def parse_filename(name: str) -> FileNameInfo:
    """Parse a TSpec-LLM markdown filename into its components.

    Raises FilenameParseError on filenames that don't match the expected
    pattern.
    """
    m = _FILENAME_RE.match(name)
    if not m:
        raise FilenameParseError(f"unrecognised TSpec-LLM filename: {name!r}")
    scope_raw = m.group("scope")
    if scope_raw is None:
        kind, scope_start, scope_end = ScopeKind.NONE, None, None
    else:
        kind, scope_start, scope_end = _split_scope(scope_raw)
    return FileNameInfo(
        spec_id=_format_spec_id(m.group("num")),
        part=m.group("part"),
        version=m.group("version"),
        scope=kind,
        scope_start=scope_start,
        scope_end=scope_end,
        raw=name,
    )


# Priority for sort_key — lower comes first within a (spec, part, version)
# group. Section ranges and single sections share priority 2 (they sort
# against each other by scope_start string).
_SCOPE_PRIORITY: dict[ScopeKind, int] = {
    ScopeKind.NONE: 0,
    ScopeKind.COVER: 1,
    ScopeKind.SECTION_RANGE: 2,
    ScopeKind.SINGLE_SECTION: 2,
    ScopeKind.ANNEX_RANGE: 3,
    ScopeKind.ANNEXES_ALL: 4,
}


def sort_key(info: FileNameInfo) -> tuple[int, str]:
    """Stable sort key for ordering files within a (spec, part, version).

    Output ordering: cover → sections (lex on scope_start) → annexes →
    annexes_all. Avoids relying on the `-` (0x2D) < `0` (0x30) ASCII edge
    case that a pure `sorted(filenames)` does.
    """
    return (_SCOPE_PRIORITY[info.scope], info.scope_start or "")
