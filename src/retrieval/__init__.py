"""Retrieval layer.

Phase A Week 2 (v2.1):
    sparse  — SQLite FTS5 (BM25), keyword/precise-token retrieval
    dense   — BGE-M3 over Chroma (semantic retrieval)

Coming in step 4 / Week 2 stretch / Week 3:
    hybrid  — RRF fusion of sparse + dense
    rerank  — local BGE reranker over the merged top-K
"""

from .dense import DenseHit, search_dense
from .sparse import SparseHit, search_sparse

__all__ = [
    "DenseHit",
    "SparseHit",
    "search_dense",
    "search_sparse",
]
