"""LLM provider abstraction for grounded answer generation (Step 7).

A thin, pluggable seam so the RAG answer path is not bound to one vendor —
Tier 1 work explicitly wants to benchmark different LLMs (CLAUDE.md §5). A
concrete provider implements one method, ``generate(system, user, ...) -> str``;
``get_provider(name)`` resolves one by config name. Only AnthropicProvider
ships now; openai / ollama are intentional empty slots.

The Anthropic SDK is imported LAZILY inside the client factory, so importing
this module (and the rest of src.generation) never requires the ``anthropic``
package — only actually calling the provider does. Mirrors how rerank.py
defers its heavy ``transformers`` import; keeps the unit tests offline.

⚠ SDK currency (CLAUDE.md §4.6): the Messages API usage here was verified
against the bundled claude-api reference (cached 2026-06-04), not written from
older training memory. The load-bearing facts: ``anthropic.Anthropic()`` reads
``ANTHROPIC_API_KEY`` from the environment; ``system`` is a TOP-LEVEL parameter
(not a message role); ``max_tokens`` is required; the response ``.content`` is
a list of blocks and the answer text is the ``.text`` of the ``type=="text"``
block(s) (thinking blocks, if any, carry a different type and are skipped).
Re-verify if the SDK's request/response shape changes.
"""

from __future__ import annotations

from typing import Protocol


class LLMProvider(Protocol):
    """Structural type for a chat-completion provider: turn a (system, user)
    pair into plain text. Knobs are keyword-only so call sites stay explicit
    and the orchestrator can pass config straight through."""

    def generate(
        self,
        system: str,
        user: str,
        *,
        model: str,
        temperature: float | None,
        max_tokens: int,
    ) -> str: ...


# Model families that REJECT sampling parameters (temperature / top_p / top_k
# -> HTTP 400): Fable 5 / Mythos 5 / Opus 4.8 / Opus 4.7. Because llm_model is
# config-driven (the Tier-1 cross-LLM-benchmark goal), the provider must drop
# temperature for these or a model switch would start 400-ing. Source: bundled
# claude-api reference / model-migration guide (cached 2026-06-04); re-verify
# if a newer model changes the sampling-param contract (§4.6).
_NO_SAMPLING_PREFIXES = (
    "claude-fable-",
    "claude-mythos-",
    "claude-opus-4-8",
    "claude-opus-4-7",
)


def accepts_temperature(model: str) -> bool:
    """Whether the model accepts a ``temperature`` argument (see above)."""
    return not model.startswith(_NO_SAMPLING_PREFIXES)


# Cache clients by api_key so repeated generate() calls reuse one HTTP client
# (same module-cache pattern as dense._model_cache). None key = resolve the key
# from the environment.
_client_cache: dict[str | None, object] = {}


def _get_client(api_key: str | None):
    if api_key not in _client_cache:
        import anthropic  # lazy: importing this module must not require the SDK

        _client_cache[api_key] = (
            anthropic.Anthropic(api_key=api_key)
            if api_key
            else anthropic.Anthropic()
        )
    return _client_cache[api_key]


class AnthropicProvider:
    """LLMProvider backed by the Anthropic Messages API. The API key resolves
    from ANTHROPIC_API_KEY (env / .env) unless one is passed explicitly."""

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key

    def generate(
        self,
        system: str,
        user: str,
        *,
        model: str,
        temperature: float | None,
        max_tokens: int,
    ) -> str:
        client = _get_client(self._api_key)
        kwargs: dict = {
            "model": model,
            "max_tokens": max_tokens,            # required by the API
            "system": system,                    # TOP-LEVEL, not a message role
            "messages": [{"role": "user", "content": user}],
        }
        if temperature is not None and accepts_temperature(model):
            kwargs["temperature"] = temperature
        message = client.messages.create(**kwargs)
        # .content is a list of blocks; concatenate text blocks, skip the rest
        # (e.g. thinking blocks). A safety-classifier refusal yields no text
        # block -> "" (the orchestrator records the gate outcome regardless).
        return "".join(
            block.text for block in message.content if block.type == "text"
        ).strip()


_PROVIDERS = {
    "anthropic": AnthropicProvider,
    # "openai": OpenAIProvider,   # intentional slot — not implemented (Tier 1 = Claude)
    # "ollama": OllamaProvider,
}


def get_provider(name: str, **kwargs) -> LLMProvider:
    """Resolve a provider by config name. Unknown name raises ValueError
    (mirrors rerank._get_reranker / GateThresholds.for_mode)."""
    factory = _PROVIDERS.get(name)
    if factory is None:
        raise ValueError(
            f"unknown LLM provider {name!r}; valid: {sorted(_PROVIDERS)}"
        )
    return factory(**kwargs)
