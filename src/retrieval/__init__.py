"""Retrieval layer.

Phase A Week 2–3 (v2.1):
    sparse  — SQLite FTS5 (BM25), keyword/precise-token retrieval
    dense   — BGE-M3 over Chroma (semantic retrieval)
    hybrid  — RRF fusion of sparse + dense (rank-based, k=60)

Coming in Week 3:
    rerank  — reranker over the hybrid top-K
"""

from .dense import DenseHit, search_dense
from .hybrid import HybridHit, search_hybrid
from .sparse import SparseHit, search_sparse

__all__ = [
    "DenseHit",
    "HybridHit",
    "SparseHit",
    "search_dense",
    "search_hybrid",
    "search_sparse",
]
