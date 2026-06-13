"""Pure value/unit tokenization for the rule-based fact extractor (Step 6).

The load-bearing guard (R8): a number must be a STANDALONE token. "1.23" must
never yield 23; "n14"/"256QAM" yield no value (the digits are glued to
letters). Footnote superscripts rendered as `^N` by the artifact cleaner are
stripped before parsing. No DB, no I/O — trivially unit-testable.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Units we recognize, longest-first so "dBm"/"dBc" win over "dB" and "kHz"/
# "MHz" over "Hz" in the alternation.
_UNITS = ("dBm", "dBc", "dBi", "dB", "kHz", "MHz", "GHz", "Hz", "ms", "ppm")
_UNIT_RE = re.compile(
    r"(?<![A-Za-z])(" + "|".join(re.escape(u) for u in _UNITS) + r")(?![A-Za-z])"
)
_UNIT_CANON = {u.lower(): u for u in _UNITS}

# Footnote superscripts (cleaner renders them as ^N); strip before parsing so
# "31^6" -> "31", "+2/-3^3" -> "+2/-3".
_FOOTNOTE_RE = re.compile(r"\^\d+")

# A standalone signed decimal: not glued to a letter/digit/dot on either side.
# Unicode minus (U+2212) is normalized to ASCII first.
_VALUE_RE = re.compile(r"(?<![A-Za-z0-9.])(-?\d+(?:\.\d+)?)(?![0-9A-Za-z])")


@dataclass(frozen=True)
class ValueToken:
    raw: str                 # verbatim cell text (stripped)
    value_num: float | None  # parsed standalone numeric, or None
    unit: str | None         # canonical unit, or None


def normalize_minus(s: str) -> str:
    """Map the unicode minus U+2212 to ASCII '-' so float() can parse."""
    return s.replace("−", "-")


def _strip_footnotes(s: str) -> str:
    return _FOOTNOTE_RE.sub("", s)


def parse_value(text: str) -> float | None:
    """First STANDALONE signed decimal in `text`, else None. Strips `^N`
    footnotes first. Guards R8: '1.23' -> 1.23 (never 23); 'n14' -> None;
    '256QAM' -> None; '31^6' -> 31.0; '-40' -> -40.0; '± 2' -> 2.0."""
    cleaned = normalize_minus(_strip_footnotes(text))
    m = _VALUE_RE.search(cleaned)
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None


def find_unit(text: str) -> str | None:
    """First recognized unit token in `text` (canonical case), else None.
    Word-boundaried so 'dBm' is not found inside an identifier."""
    m = _UNIT_RE.search(text)
    return _UNIT_CANON[m.group(1).lower()] if m else None


_FORMULA_HINTS = ("=", "log")


def _looks_like_formula(s: str) -> bool:
    """A cell like 'MBW=REF_SCS*(...)' or '-40+10log_10(BW/20)' is a formula,
    not a measured value. Such cells get value_num=None (R9): the verbatim text
    is still stored + searchable, but it cannot be value-matched. md tables
    keep these as formulae where the PDF resolves them to a number — a key
    input to the rule-based-vs-LLM measurement."""
    low = s.lower()
    return any(h in low for h in _FORMULA_HINTS)


_ALPHA_WORD_RE = re.compile(r"[A-Za-z]{2,}")
_UNIT_LOWER = frozenset(u.lower() for u in _UNITS)


def is_clean_value(cell: str) -> bool:
    """True if `cell` is a bare measured value (sign / number / unit /
    tolerance / footnote) — NOT prose. The v2 extraction filter: rejects the
    NOTE / header / formula / sentence cells that flooded the v1 index (45k
    facts). Requires a parseable number AND no non-unit alphabetic word
    (>=2 letters). Examples kept: '-40', '± 2', '9.0 dB', '+2/-3', '31^6'.
    Rejected: 'Modulation (NOTE 2)', 'Class 1 (dBm)', '-40+10log_10(BW/20)'."""
    stripped = _strip_footnotes(cell)
    if any(w.lower() not in _UNIT_LOWER for w in _ALPHA_WORD_RE.findall(stripped)):
        return False
    return parse_value(cell) is not None


def extract_value_unit(cell: str, *, header_unit: str | None = None) -> ValueToken:
    """Tokenize one table cell into (verbatim, value_num, unit). The unit falls
    back to `header_unit` (the column's unit) when the cell carries none — 3GPP
    tables routinely put the unit in the header and bare numbers in the cells.
    Formula cells yield value_num=None."""
    raw = cell.strip()
    value_num = None if _looks_like_formula(raw) else parse_value(raw)
    return ValueToken(
        raw=raw,
        value_num=value_num,
        unit=find_unit(raw) or header_unit,
    )
