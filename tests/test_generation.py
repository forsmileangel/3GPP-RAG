"""Unit tests for src/generation/ — prompt building, provider seam, and the
generate_answer orchestrator. Fully offline: the Anthropic SDK is never
imported (provider tests pre-seed the client cache with a fake; orchestrator
tests inject a fake provider), and retrieval/gate are monkeypatched, so no DB
and no network.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace

import pytest

from src.config import settings
from src.generation import (
    REFUSAL_TEXT,
    AnthropicProvider,
    Excerpt,
    accepts_temperature,
    build_grounded_prompt,
    format_excerpt,
    get_provider,
)
from src.generation import answer as answer_mod
from src.generation import providers as providers_mod
from src.retrieval import GateOutcome


# ----------------------------------------------------------------- prompt

def test_build_grounded_prompt_numbered_and_grounded():
    exs = [
        Excerpt(1, "6.3.1", 0, None, "Minimum output power is -40 dBm."),
        Excerpt(2, "6.2.1", 12, "6.2.1.5-1", "Max power 23 dBm."),
    ]
    system, user = build_grounded_prompt("What is min power?", exs)
    # system carries the grounding contract
    assert "ONLY" in system and "cite" in system.lower()
    # user = question + numbered excerpts with their texts and locators
    assert "Question: What is min power?" in user
    assert "[1]" in user and "[2]" in user
    assert "Minimum output power is -40 dBm." in user
    assert "Max power 23 dBm." in user
    assert "§6.3.1" in user and "§6.2.1" in user
    assert "Table 6.2.1.5-1" in user
    assert "p.12" in user
    assert "p.0" not in user  # md page sentinel must not leak into the locator


def test_format_excerpt_omits_zero_page_and_none_table():
    s = format_excerpt(Excerpt(1, "6.3.1", 0, None, "body"))
    assert s.startswith("[1] (§6.3.1)")
    assert "p." not in s and "Table" not in s


# --------------------------------------------------------------- providers

def test_accepts_temperature_by_family():
    # sampling-param families accept temperature...
    assert accepts_temperature("claude-sonnet-4-6") is True
    assert accepts_temperature("claude-opus-4-6") is True
    assert accepts_temperature("claude-haiku-4-5") is True
    # ...the opus-4-7/4-8 + fable/mythos families reject it (would 400)
    assert accepts_temperature("claude-opus-4-7") is False
    assert accepts_temperature("claude-opus-4-8") is False
    assert accepts_temperature("claude-fable-5") is False
    assert accepts_temperature("claude-mythos-5") is False


def test_get_provider_resolves_and_rejects():
    assert isinstance(get_provider("anthropic"), AnthropicProvider)
    with pytest.raises(ValueError):
        get_provider("nope")


class _FakeBlock:
    def __init__(self, type_: str, text: str = "") -> None:
        self.type = type_
        self.text = text


class _FakeMessages:
    def __init__(self, recorder: dict) -> None:
        self._rec = recorder

    def create(self, **kwargs):
        self._rec.clear()
        self._rec.update(kwargs)
        # a thinking block (skipped) + two text blocks (concatenated)
        return SimpleNamespace(content=[
            _FakeBlock("thinking", ""),
            _FakeBlock("text", "Answer "),
            _FakeBlock("text", "body.\n"),
        ])


class _FakeClient:
    def __init__(self, recorder: dict) -> None:
        self.messages = _FakeMessages(recorder)


def test_anthropic_provider_builds_kwargs_and_extracts_text(monkeypatch):
    rec: dict = {}
    monkeypatch.setitem(providers_mod._client_cache, None, _FakeClient(rec))
    out = AnthropicProvider().generate(
        "SYS", "USR", model="claude-sonnet-4-6", temperature=0.0, max_tokens=512,
    )
    # text blocks concatenated and stripped; thinking block skipped
    assert out == "Answer body."
    # system is a TOP-LEVEL param, not a message role
    assert rec["system"] == "SYS"
    assert rec["messages"] == [{"role": "user", "content": "USR"}]
    assert rec["max_tokens"] == 512
    assert rec["model"] == "claude-sonnet-4-6"
    assert rec["temperature"] == 0.0  # sonnet accepts it


def test_anthropic_provider_drops_temperature_for_rejecting_model(monkeypatch):
    rec: dict = {}
    monkeypatch.setitem(providers_mod._client_cache, None, _FakeClient(rec))
    AnthropicProvider().generate(
        "S", "U", model="claude-opus-4-8", temperature=0.0, max_tokens=16,
    )
    assert "temperature" not in rec  # would 400 on opus-4-8


# ----------------------------------------------------------- orchestrator

@dataclass
class _FakeHit:
    chunk_id: int
    section_number: str
    table_id: str | None
    page: int
    text_preview: str = "preview"


def _gate(outcome: GateOutcome):
    return SimpleNamespace(outcome=outcome)


class _RecordingProvider:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def generate(self, system, user, *, model, temperature, max_tokens):
        self.calls.append({
            "system": system, "user": user, "model": model,
            "temperature": temperature, "max_tokens": max_tokens,
        })
        return "GENERATED ANSWER [1]"


class _ExplodingProvider:
    def generate(self, *a, **k):
        raise AssertionError("provider must NOT be called on a gate REFUSE")


def test_generate_answer_refuse_skips_llm(monkeypatch):
    hits = [_FakeHit(1, "6.3.1", None, 0)]
    monkeypatch.setitem(
        answer_mod._RETRIEVERS, "hybrid",
        lambda s, q, *, top_k, source_format: hits,
    )
    monkeypatch.setattr(
        answer_mod, "gate_for_hits", lambda *a, **k: _gate(GateOutcome.REFUSE),
    )
    res = answer_mod.generate_answer(
        None, "Q?", backend="hybrid", provider=_ExplodingProvider(),
    )
    assert res.refused is True
    assert res.text == REFUSAL_TEXT
    assert res.citations == []
    assert res.model is None
    assert res.gate_outcome == "refuse"


def test_generate_answer_answer_path_cites_hits(monkeypatch):
    hits = [
        _FakeHit(1, "6.3.1", None, 0),
        _FakeHit(2, "6.2.1", "6.2.1.5-1", 12),
    ]
    monkeypatch.setitem(
        answer_mod._RETRIEVERS, "hybrid",
        lambda s, q, *, top_k, source_format: hits,
    )
    monkeypatch.setattr(
        answer_mod, "gate_for_hits", lambda *a, **k: _gate(GateOutcome.ANSWER),
    )
    monkeypatch.setattr(
        answer_mod, "fetch_full_texts",
        lambda s, ids: {1: "full text one", 2: "full text two"},
    )
    prov = _RecordingProvider()
    res = answer_mod.generate_answer(
        None, "Q?", backend="hybrid", provider=prov, model="claude-sonnet-4-6",
    )
    assert res.refused is False
    assert res.text == "GENERATED ANSWER [1]"
    assert res.gate_outcome == "answer"
    assert res.model == "claude-sonnet-4-6"
    assert res.backend == "hybrid"
    # citations are provenance copied from the hits (page 0 -> None), not parsed
    assert res.citations == [
        {"n": 1, "section": "6.3.1", "page": None, "table_id": None, "chunk_id": 1},
        {"n": 2, "section": "6.2.1", "page": 12, "table_id": "6.2.1.5-1", "chunk_id": 2},
    ]
    # the provider received the FULL texts as numbered excerpts + config defaults
    user = prov.calls[0]["user"]
    assert "full text one" in user and "full text two" in user
    assert "[1]" in user and "[2]" in user
    assert prov.calls[0]["temperature"] == settings.llm_temperature
    assert prov.calls[0]["max_tokens"] == settings.llm_max_tokens


def test_generate_answer_low_confidence_still_generates(monkeypatch):
    hits = [_FakeHit(1, "6.3.1", None, 0)]
    monkeypatch.setitem(
        answer_mod._RETRIEVERS, "hybrid",
        lambda s, q, *, top_k, source_format: hits,
    )
    monkeypatch.setattr(
        answer_mod, "gate_for_hits",
        lambda *a, **k: _gate(GateOutcome.LOW_CONFIDENCE),
    )
    monkeypatch.setattr(answer_mod, "fetch_full_texts", lambda s, ids: {1: "txt"})
    prov = _RecordingProvider()
    res = answer_mod.generate_answer(None, "Q?", backend="hybrid", provider=prov)
    assert res.refused is False
    assert res.gate_outcome == "low_confidence"
    assert len(prov.calls) == 1


def test_generate_answer_unknown_backend_raises():
    with pytest.raises(ValueError):
        answer_mod.generate_answer(None, "Q?", backend="bogus")


# ----------------------------------------------------- seams (Step 8 refactor)

def test_retrieve_and_gate_builds_context(monkeypatch):
    hits = [
        _FakeHit(1, "6.3.1", None, 0),
        _FakeHit(2, "6.2.1", "6.2.1.5-1", 12),
    ]
    monkeypatch.setitem(
        answer_mod._RETRIEVERS, "hybrid",
        lambda s, q, *, top_k, source_format: hits,
    )
    monkeypatch.setattr(
        answer_mod, "gate_for_hits", lambda *a, **k: _gate(GateOutcome.ANSWER),
    )
    ctx = answer_mod.retrieve_and_gate(None, "Q?", backend="hybrid")
    assert ctx.query == "Q?" and ctx.backend == "hybrid"
    assert ctx.decision.outcome is GateOutcome.ANSWER
    assert ctx.hits == hits
    assert ctx.citations == [
        {"n": 1, "section": "6.3.1", "page": None, "table_id": None, "chunk_id": 1},
        {"n": 2, "section": "6.2.1", "page": 12, "table_id": "6.2.1.5-1", "chunk_id": 2},
    ]


def test_build_grounded_answer_generates_from_context(monkeypatch):
    hits = [_FakeHit(1, "6.3.1", None, 0)]
    monkeypatch.setattr(
        answer_mod, "fetch_full_texts", lambda s, ids: {1: "the full chunk text"},
    )
    ctx = answer_mod.AnswerContext(
        query="Q?", backend="hybrid", hits=hits,
        decision=_gate(GateOutcome.ANSWER),
        citations=[{"n": 1, "section": "6.3.1", "page": None,
                    "table_id": None, "chunk_id": 1}],
    )
    prov = _RecordingProvider()
    res = answer_mod.build_grounded_answer(None, ctx, provider=prov)
    assert res.refused is False
    assert res.text == "GENERATED ANSWER [1]"
    assert res.citations == ctx.citations
    assert res.backend == "hybrid" and res.gate_outcome == "answer"
    assert "the full chunk text" in prov.calls[0]["user"]


def test_build_grounded_answer_rejects_refuse_context():
    # The firewall: generating from a REFUSE context must be impossible.
    ctx = answer_mod.AnswerContext(
        query="Q?", backend="hybrid", hits=[],
        decision=_gate(GateOutcome.REFUSE), citations=[],
    )
    with pytest.raises(ValueError):
        answer_mod.build_grounded_answer(None, ctx, provider=_ExplodingProvider())
