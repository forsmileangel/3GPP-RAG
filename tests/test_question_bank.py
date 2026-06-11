"""Scope-validate every test question against the source PDF.

For each entry in data/eval/test_questions.yaml:
  - locate expected_section in the PDF's bookmark TOC
  - extract that section's page text
  - assert at least one of expected_keywords appears in that text

This is the v2.1 lesson "every test question must scope-validate". A
failed entry means either the question's expected_section is wrong or
expected_keywords are off — fix the bank before relying on it for
retrieval evaluation.
"""

from __future__ import annotations

import re
from pathlib import Path

import fitz
import pytest
import yaml

from src.config import settings
from src.ingestion import extract_pages_text, extract_sections


REPO_ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = REPO_ROOT / "data" / "eval" / "test_questions.yaml"

REQUIRED_FIELDS = {
    "qid",
    "question",
    "spec",
    "expected_section",
    "expected_keywords",
    "question_type",
    "difficulty",
}
ALLOWED_QTYPES = {
    "numeric",
    "procedure",
    "table_lookup",
    "section_summary",
    "comparison",
    "out_of_scope",
}
ALLOWED_DIFFICULTIES = {"easy", "medium", "hard"}


# Single PDF for now — when the bank covers multiple specs, switch to a
# per-spec map. This matches the v2 plan's progressive ingestion model.
SPEC_TO_PDF = {
    "38.521-1": settings.raw_dir / "ts_138521-01_v17_05_00.pdf",
}


def _load_questions() -> list[dict]:
    with QUESTIONS_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _extract_text_for_section(pdf_path: Path, section_number: str) -> str:
    sections = extract_sections(pdf_path, [section_number])
    target = next(s for s in sections if s.section_number == section_number)
    with fitz.open(pdf_path) as doc:
        text, _ = extract_pages_text(doc, target.page_start - 1, target.page_end - 1)
    return text


@pytest.fixture(scope="module")
def questions() -> list[dict]:
    qs = _load_questions()
    assert qs, "test_questions.yaml is empty"
    return qs


def test_bank_size_at_least_30(questions):
    """Week 3 Step 1 milestone — at least 30 scope-validated questions."""
    assert len(questions) >= 30, f"only {len(questions)} questions, need >=30"


def test_qids_are_unique(questions):
    qids = [q["qid"] for q in questions]
    assert len(qids) == len(set(qids)), "duplicate qids"


def test_required_fields_present(questions):
    for q in questions:
        missing = REQUIRED_FIELDS - q.keys()
        assert not missing, f"{q.get('qid', '?')} missing fields: {missing}"


def test_xref_sections_optional_well_formed(questions):
    """xref_sections is OPTIONAL metadata on cross-reference questions: the
    other section(s) the question conceptually bridges. The evaluator ignores
    it today; the future cross-ref-resolution eval will read it. When present
    it must be a non-empty list of section-number strings."""
    section_number_re = re.compile(r"\d+(\.\d+)*")
    for q in questions:
        if "xref_sections" not in q:
            continue
        xs = q["xref_sections"]
        assert isinstance(xs, list) and xs, (
            f"{q['qid']} xref_sections must be a non-empty list"
        )
        for s in xs:
            assert isinstance(s, str) and section_number_re.fullmatch(s), (
                f"{q['qid']} xref_sections entry {s!r} is not a section number"
            )


def test_metadata_values_in_allowed_set(questions):
    for q in questions:
        assert q["question_type"] in ALLOWED_QTYPES, (
            f"{q['qid']} has unknown question_type: {q['question_type']!r}"
        )
        assert q["difficulty"] in ALLOWED_DIFFICULTIES, (
            f"{q['qid']} has unknown difficulty: {q['difficulty']!r}"
        )
        assert isinstance(q["expected_keywords"], list) and q["expected_keywords"], (
            f"{q['qid']} expected_keywords must be non-empty list"
        )


@pytest.mark.parametrize("question_idx", range(40))  # generous upper bound
def test_question_scope_validates(questions, question_idx):
    """Each question's keywords must appear in its expected_section text."""
    if question_idx >= len(questions):
        pytest.skip(f"only {len(questions)} questions in bank")

    q = questions[question_idx]
    pdf_path = SPEC_TO_PDF.get(q["spec"])
    if pdf_path is None or not pdf_path.exists():
        pytest.skip(f"PDF for spec {q['spec']!r} unavailable: {pdf_path}")

    section_text = _extract_text_for_section(pdf_path, q["expected_section"])
    section_text_lower = section_text.lower()
    matched = [
        kw for kw in q["expected_keywords"]
        if kw.lower() in section_text_lower
    ]
    assert matched, (
        f"{q['qid']} ({q['question']!r}): NONE of {q['expected_keywords']} "
        f"appeared in §{q['expected_section']} text "
        f"(text length {len(section_text)} chars). "
        f"Either expected_section is wrong or expected_keywords are off."
    )
