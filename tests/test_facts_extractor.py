"""Unit tests for src/facts/extractor.py — pure rule-based fact extraction.

Fixtures mirror the REAL §6.2/6.3 md table renderings (ragged/pivoted), so
these assert the load-bearing extractions the test bank needs (q12 -40,
q21 n14/31) plus the honest gaps (formula cells, pdf, mis-sliced).
"""

from __future__ import annotations

from src.facts.extractor import ChunkView, extract_facts_from_chunk, fact_to_text
from src.models import Confidence, FactType

_MIN_PWR = (
    "Channel bandwidth | (MHz) | 5,10,15,20 | 25,30,35,40\n"
    "Minimum output power | (dBm) | -40 | -40+10log_10 (BW /20)\n"
    "NOTE: rounded down to one decimal point.\n"
)
_PWR_CLASS = (
    "NR band | Class 1 (dBm) | Tolerance (dB) | Class 2 (dBm) | Tolerance (dB)\n"
    "n1 | 26 | +2/-3 | 23 | ± 2\n"
    "n14 | 31 | +2/-3 | 23 | ± 2\n"
)
_MIS_SLICED = (
    "P_CMAX,f,c (dBm) T | olerance T(P_CMAX,f,c) (dB)\n"
    "23 < P_CMAX,c ≤ 33 | 2 | .0\n"
    "21 ≤ P_CMAX,c ≤ 23 | 2 | .0\n"
    "20 ≤ P_CMAX,c < 21 | 2 | .5\n"
)


def _cv(text: str, *, sf: str = "tspec_md", table_id: str | None = "6.x-1") -> ChunkView:
    return ChunkView(
        chunk_id=1, section_id=2, text=text, table_id=table_id, page=0,
        source_format=sf,
    )


def test_extract_min_power_value():
    facts = extract_facts_from_chunk(_cv(_MIN_PWR, table_id="6.3.1.3-1"))
    mins = [f for f in facts if f.fact_data["row_label"] == "Minimum output power"]
    # q12's -40 is extractable as a clean value...
    assert any(f.fact_data.get("value_num") == -40.0 for f in mins)
    # ...and v2 drops the formula cell entirely (clean-value filter), so every
    # emitted fact carries a real value_num and none is a formula.
    assert all(f.fact_data.get("value_num") is not None for f in facts)
    assert not any("log" in str(f.fact_data["value"]) for f in facts)
    assert all(f.fact_type is FactType.NUMERIC for f in facts)
    assert all(f.confidence is Confidence.CONFIRMED for f in facts)
    assert all(f.extracted_by == "rule/table_v1" for f in facts)
    assert all(f.table_id == "6.3.1.3-1" and f.source_chunk_id == 1 for f in facts)


def test_extract_power_class_n14():
    facts = extract_facts_from_chunk(_cv(_PWR_CLASS, table_id="6.2.1.3-1"))
    n14 = [f for f in facts if f.fact_data["row_label"] == "n14"]
    assert any(f.fact_data.get("value_num") == 31.0 for f in n14)


def test_pdf_yields_no_facts():
    # PyMuPDF-linearized table text -> no recoverable grid -> honest [].
    pdf_text = "Channel bandwidth \n(MHz) \n5 \n-40 \n4.515 \n10 \n-40 \n9.375 \n"
    assert extract_facts_from_chunk(_cv(pdf_text, sf="pdf_pymupdf")) == []


def test_mis_sliced_yields_no_facts():
    assert extract_facts_from_chunk(_cv(_MIS_SLICED, table_id="6.2.4.3-2")) == []


def test_fact_to_text():
    fd = {
        "table_id": "6.3.1.3-1", "row_label": "Minimum output power",
        "col_label": "5 MHz", "value": "-40", "value_num": -40.0, "unit": "dBm",
    }
    text = fact_to_text(fd)
    assert "Minimum output power" in text and "5 MHz" in text and "dBm" in text
    # v2: the raw value and table_id are NOT indexed (parameter-focused).
    assert "-40" not in text and "6.3.1.3-1" not in text
