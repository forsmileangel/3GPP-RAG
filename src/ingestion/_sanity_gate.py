"""Sanity gate for ingest pipeline — catches silent download corruption.

Validates that a markdown file looks like a real 3GPP TSpec-LLM spec rather
than a 0-byte / truncated / non-utf8 file. Runs as the first step of
MarkdownAdapter.discover_inputs so corrupt files don't silently break the
pipeline downstream.

The gate accepts a file if:
  - size > 0 bytes AND size >= 100 bytes (B0d spike calibration)
  - readable as utf-8
  - contains a heading (ATX `#+ ` or setext `===` / `---`) within the first
    200 non-empty lines, OR contains "3GPP TS X.Y.Z" boilerplate within the
    first 5 non-empty lines

Validated on the 50 R18 TSpec-LLM files (B0d spike — see
research/scans/2026-05-05-tspec-llm-eval-artifacts/sanity_gate_spike.py):
catches the 0-byte 36521-1-i20_cover.md without false-positive on any of the
50 valid files.
"""

from __future__ import annotations

import re
from pathlib import Path

ATX = re.compile(r"^#+\s+\S")
SETEXT_FOLLOW = re.compile(r"^[=-]{3,}\s*$")
TS_BOILERPLATE = re.compile(r"^\s*3GPP\s+TS\s+\d", re.IGNORECASE)

# Window sizes from B0d spike calibration on 50 R18 files. Cover + 3GPP
# boilerplate can push the first heading to ~line 79 (e.g. 36521-3-i20_cover);
# 200 non-empty lines is comfortable margin.
HEADING_WINDOW_NONEMPTY_LINES = 200
BOILERPLATE_WINDOW_NONEMPTY_LINES = 5


class SanityGateError(RuntimeError):
    """Raised by `gate_directory(..., fail_fast=True)` when a file fails."""


def is_valid_md(p: Path) -> tuple[bool, str]:
    """Check a TSpec-LLM markdown file for silent corruption.

    Returns (is_valid, reason_code). Reason codes:
        ok_full                      — has both 3GPP TS boilerplate + heading
        ok_cover_boilerplate         — boilerplate but no heading (rare)
        ok_heading_no_boilerplate    — heading but no TS prefix (split files)
        empty                        — 0 bytes (cache silent corruption)
        too_small                    — < 100 bytes (truncated)
        encoding_error               — not valid utf-8
        FAIL_no_boilerplate_no_heading — content but no recognisable structure
    """
    if not p.exists() or p.stat().st_size == 0:
        return False, "empty"
    if p.stat().st_size < 100:
        return False, "too_small"
    try:
        text = p.read_text(encoding="utf-8", errors="strict")
    except UnicodeDecodeError:
        return False, "encoding_error"

    head_lines = [
        line for line in text.splitlines()[:30] if line.strip()
    ][:BOILERPLATE_WINDOW_NONEMPTY_LINES]
    has_boilerplate = any(TS_BOILERPLATE.match(line) for line in head_lines)

    lines = text.splitlines()
    seen = 0
    has_heading = False
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        seen += 1
        if ATX.match(line):
            has_heading = True
            break
        if i + 1 < len(lines) and SETEXT_FOLLOW.match(lines[i + 1]):
            has_heading = True
            break
        if seen >= HEADING_WINDOW_NONEMPTY_LINES:
            break

    if has_boilerplate and has_heading:
        return True, "ok_full"
    if has_boilerplate and not has_heading:
        return True, "ok_cover_boilerplate"
    if has_heading and not has_boilerplate:
        return True, "ok_heading_no_boilerplate"
    return False, "FAIL_no_boilerplate_no_heading"


def gate_directory(
    d: Path,
    fail_fast: bool = False,
) -> tuple[list[Path], list[tuple[Path, str]]]:
    """Walk `d` recursively; return (valid_files, failed_with_reason).

    Only `.md` files are inspected. Subdirectories are recursed.
    If `fail_fast` is True, raises SanityGateError on the first failed file.
    """
    valid: list[Path] = []
    failed: list[tuple[Path, str]] = []
    for p in sorted(d.rglob("*.md")):
        ok, reason = is_valid_md(p)
        if ok:
            valid.append(p)
        else:
            if fail_fast:
                raise SanityGateError(f"{p}: {reason}")
            failed.append((p, reason))
    return valid, failed
