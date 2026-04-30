# Phase 0 Reality Check — TS 38.521-1 retrieval spike

**Date**: 2026-04-30
**Source PDF**: `data/raw/ts_138521-01_v17_05_00.pdf` (TS 38.521-1 v17.5.0, NR FR1 UE conformance)
**Generation**: NONE in this script — top-K chunks only; LLM step done interactively in Claude Code

## TL;DR — Decision: **GO** (proceed to Phase A)

Three runs were performed:

| Run | Embedding | Section | Chunks | In-scope hit rate |
|---|---|---|---|---|
| 1 | MiniLM-L6-v2 | §6.2 only | 661 | 1.5/3 (~50%) |
| 2 | BGE-M3 | §6.2 only | 661 | 3/3 (100%) ★ |
| 3 | BGE-M3 | §6.3 only | TBD | TBD (q04/q05 verification) |

**The signal that drove the decision**: BGE-M3 found "Inner Full / Outer Full" RB allocation tables (q03) that MiniLM completely missed — proving BGE-M3's technical-term semantic ability is materially better. Combined with the discovery that q04/q05 failures were **scope problems, not retrieval problems**, the pipeline is on solid ground.

---

## Section locating — three different mistakes converged on one lesson

### Mistake 1 (run 1, original): regex on body text
Tried `^\s*6\.2\b` MULTILINE — caught the **table-of-contents entry** for §6.2 instead of the real section header. Result: only 21 chunks from 3 pages of TOC text.

**Fix**: use PyMuPDF's `doc.get_toc()` bookmark API. This gives the real page mapping.

### Mistake 2 (run 2, MiniLM): underrated embedding
Switched to MiniLM-L6-v2 because BGE-M3 download was being rate-limited by HuggingFace anonymously (256 MB cap). MiniLM gave 50% hit rate — passable but the conceptual queries (Inner/Outer, min vs max) clearly failed.

**Fix**: register HF account, get token, set `HF_TOKEN` env var → BGE-M3 download succeeds (~2.3 GB).

### Mistake 3 (run 2, BGE-M3): assumed §6.2 was self-contained
Test questions q04 (minimum output power) and q05 (Transmit OFF power) returned "irrelevant" results. Initially diagnosed as embedding weakness. Verified by inspecting the bookmark TOC:

```
§6.2  Transmitter power           p.92    ← extracted
  §6.2.1  UE maximum output power           p.92
  §6.2.2  UE maximum output power reduction p.98
  §6.2.3  UE additional MPR (A-MPR)         p.123
  §6.2.4  Configured transmitted power      p.273
§6.2A Transmitter power for CA    p.280   ← my extraction stopped HERE (next L2 sibling)
§6.2B …  §6.2C …
§6.3  Output power dynamics       p.541   ★ q04 / q05 actually live HERE
  §6.3.1  Minimum output power     p.541
  §6.3.2  Transmit OFF power       p.544
```

Direct text search in §6.3 confirmed: **`transmit OFF` appears 19 times, `minimum output power` 15 times**. Run 3 (this report) re-extracts §6.3 to confirm BGE-M3 finds them when they're in scope.

**Fix for Phase A**: ingestion must support **multiple sections at once**, not single-section-at-a-time. Also, treat `§6.2A / §6.2B / §6.2C` as **separate from `§6.2`** but jointly user-selectable (they're 3GPP's CA / DC / SUL variants).

---

## Run 1 (MiniLM) results — baseline only, kept for comparison

See `spike/last_run_62.json` (overwritten — refer to git history if needed).

Key observations:
- q01 (Tx tolerance), q02 (test procedure): clean hits
- q03 (Inner/Outer): **failed to retrieve "Inner Full" / "Outer Full" chunks** that exist in corpus
- q04, q05: failed (later attributed to scope, not embedding)

## Run 2 (BGE-M3, §6.2) results

Stored in `spike/last_run_62.json`. Per-question summary:

| qid | top-1 chunk | top-1 page | dist | keyword MATCH | verdict |
|---|---|---|---|---|---|
| q01 | c0442 | 222 | 0.333 | 23, dBm, tolerance | hit (different chunk than MiniLM but valid) |
| q02 | c0006 | 94 | 0.293 | (matches §6.2.1.4 boundary) | hit |
| q03 | c0016 + c0045 | 96, 104 | 0.330, 0.333 | channel bandwidth, **Inner Full, Outer Full** | ★ hit (MiniLM missed) |
| q04 | c0000 | 92 | 0.368 | — | scope miss (content in §6.3) |
| q05 | c0018 | 97 | 0.357 | — | scope miss (content in §6.3) |

### Q3 deep-dive — the win that swung the verdict

BGE-M3 surfaced chunk `c0045` (page 104, Test Configuration Table for PC2&3) which contains the explicit Inner/Outer allocation grid:

```
Test ID | Modulation       | RB allocation
   1    | CP-OFDM QPSK     | Inner Full
   2    | CP-OFDM QPSK     | Outer Full
   3    | CP-OFDM 16 QAM   | Inner Full
   4    | CP-OFDM 16 QAM   | Outer Full
   5    | CP-OFDM 64 QAM   | Outer Full
   6    | CP-OFDM 256 QAM  | Outer Full
```

And chunk `c0030` (page 100) defines the math:
```
RBStart,Low  = max(1, floor((NRB_alloc + NRB_gap) / 2))
RBStart,High = NRB – RBStart,Low – NRB_alloc – NRB_gap
```

MiniLM's top-5 for q03 had none of these — it returned tolerance tables sharing the term "channel bandwidth" but missed the conceptual Inner/Outer structure entirely.

### Q1 ranking divergence — both valid, complementary

- BGE-M3 top-1 (c0442, page 222): the **Test Tolerance matrix** §6.2.3.5-0 (frequency × BW → dB)
- MiniLM top-1 (c0003, page 93): the **PC3 Maximum Output Power table** §6.2.1.5-1 (per-band 23 dBm ± values)

Both correct. BGE-M3 abstracted "tolerance" to its mechanism; MiniLM matched lexically to the canonical numeric table. Argues for top-K ≥ 5 retrieval (different views are complementary), not top-1.

## Run 3 (BGE-M3, §6.3) results — q04/q05 in-scope verification

Stored in `spike/last_run_63.json`. Section §6.3 spans pages 541–590 (50 pages, 144 chunks). Same five questions, same model, just a different corpus.

| qid | top-1 chunk | top-1 page | dist | keyword MATCH on top-1 | verdict |
|---|---|---|---|---|---|
| q01 (PC3 max tolerance) | c0001 | 541 | 0.389 | dBm only | scope miss (q01 is a §6.2 question) |
| q02 (test procedure) | c0141 | 590 | 0.341 | — | scope miss |
| q03 (Inner/Outer + BW) | c0003 | 541 | 0.320 | channel bandwidth only | scope miss |
| **q04 (minimum output power)** | **c0002** | **541** | **0.252** | **minimum output power** | ★★ **strong hit** — chunk is §6.3.1.1 Test purpose |
| **q05 (Transmit OFF power)** | c0018 → top-2 c0011 | 546 → 544 | 0.320 → 0.354 | top-2: transmit OFF, OFF power | ★★ **strong hit** — top-2 is §6.3.2.1 Test purpose |

### Q4 deep-dive (§6.3 corpus)

Top-1 chunk `c0002` text (page 541):
```
6.3 Output power dynamics
6.3.1 Minimum output power
6.3.1.1 Test purpose
To verify the UE's ability to transmit with a broadband output power below the value
specified in the test requirement when the power is set to a minimum value...
```
Distance 0.252 — the lowest of any top-1 across all three runs. BGE-M3 nails this once §6.3 is in scope.

### Q5 deep-dive (§6.3 corpus)

Top-2 chunk `c0011` text (page 544):
```
...purpose
To verify that the UE transmit OFF power is lower than the value specified in the test
requirement. An excess Transmit OFF power potentially increases the Rise Over Thermal
(RoT) and therefore reduces the cell coverage area for other UEs.
6.3.2.2 Test applicability ...
```
Top-1 chunk c0018 was about the ON/OFF time mask figure (related but indirect). Top-2 is the canonical Test purpose. Top-4 (c0017, page 545) and top-5 (c0047, page 557) also had `transmit OFF` / `OFF power` keyword matches.

### Cross-corpus aggregate

| qid | §6.2 result | §6.3 result | union |
|---|---|---|---|
| q01 | ✅ hit | ⚠️ scope miss | ✅ |
| q02 | ✅ hit | ⚠️ scope miss | ✅ |
| q03 | ✅ hit | ⚠️ scope miss | ✅ |
| q04 | ⚠️ scope miss | ★ hit | ✅ |
| q05 | ⚠️ scope miss | ★ hit | ✅ |

**5/5 questions are answerable** when both sections are in corpus. This proves:
1. BGE-M3 retrieval is solid across both sections
2. The original "50% / 80% hit rate" narratives were anchored on a single-section corpus that didn't contain the answers
3. Phase A's multi-section ingestion is required, not optional

---

## Phase A entry conditions (locked in by this Phase 0)

1. **Embedding**: BGE-M3 (production), with HF_TOKEN configured
2. **Ingestion**: multi-section support from day one — user selects multiple `§N.M` (and N.M-letter variants) to ingest
3. **Section locating**: TOC bookmark API only (no body-text regex)
4. **Chunking**: Week 2 must address table fragmentation. Naive 800-char windows mid-table corrupt embedding signal. Options to evaluate:
   - Heading-aware chunker (don't split inside `Table X.Y.Z-N`)
   - Markdown-table preserving extraction (may need `unstructured.io`)
   - Larger chunks (~1500 chars) with smaller overlap
5. **Top-K**: stay at 5 for Phase A MVP; add reranker only if eval bank reveals precision floor
6. **Test bank**: questions must be **scope-validated** before grading. The q04/q05 false-fail trap is a real lesson — write expected_section + verify presence of expected text before adding to bank.

## What we explicitly proved / didn't prove

**Proved**:
- PyMuPDF text extraction is workable (noisy on tables but content is preserved)
- BGE-M3 handles 3GPP technical vocabulary (Inner/Outer, tolerance, test procedure, channel bandwidth)
- Persistent Chroma + state fingerprint correctly detects "same input → reuse" vs "params changed → rebuild"
- Single-section ingestion is too narrow; multi-section is required from day 1

**Did not prove (deferred to Phase A)**:
- LLM answer-generation quality (only demonstrated interactively in Claude Code)
- D1 generation diff engine feasibility
- 50-question test bank target with hit@5 ≥ 0.8
- Streamlit UI viability
- Reranker need

## Subjective: is this useful?

**Yes — strongly.** Pipeline plumbing works end-to-end on real 3GPP content. Top-K retrieval surfaces multiple complementary views (q01 case) and finds technical concepts MiniLM completely misses (q03 case). Once corpus is broadened (multi-section) and chunking is table-aware, this clearly clears the bar for "useful internal tool". Whether it clears "give to others" requires Phase A's beta-tester loop.
