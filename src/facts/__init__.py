"""Rule-based fact layer (Step 6).

Extracts structured numeric / table-cell facts from already-parsed TABLE
chunks so numeric/table-lookup questions can hit precise values before the
fuzzy chunk fallback. Rule-based MVP — no LLM (deferred pending the M6
measurement of whether rule-based alone lifts citation to >=0.9).

    extract_facts_from_chunk / FactRecord / ChunkView  — pure extraction
    emit_facts / FactEmitStats                         — idempotent persist
    search_facts / FactHit                             — retrieval over facts_fts
"""

from .emit import FactEmitStats, emit_facts, load_table_chunks
from .extractor import (
    ChunkView,
    FactRecord,
    extract_facts_from_chunk,
    fact_to_text,
)
from .search import FactHit, search_facts

__all__ = [
    "ChunkView",
    "FactEmitStats",
    "FactHit",
    "FactRecord",
    "emit_facts",
    "extract_facts_from_chunk",
    "fact_to_text",
    "load_table_chunks",
    "search_facts",
]
