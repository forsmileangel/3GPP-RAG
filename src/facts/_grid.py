"""Pure grid reconstruction from a rendered TABLE chunk's text (Step 6).

md TABLE chunks render as cells `" | "`-joined, rows `"\\n"`-joined
(_table_parser._render_rows). Real §6.2/6.3 tables are MESSY: ragged rows
(empty cells elided), pivoted layouts (parameters as rows), footnote markers,
and pandoc simple-tables that the fixed-offset slicer split mid-token
("2 | .0", "T | olerance"). So this module is deliberately conservative:
recover a ragged grid, REJECT the clearly mis-sliced ones (is_well_formed),
and leave the row-centric fact decision to the extractor. No DB, no I/O.
"""

from __future__ import annotations

import re
from collections import Counter

from ._tokens import parse_value

_CELL_SEP = " | "
# Lines that are not data rows: the "Table 6.x-y: caption" prefix and NOTE/NOTEn.
_CAPTION_RE = re.compile(r"^\s*Table\s+[0-9A-Za-z.\-]+\s*:", re.IGNORECASE)
_NOTE_RE = re.compile(r"^\s*NOTE\b", re.IGNORECASE)
# Mis-slice signature: a cell that starts with a dot then a digit (".0", ".5"),
# which a correctly-split numeric cell never produces.
_DOT_FRAGMENT_RE = re.compile(r"^\.\d")


def split_rendered_grid(text: str) -> list[list[str]]:
    """Split a rendered TABLE chunk back into a (ragged) grid of stripped
    cells. Drops the caption prefix line and NOTE lines (not data rows)."""
    rows: list[list[str]] = []
    for line in text.split("\n"):
        if not line.strip():
            continue
        if _CAPTION_RE.match(line) or _NOTE_RE.match(line):
            continue
        rows.append([c.strip() for c in line.split(_CELL_SEP)])
    return rows


def is_well_formed(rows: list[list[str]]) -> bool:
    """Reject grids that are too small or clearly mis-sliced.

    Heuristics (conservative — prefer NO facts over WRONG facts):
      - need >=2 rows and a modal column count >=2
      - reject if >=2 cells start with a dot+digit (the "2 | .0" pandoc
        simple-table mis-slice; a clean numeric cell never starts with ".")
    """
    if len(rows) < 2:
        return False
    widths = Counter(len(r) for r in rows)
    modal_width, _ = widths.most_common(1)[0]
    if modal_width < 2:
        return False
    dot_fragments = sum(
        1 for r in rows for c in r if _DOT_FRAGMENT_RE.match(c)
    )
    return dot_fragments < 2


def detect_header_rows(rows: list[list[str]]) -> int:
    """1 if the first row looks like a header (its cells beyond column 0 are
    majority non-numeric), else 0. Deliberately shallow — the extractor is
    row-centric (row label = column 0), so a missing header only costs the
    optional col_label, never the value."""
    if not rows:
        return 0
    head = rows[0][1:]
    if not head:
        return 0
    non_numeric = sum(1 for c in head if parse_value(c) is None)
    return 1 if non_numeric > len(head) / 2 else 0


def col_label(rows: list[list[str]], header_rows: int, col: int) -> str:
    """Best-effort column label from the header row, or "" when absent."""
    if header_rows < 1 or not rows:
        return ""
    header = rows[0]
    return header[col] if 0 <= col < len(header) else ""
