"""Unit tests for the pandoc artifact cleaner (Tier 1 md ingestion, M1)."""

from __future__ import annotations

from pathlib import Path

from src.ingestion._artifact_cleaner import (
    clean_body,
    render_sub_superscript,
    strip_html_comments,
    strip_image_refs,
    strip_pandoc_anchors,
)

FIXTURE = (
    Path(__file__).parent / "fixtures" / "md" / "artifacts_sub_super_anchor.md"
)


def test_strip_pandoc_anchors_builds_positional_map():
    text = FIXTURE.read_text(encoding="utf-8")
    cleaned, anchor_map = strip_pandoc_anchors(text)
    assert "{#" not in cleaned
    # The heading carrying the attr is line 0 of the fixture.
    assert anchor_map == {0: "ue-maximum-output-power .unnumbered"}
    # Line-count preservation is the contract that keeps line_no valid.
    assert cleaned.count("\n") == text.count("\n")


def test_superscript_special_and_generic():
    assert render_sub_superscript("Bluetooth^TM^ case") == "Bluetooth™ case"
    assert render_sub_superscript("the 1^st^ transmission") == "the 1^st transmission"
    assert render_sub_superscript("back-off of 10^-3^") == "back-off of 10^-3"


def test_subscript_renders_to_underscore():
    assert render_sub_superscript("P~CMAX,f,c~ limits") == "P_CMAX,f,c limits"
    assert render_sub_superscript("N~RB~ value") == "N_RB value"


def test_sub_superscript_does_not_touch_lone_markers():
    # A lone tilde / caret (no closing partner on the same token) stays.
    assert render_sub_superscript("~14 min on CPU") == "~14 min on CPU"
    assert render_sub_superscript("x ^ y") == "x ^ y"


def test_image_refs_keep_alt_text_only():
    assert strip_image_refs("see ![](media/image42.png) here") == "see  here"
    assert (
        strip_image_refs("see ![antenna diagram](media/image43.png)!")
        == "see antenna diagram!"
    )


def test_html_comments_preserve_line_count():
    text = "a\n<!-- note\nspanning two lines -->\nb"
    cleaned = strip_html_comments(text)
    assert "note" not in cleaned
    assert cleaned.count("\n") == text.count("\n")
    assert cleaned.split("\n")[3] == "b"


def test_clean_body_composite_and_idempotent():
    text = FIXTURE.read_text(encoding="utf-8")
    body, _ = strip_pandoc_anchors(text)
    once = clean_body(body)
    assert "™" in once
    assert "P_CMAX,f,c" in once
    assert "![" not in once
    assert "<!--" not in once
    assert once.count("\n") == text.count("\n")
    assert clean_body(once) == once
