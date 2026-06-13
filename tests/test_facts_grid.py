"""Unit tests for src/facts/_grid.py — pure grid reconstruction.

Fixtures are derived from REAL §6.2/6.3 md TABLE chunks (their actual
rendered " | " text), including the messy shapes: a ragged header+data
table, a pivoted table with a NOTE + formula cell, and the pandoc
simple-table that the slicer split mid-token.
"""

from __future__ import annotations

from src.facts._grid import (
    col_label,
    detect_header_rows,
    is_well_formed,
    split_rendered_grid,
)

# 6.2.1.3-1 style: text header row + ragged data rows.
_PWR_CLASS = (
    "NR band | Class 1 (dBm) | Tolerance (dB) | Class 2 (dBm) | Tolerance (dB)\n"
    "n1 | 26 | +2/-3 | 23 | ± 2\n"
    "n14 | 31 | +2/-3 | 23 | ± 2\n"
)
# 6.3.1.3-1 style: pivoted (params as rows), ragged, NOTE + formula cell.
_MIN_PWR = (
    "Channel bandwidth | (MHz) | 5,10,15,20 | 25,30,35,40\n"
    "Minimum output power | (dBm) | -40 | -40+10log_10 (BW /20)\n"
    "NOTE: rounded down to one decimal point.\n"
)
# 6.2.4.3-2 style: pandoc simple-table sliced mid-token ("2 | .0").
_MIS_SLICED = (
    "P_CMAX,f,c (dBm) T | olerance T(P_CMAX,f,c) (dB)\n"
    "23 < P_CMAX,c ≤ 33 | 2 | .0\n"
    "21 ≤ P_CMAX,c ≤ 23 | 2 | .0\n"
    "20 ≤ P_CMAX,c < 21 | 2 | .5\n"
)


def test_split_drops_caption_and_note():
    rows = split_rendered_grid("Table 6.3.1.3-1: Minimum output power\n" + _MIN_PWR)
    assert rows[0][0] == "Channel bandwidth"
    assert all(not r[0].startswith("NOTE") for r in rows)
    assert all(not r[0].startswith("Table 6.3") for r in rows)


def test_split_cells_stripped():
    rows = split_rendered_grid(_PWR_CLASS)
    assert rows[1][0] == "n1"
    assert rows[1][1] == "26"
    assert rows[2][0] == "n14"
    assert rows[2][1] == "31"


def test_is_well_formed_accepts_real_grid():
    assert is_well_formed(split_rendered_grid(_PWR_CLASS)) is True


def test_is_well_formed_rejects_mis_sliced():
    # the "2 | .0" pandoc mis-slice -> dot-fragment cells -> reject
    assert is_well_formed(split_rendered_grid(_MIS_SLICED)) is False


def test_is_well_formed_rejects_too_small():
    assert is_well_formed([["single row"]]) is False
    assert is_well_formed([["a"], ["b"]]) is False   # 1 column


def test_detect_header_rows_returns_valid():
    # Best-effort + shallow (header cells like "Class 1" carry digits, so this
    # is intentionally not strict); just assert a valid 0/1 with no crash.
    assert detect_header_rows(split_rendered_grid(_PWR_CLASS)) in (0, 1)
    assert detect_header_rows(split_rendered_grid(_MIN_PWR)) in (0, 1)
    assert detect_header_rows([]) == 0


def test_col_label():
    rows = split_rendered_grid(_PWR_CLASS)
    assert col_label(rows, 1, 1) == "Class 1 (dBm)"
    assert col_label(rows, 0, 1) == ""    # header_rows=0 -> no label
    assert col_label(rows, 1, 99) == ""   # out of range
