"""Measure whether the rule-based fact layer lifts citation for numeric/table
questions (Step 6 / M6). evaluate.py is NOT touched — this is a separate
script, so the committed retrieval baselines stay byte-identical.

On the numeric + table_lookup answerable subset, over `--source-format`:
  - fact value-accuracy@1/@k : does search_facts SURFACE a value-matching
    fact (extraction AND retrieval, out of ~45k facts)?
  - citation chunk-only vs facts-first : does routing numeric questions
    through facts improve top-1 section citation?
Then prints an explicit LLM decision and writes facts_eval.md.

    .venv/Scripts/python.exe scripts/evaluate_facts.py --source-format tspec_md
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.config import settings
from src.facts._tokens import parse_value
from src.facts.search import search_facts
from src.models import FactType
from src.retrieval import search_hybrid

CITATION_TARGET = 0.9
_FACT_QTYPES = ("numeric", "table_lookup")


def parse_expected_values(expected_keywords: list[str]) -> list[float]:
    """Numeric expected values parsed out of the keyword list (e.g.
    ['minimum output power','-40','9.375'] -> [-40.0, 9.375])."""
    return [v for v in (parse_value(k) for k in expected_keywords) if v is not None]


def value_matches(value_num: float | None, expected: list[float]) -> bool:
    """Float equality (not substring): the R8 guard at the metric layer too."""
    return value_num is not None and any(
        abs(value_num - e) <= 1e-6 for e in expected
    )


def section_matches(section_number: str | None, expected: str) -> bool:
    """Prefix subtree match (md sections run deeper than the expected clause)."""
    if not section_number:
        return False
    return section_number == expected or section_number.startswith(expected + ".")


@dataclass(frozen=True)
class FactQResult:
    qid: str
    qtype: str
    expected_section: str
    expected_values: list[float]
    has_values: bool
    value_hit_1: bool
    value_hit_k: bool
    chunk_cite_1: bool
    factsfirst_cite_1: bool
    top_fact: str | None


def evaluate_question(session, q: dict, *, top_k: int, source_format: str) -> FactQResult:
    exp = parse_expected_values(q["expected_keywords"])
    sec = q["expected_section"]
    fhits = search_facts(
        session, q["question"], top_k=top_k,
        source_format=source_format, fact_types=[FactType.NUMERIC],
    )
    chits = search_hybrid(
        session, q["question"], top_k=top_k, source_format=source_format,
    )
    top_vn = fhits[0].fact_data.get("value_num") if fhits else None
    value_hit_1 = bool(exp) and value_matches(top_vn, exp)
    value_hit_k = bool(exp) and any(
        value_matches(h.fact_data.get("value_num"), exp) for h in fhits
    )
    chunk_cite_1 = bool(chits) and section_matches(chits[0].section_number, sec)
    # facts-first: when the top fact value-matches, cite IT; else fall back.
    if value_hit_1:
        factsfirst_cite_1 = section_matches(fhits[0].section_number, sec)
    else:
        factsfirst_cite_1 = chunk_cite_1
    top_fact = None
    if fhits:
        fd = fhits[0].fact_data
        top_fact = (
            f"{fd.get('row_label', '')}={fd.get('value', '')} "
            f"§{fhits[0].section_number}"
        )
    return FactQResult(
        qid=q["qid"], qtype=q["question_type"], expected_section=sec,
        expected_values=exp, has_values=bool(exp),
        value_hit_1=value_hit_1, value_hit_k=value_hit_k,
        chunk_cite_1=chunk_cite_1, factsfirst_cite_1=factsfirst_cite_1,
        top_fact=top_fact,
    )


def _format_report(results: list[FactQResult], *, source_format: str) -> str:
    n = len(results)
    with_vals = [r for r in results if r.has_values]
    nv = len(with_vals)
    retr_k = sum(1 for r in with_vals if r.value_hit_k)
    vacc1 = sum(1 for r in with_vals if r.value_hit_1)
    chunk_cite = sum(1 for r in results if r.chunk_cite_1)
    ff_cite = sum(1 for r in results if r.factsfirst_cite_1)
    pct = lambda x, d: f"{(100 * x // d) if d else 0}%"  # noqa: E731

    lines = ["# Fact-layer measurement (rule-based MVP)\n"]
    lines.append(
        f"_source_format = {source_format}; {n} numeric+table_lookup "
        f"answerable questions ({nv} with a parseable expected value)_\n"
    )
    lines.append("## Headline\n")
    lines.append(f"- fact value-accuracy@1 = {vacc1}/{nv} ({pct(vacc1, nv)})")
    lines.append(f"- fact value retrieved @top-{5} = {retr_k}/{nv} ({pct(retr_k, nv)})")
    lines.append(
        f"- citation chunk-only   = {chunk_cite}/{n} ({pct(chunk_cite, n)})"
    )
    lines.append(
        f"- citation facts-first  = {ff_cite}/{n} ({pct(ff_cite, n)})  "
        f"(target >= {CITATION_TARGET:.0%})\n"
    )
    lines.append("## Per question\n")
    lines.append("| qid | type | §exp | exp vals | val@1 | val@k | chunk-cite | ff-cite | top fact |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in results:
        lines.append(
            f"| {r.qid} | {r.qtype} | {r.expected_section} | {r.expected_values} "
            f"| {'Y' if r.value_hit_1 else 'n'} | {'Y' if r.value_hit_k else 'n'} "
            f"| {'Y' if r.chunk_cite_1 else 'n'} | {'Y' if r.factsfirst_cite_1 else 'n'} "
            f"| {r.top_fact or '-'} |"
        )
    lines.append("")
    lines.append("## Decision (rule-based vs LLM)\n")
    ff_rate = ff_cite / n if n else 0.0
    if ff_rate >= CITATION_TARGET:
        lines.append(
            f"Rule-based facts-first citation = {ff_rate:.0%} >= "
            f"{CITATION_TARGET:.0%}. **LLM extraction is UNNECESSARY for this "
            f"scope.**"
        )
    else:
        missed = [r.qid for r in results if not r.factsfirst_cite_1]
        lines.append(
            f"Rule-based facts-first citation = {ff_rate:.0%} < "
            f"{CITATION_TARGET:.0%} (gap {CITATION_TARGET - ff_rate:.0%}). "
            f"Residual misses: {missed}. This gap quantifies what LLM "
            f"extraction would need to close — proceed to the LLM decision."
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-format", default="tspec_md",
                        choices=["pdf_pymupdf", "tspec_md"])
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--questions", type=Path,
                        default=settings.eval_dir / "test_questions.yaml")
    parser.add_argument("--report", type=Path,
                        default=settings.eval_dir / "facts_eval.md")
    args = parser.parse_args()

    with args.questions.open(encoding="utf-8") as f:
        questions = yaml.safe_load(f)
    targets = [
        q for q in questions
        if q.get("answerability", "answerable") == "answerable"
        and q["question_type"] in _FACT_QTYPES
    ]

    engine = create_engine(settings.db_url, future=True)
    results: list[FactQResult] = []
    with Session(engine) as session:
        for q in targets:
            print(f"[facts-eval] {q['qid']}: {q['question']}")
            results.append(evaluate_question(
                session, q, top_k=args.top_k, source_format=args.source_format,
            ))

    report = _format_report(results, source_format=args.source_format)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")
    print(f"\n[facts-eval] report -> {args.report}")

    n = len(results)
    ff = sum(1 for r in results if r.factsfirst_cite_1)
    chunk = sum(1 for r in results if r.chunk_cite_1)
    vacc1 = sum(1 for r in results if r.has_values and r.value_hit_1)
    nv = sum(1 for r in results if r.has_values)
    print("\n=== FACT LAYER (rule-based) ===")
    print(f"  value-acc@1 = {vacc1}/{nv}   citation chunk-only = {chunk}/{n}   "
          f"facts-first = {ff}/{n} (target {CITATION_TARGET:.0%})")
    print(
        "  DECISION: "
        + ("rule-based meets the citation target — LLM unnecessary"
           if (ff / n if n else 0) >= CITATION_TARGET
           else "rule-based below target — see report for gap + LLM decision")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
