"""Hybrid retrieval — RRF fusion of sparse (FTS5 BM25) and dense (BGE-M3).

Phase A Week 3 Step 2 of the v2.1 hybrid plan. Reciprocal Rank Fusion is
rank-based, so the two backends' incompatible score spaces (negative BM25
vs cosine distance) never mix: each backend contributes 1/(k + rank) per
document, and a document found by both backends sums both contributions —
mutual agreement is what lifts a hit to the top.

Sign convention: rrf_score is LARGER = better, the opposite of bm25_score
and distance. rrf_merge already returns best-first order; callers must
consume that order and never re-sort by raw score.
"""

from __future__ import annotations

from collections.abc import Hashable, Sequence
from dataclasses import dataclass

from sqlalchemy.orm import Session

from src.ingestion.embedder import DEFAULT_COLLECTION, DEFAULT_MODEL

from .dense import DenseHit, search_dense
from .sparse import SparseHit, search_sparse

# Standard constant from the RRF literature; dampens the gap between
# neighbouring ranks so deep-list agreement still counts.
RRF_K = 60


@dataclass(frozen=True)
class HybridHit:
    """One fused result. sparse_rank / dense_rank record where each backend
    placed this chunk (1-indexed; None = absent from that backend's list),
    so downstream debug views can show who contributed a hit."""
    chunk_id: int
    section_number: str
    table_id: str | None
    page: int
    rrf_score: float          # larger = better
    text_preview: str
    sparse_rank: int | None
    dense_rank: int | None


def rrf_merge(
    ranked_lists: Sequence[Sequence[Hashable]],
    *,
    k: int = RRF_K,
    top_k: int | None = None,
) -> list[tuple[Hashable, float, list[int | None]]]:
    """Fuse best-first ranked id lists with Reciprocal Rank Fusion.

    score(d) = sum over the lists containing d of 1 / (k + rank), with rank
    1-indexed. Within one list only the first occurrence of an id counts
    (defensive — backends should not emit duplicates).

    Returns (id, rrf_score, per_list_ranks) tuples in best-first order,
    where per_list_ranks[i] is the id's rank in ranked_lists[i] or None.

    Ordering is fully deterministic: (-score, min_rank, id). min_rank is
    the id's best rank in any list; id is the final total tiebreak. Ids in
    one call must therefore be mutually comparable (chunk ids are ints).
    """
    n_lists = len(ranked_lists)
    scores: dict[Hashable, float] = {}
    ranks: dict[Hashable, list[int | None]] = {}
    for list_idx, ranked in enumerate(ranked_lists):
        seen: set[Hashable] = set()
        for rank, item in enumerate(ranked, start=1):
            if item in seen:
                continue
            seen.add(item)
            scores[item] = scores.get(item, 0.0) + 1.0 / (k + rank)
            ranks.setdefault(item, [None] * n_lists)[list_idx] = rank

    def _sort_key(item: Hashable) -> tuple:
        item_ranks = ranks[item]
        min_rank = min(r for r in item_ranks if r is not None)
        return (-scores[item], min_rank, item)

    ordered = sorted(scores, key=_sort_key)
    if top_k is not None:
        ordered = ordered[:top_k]
    return [(item, scores[item], ranks[item]) for item in ordered]


def search_hybrid(
    session: Session,
    query: str,
    *,
    top_k: int = 5,
    candidate_k: int | None = None,
    model_name: str = DEFAULT_MODEL,
    collection_name: str = DEFAULT_COLLECTION,
    spec_id: int | None = None,
    source_format: str | None = None,
) -> list[HybridHit]:
    """Run sparse + dense, fuse with RRF, return top_k hits best-first.

    Pulls `candidate_k` results from EACH backend before fusing (default
    max(30, top_k)): deep enough that overlap between the backends is a
    meaningful signal, and matches the top-30 the upcoming reranker stage
    will consume, so no second retrieval pass is needed there.
    """
    depth = candidate_k if candidate_k is not None else max(30, top_k)
    sparse_hits = search_sparse(
        session, query,
        top_k=depth, spec_id=spec_id, source_format=source_format,
    )
    dense_hits = search_dense(
        session, query,
        top_k=depth, model_name=model_name, collection_name=collection_name,
        spec_id=spec_id, source_format=source_format,
    )

    merged = rrf_merge(
        [
            [h.chunk_id for h in sparse_hits],
            [h.chunk_id for h in dense_hits],
        ],
        top_k=top_k,
    )

    # The same chunk carries identical metadata in both backends; prefer
    # the sparse hit purely so the choice is deterministic.
    meta: dict[int, SparseHit | DenseHit] = {}
    for hit in [*sparse_hits, *dense_hits]:
        meta.setdefault(hit.chunk_id, hit)

    return [
        HybridHit(
            chunk_id=chunk_id,
            section_number=meta[chunk_id].section_number,
            table_id=meta[chunk_id].table_id,
            page=meta[chunk_id].page,
            rrf_score=score,
            text_preview=meta[chunk_id].text_preview,
            sparse_rank=per_list_ranks[0],
            dense_rank=per_list_ranks[1],
        )
        for chunk_id, score, per_list_ranks in merged
    ]
