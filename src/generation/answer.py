"""Grounded answer orchestration (Step 7) — the one IO seam tying retrieval,
the evidence gate, and an LLM provider together.

Flow: retrieve (backend dispatch) -> gate_for_hits -> on REFUSE return the
refusal verbatim WITHOUT calling the LLM (the gate is the hallucination
firewall) -> otherwise fetch FULL chunk text, build the grounded prompt, call
the provider, and return the answer. Citations are drawn from the retrieval
hits (provenance), NOT parsed out of the model's text — so a cited §section /
table / page is always real, never something the model invented.

Mirrors the IO-vs-pure split used across retrieval (search_reranked vs
apply_rerank): this module does the DB / network IO; prompt.py is pure.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from src.config import settings
from src.retrieval import (
    GateOutcome,
    gate_for_hits,
    search_dense,
    search_hybrid,
    search_reranked,
    search_sparse,
)
from src.retrieval._textfetch import fetch_full_texts

from .prompt import REFUSAL_TEXT, Excerpt, build_grounded_prompt
from .providers import LLMProvider, get_provider

# Backend name -> retrieval entry point. All four share the (session, query, *,
# top_k=, source_format=) signature the dispatch relies on; reranked also takes
# reranker_model/candidate_k (defaults are fine for the generate path).
_RETRIEVERS = {
    "sparse": search_sparse,
    "dense": search_dense,
    "hybrid": search_hybrid,
    "reranked": search_reranked,
}


@dataclass(frozen=True)
class AnswerResult:
    """The generation outcome. On REFUSE: refused=True, text=REFUSAL_TEXT,
    citations=[], model=None. On ANSWER/LOW_CONFIDENCE: the grounded answer,
    citations copied from the hits, and the model that produced it."""
    query: str
    text: str
    refused: bool
    gate_outcome: str
    backend: str
    citations: list[dict] = field(default_factory=list)
    model: str | None = None


def _retrieve(
    session: Session, query: str, *, backend: str, top_k: int,
    source_format: str | None,
):
    fn = _RETRIEVERS.get(backend)
    if fn is None:
        raise ValueError(
            f"unknown backend {backend!r}; valid: {sorted(_RETRIEVERS)}"
        )
    return fn(session, query, top_k=top_k, source_format=source_format)


def generate_answer(
    session: Session,
    query: str,
    *,
    backend: str = "hybrid",
    mode: str | None = None,
    top_k: int = 5,
    source_format: str | None = None,
    provider: LLMProvider | None = None,
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> AnswerResult:
    """Retrieve, gate, and (if the gate allows) generate a grounded answer.

    `mode` defaults to settings.gate_mode; `provider` / `model` / `temperature`
    / `max_tokens` default to the configured LLM (settings.llm_*). A gate REFUSE
    short-circuits before the provider is ever constructed or called.
    """
    mode = mode or settings.gate_mode
    hits = _retrieve(
        session, query, backend=backend, top_k=top_k, source_format=source_format,
    )
    decision = gate_for_hits(session, query, hits, backend=backend, mode=mode)

    if decision.outcome is GateOutcome.REFUSE:
        return AnswerResult(
            query=query, text=REFUSAL_TEXT, refused=True,
            gate_outcome=str(decision.outcome), backend=backend,
            citations=[], model=None,
        )

    # ANSWER or LOW_CONFIDENCE -> generate from the retrieved evidence. Fetch
    # FULL text (the 240-char preview would starve the prompt of the answer).
    texts = fetch_full_texts(session, [h.chunk_id for h in hits])
    excerpts: list[Excerpt] = []
    citations: list[dict] = []
    for i, h in enumerate(hits, start=1):
        excerpts.append(Excerpt(
            n=i, section_number=h.section_number, page=h.page,
            table_id=h.table_id,
            text=texts.get(h.chunk_id) or getattr(h, "text_preview", ""),
        ))
        citations.append({
            "n": i, "section": h.section_number,
            "page": h.page or None, "table_id": h.table_id,
            "chunk_id": h.chunk_id,
        })

    system, user = build_grounded_prompt(query, excerpts)
    provider = provider or get_provider(settings.llm_provider)
    model = model or settings.llm_model
    temperature = settings.llm_temperature if temperature is None else temperature
    max_tokens = max_tokens or settings.llm_max_tokens
    text = provider.generate(
        system, user, model=model, temperature=temperature, max_tokens=max_tokens,
    )
    return AnswerResult(
        query=query, text=text, refused=False,
        gate_outcome=str(decision.outcome), backend=backend,
        citations=citations, model=model,
    )
