"""Dense embedding step: chunks (SQL) -> BGE-M3 -> Chroma.

Phase A Week 2 step 3 of the v2.1 hybrid plan. The chunker has already
written chunks to SQL; this step:
  1. Reads chunks that haven't been embedded yet (vector_id IS NULL)
  2. Encodes their `text` with BAAI/bge-m3 via sentence-transformers
  3. Writes vectors into a persistent Chroma collection
  4. Updates each chunk's vector_id + embedding_model in SQL so we know
     it's done

Idempotent: re-running only embeds new chunks. Use `--refresh-collection`
on the CLI wrapper to force a full rebuild.

Settings flowing through src.config.settings:
  - chroma_path  -> Chroma's PersistentClient directory
  - data_dir     -> only used indirectly (HF cache via env)

The HF cache (~/.cache/huggingface) is reused across runs so model
downloads don't repeat.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config import settings
from src.models import Chunk


DEFAULT_MODEL = "BAAI/bge-m3"
DEFAULT_COLLECTION = "chunks"
DEFAULT_BATCH = 32


@dataclass
class EmbedResult:
    embedded: int       # newly embedded this run
    skipped: int        # already had vector_id
    total_in_collection: int
    model_name: str


def _vector_id_for(chunk_id: int) -> str:
    """Stable Chroma id derived from chunks.chunk_id."""
    return f"c{chunk_id:06d}"


def _open_chroma(path_str: str, collection_name: str) -> chromadb.Collection:
    client = chromadb.PersistentClient(
        path=path_str,
        settings=ChromaSettings(anonymized_telemetry=False),
    )
    try:
        return client.get_collection(name=collection_name)
    except Exception:
        return client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )


def embed_pending_chunks(
    session: Session,
    *,
    model_name: str = DEFAULT_MODEL,
    collection_name: str = DEFAULT_COLLECTION,
    batch_size: int = DEFAULT_BATCH,
    progress: bool = True,
) -> EmbedResult:
    """Embed chunks where vector_id IS NULL; idempotent."""
    settings.chroma_path.mkdir(parents=True, exist_ok=True)
    coll = _open_chroma(str(settings.chroma_path), collection_name)

    pending = list(session.execute(
        select(Chunk).where(Chunk.vector_id.is_(None)).order_by(Chunk.chunk_id)
    ).scalars())

    skipped = session.execute(
        select(Chunk).where(Chunk.vector_id.is_not(None))
    ).scalars().all()

    if not pending:
        return EmbedResult(
            embedded=0,
            skipped=len(skipped),
            total_in_collection=coll.count(),
            model_name=model_name,
        )

    if progress:
        print(f"[embed] Loading {model_name} (cached if previously downloaded) ...")
    t0 = time.time()
    model = SentenceTransformer(model_name)
    if progress:
        print(f"[embed] Loaded in {time.time() - t0:.1f}s; encoding {len(pending)} chunks")

    embedded = 0
    for start in range(0, len(pending), batch_size):
        batch = pending[start:start + batch_size]
        texts = [c.text for c in batch]
        vectors = model.encode(texts, show_progress_bar=False).tolist()
        ids = [_vector_id_for(c.chunk_id) for c in batch]

        # Chroma metadata — keep small, we already have full row in SQL.
        metas = [
            {
                "chunk_id": int(c.chunk_id),
                "section_id": int(c.section_id),
                "page": int(c.page),
                "chunk_type": c.chunk_type.value,
                "table_id": c.table_id or "",
            }
            for c in batch
        ]

        coll.upsert(ids=ids, embeddings=vectors, documents=texts, metadatas=metas)

        # Mark each as embedded
        for c, vid in zip(batch, ids):
            c.vector_id = vid
            c.embedding_model = model_name
        session.flush()
        embedded += len(batch)
        if progress:
            print(f"[embed] {embedded}/{len(pending)} chunks done")

    return EmbedResult(
        embedded=embedded,
        skipped=len(skipped),
        total_in_collection=coll.count(),
        model_name=model_name,
    )
