"""Streamlit query MVP (Step 8) — a thin client over the RAG backend.

Run:  streamlit run app/streamlit_app.py

Interface-neutrality (README design rule #1): this file imports from src/;
src/ never imports from app/. All `st.*` side effects live INSIDE main() (the
module-level `@st.cache_resource` decorator only wraps, it does not call), so
importing this module — e.g. the smoke test — never starts the UI. Under
`streamlit run` the script executes as __main__, so the guard at the bottom
fires; under `import app.streamlit_app` the name differs and main() does not.

The evidence gate + sources panel work WITHOUT an API key; generation is an
opt-in toggle (default off) that calls the LLM only when the gate isn't REFUSE.
"""

from __future__ import annotations

import sys
from pathlib import Path

# scripts/ idiom: make the repo root importable when run via `streamlit run`
# (streamlit puts the script's own dir on sys.path, not the repo root).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app._render import citation_line, gate_badge, hit_locator
from src.config import settings
from src.generation import build_grounded_answer, retrieve_and_gate
from src.generation.prompt import REFUSAL_TEXT
from src.retrieval import GateOutcome
from src.retrieval._textfetch import fetch_full_texts


@st.cache_resource
def get_engine():
    """One SQLAlchemy engine (connection-pool factory) for the whole server
    process — cached across reruns. A fresh Session is opened per query."""
    return create_engine(settings.db_url, future=True)


def _render_gate(decision) -> None:
    label, color = gate_badge(decision.outcome)
    st.markdown(f":{color}[**Gate: {label}**]")
    st.caption(decision.reason)


def _render_sources(hits, full_texts: dict[int, str]) -> None:
    st.subheader(f"來源 ({len(hits)})")
    if not hits:
        st.caption("檢索無結果。")
        return
    for i, h in enumerate(hits, start=1):
        with st.expander(f"[{i}] {hit_locator(h)}  ·  chunk {h.chunk_id}"):
            st.text(full_texts.get(h.chunk_id) or h.text_preview)


def _render_answer(result) -> None:
    st.subheader("答案")
    if result.text.strip():
        st.markdown(result.text)
    else:
        st.warning("(模型無輸出 — 可能安全拒答;未杜撰)")
    if result.citations:
        st.markdown("**引用**")
        for c in result.citations:
            st.markdown(citation_line(c))


def main() -> None:
    st.set_page_config(page_title="3GPP RAG", layout="wide")
    st.title("3GPP 規格查詢 (MVP)")

    with st.sidebar:
        backend = st.selectbox(
            "Backend", ["sparse", "dense", "hybrid", "reranked"], index=2,
        )
        sf_label = st.selectbox(
            "Source format", ["全部", "pdf_pymupdf", "tspec_md"], index=2,
        )
        mode = st.selectbox(
            "Gate mode", ["balanced", "strict", "permissive"], index=0,
        )
        top_k = st.slider("top_k", 1, 10, 5)
        do_generate = st.toggle("用 LLM 生成回答(會呼叫 API,1 次)", value=False)
        if backend == "reranked":
            st.caption("⚠ reranked 在 CPU 上首查較慢(數秒)。")

    # The only place the UI label space and the src value space diverge.
    source_format = None if sf_label == "全部" else sf_label

    query = st.text_input("輸入查詢")
    if not st.button("查詢", type="primary") or not query.strip():
        return

    engine = get_engine()
    try:
        with Session(engine) as session:
            with st.spinner("檢索中(首查需載入模型)…"):
                ctx = retrieve_and_gate(
                    session, query, backend=backend, mode=mode,
                    top_k=top_k, source_format=source_format,
                )
                full_texts = fetch_full_texts(
                    session, [h.chunk_id for h in ctx.hits],
                )
            # Sources + gate render BEFORE any generation, so a later LLM error
            # never blanks the page (and the no-key path is fully useful).
            _render_gate(ctx.decision)
            _render_sources(ctx.hits, full_texts)

            if do_generate:
                if ctx.decision.outcome is GateOutcome.REFUSE:
                    st.info(REFUSAL_TEXT)
                else:
                    with st.spinner("生成中…"):
                        try:
                            _render_answer(build_grounded_answer(session, ctx))
                        except Exception as exc:
                            st.error(
                                "生成失敗(可能未設定 ANTHROPIC_API_KEY)。"
                                "上方來源仍可用。\n\n" + repr(exc)
                            )
    except Exception as exc:
        st.error(
            "檢索失敗 — 索引可能未建立。請先跑 "
            "scripts/init_db.py → ingest → embed_chunks。\n\n" + repr(exc)
        )


if __name__ == "__main__":
    main()
