"""Dense retrieval over Chroma using BGE-M3 query embeddings.

Phase A Week 2 step 3 (v2.1) — pairs with src/retrieval/sparse.py.
The model loaded here MUST match the model used at ingestion time
(stored on each chunk's `embedding_model`); a mismatch will produce
nonsense distances since the spaces aren't comparable.
"""

from __future__ import annotations

from dataclasses import dataclass

import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config import settings
from src.ingestion.embedder import DEFAULT_COLLECTION, DEFAULT_MODEL
from src.models import Chunk, Section


@dataclass(frozen=True)
class DenseHit:
    chunk_id: int
    section_number: str
    table_id: str | None
    page: int
    distance: float
    text_preview: str


# Module-level model + collection caches: re-loading BGE-M3 is expensive,
# so callers can hit search_dense() repeatedly without paying the load cost.
_model_cache: dict[str, SentenceTransformer] = {}
_collection_cache: dict[tuple[str, str], chromadb.Collection] = {}


def _get_model(model_name: str) -> SentenceTransformer:
    if model_name not in _model_cache:
        _model_cache[model_name] = SentenceTransformer(model_name)
    return _model_cache[model_name]


def _get_collection(path: str, name: str) -> chromadb.Collection:
    key = (path, name)
    if key not in _collection_cache:
        client = chromadb.PersistentClient(
            path=path,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        _collection_cache[key] = client.get_collection(name=name)
    return _collection_cache[key]


def search_dense(
    session: Session,
    query: str,
    *,
    top_k: int = 5,
    model_name: str = DEFAULT_MODEL,
    collection_name: str = DEFAULT_COLLECTION,
) -> list[DenseHit]:
    """Encode `query` with BGE-M3, query Chroma, JOIN back to chunks +
    sections to populate metadata for each hit."""
    model = _get_model(model_name)
    coll = _get_collection(str(settings.chroma_path), collection_name)

    qvec = model.encode([query], show_progress_bar=False).tolist()
    raw = coll.query(query_embeddings=qvec, n_results=top_k)
    if not raw["ids"] or not raw["ids"][0]:
        return []

    ids = raw["ids"][0]
    distances = raw["distances"][0]
    documents = raw["documents"][0]

    # Pull chunk_id + section_number from SQL in one shot; metadatas in
    # Chroma are a bit denormalized, but section_number lives only in
    # SQL so we JOIN here.
    chunk_id_lookup = {f"c{0:06d}": 0}  # noqa: F841 — placeholder so we keep types tidy
    rows = session.execute(
        select(Chunk.chunk_id, Chunk.vector_id, Chunk.table_id, Chunk.page,
               Section.section_number)
        .join(Section, Chunk.section_id == Section.section_id)
        .where(Chunk.vector_id.in_(ids))
    ).all()
    by_vid = {
        r.vector_id: (r.chunk_id, r.section_number, r.table_id, r.page)
        for r in rows
    }

    hits: list[DenseHit] = []
    for vid, dist, doc in zip(ids, distances, documents):
        meta = by_vid.get(vid)
        if meta is None:
            continue
        chunk_id, section_number, table_id, page = meta
        hits.append(DenseHit(
            chunk_id=int(chunk_id),
            section_number=section_number,
            table_id=table_id,
            page=int(page),
            distance=float(dist),
            text_preview=(doc or "")[:240].replace("\n", " "),
        ))
    return hits
