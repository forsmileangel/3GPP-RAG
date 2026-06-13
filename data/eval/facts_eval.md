# Fact-layer measurement (rule-based MVP)

_source_format = tspec_md; 16 numeric+table_lookup answerable questions (13 with a parseable expected value)_

## Headline

- fact value-accuracy@1 = 2/13 (15%)
- fact value retrieved @top-5 = 5/13 (38%)
- citation chunk-only   = 14/16 (87%)
- citation facts-first  = 13/16 (81%)  (target >= 90%)

## Per question

| qid | type | §exp | exp vals | val@1 | val@k | chunk-cite | ff-cite | top fact |
|---|---|---|---|---|---|---|---|---|
| q01 | numeric | 6.2.1 | [23.0] | n | n | n | n | N/A for maximum output=Modulation (NOTE 2) §6.2.1.4.1 |
| q03 | table_lookup | 6.2.1 | [] | n | n | Y | Y | Test Channel Bandwidths as specified in TS 38.508-1 \[5\] subclause 4.3.1=Lowest, Highest for all RB allocations Ad ditionally, for edge RB a llocations, the maximum channel bandwidth \<50MHz and the minimum channel bandwidth ≥50MHz that are supported by the UE (NOTE 4) §6.2.2.4.1 |
| q04 | numeric | 6.3.1 | [] | n | n | Y | Y | Minimum output power=-40 §6.3.1.3 |
| q05 | numeric | 6.3.2 | [] | n | n | Y | Y | **Transmit OFF power**=-50 §6.3.2.3 |
| q11 | numeric | 6.2.1 | [2.0, 26.0] | Y | Y | Y | n | N/A for Maximum Power=Modulation (NOTE 2) §6.2.2.4.1 |
| q12 | numeric | 6.3.1 | [-40.0, 9.375] | n | n | Y | Y | Test Channel Bandwidths as specified in TS 38.508-1 \[5\] subclause 4.3.1=Lowest, Highest for all RB allocations Ad ditionally, for edge RB a llocations, the maximum channel bandwidth \<50MHz and the minimum channel bandwidth ≥50MHz that are supported by the UE (NOTE 4) §6.2.2.4.1 |
| q13 | numeric | 6.3.4.2 | [9.0] | Y | Y | Y | Y | Normal=± 9.0 dB §6.3.4.2.3 |
| q14 | numeric | 6.3.4.4 | [3.5] | n | Y | Y | Y | N/A for aggregate power tolerance testcase=RB allocation (NOTE 1) §6.3.4.4.4.1 |
| q15 | numeric | 6.2.4 | [2.0] | n | Y | n | n | 0 dB=Given 5 power measurements in the pattern, the 2^nd, and later measurements shall be within ± (3.5 + TT) dB of the 1^st measurement. §6.3.4.4.5 |
| q16 | numeric | 6.2.2 | [256.0, 4.5] | n | n | Y | Y | N/A for Maximum Power=Modulation (NOTE 2) §6.2.2.4.1 |
| q18 | table_lookup | 6.3.3.4 | [0.903125] | n | n | Y | Y | Expected PRACH Transmission ON Measured Power for PRACH Format 0 and PRACH Format A3 for SCS 30kHz=-1 dBm §6.3.3.4.5 |
| q21 | table_lookup | 6.2.1 | [31.0] | n | n | Y | Y | 0 dB=Given 5 power measurements in the pattern, the 2^nd, and later measurements shall be within ± (3.5 + TT) dB of the 1^st measurement. §6.3.4.4.5 |
| q22 | table_lookup | 6.2.2 | [256.0, 6.5] | n | n | Y | Y | Test Channel Bandwidths as specified in TS 38.508-1 \[5\] subclause 4.3.1=Lowest, Highest for all RB allocations Ad ditionally, for edge RB a llocations, the maximum channel bandwidth \<50MHz and the minimum channel bandwidth ≥50MHz that are supported by the UE (NOTE 4) §6.2.2.4.1 |
| q23 | table_lookup | 6.3.3.4 | [0.333333] | n | n | Y | Y | one=FR1 5MHz PRACH Format A3 for SCS 15 kHz OR FR1 10MHz PRACH Format A3 for SCS 30 kHz OR FR1 10MHz PRACH Format A3 for SCS 60 kHz §6.3.3.4.4.3 |
| q24 | table_lookup | 6.2.4 | [2.0, 10.0] | n | Y | Y | Y | Measured UE output power test point 4=Note 3 §6.2.4.5 |
| q25 | table_lookup | 6.3.4.3 | [12.76] | n | n | Y | Y | 0 dB=Given 5 power measurements in the pattern, the 2^nd, and later measurements shall be within ± (3.5 + TT) dB of the 1^st measurement. §6.3.4.4.5 |

## Decision (rule-based vs LLM)

Rule-based facts-first citation = 81% < 90% (gap 9%). Residual misses: ['q01', 'q11', 'q15']. This gap quantifies what LLM extraction would need to close — proceed to the LLM decision.
