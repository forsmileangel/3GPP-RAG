"""Rerank stage over hybrid retrieval (Phase A Week 3 Step 3).

Takes the hybrid (RRF) top candidates, re-scores each (query, FULL chunk
text) pair with a cross-encoder, and returns the re-ordered top_k. Full
text is fetched from SQL — the hits' text_preview is 240-char truncated
and would throw the ranking signal away.

Two models behind one adapter:
    jina — jinaai/jina-reranker-v3 (BEIR 61.94; CC BY-NC 4.0 — Tier-1
           personal use; custom remote code via AutoModel + model.rerank())
    bge  — BAAI/bge-reranker-v2-m3 (BEIR 56.51; Apache 2.0 — the
           commercial-tier fallback; standard CrossEncoder)

Revisions are pinned. For jina that pins the *executed remote code*
(trust_remote_code=True) as well as the weights — supply-chain safety and
reproducibility in one constant.

Sign convention: rerank_score is larger = better (same direction as
rrf_score, opposite to bm25_score / distance).
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.ingestion.embedder import DEFAULT_COLLECTION, DEFAULT_MODEL
from src.models import Chunk

from .hybrid import HybridHit, search_hybrid

# Cap per-doc text passed to the cross-encoder. Whole-table chunks can be
# tens of KB; 4000 chars (~1-1.4k tokens) fits both models' windows with
# headroom and bounds worst-case CPU latency. Single tuning point.
MAX_DOC_CHARS = 4000
BATCH_SIZE = 16           # CrossEncoder.predict batching (jina batches internally)
DEFAULT_CANDIDATE_K = 30  # matches the depth hybrid was designed to feed
DEFAULT_RERANKER = "jina"


@dataclass(frozen=True)
class _RerankerSpec:
    hf_id: str
    revision: str  # pinned HF commit — never "main"
    kind: str      # "jina_rerank" | "cross_encoder"


_RERANKERS: dict[str, _RerankerSpec] = {
    "jina": _RerankerSpec(
        hf_id="jinaai/jina-reranker-v3",
        revision="10fb694fc21f7a710a563ff1eb977a460f3868e4",  # 2026-03-27
        kind="jina_rerank",
    ),
    "bge": _RerankerSpec(
        hf_id="BAAI/bge-reranker-v2-m3",
        revision="953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e",  # 2024-06-24
        kind="cross_encoder",
    ),
}

# Module-level cache so 30 benchmark questions pay the model load once
# (same pattern as dense._model_cache).
_reranker_cache: dict[str, object] = {}


@dataclass(frozen=True)
class RerankedHit:
    """One reranked result. hybrid_rank / rrf_score / sparse_rank /
    dense_rank carry the full pre-rerank provenance so reports can show
    exactly what the reranker changed."""
    chunk_id: int
    section_number: str
    table_id: str | None
    page: int
    rerank_score: float       # larger = better
    text_preview: str
    hybrid_rank: int          # 1-indexed position in the hybrid input
    rrf_score: float
    sparse_rank: int | None
    dense_rank: int | None


def _get_reranker(reranker_model: str):
    spec = _RERANKERS.get(reranker_model)
    if spec is None:
        raise ValueError(
            f"unknown reranker {reranker_model!r}; valid: {sorted(_RERANKERS)}"
        )
    if reranker_model not in _reranker_cache:
        if spec.kind == "jina_rerank":
            from transformers import AutoModel

            model = AutoModel.from_pretrained(
                spec.hf_id,
                dtype="auto",
                trust_remote_code=True,
                revision=spec.revision,
            )
            model.eval()
            _reranker_cache[reranker_model] = model
        else:
            from sentence_transformers import CrossEncoder

            _reranker_cache[reranker_model] = CrossEncoder(
                spec.hf_id, revision=spec.revision,
            )
    return _reranker_cache[reranker_model]


def _score_jina(model, query: str, docs: list[str]) -> list[float]:
    """jina's rerank() returns dicts SORTED BY RELEVANCE with an `index`
    field; re-map to input order — assuming output order would silently
    corrupt the scores."""
    with torch.inference_mode():
        results = model.rerank(query, docs)
    scores = [0.0] * len(docs)
    for result in results:
        scores[int(result["index"])] = float(result["relevance_score"])
    return scores


def _score_cross_encoder(model, query: str, docs: list[str]) -> list[float]:
    """CrossEncoder.predict already returns input-order scores."""
    with torch.inference_mode():
        predictions = model.predict(
            [(query, doc) for doc in docs],
            batch_size=BATCH_SIZE,
            show_progress_bar=False,
        )
    return [float(score) for score in predictions]


def score_pairs(
    query: str, docs: list[str], *, reranker_model: str = DEFAULT_RERANKER,
) -> list[float]:
    """Score every doc against the query; larger = better, INPUT order."""
    if not docs:
        return []
    model = _get_reranker(reranker_model)  # raises on unknown name
    if _RERANKERS[reranker_model].kind == "jina_rerank":
        return _score_jina(model, query, docs)
    return _score_cross_encoder(model, query, docs)


def apply_rerank(
    hits: list[HybridHit], scores: list[float], *, top_k: int,
) -> list[RerankedHit]:
    """Pure: zip hybrid hits with their rerank scores, sort best-first,
    truncate to top_k.

    Tie-break (-rerank_score, hybrid_rank, chunk_id): on equal scores the
    hybrid order wins, so a flat-scoring reranker degrades gracefully to
    the RRF ranking instead of shuffling it; chunk_id keeps the order
    total and machine-stable.
    """
    if len(hits) != len(scores):
        raise ValueError(
            f"hits/scores length mismatch: {len(hits)} vs {len(scores)}"
        )
    reranked = [
        RerankedHit(
            chunk_id=hit.chunk_id,
            section_number=hit.section_number,
            table_id=hit.table_id,
            page=hit.page,
            rerank_score=float(score),
            text_preview=hit.text_preview,
            hybrid_rank=rank,
            rrf_score=hit.rrf_score,
            sparse_rank=hit.sparse_rank,
            dense_rank=hit.dense_rank,
        )
        for rank, (hit, score) in enumerate(zip(hits, scores), start=1)
    ]
    reranked.sort(key=lambda r: (-r.rerank_score, r.hybrid_rank, r.chunk_id))
    return reranked[:top_k]


def _fetch_full_texts(session: Session, chunk_ids: list[int]) -> dict[int, str]:
    """Full chunk text by id — the load-bearing step that text_preview
    (240 chars) cannot substitute for."""
    if not chunk_ids:
        return {}
    rows = session.execute(
        select(Chunk.chunk_id, Chunk.text).where(Chunk.chunk_id.in_(chunk_ids))
    ).all()
    return {int(chunk_id): text for chunk_id, text in rows}


def search_reranked(
    session: Session,
    query: str,
    *,
    top_k: int = 5,
    reranker_model: str = DEFAULT_RERANKER,
    candidate_k: int = DEFAULT_CANDIDATE_K,
    model_name: str = DEFAULT_MODEL,
    collection_name: str = DEFAULT_COLLECTION,
    spec_id: int | None = None,
    source_format: str | None = None,
) -> list[RerankedHit]:
    """hybrid top-candidate_k → fetch FULL chunk text → cross-encoder
    scores → apply_rerank top_k. Empty hybrid result short-circuits."""
    hybrid_hits = search_hybrid(
        session, query,
        top_k=candidate_k, candidate_k=candidate_k,
        model_name=model_name, collection_name=collection_name,
        spec_id=spec_id, source_format=source_format,
    )
    if not hybrid_hits:
        return []

    texts = _fetch_full_texts(session, [h.chunk_id for h in hybrid_hits])
    docs = [
        (texts.get(hit.chunk_id) or hit.text_preview)[:MAX_DOC_CHARS]
        for hit in hybrid_hits
    ]
    scores = score_pairs(query, docs, reranker_model=reranker_model)
    return apply_rerank(hybrid_hits, scores, top_k=top_k)
