"""Answer a question against the indexed corpus — grounded, gate-gated, cited.

Retrieves, runs the evidence gate, and (unless the gate refuses) asks the
configured LLM to answer using ONLY the retrieved excerpts. Prints the gate
decision, the answer (or the refusal), and the citations behind it.

    .venv/Scripts/python.exe scripts/answer.py \
        --query "What is the minimum output power for NR?" \
        --source-format tspec_md --backend hybrid
    ... --backend reranked --mode strict --top-k 5 --model claude-opus-4-8

Needs ANTHROPIC_API_KEY in the environment / .env (the only command here that
calls the LLM — retrieval + gate are offline).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.config import settings
from src.generation import generate_answer


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="the question to answer")
    parser.add_argument(
        "--backend", default="hybrid",
        choices=["sparse", "dense", "hybrid", "reranked"],
    )
    parser.add_argument(
        "--source-format", default=None, choices=["pdf_pymupdf", "tspec_md"],
        help="restrict retrieval to one corpus (avoids mixed-source contamination)",
    )
    parser.add_argument(
        "--mode", default=None, choices=["balanced", "strict", "permissive"],
        help=f"gate mode (default: settings.gate_mode = {settings.gate_mode})",
    )
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument(
        "--model", default=None,
        help=f"override the LLM model (default: {settings.llm_model})",
    )
    args = parser.parse_args()

    engine = create_engine(settings.db_url, future=True)
    with Session(engine) as session:
        result = generate_answer(
            session, args.query,
            backend=args.backend, mode=args.mode, top_k=args.top_k,
            source_format=args.source_format, model=args.model,
        )

    print(f"=== gate: {result.gate_outcome}  (backend={result.backend}) ===")
    if result.refused:
        print(result.text)
        return 0

    if result.text.strip():
        print(f"\n{result.text}\n")
    else:
        print("\n(model returned no text — possibly a safety refusal or an "
              "empty completion; nothing was hallucinated)\n")
    print(f"--- citations ({result.model}) ---")
    for c in result.citations:
        loc = f"§{c['section']}"
        if c["table_id"]:
            loc += f", Table {c['table_id']}"
        if c["page"]:
            loc += f", p.{c['page']}"
        print(f"  [{c['n']}] {loc}  (chunk {c['chunk_id']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
