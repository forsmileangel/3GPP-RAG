"""Retrieval layer.

Phase A Week 2–3 (v2.1):
    sparse  — SQLite FTS5 (BM25), keyword/precise-token retrieval
    dense   — BGE-M3 over Chroma (semantic retrieval)
    hybrid  — RRF fusion of sparse + dense (rank-based, k=60)
    rerank  — cross-encoder over the hybrid top-30 (jina / bge, pinned)
    gate    — evidence gate: ANSWER / LOW_CONFIDENCE / REFUSE over a result set
"""

from .dense import DenseHit, search_dense
from .gate import (
    GateDecision,
    GateOutcome,
    GateSignals,
    GateThresholds,
    gate_for_hits,
    make_gate_decision,
)
from .hybrid import HybridHit, search_hybrid
from .rerank import RerankedHit, search_reranked
from .sparse import SparseHit, search_sparse

__all__ = [
    "DenseHit",
    "GateDecision",
    "GateOutcome",
    "GateSignals",
    "GateThresholds",
    "HybridHit",
    "RerankedHit",
    "SparseHit",
    "gate_for_hits",
    "make_gate_decision",
    "search_dense",
    "search_hybrid",
    "search_reranked",
    "search_sparse",
]
