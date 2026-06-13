# Fact-layer measurement (rule-based MVP)

_source_format = tspec_md; 16 numeric+table_lookup answerable questions (13 with a parseable expected value)_

## Headline

- fact value-accuracy@1 = 1/13 (7%)
- fact value retrieved @top-5 = 4/13 (30%)
- citation chunk-only   = 14/16 (87%)
- citation facts-first  = 14/16 (87%)  (target >= 90%)

## Per question

| qid | type | §exp | exp vals | val@1 | val@k | chunk-cite | ff-cite | top fact |
|---|---|---|---|---|---|---|---|---|
| q01 | numeric | 6.2.1 | [23.0] | n | n | n | n | Minimum output power=-40 §6.3.1.3 |
| q03 | table_lookup | 6.2.1 | [] | n | n | Y | Y | 5=1 §6.3.3.6.5 |
| q04 | numeric | 6.3.1 | [] | n | n | Y | Y | Minimum output power=-40 §6.3.1.3 |
| q05 | numeric | 6.3.2 | [] | n | n | Y | Y | **Transmit OFF power**=-50 §6.3.2.3 |
| q11 | numeric | 6.2.1 | [2.0, 26.0] | n | n | Y | Y | Minimum output power=-40 §6.3.1.3 |
| q12 | numeric | 6.3.1 | [-40.0, 9.375] | n | Y | Y | Y | 5=1 §6.3.3.6.5 |
| q13 | numeric | 6.3.4.2 | [9.0] | Y | Y | Y | Y | Normal=± 9.0 dB §6.3.4.2.3 |
| q14 | numeric | 6.3.4.4 | [3.5] | n | Y | Y | Y | 0 dB=± 2.5 dB §6.3.4.4.3 |
| q15 | numeric | 6.2.4 | [2.0] | n | n | n | n | Minimum output power=-40 §6.3.1.3 |
| q16 | numeric | 6.2.2 | [256.0, 4.5] | n | n | Y | Y | Minimum output power=-40 §6.3.1.3 |
| q18 | table_lookup | 6.3.3.4 | [0.903125] | n | n | Y | Y | Expected PRACH Transmission ON Measured Power for PRACH Format 0 and PRACH Format A3 for SCS 30kHz=-1 dBm §6.3.3.4.5 |
| q21 | table_lookup | 6.2.1 | [31.0] | n | n | Y | Y | Minimum output power=-40 §6.3.1.3 |
| q22 | table_lookup | 6.2.2 | [256.0, 6.5] | n | Y | Y | Y | 256 QAM=≤ 4.5 §6.2.3.3.1 |
| q23 | table_lookup | 6.3.3.4 | [0.333333] | n | n | Y | Y | Expected PRACH Transmission ON Measured Power for PRACH Format 0 and PRACH Format A3 for SCS 30kHz=-1 dBm §6.3.3.4.5 |
| q24 | table_lookup | 6.2.4 | [2.0, 10.0] | n | n | Y | Y | Minimum output power=-40 §6.3.1.3 |
| q25 | table_lookup | 6.3.4.3 | [12.76] | n | n | Y | Y | 15=7.99 §6.3.4.3.5 |

## Decision (rule-based vs LLM)

Rule-based facts-first citation = 88% < 90% (gap 3%). Residual misses: ['q01', 'q15']. This gap quantifies what LLM extraction would need to close — proceed to the LLM decision.
