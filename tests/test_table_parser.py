"""Unit tests for the three-format table parser (M2)."""

from __future__ import annotations

from pathlib import Path

from src.ingestion._table_parser import (
    find_table_blocks,
    parse_tables,
    render_latex,
)

FIXTURES = Path(__file__).parent / "fixtures" / "md"


def _load(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


# ------------------------------------------------------------------- grid

def test_grid_math_cell_reassembles_formula():
    tables, remaining, warnings = parse_tables(_load("table_grid_math.md"))
    assert len(tables) == 1
    t = tables[0]
    assert t.raw_format == "grid"
    assert t.caption_id == "5.2.1-1"
    # The $-cell fragments joined WITHOUT spaces, then pylatexenc rendered
    # the formula into one searchable line: "DataRate" must be whole again.
    assert "DataRate" in t.rendered_text
    assert "$" not in t.rendered_text          # rendered, not raw
    assert warnings == []
    # Non-math wrapped cell joined with spaces (mid-word break accepted).
    assert "CA_AX capability" in t.rendered_text.replace("\\_", "_")
    # Table block removed from prose, line count preserved.
    assert "+--" not in remaining
    assert remaining.count("\n") == _load("table_grid_math.md").count("\n")
    assert "Prose after the grid table." in remaining


def test_grid_header_and_note_rows_counted():
    tables, _, _ = parse_tables(_load("table_grid_math.md"))
    # header row + math row + NOTE row
    assert tables[0].n_rows == 3
    assert tables[0].n_cols == 2


def test_grid_escaped_pipes_stay_in_one_cell():
    # Real §6.3 pattern: |F_UL_Meas -- F_center| written as \| ... \|.
    text = (
        "+------------------------------+------+---------+\n"
        "| Condition                    | X    | Limit   |\n"
        "+==============================+======+=========+\n"
        "| \\|F~UL\\_Meas~ -- F\\_center\\| | X1   | 6 (p-p) |\n"
        "+------------------------------+------+---------+\n"
    )
    tables, _, warnings = parse_tables(text)
    assert len(tables) == 1
    assert tables[0].n_cols == 3                # not scattered to 5 columns
    assert "|F~UL\\_Meas~ -- F\\_center|" in tables[0].rendered_text
    assert warnings == []


# ------------------------------------------------------------------- html

def test_html_table_flat_walk_and_subsup():
    tables, remaining, warnings = parse_tables(_load("table_html_6_1_1.md"))
    assert len(tables) == 1
    t = tables[0]
    assert t.raw_format == "html"
    assert t.caption_id == "6.1-1"
    assert t.n_rows == 4                        # thead row + 3 body rows
    assert t.n_cols == 4
    # multi-<p> cell joined into one cell text
    assert "Edge_Full_Left (Note 2)" in t.rendered_text
    # <sub>/<sup> render to the cleaner's _x / ^x convention
    assert "L_CRB" in t.rendered_text
    assert "5@2^1" in t.rendered_text
    assert "<" not in t.rendered_text
    assert "Prose after the html table." in remaining
    assert warnings == []


# ----------------------------------------------------------------- simple

def test_simple_table_sliced_by_rule_spans():
    tables, remaining, _ = parse_tables(_load("table_simple_a_2_1_1.md"))
    assert len(tables) == 1
    t = tables[0]
    assert t.raw_format == "simple"
    assert t.caption_id == "A.2.1-1"
    assert t.n_rows == 4                        # header + 3 data rows
    assert t.n_cols == 2
    assert "15 kHz | 4, 9" in t.rendered_text
    assert "60 kHz | 16, 17, 18, 19, 36, 37, 38, 39" in t.rendered_text
    # The setext heading AFTER the table must survive in the remaining text
    # (the table parser must not eat the heading's underline).
    assert "A.2.2 Reference measurement channels for FDD\n----" in remaining


def test_simple_rule_is_not_treated_as_table_when_alone():
    # A setext H2 underline (single dash run) must not be detected.
    text = "6.1 General\n-----------\n\nprose\n"
    assert find_table_blocks(text) == []


# ------------------------------------------------------------ render_latex

def test_render_latex_happy_path():
    rendered, warnings = render_latex(r"rate is $\text{DataRate} = 10^{-6}$")
    assert warnings == []
    assert "$" not in rendered
    assert "DataRate" in rendered


def test_render_latex_degrades_without_pylatexenc(monkeypatch):
    import builtins

    real_import = builtins.__import__

    def _no_pylatexenc(name, *args, **kwargs):
        if name.startswith("pylatexenc"):
            raise ImportError("simulated absence")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _no_pylatexenc)
    rendered, warnings = render_latex(r"$\text{x}$ stays raw")
    assert rendered.startswith("$")             # raw literal kept
    assert len(warnings) == 1
    assert "latex render failed" in warnings[0]


# ------------------------------------------------------------- block scan

def test_find_table_blocks_mixed_document():
    text = "\n".join([
        _load("table_html_6_1_1.md"),
        _load("table_grid_math.md"),
        _load("table_simple_a_2_1_1.md"),
    ])
    formats = [b.raw_format for b in find_table_blocks(text)]
    assert formats == ["html", "grid", "simple"]
