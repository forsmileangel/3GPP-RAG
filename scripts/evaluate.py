"""Week 2 出口 benchmark — retrieval-only evaluation.

For every question in data/eval/test_questions.yaml:
  - run sparse (FTS5) retrieval
  - run dense (BGE-M3 → Chroma) retrieval
  - compute per-question metrics:
      hit@5     — does any top-5 chunk live in expected_section's subtree?
      coverage  — fraction of expected_keywords found in any top-5 chunk
      sec_drift — top-1's section_number (so q04/q05 drifting back to §6.2
                  vs staying in §6.3.x is visible at a glance)
  - aggregate hit@5 across all questions
  - emit a markdown report to data/eval/last_eval.md (also stdout)

This is the Week 2 benchmark gate:
  - hit@5 ≥ 8/10 across both sparse & dense (independently)
  - q04 / q05 must surface §6.3.x at top-K, NOT drift to §6.2
  - keyword coverage reported with explicit numerator/denominator
    (not the spike's "at least one keyword" hand-wave)

Usage:
    .venv/Scripts/python.exe scripts/evaluate.py
    .venv/Scripts/python.exe scripts/evaluate.py --top-k 10
    .venv/Scripts/python.exe scripts/evaluate.py --backend sparse,dense
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dataclasses import dataclass

import yaml
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.config import settings
from src.models import Section
from src.retrieval import search_dense, search_sparse


@dataclass
class QuestionMetrics:
    qid: str
    backend: str
    hit_at_k: bool                # any top-K chunk in expected_section subtree
    keyword_coverage: float       # 0..1
    keywords_found: list[str]
    keywords_missing: list[str]
    top1_section: str | None
    top1_page: int | None
    top1_table_id: str | None
    top_chunk_summaries: list[str]


def _build_section_subtree(session: Session) -> dict[str, set[str]]:
    """Map section_number -> set of section_numbers that are it OR its
    descendants. Used to score 'is this hit in the expected subtree?'."""
    sections = list(session.execute(select(Section)).scalars())
    by_id = {s.section_id: s for s in sections}

    descendants: dict[int, set[int]] = {s.section_id: {s.section_id} for s in sections}
    # Bottom-up roll-up: for each section, walk parents adding self.
    for s in sections:
        cur = s
        while cur.parent_id is not None:
            descendants[cur.parent_id].add(s.section_id)
            cur = by_id.get(cur.parent_id)
            if cur is None:
                break

    return {
        s.section_number: {by_id[d].section_number for d in descendants[s.section_id]}
        for s in sections
    }


def _evaluate_question(
    *,
    question: dict,
    hits: list,  # SparseHit or DenseHit
    subtree: dict[str, set[str]],
    backend: str,
    session: Session,
) -> QuestionMetrics:
    expected_subtree = subtree.get(question["expected_section"], {question["expected_section"]})
    expected_kws = [k.lower() for k in question["expected_keywords"]]

    # hit@k
    in_subtree = [h for h in hits if h.section_number in expected_subtree]
    hit_at_k = len(in_subtree) > 0

    # keyword coverage — query the FULL chunk text from SQL (the hit's
    # text_preview is truncated to 240 chars; matching against preview
    # under-counts coverage when the keyword appears later in a long chunk).
    from src.models import Chunk

    chunk_ids = [h.chunk_id for h in hits]
    full_texts = []
    if chunk_ids:
        rows = session.execute(
            select(Chunk.text).where(Chunk.chunk_id.in_(chunk_ids))
        ).scalars().all()
        full_texts = [t.lower() for t in rows]
    all_text = " ".join(full_texts)
    found = [k for k in expected_kws if k in all_text]
    missing = [k for k in expected_kws if k not in all_text]
    coverage = len(found) / len(expected_kws) if expected_kws else 0.0

    top1 = hits[0] if hits else None

    summaries = [
        f"#{i + 1} sec={h.section_number} page={h.page} table={h.table_id or '-'} "
        f"score={(getattr(h, 'distance', None) or getattr(h, 'bm25_score', 0)):.3f}"
        for i, h in enumerate(hits)
    ]

    return QuestionMetrics(
        qid=question["qid"],
        backend=backend,
        hit_at_k=hit_at_k,
        keyword_coverage=coverage,
        keywords_found=found,
        keywords_missing=missing,
        top1_section=top1.section_number if top1 else None,
        top1_page=top1.page if top1 else None,
        top1_table_id=top1.table_id if top1 else None,
        top_chunk_summaries=summaries,
    )


def _format_report(
    *,
    backend_metrics: dict[str, list[QuestionMetrics]],
    questions: list[dict],
    top_k: int,
) -> str:
    lines: list[str] = []
    lines.append("# Week 2 Retrieval Benchmark\n")
    lines.append(f"_top_k = {top_k}; backends = {', '.join(backend_metrics.keys())}_\n")

    # Aggregate header
    lines.append("## Aggregate\n")
    lines.append("| backend | hit@K | mean coverage |")
    lines.append("|---|---|---|")
    for backend, ms in backend_metrics.items():
        n = len(ms)
        hits = sum(1 for m in ms if m.hit_at_k)
        cov = sum(m.keyword_coverage for m in ms) / n if n else 0
        lines.append(f"| {backend} | {hits}/{n} | {cov:.0%} |")
    lines.append("")

    # Per-question detail
    by_qid = {q["qid"]: q for q in questions}
    qids = [q["qid"] for q in questions]
    for qid in qids:
        q = by_qid[qid]
        lines.append(f"## {qid} — {q['question']}")
        lines.append(
            f"_expected_section = §{q['expected_section']} · "
            f"type = {q['question_type']} · "
            f"difficulty = {q['difficulty']}_\n"
        )
        for backend, ms in backend_metrics.items():
            m = next(x for x in ms if x.qid == qid)
            verdict = "HIT" if m.hit_at_k else "MISS"
            lines.append(
                f"**{backend}** — {verdict} · "
                f"coverage = {len(m.keywords_found)}/{len(m.keywords_found) + len(m.keywords_missing)} "
                f"({m.keyword_coverage:.0%}) · "
                f"top-1 = §{m.top1_section} p{m.top1_page} table={m.top1_table_id or '-'}"
            )
            if m.keywords_missing:
                lines.append(f"  missing keywords: {m.keywords_missing}")
            for s in m.top_chunk_summaries:
                lines.append(f"    {s}")
            lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument(
        "--backend",
        default="sparse,dense",
        help="Comma-separated subset of {sparse, dense}",
    )
    parser.add_argument(
        "--questions",
        type=Path,
        default=settings.eval_dir / "test_questions.yaml",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=settings.eval_dir / "last_eval.md",
    )
    args = parser.parse_args()

    backends = [b.strip() for b in args.backend.split(",") if b.strip()]
    valid = {"sparse", "dense"}
    bad = set(backends) - valid
    if bad:
        print(f"ERROR: unknown backend(s) {bad}; valid: {valid}", file=sys.stderr)
        return 2

    if not args.questions.exists():
        print(f"ERROR: questions file not found: {args.questions}", file=sys.stderr)
        return 1

    # Pre-flight check: dense backend requires Chroma collection to exist
    # and chunks.vector_id to be populated. Bail early with a clear message
    # if the user runs evaluate.py before embed_chunks.py completes.
    if "dense" in backends:
        engine_pre = create_engine(settings.db_url, future=True)
        with Session(engine_pre) as s:
            from src.models import Chunk

            unembedded = s.execute(
                select(Chunk).where(Chunk.vector_id.is_(None)).limit(1)
            ).scalar_one_or_none()
            embedded_count = s.execute(
                select(Chunk).where(Chunk.vector_id.is_not(None)).limit(1)
            ).scalar_one_or_none()
        if embedded_count is None:
            print(
                "ERROR: dense backend requested but no chunks have vector_id set. "
                "Run scripts/embed_chunks.py first.",
                file=sys.stderr,
            )
            return 1
        if unembedded is not None:
            print(
                "WARN: some chunks still have vector_id=NULL — dense retrieval "
                "will only see the partially-embedded subset.",
                file=sys.stderr,
            )

    with args.questions.open(encoding="utf-8") as f:
        questions = yaml.safe_load(f)

    engine = create_engine(settings.db_url, future=True)
    backend_metrics: dict[str, list[QuestionMetrics]] = {b: [] for b in backends}

    with Session(engine) as session:
        subtree = _build_section_subtree(session)

        for q in questions:
            print(f"[eval] {q['qid']}: {q['question']}")
            for backend in backends:
                if backend == "sparse":
                    hits = search_sparse(session, q["question"], top_k=args.top_k)
                else:
                    hits = search_dense(session, q["question"], top_k=args.top_k)
                m = _evaluate_question(
                    question=q,
                    hits=hits,
                    subtree=subtree,
                    backend=backend,
                    session=session,
                )
                backend_metrics[backend].append(m)
                marker = "HIT " if m.hit_at_k else "MISS"
                print(
                    f"  [{backend:6s}] {marker}  cov={m.keyword_coverage:.0%}  "
                    f"top-1=§{m.top1_section} p{m.top1_page}"
                )

    report = _format_report(
        backend_metrics=backend_metrics,
        questions=questions,
        top_k=args.top_k,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")
    print(f"\n[eval] Report written to {args.report}")

    # Aggregate summary at end
    print("\n=== AGGREGATE ===")
    for backend, ms in backend_metrics.items():
        n = len(ms)
        hits = sum(1 for m in ms if m.hit_at_k)
        cov = sum(m.keyword_coverage for m in ms) / n if n else 0
        print(f"  {backend:6s}  hit@{args.top_k}={hits}/{n}  mean_coverage={cov:.0%}")

    # Week 2 gate: BOTH backends should clear hit@5 >= 8/10
    gate_ok = True
    for backend, ms in backend_metrics.items():
        n = len(ms)
        hits = sum(1 for m in ms if m.hit_at_k)
        if hits < 8:
            print(f"\n  GATE FAIL  {backend} hit@{args.top_k} = {hits}/{n} (< 8 required)")
            gate_ok = False
    if gate_ok:
        print("\n  GATE OK  hit@K threshold met by all backends")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
