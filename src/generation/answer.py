"""Grounded answer orchestration (Step 7/8) — the IO seam tying retrieval, the
evidence gate, and an LLM provider together.

Split into two reusable seams (mirrors the IO-vs-pure split across retrieval,
e.g. search_reranked vs apply_rerank):

    retrieve_and_gate(...)  -> AnswerContext   # retrieve + gate + citations, NO LLM
    build_grounded_answer(ctx, ...) -> AnswerResult  # generate from a non-REFUSE ctx

`generate_answer` composes the two and is behaviourally identical to before.
The split lets a caller (the Streamlit app, a future MCP server) render the
gate decision + sources WITHOUT an API key, then optionally generate from the
SAME hits — no second retrieval.

The evidence gate is the hallucination firewall: a REFUSE never reaches the
provider. Citations are drawn from the retrieval hits (provenance), NOT parsed
out of the model's text — a cited §section / table / page is always real.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from src.config import settings
from src.retrieval import (
    GateDecision,
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
class AnswerContext:
    """Retrieval + gate result for one query — the no-LLM half of the pipeline.
    Reusable by the 'sources + gate' view (needs no API key) and the generate
    path. `citations` are the provenance built from `hits`; `decision` is the
    gate's call (ANSWER / LOW_CONFIDENCE / REFUSE)."""
    query: str
    backend: str
    hits: list
    decision: GateDecision
    citations: list[dict]


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


def _citations_from_hits(hits) -> list[dict]:
    """Provenance for each hit: 1-based label + section / page / table / chunk.
    page 0 (the md sentinel) collapses to None — same rule as prompt.py."""
    return [
        {
            "n": i, "section": h.section_number, "page": h.page or None,
            "table_id": h.table_id, "chunk_id": h.chunk_id,
        }
        for i, h in enumerate(hits, start=1)
    ]


def retrieve_and_gate(
    session: Session,
    query: str,
    *,
    backend: str = "hybrid",
    mode: str | None = None,
    top_k: int = 5,
    source_format: str | None = None,
) -> AnswerContext:
    """Retrieve via the backend dispatch and run the evidence gate. No LLM, no
    API key — this is the 'sources + gate' half a frontend can show on its own.
    `mode` defaults to settings.gate_mode."""
    mode = mode or settings.gate_mode
    hits = _retrieve(
        session, query, backend=backend, top_k=top_k, source_format=source_format,
    )
    decision = gate_for_hits(session, query, hits, backend=backend, mode=mode)
    return AnswerContext(
        query=query, backend=backend, hits=list(hits),
        decision=decision, citations=_citations_from_hits(hits),
    )


def build_grounded_answer(
    session: Session,
    ctx: AnswerContext,
    *,
    provider: LLMProvider | None = None,
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> AnswerResult:
    """Generate a grounded answer from a non-REFUSE context.

    PRECONDITION: ctx.decision.outcome is not REFUSE — enforced with an explicit
    raise (not a strippable assert) because this is the hallucination firewall.
    Fetches FULL chunk text (the 240-char preview would starve the prompt),
    builds the grounded prompt, and calls the provider. provider/model/
    temperature/max_tokens default to the configured LLM (settings.llm_*).
    """
    if ctx.decision.outcome is GateOutcome.REFUSE:
        raise ValueError(
            "build_grounded_answer called on a REFUSE context; the gate is the "
            "hallucination firewall and must short-circuit before generation"
        )

    texts = fetch_full_texts(session, [h.chunk_id for h in ctx.hits])
    excerpts = [
        Excerpt(
            n=i, section_number=h.section_number, page=h.page,
            table_id=h.table_id,
            text=texts.get(h.chunk_id) or getattr(h, "text_preview", ""),
        )
        for i, h in enumerate(ctx.hits, start=1)
    ]
    system, user = build_grounded_prompt(ctx.query, excerpts)
    provider = provider or get_provider(settings.llm_provider)
    model = model or settings.llm_model
    temperature = settings.llm_temperature if temperature is None else temperature
    max_tokens = max_tokens or settings.llm_max_tokens
    text = provider.generate(
        system, user, model=model, temperature=temperature, max_tokens=max_tokens,
    )
    return AnswerResult(
        query=ctx.query, text=text, refused=False,
        gate_outcome=str(ctx.decision.outcome), backend=ctx.backend,
        citations=ctx.citations, model=model,
    )


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

    Composed from retrieve_and_gate + build_grounded_answer; behaviour is
    identical to the pre-split version. A gate REFUSE short-circuits before the
    provider is ever constructed or called.
    """
    ctx = retrieve_and_gate(
        session, query, backend=backend, mode=mode, top_k=top_k,
        source_format=source_format,
    )
    if ctx.decision.outcome is GateOutcome.REFUSE:
        return AnswerResult(
            query=query, text=REFUSAL_TEXT, refused=True,
            gate_outcome=str(ctx.decision.outcome), backend=backend,
            citations=[], model=None,
        )
    return build_grounded_answer(
        session, ctx, provider=provider, model=model,
        temperature=temperature, max_tokens=max_tokens,
    )
