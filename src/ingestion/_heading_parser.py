"""Heading detection + section-number anchor extraction for TSpec-LLM md.

Corpus-measured properties (research/scans/2026-05-05-tspec-llm-eval.md +
direct corpus reads):
  - setext (`===` / `---` underlines) carries the TOP sections in
    conformance specs (`6` is setext H1, `6.1` setext H2); ATX `#`-style
    carries deeper levels. Both must be handled.
  - `######## Annex A ...` H8 markers open annex parts (85 across the 50
    files). Heading.level stays raw 1..8 here; tree depth downstream comes
    from the anchor's dotted form, which is authoritative.
  - pandoc {#...} ids cover only a fraction of headings (199 in a file
    with thousands), so the section number is extracted from the TITLE's
    leading token. extract_anchor is the single source of truth for
    section_number strings and must produce forms byte-identical to the
    PDF flow's ("6.3.4.2", "6.2A", "A.2.2.1").
  - Level jumps (H2 -> H4, 0.88% of transitions) are warnings, never
    errors.

The headline ambiguity: a `----` line is EITHER a setext H2 underline OR a
pandoc simple-table rule (`------ ------`). _is_setext_underline encodes
the disambiguation; the table side is handled by _table_parser (M2).
"""

from __future__ import annotations

import re

from ._artifact_cleaner import unescape_pandoc_underscore
from ._base import Heading

# Leading-token anchor forms, tried in order:
#   numeric dotted (+optional capital suffix per segment): 6 / 6.1 /
#     6.3.1A / 6.2A / 6.3.1.1.1
#   inserted-clause lowercase variant: at most ONE trailing lowercase letter
#     per segment ("6.4.2.1a", "6.5A.1.0.1a" — 3GPP's inserted-clause
#     numbering; 13 such headings corpus-wide). Bounded to one letter so a
#     hypothetical glued word ("6.2General") cannot be absorbed — the regex
#     then backtracks exactly like the pre-fix form.
#   band-combination: one optional underscore-joined index inside the chain
#     ("6.2D.1\_1.1" / "7.7D\_1.1" — pandoc escapes the literal '_'; the
#     regex accepts both the escaped and plain form, extract_anchor
#     normalises the captured group). NOTE: unescape-first would NOT work —
#     on the plain form the old regex's \b backtracks to "6.2D".
#   annex letter dotted: A.1 / A.2.2.1
#   annex top marker: "Annex A (normative): ..." -> "A"
_NUMERIC_ANCHOR_RE = re.compile(
    r"^(\d+[A-Z]*[a-z]?(?:\.\d+[A-Z]*[a-z]?)*"
    r"(?:\\?_\d+)?(?:\.\d+[A-Z]*[a-z]?)*)\b"
)
_ANNEX_DOTTED_RE = re.compile(r"^([A-Z](?:\.\d+[A-Z]*)+)\b")
_ANNEX_TOP_RE = re.compile(r"^Annex\s+([A-Z])\b", re.IGNORECASE)

_ATX_RE = re.compile(r"^(#{1,8})\s+(.*\S)\s*$")
_SETEXT_H1_RE = re.compile(r"^=+\s*$")
_SETEXT_H2_RE = re.compile(r"^-+\s*$")
# A dash line with 2+ runs ("---- ----") is a simple-table rule.
_MULTI_RUN_RE = re.compile(r"^[=\-]+(\s+[=\-]+)+\s*$")
# Column layout in the line above ("SCS  Active Uplink slots") means the
# underline below it belongs to a table, not a heading.
_COLUMN_GAP_RE = re.compile(r"\S\s{2,}\S")


def extract_anchor(title: str) -> tuple[str | None, str]:
    """Parse the section number out of a heading title.

    Returns (anchor, residual_title). anchor is None when the title has no
    recognisable leading number ("General", "Scope")."""
    title = title.strip()
    match = _NUMERIC_ANCHOR_RE.match(title) or _ANNEX_DOTTED_RE.match(title)
    if match:
        # Normalise only the captured anchor ("\_" -> "_"); the residual is
        # sliced from the ORIGINAL title so its bytes never change. Annex
        # anchors cannot contain "_", so the unescape is a no-op there.
        anchor = unescape_pandoc_underscore(match.group(1))
        return anchor, title[match.end():].strip()
    match = _ANNEX_TOP_RE.match(title)
    if match:
        return match.group(1).upper(), title
    return None, title


def _is_setext_underline(underline: str, prev_line: str | None,
                         prev_prev_line: str | None) -> bool:
    """True when `underline` really closes a setext heading.

    Rejects: multi-run rules ("---- ----" = simple-table separator), an
    empty/absent previous line, a previous line that is itself column-
    formatted (table header), or a previous line that looks like another
    underline."""
    if _MULTI_RUN_RE.match(underline):
        return False
    if not prev_line or not prev_line.strip():
        return False
    if _SETEXT_H1_RE.match(prev_line) or _SETEXT_H2_RE.match(prev_line):
        return False
    if _COLUMN_GAP_RE.search(prev_line):
        return False
    # pandoc setext needs the heading line to start a block: line above it
    # blank or beginning-of-text. Known limit: two setext headings with NO
    # blank line between them would drop the second — pandoc output always
    # emits that blank line, so this is unreachable on TSpec-LLM input.
    if prev_prev_line is not None and prev_prev_line.strip():
        return False
    return True


def parse_headings(
    merged_text: str, anchor_map: dict[int, str] | None = None,
) -> tuple[list[Heading], list[str]]:
    """Walk the merged source text and emit Heading DTOs (raw level 1..8)
    plus non-fatal warnings (level jumps, unparseable anchors)."""
    anchor_map = anchor_map or {}
    lines = merged_text.split("\n")
    headings: list[Heading] = []
    warnings: list[str] = []
    consumed_underline: set[int] = set()
    seen_anchors: dict[str, int] = {}  # anchor -> first line_no

    for line_no, line in enumerate(lines):
        if line_no in consumed_underline:
            continue

        level: int | None = None
        raw_title: str | None = None

        atx = _ATX_RE.match(line)
        if atx:
            level = len(atx.group(1))
            raw_title = atx.group(2)
        else:
            nxt = lines[line_no + 1] if line_no + 1 < len(lines) else None
            if nxt is not None and (
                _SETEXT_H1_RE.match(nxt) or _SETEXT_H2_RE.match(nxt)
            ):
                prev = lines[line_no - 1] if line_no > 0 else None
                if line.strip() and _is_setext_underline(
                    nxt, line, prev,
                ):
                    level = 1 if _SETEXT_H1_RE.match(nxt) else 2
                    raw_title = line.strip()
                    consumed_underline.add(line_no + 1)

        if level is None or raw_title is None:
            continue

        anchor, _residual = extract_anchor(raw_title)
        if anchor is None:
            warnings.append(
                f"line {line_no}: heading without parseable anchor: "
                f"{raw_title[:60]!r}"
            )
        elif anchor in seen_anchors:
            # Two headings resolving to one section number: downstream the
            # section tree's by_anchor lookup silently takes the last writer,
            # so surface the ambiguity here (warning-only, never fatal).
            warnings.append(
                f"line {line_no}: duplicate anchor {anchor!r} "
                f"(first seen at line {seen_anchors[anchor]})"
            )
        else:
            seen_anchors[anchor] = line_no
        if headings and level - headings[-1].level > 1:
            warnings.append(
                f"line {line_no}: level jump "
                f"H{headings[-1].level} -> H{level}: {raw_title[:60]!r}"
            )

        headings.append(Heading(
            level=level,
            title=raw_title,
            anchor=anchor,
            pandoc_id=anchor_map.get(line_no),
            line_no=line_no,
        ))

    return headings, warnings
