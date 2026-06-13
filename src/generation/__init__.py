"""Answer generation layer (Step 7): grounded, gate-gated, cited answers.

generate_answer() is the orchestrator; build_grounded_prompt() the pure prompt
builder; providers expose a pluggable LLMProvider seam (AnthropicProvider by
default — Tier 1 benchmarks across LLMs, see CLAUDE.md §5). The evidence gate
(src/retrieval/gate.py) decides ANSWER / LOW_CONFIDENCE / REFUSE upstream of any
LLM call, so a REFUSE never reaches the provider.
"""

from .answer import AnswerResult, generate_answer
from .prompt import (
    REFUSAL_TEXT,
    Excerpt,
    build_grounded_prompt,
    format_excerpt,
)
from .providers import (
    AnthropicProvider,
    LLMProvider,
    accepts_temperature,
    get_provider,
)

__all__ = [
    "AnswerResult",
    "AnthropicProvider",
    "Excerpt",
    "LLMProvider",
    "REFUSAL_TEXT",
    "accepts_temperature",
    "build_grounded_prompt",
    "format_excerpt",
    "generate_answer",
    "get_provider",
]
