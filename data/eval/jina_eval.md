# Retrieval Benchmark

_scored at k=10 (hit@1/3/5, MRR@10); detail rows show top 5; backends = reranked:jina_

## Aggregate

| backend | hit@1 | hit@3 | hit@5 | MRR@10 | mean coverage |
|---|---|---|---|---|---|
| reranked:jina | 26/30 | 30/30 | 30/30 | 0.93 | 96% |

## By question type

| backend | type | n | hit@1 | hit@3 | hit@5 | MRR@10 | coverage |
|---|---|---|---|---|---|---|---|
| reranked:jina | numeric | 9 | 89% | 100% | 100% | 0.94 | 100% |
| reranked:jina | procedure | 3 | 100% | 100% | 100% | 1.00 | 61% |
| reranked:jina | section_summary | 11 | 73% | 100% | 100% | 0.86 | 100% |
| reranked:jina | table_lookup | 7 | 100% | 100% | 100% | 1.00 | 100% |

## q01 — What is the maximum output power tolerance for FR1 PC3 UE?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.455
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.271
    #3 sec=6.2.1 page=96 table=6.2.1.5-1 score=0.233
    #4 sec=6.2.4 page=274 table=- score=0.203
    #5 sec=6.2.1 page=92 table=- score=0.172

## q02 — How is the test procedure defined for UE maximum output power across power classes?
_expected_section = §6.2.1 · type = procedure · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1 p92 table=-
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2.1 page=92 table=- score=0.527
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.322
    #3 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.306
    #4 sec=6.2.2 page=107 table=- score=0.305
    #5 sec=6.2.4 page=273 table=- score=0.292

## q03 — What are the test conditions and channel bandwidth for inner / outer maximum output power?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p94 table=6.2.1.4.1-1
    #1 sec=6.2.1 page=94 table=6.2.1.4.1-1 score=0.458
    #2 sec=6.2.2 page=102 table=6.2.2.4.1-2 score=0.324
    #3 sec=6.2.1 page=97 table=6.2.1.5-3 score=0.266
    #4 sec=6.3.3.2 page=546 table=6.3.3.2.4.1-1 score=0.262
    #5 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=0.248

## q04 — Define UE output power dynamics — minimum output power requirement.
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.678
    #2 sec=6.3.1 page=542 table=6.3.1.3-1 score=0.176
    #3 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.062
    #4 sec=6.3.1 page=543 table=6.3.1.5-1 score=0.057
    #5 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=0.054

## q05 — What is the transmit OFF power requirement for NR FR1 UE?
_expected_section = §6.3.2 · type = numeric · difficulty = easy_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=6.3.2.3-1
    #1 sec=6.3.2 page=544 table=6.3.2.3-1 score=0.377
    #2 sec=6.3.2 page=544 table=- score=0.336
    #3 sec=6.3.2 page=544 table=6.3.2.5-1 score=0.292
    #4 sec=6.2.4 page=274 table=- score=0.166
    #5 sec=6.3.3.2 page=546 table=6.3.3.2.4.1-1 score=0.162

## q06 — What are the absolute and relative power tolerance requirements?
_expected_section = §6.3.4 · type = section_summary · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3 p570 table=6.3.4.3.3-1
    #1 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.408
    #2 sec=6.3.4.3 page=570 table=- score=0.405
    #3 sec=6.3.4.3 page=570 table=- score=0.266
    #4 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=0.265
    #5 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=0.239

## q07 — What is the configured transmitted power for UE in NR?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**reranked:jina** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/1 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.340
    #2 sec=6.2.4 page=273 table=- score=0.333
    #3 sec=6.2.4 page=279 table=6.2.4.5-2 score=0.317
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.183
    #5 sec=6.2.4 page=273 table=- score=0.153

## q08 — How are additional MPR (A-MPR) requirements defined for NR FR1?
_expected_section = §6.2.3 · type = procedure · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.2.3 p123 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2.3 page=123 table=- score=0.387
    #2 sec=6.2.3 page=125 table=6.2.3.3.1-1 score=0.260
    #3 sec=6.2.3 page=123 table=6.2.3.3.1-1 score=0.257
    #4 sec=6.2.3 page=139 table=6.2.3.3.15-2 score=0.131
    #5 sec=6.2.3 page=129 table=- score=0.107

## q09 — What is the test purpose for the minimum output power conformance test?
_expected_section = §6.3.1 · type = section_summary · difficulty = easy_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.678
    #2 sec=6.3.4.1 page=567 table=- score=0.112
    #3 sec=6.3.4.3 page=570 table=- score=0.097
    #4 sec=6.2.1 page=92 table=- score=0.082
    #5 sec=6.3.1 page=542 table=6.3.1.3-1 score=0.066

## q10 — Why does excess Transmit OFF power matter for cell coverage?
_expected_section = §6.3.2 · type = section_summary · difficulty = hard_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.625
    #2 sec=6.2.1 page=92 table=- score=0.100
    #3 sec=6.3.2 page=544 table=6.3.2.5-1 score=0.072
    #4 sec=6.3.2 page=544 table=6.3.2.3-1 score=0.048
    #5 sec=6.3.3.1 page=545 table=- score=0.029

## q11 — What is the maximum output power for a Power Class 2 UE in NR band n78?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p97 table=6.2.1.5-2
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.512
    #2 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.354
    #3 sec=6.2.2 page=121 table=6.2.2.5-9 score=0.301
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.256
    #5 sec=6.2.4 page=273 table=- score=0.176

## q12 — What is the minimum output power limit and measurement bandwidth for a 10 MHz channel in FR1?
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.1 p542 table=6.3.1.3-1
    #1 sec=6.3.1 page=542 table=6.3.1.3-1 score=0.527
    #2 sec=6.3.1 page=543 table=6.3.1.5-1 score=0.259
    #3 sec=6.3.3.6 page=565 table=6.3.3.6.5-1 score=0.205
    #4 sec=6.3.3.3 page=550 table=6.3.3.2.5-1 score=0.138
    #5 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=0.128

## q13 — What is the absolute power tolerance for an NR UE under normal conditions?
_expected_section = §6.3.4.2 · type = numeric · difficulty = easy_

**reranked:jina** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=6.3.4.2.3-1
    #1 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=0.522
    #2 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=0.470
    #3 sec=6.3.4.1 page=567 table=- score=0.360
    #4 sec=6.3.4.2 page=567 table=- score=0.328
    #5 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.304

## q14 — What is the aggregate power tolerance for PUSCH transmissions with 0 dB TPC commands?
_expected_section = §6.3.4.4 · type = numeric · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p588 table=6.3.4.4.3-1
    #1 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=0.600
    #2 sec=6.3.4.4 page=587 table=- score=0.321
    #3 sec=6.3.4.3 page=576 table=- score=0.178
    #4 sec=6.3.4.4 page=590 table=- score=0.160
    #5 sec=6.3.4.4 page=587 table=6.3.4.3.5-7 score=0.158

## q15 — What is the PCMAX tolerance when the configured maximum output power is between 21 and 23 dBm?
_expected_section = §6.2.4 · type = numeric · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p276 table=6.2.4.3-2
    #1 sec=6.2.4 page=276 table=6.2.4.3-2 score=0.761
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.376
    #3 sec=6.2.4 page=273 table=- score=0.288
    #4 sec=6.2.2 page=107 table=- score=0.284
    #5 sec=6.2.4 page=275 table=6.2.4.3-1 score=0.169

## q16 — What is the allowed maximum power reduction for a power class 3 UE using DFT-s-OFDM 256 QAM modulation?
_expected_section = §6.2.2 · type = numeric · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p98 table=6.2.2.3-1
    #1 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.610
    #2 sec=6.2.3 page=147 table=6.2.3.3.26-2 score=0.384
    #3 sec=6.2.3 page=142 table=6.2.3.3.19-2 score=0.277
    #4 sec=6.2.3 page=145 table=6.2.3.3.22-2 score=0.203
    #5 sec=6.2.3 page=144 table=6.2.3.3.21-2 score=0.183

## q17 — Which test verifies the UE's ability to set its initial output power at the start of a transmission after a gap longer than 20ms?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**reranked:jina** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=0.487
    #2 sec=6.3.4.2 page=567 table=- score=0.450
    #3 sec=6.3.4.3 page=570 table=- score=0.378
    #4 sec=6.3.4.2 page=568 table=- score=0.281
    #5 sec=6.3.3.6 page=561 table=- score=0.123

## q18 — What is the PRACH ON power measurement period for preamble format 0?
_expected_section = §6.3.3.4 · type = table_lookup · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.616
    #2 sec=6.3.3.3 page=550 table=- score=0.319
    #3 sec=6.3.3.4 page=550 table=- score=0.252
    #4 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.198
    #5 sec=6.3.3.4 page=551 table=- score=0.101

## q19 — Which power control commands does the SS send to drive the UE to its minimum output power during the conformance test?
_expected_section = §6.3.1 · type = procedure · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.1 p543 table=-
    #1 sec=6.3.1 page=543 table=- score=0.509
    #2 sec=6.3.4.3 page=576 table=- score=0.443
    #3 sec=6.3.3.2 page=547 table=- score=0.387
    #4 sec=6.3.4.3 page=577 table=- score=0.354
    #5 sec=6.3.4.4 page=590 table=- score=0.338

## q20 — What is P-MPR in the PCMAX equation and what value must it take during UE conducted conformance testing?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p275 table=-
    #1 sec=6.2.4 page=275 table=- score=0.614
    #2 sec=6.2.4 page=275 table=- score=0.076
    #3 sec=6.2.4 page=273 table=- score=0.067
    #4 sec=6.2.2 page=119 table=6.2.2.5-7 score=0.055
    #5 sec=6.2.2 page=115 table=6.2.2.5-4 score=0.037

## q21 — In the UE Power Class table, what maximum output power and tolerance apply to band n14 for Power Class 1?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.667
    #2 sec=6.2.3 page=270 table=6.2.3.5-35 score=0.320
    #3 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.187
    #4 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.164
    #5 sec=6.2.4 page=273 table=- score=0.100

## q22 — What is the allowed MPR for CP-OFDM 256 QAM modulation in outer RB allocations for a power class 3 UE?
_expected_section = §6.2.2 · type = table_lookup · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p98 table=6.2.2.3-1
    #1 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.609
    #2 sec=6.2.2 page=99 table=6.2.2.3-2 score=0.458
    #3 sec=6.2.3 page=147 table=6.2.3.3.26-2 score=0.301
    #4 sec=6.2.3 page=123 table=6.2.3.3.1-1 score=0.216
    #5 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.190

## q23 — What is the PRACH ON power measurement period for preamble format C2 with 15 kHz SCS?
_expected_section = §6.3.3.4 · type = table_lookup · difficulty = hard_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.577
    #2 sec=6.3.3.4 page=551 table=- score=0.250
    #3 sec=6.3.3.3 page=550 table=- score=0.141
    #4 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.113
    #5 sec=6.3.3.4 page=550 table=- score=0.089

## q24 — What is the test requirement for measured UE output power at test point 2 in the configured transmitted power test?
_expected_section = §6.2.4 · type = table_lookup · difficulty = hard_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.2.4 p278 table=6.2.4.5-1
    #1 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.558
    #2 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.357
    #3 sec=6.2.4 page=273 table=- score=0.216
    #4 sec=6.3.4.3 page=578 table=- score=0.169
    #5 sec=6.3.4.3 page=570 table=- score=0.134

## q25 — In the 5 MHz ramp up sub-test, what is the expected power step size when the RB allocation changes from 1 RB to 15 RBs?
_expected_section = §6.3.4.3 · type = table_lookup · difficulty = hard_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3 p579 table=6.3.4.3.5-1
    #1 sec=6.3.4.3 page=579 table=6.3.4.3.5-1 score=0.629
    #2 sec=6.3.4.3 page=581 table=6.3.4.3.5-3 score=0.209
    #3 sec=6.3.4.3 page=585 table=6.3.4.3.5-5 score=0.170
    #4 sec=6.3.4.3 page=580 table=6.3.4.3.5-2 score=0.149
    #5 sec=6.3.4.3 page=578 table=- score=0.088

## q26 — Where is the Transmit OFF power requirement actually tested, given that clause 6.3.2 defines no standalone test procedure?
_expected_section = §6.3.2 · type = section_summary · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.537
    #2 sec=6.3.2 page=544 table=- score=0.315
    #3 sec=6.3.2 page=544 table=6.3.2.3-1 score=0.266
    #4 sec=6.3.3.2 page=545 table=- score=0.193
    #5 sec=6.3.3.1 page=545 table=- score=0.192

## q27 — Which clauses define the MPR and A-MPR values used in the PCMAX_L formula for configured maximum output power?
_expected_section = §6.2.4 · type = section_summary · difficulty = hard_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p273 table=-
    #1 sec=6.2.4 page=273 table=- score=0.372
    #2 sec=6.2.3 page=222 table=- score=0.326
    #3 sec=6.2.3 page=123 table=- score=0.310
    #4 sec=6.2.3 page=139 table=6.2.3.3.15-2 score=0.239
    #5 sec=6.2.3 page=129 table=- score=0.228

## q28 — What is the test purpose of the absolute power tolerance test?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**reranked:jina** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=0.475
    #2 sec=6.3.4.2 page=567 table=- score=0.468
    #3 sec=6.2.1 page=92 table=- score=0.203
    #4 sec=6.3.4.3 page=570 table=- score=0.175
    #5 sec=6.3.4.2 page=568 table=6.3.4.2.4.1-1 score=0.147

## q29 — What does the aggregate power tolerance test verify about UE transmitter behaviour?
_expected_section = §6.3.4.4 · type = section_summary · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=0.650
    #2 sec=6.3.4.3 page=570 table=- score=0.212
    #3 sec=6.3.4.1 page=567 table=- score=0.195
    #4 sec=6.3.4.2 page=567 table=- score=0.136
    #5 sec=6.2.1 page=92 table=- score=0.104

## q30 — What is the test purpose of the relative power tolerance test, and within what transmission gap does it apply?
_expected_section = §6.3.4.3 · type = section_summary · difficulty = medium_

**reranked:jina** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.3 p570 table=-
    #1 sec=6.3.4.3 page=570 table=- score=0.668
    #2 sec=6.3.4.1 page=567 table=- score=0.220
    #3 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.189
    #4 sec=6.3.4.3 page=570 table=- score=0.167
    #5 sec=6.3.4.2 page=567 table=- score=0.143
