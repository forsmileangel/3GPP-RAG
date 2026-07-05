"""Pandoc artifact cleaning for TSpec-LLM markdown (Tier 1 ingestion).

Corpus-measured inventory (research/scans/2026-05-05-tspec-llm-eval.md):
  {#anchor .class} pandoc attrs  17,483  -> strip to metadata (anchor map)
  ^x^ / ~x~ sub/superscript      ~45K    -> RENDER to searchable text,
                                            never bare-strip (loses meaning)
  ![](path) image refs            1,701  -> drop, keep non-empty alt text
  <!-- --> html comments                  -> drop

Every transform is LINE-COUNT PRESERVING: Heading.line_no in the merged
source text must stay valid after cleaning, so nothing here may add or
remove newlines.
"""

from __future__ import annotations

import re

# Pandoc auto-generated attribute blocks, e.g. {#maximum-output-power
# .unnumbered}. The inside is kept (anchor map) for future cross-reference
# resolution (DeepSpecs pattern); the span is removed from text.
_PANDOC_ATTR_RE = re.compile(r"\s*\{#([^}\n]*)\}")

# Exact-form specials rendered to a conventional glyph.
_SUPERSCRIPT_SPECIALS = {
    "TM": "™",
    "(R)": "®",
}

# ^x^ -> ^x  keeps "10^-3^" meaningful as "10^-3" (unicode61 tokenizes on ^,
# so "1^st" still matches a "1st"/"st" query). ~x~ -> _x mirrors how the
# specs themselves write subscripts elsewhere (P_CMAX).
_SUPERSCRIPT_RE = re.compile(r"\^([^\^\s]{1,40})\^")
_SUBSCRIPT_RE = re.compile(r"~([^~\s]{1,40})~")

_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)\n]*\)")
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def strip_pandoc_anchors(text: str) -> tuple[str, dict[int, str]]:
    """Remove {#...} attribute spans; return (cleaned text, line_no -> raw
    attr content map). Line numbers are 0-indexed into `text`'s lines and
    remain valid in the cleaned text (removal is inline-only)."""
    anchor_map: dict[int, str] = {}
    out_lines: list[str] = []
    for line_no, line in enumerate(text.split("\n")):
        match = _PANDOC_ATTR_RE.search(line)
        if match:
            anchor_map[line_no] = match.group(1)
            line = _PANDOC_ATTR_RE.sub("", line)
        out_lines.append(line)
    return "\n".join(out_lines), anchor_map


def render_sub_superscript(text: str) -> str:
    """Convert pandoc ^x^ / ~x~ markup to searchable plain text."""

    def _sup(match: re.Match) -> str:
        content = match.group(1)
        return _SUPERSCRIPT_SPECIALS.get(content, f"^{content}")

    text = _SUPERSCRIPT_RE.sub(_sup, text)
    return _SUBSCRIPT_RE.sub(r"_\1", text)


def strip_image_refs(text: str) -> str:
    """Drop image syntax; keep non-empty alt text in place."""
    return _IMAGE_RE.sub(r"\1", text)


def unescape_pandoc_underscore(s: str) -> str:
    r"""Pandoc escapes literal underscores as '\_'; the backslash is a markup
    artifact, the real character is '_'. Underscores are LOAD-BEARING in two
    identifier families: table caption ids ("6.2.2\_1.3-1") and
    band-combination clause numbers ("6.2D.1\_1.1") — the shared unescape for
    both the caption path (_table_parser._caption_above) and the anchor path
    (_heading_parser.extract_anchor)."""
    return s.replace("\\_", "_")


def strip_html_comments(text: str) -> str:
    """Remove <!-- --> blocks, preserving the newlines they spanned so
    line numbers downstream stay stable."""

    def _keep_newlines(match: re.Match) -> str:
        return "\n" * match.group(0).count("\n")

    return _HTML_COMMENT_RE.sub(_keep_newlines, text)


def clean_body(text: str) -> str:
    """The prose-safe composite: comments -> images -> sub/superscript.

    Pandoc anchors are NOT handled here — callers strip them first via
    strip_pandoc_anchors so the positional anchor map can be built."""
    text = strip_html_comments(text)
    text = strip_image_refs(text)
    return render_sub_superscript(text)
