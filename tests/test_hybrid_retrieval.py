"""Unit tests for RRF fusion (src/retrieval/hybrid.py).

Pure rrf_merge math plus search_hybrid integration with monkeypatched
backends — no DB, no Chroma, no embedding model. The backend fakes are
patched on the hybrid module's namespace (it binds search_sparse /
search_dense at import time), mirroring how test_dense_retrieval.py
patches dense._get_model / dense._get_collection.
"""

from __future__ import annotations

import src.retrieval.hybrid as hybrid
from src.retrieval.dense import DenseHit
from src.retrieval.hybrid import HybridHit, rrf_merge, search_hybrid
from src.retrieval.sparse import SparseHit


# ---------------------------------------------------------------- rrf_merge

def test_overlap_outranks_single_list():
    # 7 sits at rank 3 in BOTH lists: 2/(60+3). 1 and 2 are rank-1 in only
    # one list each: 1/(60+1). Agreement must win.
    merged = rrf_merge([[1, 8, 7], [2, 9, 7]])
    assert merged[0][0] == 7
    assert abs(merged[0][1] - 2 / 63) < 1e-12


def test_disjoint_lists():
    merged = rrf_merge([[1, 3], [2, 4]])
    # 1 & 2 tie at 1/61 (same min_rank) -> id ascending; same for 3 & 4.
    assert [m[0] for m in merged] == [1, 2, 3, 4]


def test_empty_one_side():
    merged = rrf_merge([[1, 2, 3], []])
    assert [m[0] for m in merged] == [1, 2, 3]
    assert merged[0][2] == [1, None]


def test_empty_both():
    assert rrf_merge([[], []]) == []


def test_tiebreak_min_rank_then_id():
    # k=2 constructs exact score ties: 10/101/201 are rank-1 singletons
    # (1/3 each); 5 appears at rank 4 in two lists (1/6 + 1/6 = 1/3).
    # Tie resolution: min_rank first (1 beats 4, so 5 goes last despite the
    # smallest id), then id ascending among the rank-1 group.
    merged = rrf_merge([[10], [101, 102, 103, 5], [201, 202, 203, 5]], k=2)
    assert [m[0] for m in merged][:4] == [10, 101, 201, 5]


def test_determinism_across_runs():
    lists = [[3, 1, 4, 1, 5], [9, 2, 6, 5, 3]]
    first = rrf_merge(lists)
    second = rrf_merge(lists)
    assert first == second


def test_k_controls_top_rank_weighting():
    # A(=1) is rank 1 in one list; B(=2) is rank 4 in both lists.
    # k=60: A = 1/61 < B = 2/64 -> agreement wins.
    # k=1:  A = 1/2  > B = 2/5  -> top rank wins.
    lists = [[1, 11, 12, 2], [21, 22, 23, 2]]
    ids_k60 = [m[0] for m in rrf_merge(lists, k=60)]
    ids_k1 = [m[0] for m in rrf_merge(lists, k=1)]
    assert ids_k60.index(2) < ids_k60.index(1)
    assert ids_k1.index(1) < ids_k1.index(2)


def test_top_k_truncation():
    full = rrf_merge([[1, 2, 3], [4, 5, 6]])
    cut = rrf_merge([[1, 2, 3], [4, 5, 6]], top_k=2)
    assert len(cut) == 2
    assert cut == full[:2]


def test_provenance_ranks():
    merged = rrf_merge([[5, 6], [6, 7]])
    ranks = {item: per_list for item, _, per_list in merged}
    assert ranks[5] == [1, None]
    assert ranks[6] == [2, 1]
    assert ranks[7] == [None, 2]


def test_intra_list_duplicate_counts_once():
    merged = rrf_merge([[5, 5, 9]])
    by_id = {item: (score, per_list) for item, score, per_list in merged}
    assert abs(by_id[5][0] - 1 / 61) < 1e-12   # rank 1 only, not 1+2
    assert by_id[5][1] == [1]
    assert by_id[9][1] == [3]


# ------------------------------------------------------------ search_hybrid

def _sparse(chunk_id: int, sec: str = "6.2.1", page: int = 92) -> SparseHit:
    return SparseHit(
        chunk_id=chunk_id, section_number=sec, table_id=None, page=page,
        bm25_score=-10.0, text_preview="sparse text",
    )


def _dense(chunk_id: int, sec: str = "6.3.1", page: int = 541) -> DenseHit:
    return DenseHit(
        chunk_id=chunk_id, section_number=sec, table_id=None, page=page,
        distance=0.3, text_preview="dense text",
    )


def test_search_hybrid_fusion_and_metadata(monkeypatch):
    sparse_hits = [_sparse(1), _sparse(7, sec="6.2.3", page=123)]
    dense_hits = [_dense(7, sec="6.2.3", page=123), _dense(2)]
    monkeypatch.setattr(hybrid, "search_sparse", lambda s, q, **kw: sparse_hits)
    monkeypatch.setattr(hybrid, "search_dense", lambda s, q, **kw: dense_hits)

    hits = search_hybrid(None, "q", top_k=5)

    # 7 is in both lists (sparse rank 2 + dense rank 1) and must outrank
    # the rank-1 singletons.
    assert hits[0].chunk_id == 7
    assert abs(hits[0].rrf_score - (1 / 62 + 1 / 61)) < 1e-12
    assert hits[0].section_number == "6.2.3"
    assert hits[0].page == 123
    # Metadata is copied from the sparse hit when both backends have it.
    assert hits[0].text_preview == "sparse text"
    assert all(isinstance(h, HybridHit) for h in hits)


def test_search_hybrid_provenance(monkeypatch):
    monkeypatch.setattr(
        hybrid, "search_sparse", lambda s, q, **kw: [_sparse(1), _sparse(7)],
    )
    monkeypatch.setattr(
        hybrid, "search_dense", lambda s, q, **kw: [_dense(7), _dense(2)],
    )
    by_id = {h.chunk_id: h for h in search_hybrid(None, "q", top_k=5)}
    assert (by_id[1].sparse_rank, by_id[1].dense_rank) == (1, None)
    assert (by_id[7].sparse_rank, by_id[7].dense_rank) == (2, 1)
    assert (by_id[2].sparse_rank, by_id[2].dense_rank) == (None, 2)


def test_candidate_depth_passthrough(monkeypatch):
    captured: dict[str, int] = {}

    def fake_sparse(session, query, *, top_k, **kw):
        captured["sparse"] = top_k
        return []

    def fake_dense(session, query, *, top_k, **kw):
        captured["dense"] = top_k
        return []

    monkeypatch.setattr(hybrid, "search_sparse", fake_sparse)
    monkeypatch.setattr(hybrid, "search_dense", fake_dense)

    search_hybrid(None, "q", top_k=5)
    assert captured == {"sparse": 30, "dense": 30}   # max(30, 5)

    search_hybrid(None, "q", top_k=50)
    assert captured == {"sparse": 50, "dense": 50}   # max(30, 50)

    search_hybrid(None, "q", top_k=5, candidate_k=12)
    assert captured == {"sparse": 12, "dense": 12}   # explicit override


def test_search_hybrid_top_k_truncation(monkeypatch):
    monkeypatch.setattr(
        hybrid, "search_sparse",
        lambda s, q, **kw: [_sparse(i) for i in (1, 2, 3, 4)],
    )
    monkeypatch.setattr(
        hybrid, "search_dense",
        lambda s, q, **kw: [_dense(i) for i in (5, 6, 7, 8)],
    )
    hits = search_hybrid(None, "q", top_k=3)
    assert len(hits) == 3


def test_search_hybrid_both_empty(monkeypatch):
    monkeypatch.setattr(hybrid, "search_sparse", lambda s, q, **kw: [])
    monkeypatch.setattr(hybrid, "search_dense", lambda s, q, **kw: [])
    assert search_hybrid(None, "q", top_k=5) == []
