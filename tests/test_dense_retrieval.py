"""Dense retrieval filter behavior without loading BGE-M3 or Chroma."""

from __future__ import annotations

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.models import Base, Chunk, ChunkType, Section, Spec
from src.retrieval import dense
from src.source_formats import SOURCE_FORMAT_PDF_PYMUPDF, SOURCE_FORMAT_TSPEC_MD


class _FakeEmbedding:
    def tolist(self):
        return [[0.1, 0.2, 0.3]]


class _FakeModel:
    def encode(self, texts, show_progress_bar=False):
        assert texts == ["shared query"]
        assert show_progress_bar is False
        return _FakeEmbedding()


class _FakeCollection:
    def __init__(self, ids: list[str], distances: list[float], documents: list[str]):
        self.ids = ids
        self.distances = distances
        self.documents = documents
        self.requested_n_results: list[int] = []

    def query(self, query_embeddings, n_results: int):
        assert query_embeddings == [[0.1, 0.2, 0.3]]
        self.requested_n_results.append(n_results)
        return {
            "ids": [self.ids[:n_results]],
            "distances": [self.distances[:n_results]],
            "documents": [self.documents[:n_results]],
        }


def _make_session(tmp_path) -> Session:
    engine = create_engine(
        f"sqlite:///{(tmp_path / 'dense.sqlite').as_posix()}",
        future=True,
    )
    Base.metadata.create_all(engine)
    session = Session(engine)

    pdf_spec = Spec(
        name="38.521-1",
        version="17.5.0",
        source_file="pdf.pdf",
        source_format=SOURCE_FORMAT_PDF_PYMUPDF,
    )
    md_spec = Spec(
        name="36.521-1",
        version="i20",
        source_file="md.md",
        source_format=SOURCE_FORMAT_TSPEC_MD,
    )
    session.add_all([pdf_spec, md_spec])
    session.flush()

    pdf_sec = Section(
        spec_id=pdf_spec.spec_id,
        section_number="6.2.1",
        title="PDF section",
        level=3,
        page_start=1,
        page_end=1,
    )
    md_sec = Section(
        spec_id=md_spec.spec_id,
        section_number="6.2.1",
        title="Markdown section",
        level=3,
        page_start=1,
        page_end=1,
    )
    session.add_all([pdf_sec, md_sec])
    session.flush()

    session.add_all([
        Chunk(
            section_id=md_sec.section_id,
            text="md first",
            source_format=SOURCE_FORMAT_TSPEC_MD,
            page=10,
            char_offset=0,
            chunk_type=ChunkType.PROSE,
            vector_id="md-1",
        ),
        Chunk(
            section_id=pdf_sec.section_id,
            text="pdf second",
            source_format=SOURCE_FORMAT_PDF_PYMUPDF,
            page=11,
            char_offset=0,
            chunk_type=ChunkType.PROSE,
            vector_id="pdf-2",
        ),
        Chunk(
            section_id=pdf_sec.section_id,
            text="pdf third",
            source_format=SOURCE_FORMAT_PDF_PYMUPDF,
            page=12,
            char_offset=0,
            chunk_type=ChunkType.TABLE,
            table_id="Table 6.2.1-1",
            vector_id="pdf-1",
        ),
        Chunk(
            section_id=md_sec.section_id,
            text="md fourth",
            source_format=SOURCE_FORMAT_TSPEC_MD,
            page=13,
            char_offset=0,
            chunk_type=ChunkType.PROSE,
            vector_id="md-2",
        ),
    ])
    session.commit()
    return session


def _patch_dense(monkeypatch, collection: _FakeCollection):
    monkeypatch.setattr(dense, "_get_model", lambda model_name: _FakeModel())
    monkeypatch.setattr(dense, "_get_collection", lambda path, name: collection)


def test_dense_without_filter_does_not_overfetch(tmp_path, monkeypatch):
    session = _make_session(tmp_path)
    collection = _FakeCollection(
        ids=["md-1", "pdf-2", "pdf-1"],
        distances=[0.01, 0.02, 0.03],
        documents=["md doc", "pdf doc 2", "pdf doc 1"],
    )
    _patch_dense(monkeypatch, collection)

    hits = dense.search_dense(session, "shared query", top_k=2)

    assert collection.requested_n_results == [2]
    assert [hit.text_preview for hit in hits] == ["md doc", "pdf doc 2"]

    session.close()


def test_dense_filter_overfetches_and_preserves_chroma_order(tmp_path, monkeypatch):
    session = _make_session(tmp_path)
    pdf_spec_id = session.execute(
        select(Spec.spec_id).where(Spec.name == "38.521-1")
    ).scalar_one()
    collection = _FakeCollection(
        ids=["md-1", "pdf-2", "pdf-1", "md-2"],
        distances=[0.01, 0.02, 0.03, 0.04],
        documents=["md doc 1", "pdf doc 2", "pdf doc 1", "md doc 2"],
    )
    _patch_dense(monkeypatch, collection)

    hits = dense.search_dense(
        session,
        "shared query",
        top_k=2,
        spec_id=pdf_spec_id,
        source_format=SOURCE_FORMAT_PDF_PYMUPDF,
    )

    assert collection.requested_n_results == [10]
    assert [hit.text_preview for hit in hits] == ["pdf doc 2", "pdf doc 1"]
    assert [hit.distance for hit in hits] == [0.02, 0.03]
    assert hits[1].table_id == "Table 6.2.1-1"

    session.close()


def test_dense_source_format_filter_excludes_other_sources(tmp_path, monkeypatch):
    session = _make_session(tmp_path)
    collection = _FakeCollection(
        ids=["md-1", "pdf-2", "pdf-1", "md-2"],
        distances=[0.01, 0.02, 0.03, 0.04],
        documents=["md doc 1", "pdf doc 2", "pdf doc 1", "md doc 2"],
    )
    _patch_dense(monkeypatch, collection)

    hits = dense.search_dense(
        session,
        "shared query",
        top_k=3,
        source_format=SOURCE_FORMAT_TSPEC_MD,
    )

    assert collection.requested_n_results == [15]
    assert [hit.text_preview for hit in hits] == ["md doc 1", "md doc 2"]

    session.close()
