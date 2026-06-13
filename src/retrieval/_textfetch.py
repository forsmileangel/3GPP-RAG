"""Shared helper: fetch full chunk text by id.

Retrieval hits carry only a 240-char ``text_preview``. Any stage that needs
the real chunk text — the reranker cross-encoder, the evidence gate's term
coverage — fetches it here, so the truncation never silently throws signal
away. Kept in its own module so both src/retrieval/rerank.py and
src/retrieval/gate.py depend on one implementation, not a private copy.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import Chunk


def fetch_full_texts(session: Session, chunk_ids: list[int]) -> dict[int, str]:
    """Map chunk_id -> full text for the given ids. Empty in, empty out."""
    if not chunk_ids:
        return {}
    rows = session.execute(
        select(Chunk.chunk_id, Chunk.text).where(Chunk.chunk_id.in_(chunk_ids))
    ).all()
    return {int(chunk_id): text for chunk_id, text in rows}
