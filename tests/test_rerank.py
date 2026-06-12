"""Unit tests for the rerank stage (src/retrieval/rerank.py).

Pure apply_rerank math plus search_reranked integration with a
monkeypatched hybrid backend and a fake scorer — no model downloads, no
Chroma, no network. _fetch_full_texts is exercised against a real
throwaway SQLite (same pattern as test_dense_retrieval.py).
"""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import src.retrieval.rerank as rerank
from src.models import Base, Chunk, ChunkType, Section, Spec
from src.retrieval.hybrid import HybridHit
from src.retrieval.rerank import (
    MAX_DOC_CHARS,
    RerankedHit,
    apply_rerank,
    search_reranked,
)
from src.source_formats import SOURCE_FORMAT_PDF_PYMUPDF


def _hit(chunk_id: int, sec: str = "6.2.1", page: int = 92,
         rrf: float = 0.03, sr: int | None = 1, dr: int | None = None) -> HybridHit:
    return HybridHit(
        chunk_id=chunk_id, section_number=sec, table_id=None, page=page,
        rrf_score=rrf, text_preview=f"preview-{chunk_id}",
        sparse_rank=sr, dense_rank=dr,
    )


# -------------------------------------------------------------- apply_rerank

def test_apply_rerank_reorders_by_score():
    hits = [_hit(1), _hit(2), _hit(3)]
    out = apply_rerank(hits, [0.1, 0.9, 0.5], top_k=3)
    assert [h.chunk_id for h in out] == [2, 3, 1]
    assert [h.rerank_score for h in out] == [0.9, 0.5, 0.1]


def test_apply_rerank_tie_breaks_by_hybrid_rank():
    # Equal scores -> hybrid order wins (flat-scoring reranker degrades
    # gracefully to the RRF ranking).
    hits = [_hit(9), _hit(4), _hit(7)]
    out = apply_rerank(hits, [0.5, 0.5, 0.5], top_k=3)
    assert [h.chunk_id for h in out] == [9, 4, 7]


def test_apply_rerank_top_k_truncation():
    hits = [_hit(i) for i in (1, 2, 3, 4, 5)]
    out = apply_rerank(hits, [0.1, 0.2, 0.3, 0.4, 0.5], top_k=3)
    assert len(out) == 3
    assert [h.chunk_id for h in out] == [5, 4, 3]


def test_apply_rerank_empty():
    assert apply_rerank([], [], top_k=5) == []


def test_apply_rerank_length_mismatch_raises():
    with pytest.raises(ValueError, match="mismatch"):
        apply_rerank([_hit(1)], [0.1, 0.2], top_k=5)


def test_apply_rerank_carries_provenance():
    hits = [_hit(1, rrf=0.04, sr=2, dr=1), _hit(2, rrf=0.02, sr=None, dr=3)]
    out = apply_rerank(hits, [0.1, 0.9], top_k=2)
    top = out[0]
    assert isinstance(top, RerankedHit)
    assert top.chunk_id == 2
    assert top.hybrid_rank == 2          # was second in the hybrid input
    assert top.rrf_score == 0.02
    assert (top.sparse_rank, top.dense_rank) == (None, 3)


def test_apply_rerank_preserves_metadata():
    hits = [_hit(1, sec="6.3.2", page=544)]
    out = apply_rerank(hits, [0.7], top_k=1)
    assert out[0].section_number == "6.3.2"
    assert out[0].page == 544
    assert out[0].table_id is None
    assert out[0].text_preview == "preview-1"


# ----------------------------------------------------------- search_reranked

def _make_session(tmp_path) -> tuple[Session, list[int]]:
    """Real throwaway SQLite with one spec/section and chunks whose full
    text is much longer than text_preview would carry."""
    engine = create_engine(
        f"sqlite:///{(tmp_path / 'rerank.sqlite').as_posix()}", future=True,
    )
    Base.metadata.create_all(engine)
    session = Session(engine)

    spec = Spec(
        name="38.521-1", version="17.5.0",
        source_file="pdf.pdf", source_format=SOURCE_FORMAT_PDF_PYMUPDF,
    )
    session.add(spec)
    session.flush()
    sec = Section(
        spec_id=spec.spec_id, section_number="6.2.1", title="Sec",
        level=3, page_start=1, page_end=1,
    )
    session.add(sec)
    session.flush()

    chunks = [
        Chunk(
            section_id=sec.section_id,
            text=f"chunk-{i}-body " + ("x" * 6000),   # > MAX_DOC_CHARS
            source_format=SOURCE_FORMAT_PDF_PYMUPDF,
            page=90 + i, char_offset=0, chunk_type=ChunkType.PROSE,
        )
        for i in (1, 2, 3)
    ]
    session.add_all(chunks)
    session.commit()
    return session, [c.chunk_id for c in chunks]


def test_search_reranked_uses_full_text_not_preview(tmp_path, monkeypatch):
    session, ids = _make_session(tmp_path)
    hits = [_hit(ids[0]), _hit(ids[1]), _hit(ids[2])]
    monkeypatch.setattr(rerank, "search_hybrid", lambda s, q, **kw: hits)

    received: list[str] = []

    def fake_score(query, docs, *, reranker_model):
        received.extend(docs)
        return [0.1] * len(docs)

    monkeypatch.setattr(rerank, "score_pairs", fake_score)
    search_reranked(session, "q", top_k=3)

    assert len(received) == 3
    for i, doc in zip((1, 2, 3), received):
        assert doc.startswith(f"chunk-{i}-body")
        assert len(doc) > 240                      # not the preview
        assert len(doc) == MAX_DOC_CHARS           # truncated full text


def test_search_reranked_calls_hybrid_with_candidate_k(tmp_path, monkeypatch):
    session, _ = _make_session(tmp_path)
    captured: dict[str, int] = {}

    def fake_hybrid(s, q, *, top_k, candidate_k, **kw):
        captured["top_k"] = top_k
        captured["candidate_k"] = candidate_k
        return []

    monkeypatch.setattr(rerank, "search_hybrid", fake_hybrid)
    search_reranked(session, "q", top_k=5)
    # The rerank pool must be the full 30-candidate depth, not the small
    # final top_k.
    assert captured == {"top_k": 30, "candidate_k": 30}


def test_search_reranked_empty_hybrid_short_circuits(tmp_path, monkeypatch):
    session, _ = _make_session(tmp_path)
    monkeypatch.setattr(rerank, "search_hybrid", lambda s, q, **kw: [])

    def boom(*a, **kw):
        raise AssertionError("scorer must not be called on empty hybrid")

    monkeypatch.setattr(rerank, "score_pairs", boom)
    assert search_reranked(session, "q", top_k=5) == []


def test_search_reranked_reorders_end_to_end(tmp_path, monkeypatch):
    session, ids = _make_session(tmp_path)
    hits = [_hit(ids[0]), _hit(ids[1]), _hit(ids[2])]
    monkeypatch.setattr(rerank, "search_hybrid", lambda s, q, **kw: hits)
    # Highest score on the LAST hybrid candidate -> it must land first.
    monkeypatch.setattr(
        rerank, "score_pairs", lambda q, d, *, reranker_model: [0.1, 0.2, 0.9],
    )
    out = search_reranked(session, "q", top_k=2)
    assert [h.chunk_id for h in out] == [ids[2], ids[1]]
    assert out[0].hybrid_rank == 3


def test_search_reranked_passes_reranker_model(tmp_path, monkeypatch):
    session, ids = _make_session(tmp_path)
    monkeypatch.setattr(
        rerank, "search_hybrid", lambda s, q, **kw: [_hit(ids[0])],
    )
    seen: dict[str, str] = {}

    def fake_score(query, docs, *, reranker_model):
        seen["model"] = reranker_model
        return [0.5] * len(docs)

    monkeypatch.setattr(rerank, "score_pairs", fake_score)
    search_reranked(session, "q", top_k=1, reranker_model="bge")
    assert seen["model"] == "bge"


# ------------------------------------------------------------- score_pairs

def test_score_pairs_unknown_model_raises():
    with pytest.raises(ValueError, match="unknown reranker"):
        rerank.score_pairs("q", ["doc"], reranker_model="nope")


def test_score_pairs_empty_docs_no_model_load():
    # Must short-circuit BEFORE any model load (would download gigabytes).
    assert rerank.score_pairs("q", [], reranker_model="jina") == []


def test_score_jina_remaps_to_input_order():
    class FakeJina:
        def rerank(self, query, docs):
            # jina returns relevance-sorted results with original indices
            return [
                {"index": 2, "relevance_score": 0.9, "document": docs[2]},
                {"index": 0, "relevance_score": 0.5, "document": docs[0]},
                {"index": 1, "relevance_score": 0.1, "document": docs[1]},
            ]

    scores = rerank._score_jina(FakeJina(), "q", ["a", "b", "c"])
    assert scores == [0.5, 0.1, 0.9]   # input order, not output order
