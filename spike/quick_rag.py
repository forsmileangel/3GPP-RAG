"""
Phase 0 spike — retrieval-only RAG over a single TS 38.521-1 section.

Goal: answer "does vector search reliably find the right chunk for my real
questions?" before committing to Phase A.

This script does NOT call any LLM — it stops at retrieval and prints the
top-K chunks. The "chunks → natural language answer" step is done
interactively by Claude Code in the parent conversation.

Resilience:
- PDF extraction + chunking is cached to spike/extracted.json (key = PDF
  mtime + chunk params + section). Re-run skips this step.
- Chroma vectors persist to data/db/chroma_spike/ and a state file tracks
  the embedding fingerprint (chunks + model). Same chunks + same model =>
  reuse, no re-embed.
- HuggingFace caches BGE-M3 in ~/.cache/huggingface/ automatically.
- Net effect: 1st run = slow (model download + embed); 2nd run with same
  inputs = seconds.

Usage:
    cd 3gpp-rag/
    .venv/Scripts/python.exe spike/quick_rag.py
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path

import fitz  # PyMuPDF
import yaml
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings


# --------------------------------------------------------------------------
# Config — keep this file self-contained on purpose (spike is throwaway).
# --------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "data" / "raw" / "ts_138521-01_v17_05_00.pdf"
QUESTIONS_PATH = ROOT / "spike" / "questions.yaml"
OUTPUT_PATH = ROOT / "spike" / "last_run.json"

EXTRACT_CACHE_PATH = ROOT / "spike" / "extracted.json"
CHROMA_PATH = ROOT / "data" / "db" / "chroma_spike"
STATE_PATH = ROOT / "data" / "db" / "spike_state.json"

# Section to ingest. The PDF is TS 38.521-1 (FR1 UE conformance — radio Tx/Rx).
# We narrow to a clearly-bounded chapter via PDF bookmark TOC (NOT regex on
# body text — that would catch the table-of-contents entry instead of the
# real section).
TARGET_SECTION = "6.2"  # Default; flip to "6.3" to reproduce the q04/q05 verification described in reality_check.md.

# Embedding model. BGE-M3 (~2.3 GB) is the target — multilingual, long-context,
# strong on technical text. MiniLM is kept as fallback only in case BGE-M3
# fails to load (e.g. network really dies). HF should resume the partial
# download from ~/.cache/huggingface/hub/.../*.incomplete.
EMBED_MODEL_PRIMARY = "BAAI/bge-m3"
EMBED_MODEL_FALLBACK = "sentence-transformers/all-MiniLM-L6-v2"

# Naive char-based chunking on purpose: we want to see baseline retrieval
# quality without smart splitting hiding the truth.
CHUNK_CHARS = 800
CHUNK_OVERLAP = 150

TOP_K = 5
COLLECTION_NAME = "spike"


# --------------------------------------------------------------------------
# Data shapes
# --------------------------------------------------------------------------

@dataclass
class Chunk:
    chunk_id: str
    page: int           # 1-indexed in the PDF
    text: str
    char_offset: int    # offset within section text


@dataclass
class Hit:
    chunk_id: str
    page: int
    distance: float
    text_preview: str
    full_text: str


@dataclass
class QueryResult:
    qid: str
    question: str
    expected_section: str | None
    expected_keywords: list[str]
    hits: list[Hit]


# --------------------------------------------------------------------------
# Section locating via PDF bookmarks (not regex)
# --------------------------------------------------------------------------

def _matches_section_token(title: str, section_num: str) -> bool:
    """`title` is a TOC entry like '6.2 Transmit power'. We want the leading
    token to equal `section_num` exactly (so '6.2' matches '6.2 ...' but
    not '6.20 ...' or '16.2 ...')."""
    parts = title.strip().split(maxsplit=1)
    return len(parts) >= 1 and parts[0] == section_num


def find_section_page_range(doc: fitz.Document, section_num: str) -> tuple[int, int]:
    """Return (start_page_0idx, end_page_0idx) inclusive, using the PDF's
    bookmark table-of-contents. Includes all sub-sections (§6.2.x.y) by
    extending until the next entry at the same or shallower depth."""
    toc = doc.get_toc()
    if not toc:
        raise SystemExit(
            f"PDF has no bookmark TOC — cannot locate §{section_num} reliably. "
            "Falling back to regex on body text would re-introduce the "
            "TOC-entry-vs-real-section bug."
        )

    target_idx = None
    for i, (_level, title, _page) in enumerate(toc):
        if _matches_section_token(title, section_num):
            target_idx = i
            break
    if target_idx is None:
        raise SystemExit(f"§{section_num} not found in PDF bookmarks")

    target_level, target_title, target_page = toc[target_idx]
    start_page = target_page - 1  # to 0-indexed

    end_page = doc.page_count - 1
    for level, _title, page in toc[target_idx + 1:]:
        if level <= target_level:
            end_page = page - 2  # page before next sibling, 0-indexed
            if end_page < start_page:
                end_page = start_page
            break

    print(
        f"[locate] §{section_num} ('{target_title.strip()}') "
        f"-> pages {start_page + 1}..{end_page + 1} "
        f"({end_page - start_page + 1} pages)",
        file=sys.stderr,
    )
    return start_page, end_page


def extract_pages_text(doc: fitz.Document, start_page: int, end_page: int) -> tuple[str, list[int]]:
    """Concatenate text from pages [start..end]. Return (text, page_offsets)
    where page_offsets[i] is the char offset of the i-th included page's
    start within the returned text."""
    parts: list[str] = []
    page_offsets: list[int] = []
    cursor = 0
    for p_idx in range(start_page, end_page + 1):
        page = doc[p_idx]
        t = page.get_text("text")
        page_offsets.append(cursor)
        parts.append(t)
        cursor += len(t) + 1  # +1 for joining "\n"
    return "\n".join(parts), page_offsets


# --------------------------------------------------------------------------
# Chunking
# --------------------------------------------------------------------------

def chunk_text(
    text: str,
    page_offsets: list[int],
    page_start_1idx: int,
) -> list[Chunk]:
    """Char-window chunker. `page_offsets[i]` is the i-th included page's
    text-start offset within `text`; `page_start_1idx` is the 1-indexed
    PDF page number of the first included page."""
    chunks: list[Chunk] = []
    n = len(text)
    i = 0
    idx = 0
    while i < n:
        end = min(i + CHUNK_CHARS, n)
        body = text[i:end].strip()
        if body:
            page = _offset_to_page(i, page_offsets, page_start_1idx)
            chunks.append(Chunk(
                chunk_id=f"c{idx:04d}",
                page=page,
                text=body,
                char_offset=i,
            ))
            idx += 1
        if end >= n:
            break
        i = end - CHUNK_OVERLAP
    return chunks


def _offset_to_page(offset: int, page_offsets: list[int], page_start_1idx: int) -> int:
    last_idx = 0
    for i, off in enumerate(page_offsets):
        if off > offset:
            break
        last_idx = i
    return page_start_1idx + last_idx


# --------------------------------------------------------------------------
# Cached extract+chunk
# --------------------------------------------------------------------------

def extract_and_chunk_cached(pdf_path: Path) -> list[Chunk]:
    pdf_stat = pdf_path.stat()
    cache_key = {
        "pdf_path": str(pdf_path),
        "pdf_mtime": pdf_stat.st_mtime,
        "pdf_size": pdf_stat.st_size,
        "section": TARGET_SECTION,
        "chunk_chars": CHUNK_CHARS,
        "chunk_overlap": CHUNK_OVERLAP,
    }

    if EXTRACT_CACHE_PATH.exists():
        try:
            blob = json.loads(EXTRACT_CACHE_PATH.read_text(encoding="utf-8"))
            if blob.get("key") == cache_key:
                chunks = [Chunk(**c) for c in blob["chunks"]]
                print(
                    f"[cache] Extract cache HIT ({len(chunks)} chunks reused)",
                    file=sys.stderr,
                )
                return chunks
            print("[cache] Extract cache key mismatch — regenerating", file=sys.stderr)
        except Exception as e:
            print(f"[cache] Extract cache unreadable: {e} — regenerating", file=sys.stderr)

    doc = fitz.open(pdf_path)
    print(f"[extract] PDF has {doc.page_count} pages", file=sys.stderr)
    start_page, end_page = find_section_page_range(doc, TARGET_SECTION)
    text, page_offsets = extract_pages_text(doc, start_page, end_page)
    doc.close()

    chunks = chunk_text(text, page_offsets, start_page + 1)
    print(
        f"[extract] Section text {len(text)} chars -> {len(chunks)} chunks "
        f"(~{CHUNK_CHARS} chars each)",
        file=sys.stderr,
    )

    EXTRACT_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXTRACT_CACHE_PATH.write_text(
        json.dumps({"key": cache_key, "chunks": [asdict(c) for c in chunks]},
                   indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"[cache] Wrote {EXTRACT_CACHE_PATH.name}", file=sys.stderr)
    return chunks


# --------------------------------------------------------------------------
# Embedding + persistent Chroma
# --------------------------------------------------------------------------

def load_embedder() -> tuple[SentenceTransformer, str]:
    for name in (EMBED_MODEL_PRIMARY, EMBED_MODEL_FALLBACK):
        try:
            print(f"[embed] Loading {name} ...", file=sys.stderr)
            t0 = time.time()
            model = SentenceTransformer(name)
            print(f"[embed] Loaded in {time.time() - t0:.1f}s", file=sys.stderr)
            return model, name
        except Exception as e:
            print(f"[embed] Failed to load {name}: {e}", file=sys.stderr)
    raise SystemExit("No embedding model could be loaded")


def _fingerprint(chunks: list[Chunk], model_name: str) -> str:
    h = hashlib.sha256()
    h.update(model_name.encode())
    h.update(str(len(chunks)).encode())
    for c in chunks:
        h.update(c.chunk_id.encode())
        h.update(c.text[:200].encode("utf-8", errors="replace"))
    return h.hexdigest()[:16]


def get_or_build_collection(
    chunks: list[Chunk],
    embedder: SentenceTransformer,
    model_name: str,
) -> chromadb.Collection:
    fp = _fingerprint(chunks, model_name)
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH),
        settings=Settings(anonymized_telemetry=False),
    )

    last_state: dict | None = None
    if STATE_PATH.exists():
        try:
            last_state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            last_state = None

    if last_state and last_state.get("fingerprint") == fp:
        try:
            coll = client.get_collection(name=COLLECTION_NAME)
            if coll.count() == len(chunks):
                print(
                    f"[index] Embedding cache HIT (fp={fp}, "
                    f"{coll.count()} vectors reused)",
                    file=sys.stderr,
                )
                return coll
            print(
                f"[index] Fingerprint matched but count mismatch "
                f"({coll.count()} vs {len(chunks)}) — rebuilding",
                file=sys.stderr,
            )
        except Exception as e:
            print(f"[index] Could not re-open collection: {e} — rebuilding", file=sys.stderr)

    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    coll = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    print(f"[index] Embedding {len(chunks)} chunks (fp={fp}) ...", file=sys.stderr)
    t0 = time.time()
    embeddings = embedder.encode(
        [c.text for c in chunks], show_progress_bar=False
    ).tolist()
    print(f"[index] Embedded in {time.time() - t0:.1f}s", file=sys.stderr)

    coll.add(
        ids=[c.chunk_id for c in chunks],
        documents=[c.text for c in chunks],
        embeddings=embeddings,
        metadatas=[{"page": c.page, "char_offset": c.char_offset} for c in chunks],
    )
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(
        json.dumps({
            "fingerprint": fp,
            "model": model_name,
            "n_chunks": len(chunks),
            "chunk_chars": CHUNK_CHARS,
            "chunk_overlap": CHUNK_OVERLAP,
            "section": TARGET_SECTION,
        }, indent=2),
        encoding="utf-8",
    )
    return coll


# --------------------------------------------------------------------------
# Querying
# --------------------------------------------------------------------------

DEFAULT_QUESTIONS = [
    {"qid": "q01",
     "question": "What is the maximum output power tolerance for FR1 PC3 UE?",
     "expected_section": "6.2.1",
     "expected_keywords": ["23", "dBm", "tolerance"]},
    {"qid": "q02",
     "question": "How is the test procedure defined for UE maximum output power across power classes?",
     "expected_section": "6.2.1",
     "expected_keywords": ["Tx power", "test procedure", "PC2", "PC3"]},
    {"qid": "q03",
     "question": "What are the test conditions and channel bandwidth for inner / outer maximum output power?",
     "expected_section": "6.2.1.3",
     "expected_keywords": ["channel bandwidth", "inner", "outer"]},
    {"qid": "q04",
     "question": "Define UE output power dynamics — minimum output power requirement.",
     "expected_section": "6.2.4",
     "expected_keywords": ["minimum output power", "-40", "dBm"]},
    {"qid": "q05",
     "question": "What is the transmit OFF power requirement for NR FR1 UE?",
     "expected_section": "6.2.5",
     "expected_keywords": ["transmit OFF", "OFF power"]},
]


def load_questions() -> list[dict]:
    if not QUESTIONS_PATH.exists():
        print(f"[questions] {QUESTIONS_PATH.name} missing — using built-in defaults", file=sys.stderr)
        return DEFAULT_QUESTIONS
    with QUESTIONS_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_query(coll: chromadb.Collection, embedder: SentenceTransformer, q: dict) -> QueryResult:
    qvec = embedder.encode([q["question"]]).tolist()
    res = coll.query(query_embeddings=qvec, n_results=TOP_K)
    hits: list[Hit] = []
    for doc, meta, dist, hid in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0], res["ids"][0]
    ):
        hits.append(Hit(
            chunk_id=hid,
            page=int(meta.get("page", -1)),
            distance=float(dist),
            text_preview=doc[:300].replace("\n", " "),
            full_text=doc,
        ))
    return QueryResult(
        qid=q["qid"],
        question=q["question"],
        expected_section=q.get("expected_section"),
        expected_keywords=q.get("expected_keywords", []),
        hits=hits,
    )


def print_result(qr: QueryResult) -> None:
    print(f"\n{'=' * 78}")
    print(f"[{qr.qid}] {qr.question}")
    print(f"  expected: section ~ {qr.expected_section}  kws={qr.expected_keywords}")
    print(f"{'=' * 78}")
    for rank, h in enumerate(qr.hits, 1):
        kw_hits = [k for k in qr.expected_keywords if k.lower() in h.full_text.lower()]
        marker = "MATCH" if kw_hits else "    "
        print(f"  #{rank} {marker}  page={h.page:>4}  dist={h.distance:.3f}  {h.chunk_id}")
        if kw_hits:
            print(f"        keywords matched: {kw_hits}")
        print(f"        {h.text_preview}")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    if not PDF_PATH.exists():
        raise SystemExit(f"PDF not found: {PDF_PATH}")

    chunks = extract_and_chunk_cached(PDF_PATH)
    if not chunks:
        raise SystemExit("No chunks produced")

    embedder, model_name = load_embedder()
    coll = get_or_build_collection(chunks, embedder, model_name)

    questions = load_questions()
    results: list[QueryResult] = []
    for q in questions:
        qr = run_query(coll, embedder, q)
        print_result(qr)
        results.append(qr)

    summary = {
        "embedding_model": model_name,
        "section": TARGET_SECTION,
        "chunk_chars": CHUNK_CHARS,
        "chunk_overlap": CHUNK_OVERLAP,
        "n_chunks": len(chunks),
        "top_k": TOP_K,
        "questions": [asdict(r) for r in results],
    }
    OUTPUT_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\n[done] Wrote {OUTPUT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
