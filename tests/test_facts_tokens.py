"""Unit tests for src/facts/_tokens.py — pure value/unit tokenization."""

from __future__ import annotations

from src.facts._tokens import (
    extract_value_unit,
    find_unit,
    is_clean_value,
    normalize_minus,
    parse_value,
)


def test_parse_value_basic():
    assert parse_value("-40") == -40.0
    assert parse_value("9.375") == 9.375
    assert parse_value("23") == 23.0


def test_parse_value_strips_footnote():
    assert parse_value("31^6") == 31.0
    assert parse_value("26^3") == 26.0


def test_parse_value_r8_no_substring():
    # The load-bearing guard: a value must be a STANDALONE token.
    assert parse_value("1.23") == 1.23          # never 23
    assert parse_value("n14") is None           # digit glued to a letter
    assert parse_value("256QAM") is None         # digits glued to letters
    assert parse_value("REF_SCS") is None


def test_parse_value_unicode_minus():
    assert parse_value("−40") == -40.0           # U+2212


def test_parse_value_tolerance_magnitude():
    assert parse_value("± 2") == 2.0             # space-separated -> standalone


def test_parse_value_empty_and_unit_only():
    assert parse_value("") is None
    assert parse_value("dBm") is None


def test_find_unit_longest_match():
    assert find_unit("(dBm)") == "dBm"
    assert find_unit("Tolerance (dB)") == "dB"
    assert find_unit("(MHz)") == "MHz"
    assert find_unit("(kHz)") == "kHz"
    assert find_unit("23 dBm") == "dBm"          # dBm wins over dB
    assert find_unit("no unit here") is None


def test_extract_value_unit_header_fallback():
    t = extract_value_unit("-40", header_unit="dBm")
    assert t.value_num == -40.0 and t.unit == "dBm"
    t2 = extract_value_unit("23 dBm", header_unit="dB")   # inline unit wins
    assert t2.unit == "dBm"


def test_extract_value_unit_formula_nulls_value():
    # R9: md keeps formulae where the PDF resolves a number; not value-matchable.
    t = extract_value_unit("MBW=REF_SCS*(12*N_RB+1)/1000", header_unit="MHz")
    assert t.value_num is None and t.raw.startswith("MBW=")
    t2 = extract_value_unit("-40+10log_10 (BW_Channel /20)", header_unit="dBm")
    assert t2.value_num is None


def test_normalize_minus():
    assert normalize_minus("−40") == "-40"


def test_is_clean_value():
    # kept: bare measured values (sign / number / unit / tolerance / footnote)
    assert is_clean_value("-40") is True
    assert is_clean_value("± 2") is True
    assert is_clean_value("9.0 dB") is True        # dB is a unit, not prose
    assert is_clean_value("+2/-3") is True
    assert is_clean_value("31^6") is True          # footnote stripped
    # rejected: prose / header / note / formula / no-number cells
    assert is_clean_value("Modulation (NOTE 2)") is False
    assert is_clean_value("Class 1 (dBm)") is False
    assert is_clean_value("-40+10log_10 (BW /20)") is False
    assert is_clean_value("(dBm)") is False        # no number
    assert is_clean_value("") is False
