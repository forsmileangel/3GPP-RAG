"""Grounded-answer prompt construction (Step 7, pure).

Builds the (system, user) pair for a generation request that must answer ONLY
from retrieved 3GPP excerpts and cite them by number. No IO, no provider/model
detail — trivially unit-testable and reusable across providers. The grounding
contract here is the second half of the anti-hallucination design (the evidence
gate is the first: it refuses upstream before any LLM call).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

# Returned verbatim when the evidence gate refuses (answer.py); kept here so the
# refusal string lives next to the prompt contract it complements.
REFUSAL_TEXT = "目前索引資料不足以回答"

_SYSTEM = (
    "You are a 3GPP specification assistant. Answer the question using ONLY "
    "the numbered excerpts provided below.\n"
    "- Ground every statement in the excerpts and cite the excerpt number(s) "
    "inline, e.g. [1], [2].\n"
    "- Quote numeric values, units, and section numbers exactly as they "
    "appear; never round, convert, or infer a value that is not stated.\n"
    "- If the excerpts do not contain enough information to answer, say so "
    "plainly rather than guessing.\n"
    "- Be concise and factual; add nothing from outside the excerpts."
)


@dataclass(frozen=True)
class Excerpt:
    """One numbered piece of evidence. ``n`` is the 1-based citation label the
    model is told to use; section / page / table_id locate it for the reader.
    page may be 0 (the md sentinel — no page numbering) or None; both are
    omitted from the rendered locator."""
    n: int
    section_number: str
    page: int | None
    table_id: str | None
    text: str


def format_excerpt(ex: Excerpt) -> str:
    """Render one excerpt as ``[n] (locator)\\n<text>``."""
    loc = [f"§{ex.section_number}"]
    if ex.table_id:
        loc.append(f"Table {ex.table_id}")
    if ex.page:  # 0 (md sentinel) and None both skipped
        loc.append(f"p.{ex.page}")
    return f"[{ex.n}] ({', '.join(loc)})\n{ex.text}"


def build_grounded_prompt(
    query: str, excerpts: Sequence[Excerpt],
) -> tuple[str, str]:
    """Return (system, user). system carries the grounding contract; user is
    the question followed by the numbered excerpts the answer must rely on."""
    body = "\n\n".join(format_excerpt(ex) for ex in excerpts)
    user = f"Question: {query}\n\nExcerpts:\n{body}"
    return _SYSTEM, user
