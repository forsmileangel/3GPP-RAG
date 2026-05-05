"""Stage 3 ingestion: embed pending chunks into Chroma.

Run after `chunk_sections.py`. Idempotent — re-runs only embed chunks
where vector_id IS NULL. Pass `--refresh-collection` to wipe the Chroma
collection and re-embed all chunks (slow on first run because BGE-M3
must reload).

    .venv/Scripts/python.exe scripts/embed_chunks.py
    .venv/Scripts/python.exe scripts/embed_chunks.py --batch-size 16
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session

from src.config import settings
from src.ingestion.embedder import (
    DEFAULT_BATCH,
    DEFAULT_COLLECTION,
    DEFAULT_MODEL,
    embed_pending_chunks,
)
from src.models import Chunk


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH)
    parser.add_argument(
        "--refresh-collection",
        action="store_true",
        help="Drop Chroma collection + clear chunks.vector_id before embedding",
    )
    args = parser.parse_args()

    engine = create_engine(settings.db_url, future=True)

    if args.refresh_collection:
        # Drop Chroma collection
        import chromadb
        from chromadb.config import Settings as ChromaSettings

        client = chromadb.PersistentClient(
            path=str(settings.chroma_path),
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        try:
            client.delete_collection(name=args.collection)
            print(f"[refresh] Dropped Chroma collection {args.collection!r}")
        except Exception as e:
            print(f"[refresh] Could not drop collection (ok if missing): {e}")
        # Clear vector_id so embedder re-processes
        with Session(engine) as s, s.begin():
            s.execute(update(Chunk).values(vector_id=None, embedding_model=None))
        print("[refresh] Cleared all chunks.vector_id / embedding_model")

    with Session(engine) as session, session.begin():
        result = embed_pending_chunks(
            session,
            model_name=args.model,
            collection_name=args.collection,
            batch_size=args.batch_size,
        )

    print(
        f"[embed] embedded={result.embedded}  skipped={result.skipped}  "
        f"chroma_total={result.total_in_collection}  model={result.model_name}"
    )
    print("OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
