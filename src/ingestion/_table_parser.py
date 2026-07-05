"""Table extraction for TSpec-LLM markdown — three coexisting formats.

Corpus reality (B0 spikes + direct reads): pandoc grid tables (`+--+`
borders, the majority), raw HTML `<table>` blocks (B0b measured 0
rowspan/colspan corpus-wide, so a flat row/cell walk suffices), and
pandoc *simple* tables (indented columnar rows under a `----- -----`
rule — e.g. Table A.2.1-1). The simple-table rule line shares characters
with a setext H2 underline; _heading_parser._is_setext_underline rejects
the table side, this module claims it.

Cell-join rule for wrapped grid cells (B0a): if a cell's fragments
contain `$` (LaTeX), concatenate WITHOUT spaces so a formula wrapped
across physical lines reassembles into one parseable string; otherwise
space-join. Pandoc also hard-wraps mid-word without hyphens ("co" /
"nfiguration") — with space-join those become "co nfiguration"; accepted
imperfection, not reconstructable reliably.

LaTeX rendering uses pylatexenc (B0a: 100% round-trip on 349 corpus
formulas) and degrades to the raw `$...$` literal plus a warning on any
error — never raises.

Known limitation (M2 review P1-b): pandoc *multiline* simple tables use a
SINGLE unbroken dash rule (29 such blocks corpus-wide, mostly 36-series).
Neither this module (needs 2+ runs) nor the heading parser (columnar
header rejected) claims them, so their rows fall through into section
prose — still searchable, just not structured as Table chunks.

caption_id stores the BARE table number ("6.1-1", "A.2.1-1") to match the
PDF flow's Chunk.table_id convention (DB parity is load-bearing for the
benchmark's table= column); _base.Table's docstring example shows the
"Table "-prefixed form, which predates this decision.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser

from ._artifact_cleaner import unescape_pandoc_underscore
from ._base import Table

_CAPTION_RE = re.compile(r"Table\s+([A-Z0-9][\w.]*-\d+[a-z]?)\s*:", re.IGNORECASE)
_UNESCAPED_PIPE_RE = re.compile(r"(?<!\\)\|")
_GRID_BORDER_RE = re.compile(r"^\s*\+[-=+]+\+\s*$")
_GRID_CONTENT_RE = re.compile(r"^\s*\|.*\|\s*$")
_SIMPLE_RULE_RE = re.compile(r"^(\s*)-+(\s+-+)+\s*$")
_LATEX_SPAN_RE = re.compile(r"\$([^$]+)\$")


@dataclass(frozen=True)
class TableBlock:
    """A located table region: [start, end) line span in the source text."""
    start: int
    end: int
    raw_format: str  # "grid" | "html" | "simple"


def render_latex(text: str) -> tuple[str, list[str]]:
    """Render $...$ spans to searchable text via pylatexenc; on failure keep
    the raw literal and record a warning. Never raises."""
    warnings: list[str] = []

    def _render(match: re.Match) -> str:
        formula = match.group(1)
        try:
            from pylatexenc.latex2text import LatexNodes2Text

            rendered = LatexNodes2Text().latex_to_text(formula)
            return " ".join(rendered.split())
        except Exception as exc:  # noqa: BLE001 — degrade, never fail ingest
            warnings.append(f"latex render failed ({exc}): {formula[:60]!r}")
            return match.group(0)

    return _LATEX_SPAN_RE.sub(_render, text), warnings


def _join_cell_fragments(fragments: list[str]) -> str:
    """Reassemble one logical cell from its wrapped physical lines."""
    parts = [f.strip() for f in fragments if f.strip()]
    if not parts:
        return ""
    if any("$" in p for p in parts):
        return "".join(parts)
    return " ".join(parts)


def _parse_grid(lines: list[str]) -> tuple[list[list[str]], list[str]]:
    """Grid table lines -> (rows of joined cells, warnings)."""
    rows: list[list[str]] = []
    pending: list[list[str]] | None = None
    warnings: list[str] = []

    for line in lines:
        if _GRID_BORDER_RE.match(line):
            if pending is not None:
                rows.append([_join_cell_fragments(c) for c in pending])
                pending = None
            continue
        if not _GRID_CONTENT_RE.match(line):
            warnings.append(f"grid: unexpected line inside table: {line[:50]!r}")
            continue
        # Split on UNESCAPED pipes only — pandoc writes a literal | inside a
        # cell as \| (real case: |F_UL_Meas -- F_center| formulas in §6.3),
        # and a naive split scatters such cells across phantom columns.
        cells = _UNESCAPED_PIPE_RE.split(line.strip())
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        cells = [c.replace("\\|", "|") for c in cells]
        if pending is None:
            pending = [[] for _ in cells]
        if len(cells) != len(pending):
            # ragged continuation — pad defensively
            while len(pending) < len(cells):
                pending.append([])
        for idx, cell in enumerate(cells):
            pending[idx].append(cell)
    if pending is not None:
        rows.append([_join_cell_fragments(c) for c in pending])
    return rows, warnings


class _HtmlTableWalker(HTMLParser):
    """Flat row/cell extraction — B0b measured zero rowspan/colspan in the
    corpus, so no spanning logic is needed. <sup>/<sub> render to the same
    ^x / _x convention the artifact cleaner uses."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "tr":
            self.rows.append([])
        elif tag in ("td", "th"):
            self._cell = []
        elif tag == "sup" and self._cell is not None:
            self._cell.append("^")
        elif tag == "sub" and self._cell is not None:
            self._cell.append("_")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("td", "th") and self._cell is not None:
            text = " ".join("".join(self._cell).split())
            # ^ / _ markers bind to the following token, not a space
            text = text.replace("^ ", "^").replace("_ ", "_")
            if self.rows:
                self.rows[-1].append(text)
            self._cell = None

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)


def _parse_html(block_text: str) -> list[list[str]]:
    walker = _HtmlTableWalker()
    walker.feed(block_text)
    return [row for row in walker.rows if row]


def _parse_simple(lines: list[str], rule_idx: int) -> list[list[str]]:
    """Pandoc simple table: header line above the rule, rows below until a
    blank line or closing rule. Columns sliced by the rule's dash runs."""
    rule = lines[rule_idx]
    spans = [(m.start(), m.end()) for m in re.finditer(r"-+", rule)]

    def _slice(line: str) -> list[str]:
        return [line[s:e + 1].strip() if s < len(line) else ""
                for s, e in spans[:-1]] + [line[spans[-1][0]:].strip()]

    rows = [_slice(lines[rule_idx - 1])]
    for line in lines[rule_idx + 1:]:
        if not line.strip() or _SIMPLE_RULE_RE.match(line):
            break
        rows.append(_slice(line))
    return rows


def _render_rows(rows: list[list[str]]) -> tuple[str, list[str]]:
    """Rows -> one searchable string (cells ' | '-joined, rows newline-
    joined), with LaTeX rendered."""
    text = "\n".join(" | ".join(c for c in row if c) for row in rows)
    return render_latex(text)


def _caption_above(lines: list[str], block_start: int) -> str | None:
    for line in reversed(lines[max(0, block_start - 4):block_start]):
        # pandoc escapes underscores in caption ids ("6.2.2\_1.3-1"); the
        # backslash would otherwise truncate the match.
        match = _CAPTION_RE.search(unescape_pandoc_underscore(line))
        if match:
            return match.group(1)
    return None


def find_table_blocks(text: str) -> list[TableBlock]:
    """Locate every table span, any of the three formats, in line space."""
    lines = text.split("\n")
    blocks: list[TableBlock] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if "<table" in line.lower():
            end = i
            while end < len(lines) and "</table>" not in lines[end].lower():
                end += 1
            blocks.append(TableBlock(i, min(end + 1, len(lines)), "html"))
            i = end + 1
            continue
        if _GRID_BORDER_RE.match(line):
            end = i
            while end < len(lines) and (
                _GRID_BORDER_RE.match(lines[end])
                or _GRID_CONTENT_RE.match(lines[end])
            ):
                end += 1
            blocks.append(TableBlock(i, end, "grid"))
            i = end
            continue
        if (
            _SIMPLE_RULE_RE.match(line)
            and i > 0
            and lines[i - 1].strip()
            and not _SIMPLE_RULE_RE.match(lines[i - 1])
        ):
            end = i + 1
            while end < len(lines) and lines[end].strip():
                if _SIMPLE_RULE_RE.match(lines[end]):
                    end += 1
                    break
                end += 1
            blocks.append(TableBlock(i - 1, end, "simple"))
            i = end
            continue
        i += 1
    return blocks


def parse_tables(text: str) -> tuple[list[Table], str, list[str]]:
    """Extract all tables; return (tables, text with table blocks removed,
    warnings). Removal blanks the table lines (line-count preserving)."""
    lines = text.split("\n")
    blocks = find_table_blocks(text)
    tables: list[Table] = []
    warnings: list[str] = []

    for block in blocks:
        block_lines = lines[block.start:block.end]
        if block.raw_format == "html":
            rows = _parse_html("\n".join(block_lines))
        elif block.raw_format == "grid":
            rows, grid_warnings = _parse_grid(block_lines)
            warnings.extend(grid_warnings)
        else:
            rows = _parse_simple(block_lines, rule_idx=1)
        if not rows:
            warnings.append(
                f"{block.raw_format} table at line {block.start} parsed empty"
            )
            continue
        rendered, latex_warnings = _render_rows(rows)
        warnings.extend(latex_warnings)
        tables.append(Table(
            rendered_text=rendered,
            raw_format=block.raw_format,
            n_rows=len(rows),
            n_cols=max(len(r) for r in rows),
            caption_id=_caption_above(lines, block.start),
        ))

    for block in blocks:
        for line_no in range(block.start, block.end):
            lines[line_no] = ""
    return tables, "\n".join(lines), warnings
