"""Unit tests for the ingest sanity gate.

Covers all 7 reason codes plus the gate_directory batch helper and the
fail_fast SanityGateError path.
"""

from __future__ import annotations

import pytest

from src.ingestion._sanity_gate import (
    SanityGateError,
    gate_directory,
    is_valid_md,
)


# Realistic-ish content that passes the >= 100 byte threshold.
_PADDING = "x" * 200


# --------------------------------------------------------------------------
# Failure cases — each reason code
# --------------------------------------------------------------------------

def test_empty_file(tmp_path):
    p = tmp_path / "empty.md"
    p.write_text("")
    ok, reason = is_valid_md(p)
    assert not ok
    assert reason == "empty"


def test_nonexistent_file(tmp_path):
    p = tmp_path / "ghost.md"
    ok, reason = is_valid_md(p)
    assert not ok
    assert reason == "empty"


def test_too_small(tmp_path):
    p = tmp_path / "tiny.md"
    p.write_text("# tiny\n")  # ~7 bytes, way under 100
    ok, reason = is_valid_md(p)
    assert not ok
    assert reason == "too_small"


def test_encoding_error(tmp_path):
    p = tmp_path / "bad.md"
    p.write_bytes(b"\xff\xfe\xfd" * 50)  # invalid utf-8, > 100 bytes
    ok, reason = is_valid_md(p)
    assert not ok
    assert reason == "encoding_error"


def test_no_boilerplate_no_heading(tmp_path):
    """Plain text with neither 3GPP boilerplate nor markdown headings."""
    p = tmp_path / "lorem.md"
    p.write_text("lorem ipsum dolor sit amet " * 20)  # ~520 bytes
    ok, reason = is_valid_md(p)
    assert not ok
    assert reason == "FAIL_no_boilerplate_no_heading"


# --------------------------------------------------------------------------
# Pass cases — each ok reason code
# --------------------------------------------------------------------------

def test_ok_full(tmp_path):
    """Both boilerplate (3GPP TS …) AND a heading."""
    content = (
        "3GPP TS 38.521-1 V18.0.0 (2023-09)\n\n"
        "Technical Specification\n\n"
        + _PADDING + "\n\n"
        + "# 1 Scope\n\nSome content.\n"
    )
    p = tmp_path / "spec.md"
    p.write_text(content)
    ok, reason = is_valid_md(p)
    assert ok
    assert reason == "ok_full"


def test_ok_heading_no_boilerplate(tmp_path):
    """Annex split file: ATX heading present, no TS boilerplate."""
    content = (
        "######## Annex A (normative): Measurement channels\n\n"
        + _PADDING + "\n\n"
        + "### A.2.2.1 DFT-s-OFDM Pi/2-BPSK\n\nbody.\n"
    )
    p = tmp_path / "annex.md"
    p.write_text(content)
    ok, reason = is_valid_md(p)
    assert ok
    assert reason == "ok_heading_no_boilerplate"


def test_ok_setext_heading(tmp_path):
    """Setext-style (=== underline) heading should also be detected."""
    content = (
        "Contents\n"
        "========\n\n"
        + _PADDING + "\n"
    )
    p = tmp_path / "setext.md"
    p.write_text(content)
    ok, reason = is_valid_md(p)
    assert ok
    # No 3GPP TS prefix → ok_heading_no_boilerplate
    assert reason == "ok_heading_no_boilerplate"


# --------------------------------------------------------------------------
# gate_directory batch helper
# --------------------------------------------------------------------------

def test_gate_directory_mixed(tmp_path):
    """Folder with one good file, one 0-byte, one nested good file."""
    (tmp_path / "good.md").write_text(
        "# heading\n" + _PADDING + "\n## subsection\n"
    )
    (tmp_path / "bad.md").write_text("")  # 0 bytes
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "split.md").write_text(
        "######## Annex A\n" + _PADDING + "\n### A.1 Foo\n"
    )

    valid, failed = gate_directory(tmp_path)
    assert len(valid) == 2
    assert len(failed) == 1
    assert failed[0][1] == "empty"


def test_gate_directory_empty_folder(tmp_path):
    valid, failed = gate_directory(tmp_path)
    assert valid == []
    assert failed == []


def test_gate_directory_fail_fast(tmp_path):
    """fail_fast raises on the first bad file."""
    (tmp_path / "bad.md").write_text("")  # 0-byte
    with pytest.raises(SanityGateError) as exc_info:
        gate_directory(tmp_path, fail_fast=True)
    assert "empty" in str(exc_info.value)
