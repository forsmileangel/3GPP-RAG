"""Pure rendering helpers for the Streamlit app (Step 8).

string -> string, no IO, no `streamlit`, no `src` imports — so they unit-test
offline and the interface-neutrality rule (frontend depends on backend, never
the reverse) cannot be violated through here. `streamlit_app.py` glues these to
`st.*` calls. The locator rules mirror prompt.format_excerpt / scripts.answer.
"""

from __future__ import annotations

# Gate outcome (str or GateOutcome StrEnum) -> (display label, st color name).
_GATE_BADGES = {
    "answer": ("ANSWER", "green"),
    "low_confidence": ("LOW CONFIDENCE", "orange"),
    "refuse": ("REFUSE", "red"),
}


def gate_badge(outcome) -> tuple[str, str]:
    """Map a gate outcome to (label, color). Accepts a GateOutcome StrEnum or a
    plain string (compares on str(outcome)); unknown -> (UPPER, 'gray')."""
    key = str(outcome)
    return _GATE_BADGES.get(key, (key.upper(), "gray"))


def format_source_locator(*, section: str, table_id=None, page=None) -> str:
    """'§{section}[, Table {table_id}][, p.{page}]'. table_id omitted when
    falsy; page omitted when None or 0 (the md sentinel) — same rule as
    prompt.format_excerpt (page 0 = md has no page numbering)."""
    parts = [f"§{section}"]
    if table_id:
        parts.append(f"Table {table_id}")
    if page:  # None and 0 both skipped
        parts.append(f"p.{page}")
    return ", ".join(parts)


def citation_line(citation: dict) -> str:
    """'[{n}] §{section}[, Table ...][, p....]' from a citation dict
    ({n, section, page, table_id, chunk_id}); page may already be None."""
    loc = format_source_locator(
        section=citation["section"], table_id=citation.get("table_id"),
        page=citation.get("page"),
    )
    return f"[{citation['n']}] {loc}"


def hit_locator(hit) -> str:
    """Locator for a raw retrieval hit (the sources panel renders hits directly,
    needing no API key). Reads .section_number / .table_id / .page by attribute
    — does not import the hit classes, so this stays src-free."""
    return format_source_locator(
        section=hit.section_number, table_id=hit.table_id, page=hit.page,
    )
