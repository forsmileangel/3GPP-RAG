# Retrieval Benchmark

_scored at k=10 (hit@1/3/5, MRR@10); detail rows show top 5; source_format = mixed; backends = sparse, dense, hybrid, reranked:bge_

## Aggregate

| backend | hit@1 | hit@3 | hit@5 | MRR@10 | mean coverage |
|---|---|---|---|---|---|
| sparse | 14/30 | 22/30 | 27/30 | 0.63 | 88% |
| dense | 18/30 | 23/30 | 24/30 | 0.69 | 82% |
| hybrid | 20/30 | 27/30 | 29/30 | 0.78 | 88% |
| reranked:bge | 16/30 | 22/30 | 25/30 | 0.66 | 87% |

## By question type

| backend | type | n | hit@1 | hit@3 | hit@5 | MRR@10 | coverage |
|---|---|---|---|---|---|---|---|
| sparse | numeric | 9 | 44% | 89% | 100% | 0.67 | 100% |
| sparse | procedure | 3 | 0% | 67% | 100% | 0.29 | 61% |
| sparse | section_summary | 11 | 45% | 64% | 82% | 0.60 | 88% |
| sparse | table_lookup | 7 | 71% | 71% | 86% | 0.75 | 86% |
| dense | numeric | 9 | 56% | 67% | 78% | 0.65 | 89% |
| dense | procedure | 3 | 0% | 67% | 67% | 0.28 | 44% |
| dense | section_summary | 11 | 73% | 82% | 82% | 0.79 | 88% |
| dense | table_lookup | 7 | 71% | 86% | 86% | 0.79 | 79% |
| hybrid | numeric | 9 | 89% | 100% | 100% | 0.93 | 94% |
| hybrid | procedure | 3 | 33% | 67% | 100% | 0.53 | 61% |
| hybrid | section_summary | 11 | 55% | 91% | 91% | 0.71 | 92% |
| hybrid | table_lookup | 7 | 71% | 86% | 100% | 0.82 | 86% |
| reranked:bge | numeric | 9 | 56% | 78% | 89% | 0.68 | 91% |
| reranked:bge | procedure | 3 | 0% | 67% | 67% | 0.33 | 72% |
| reranked:bge | section_summary | 11 | 55% | 73% | 82% | 0.67 | 80% |
| reranked:bge | table_lookup | 7 | 71% | 71% | 86% | 0.74 | 100% |

## q01 — What is the maximum output power tolerance for FR1 PC3 UE?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=N hit@3=N hit@5=Y RR@10=0.20 · coverage = 3/3 (100%) · top-1 = §6.2A.2.1.5 p0 table=-
    #1 sec=6.2A.2.1.5 page=0 table=- score=-19.083
    #2 sec=6.2A.2.1.5 page=0 table=- score=-19.031
    #3 sec=6.2A.3.1.5 page=0 table=- score=-17.481
    #4 sec=6.2A.2.1.5 page=0 table=- score=-13.839
    #5 sec=6.2.1 page=93 table=6.2.1.3-1 score=-13.600

**dense** — hit@1=N hit@3=N hit@5=Y RR@10=0.20 · coverage = 3/3 (100%) · top-1 = §6.2.4 p273 table=-
    #1 sec=6.2.4 page=273 table=- score=0.332
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.334
    #3 sec=6.2A.2.1.5 page=0 table=- score=0.340
    #4 sec=6.2A.3.1.5 page=0 table=- score=0.342
    #5 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.347

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 3/3 (100%) · top-1 = §6.2A.2.1.5 p0 table=-
    #1 sec=6.2A.2.1.5 page=0 table=- score=0.032
    #2 sec=6.2A.3.1.5 page=0 table=- score=0.031
    #3 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.031
    #4 sec=6.2A.2.1.5 page=0 table=- score=0.031
    #5 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.026

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.972
    #2 sec=6.2A.2.1.5 page=0 table=- score=0.910
    #3 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.857
    #4 sec=6.2.4 page=273 table=- score=0.819
    #5 sec=6.2D.2.3 page=0 table=- score=0.790

## q02 — How is the test procedure defined for UE maximum output power across power classes?
_expected_section = §6.2.1 · type = procedure · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 1/3 (33%) · top-1 = §6.2A.1.0.4 p0 table=-
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2A.1.0.4 page=0 table=- score=-17.575
    #2 sec=6.2A.1.0.3 page=0 table=- score=-16.882
    #3 sec=6.2.1 page=92 table=- score=-16.397
    #4 sec=6.2.1.3 page=0 table=- score=-16.390
    #5 sec=6.2A.1.0.5 page=0 table=- score=-16.293

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/3 (33%) · top-1 = §6.2G.1.3 p0 table=-
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2G.1.3 page=0 table=- score=0.268
    #2 sec=6.2.1.3 page=0 table=- score=0.292
    #3 sec=6.2D.2.5 page=0 table=- score=0.293
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.294
    #5 sec=6.2G.1.5 page=0 table=- score=0.304

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1.3 p0 table=-
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2.1.3 page=0 table=- score=0.032
    #2 sec=6.2.1 page=92 table=- score=0.031
    #3 sec=6.2G.1.3 page=0 table=- score=0.028
    #4 sec=6.2G.2.3 page=0 table=- score=0.028
    #5 sec=6.2G.1.5 page=0 table=- score=0.027

**reranked:bge** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/3 (67%) · top-1 = §6.2G.2.3 p0 table=-
  missing keywords: ['test procedure']
    #1 sec=6.2G.2.3 page=0 table=- score=0.971
    #2 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.966
    #3 sec=6.2G.1.3 page=0 table=- score=0.957
    #4 sec=6.2D.2.3 page=0 table=- score=0.941
    #5 sec=6.2A.1.0.3 page=0 table=- score=0.941

## q03 — What are the test conditions and channel bandwidth for inner / outer maximum output power?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 3/3 (100%) · top-1 = §6.2E.2.0.2 p0 table=-
    #1 sec=6.2E.2.0.2 page=0 table=- score=-18.471
    #2 sec=6.2.2 page=99 table=6.2.2.3-5 score=-16.742
    #3 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-2c score=-15.488
    #4 sec=6.2A.2.1.4.1 page=0 table=6.2A.2.1.4.1-2b score=-15.366
    #5 sec=6.2A.2.1.4.1 page=0 table=6.2A.2.1.4.1-2a score=-15.189

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2A.2.1.4.1 p0 table=6.2A.2.1.4.1-3a
    #1 sec=6.2A.2.1.4.1 page=0 table=6.2A.2.1.4.1-3a score=0.299
    #2 sec=6.2.1.4.1 page=0 table=6.2.1.4.1-1 score=0.312
    #3 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-3 score=0.315
    #4 sec=6.2G.2.4.1 page=0 table=6.2G.2.4.1-3 score=0.316
    #5 sec=6.2C.1.5 page=0 table=6.2C.1.5-1 score=0.319

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2.2.4.1 p0 table=6.2.2.4.1-2c
    #1 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-2c score=0.031
    #2 sec=6.2.1.4.1 page=0 table=6.2.1.4.1-1 score=0.030
    #3 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-3 score=0.029
    #4 sec=6.2G.2.4.1 page=0 table=6.2G.2.4.1-3 score=0.029
    #5 sec=6.2G.2.4.1 page=0 table=6.2G.2.4.1-2 score=0.028

**reranked:bge** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 3/3 (100%) · top-1 = §6.2.2.4.1 p0 table=6.2.2.4.1-2c
    #1 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-2c score=0.894
    #2 sec=6.2G.2.4.1 page=0 table=6.2G.2.4.1-3 score=0.859
    #3 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-3 score=0.855
    #4 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-1 score=0.854
    #5 sec=6.2G.2.4.1 page=0 table=6.2G.2.4.1-2a score=0.854

## q04 — Define UE output power dynamics — minimum output power requirement.
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=-25.551
    #2 sec=6.2.1 page=92 table=- score=-20.074
    #3 sec=6.3B page=0 table=- score=-19.065
    #4 sec=6.3.1.3 page=0 table=- score=-17.914
    #5 sec=6.3F.1.3 page=0 table=- score=-17.849

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/1 (100%) · top-1 = §6.3F.1.3 p0 table=-
    #1 sec=6.3F.1.3 page=0 table=- score=0.231
    #2 sec=6.3.1.3 page=0 table=- score=0.235
    #3 sec=6.3.1 page=541 table=- score=0.252
    #4 sec=6.3G.1.3 page=0 table=- score=0.257
    #5 sec=6.3D.1.3 page=0 table=- score=0.295

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.032
    #2 sec=6.3F.1.3 page=0 table=- score=0.032
    #3 sec=6.3.1.3 page=0 table=- score=0.032
    #4 sec=6.3D.1.3 page=0 table=- score=0.030
    #5 sec=6.3G.1.3 page=0 table=- score=0.030

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.992
    #2 sec=6.3.1.3 page=0 table=- score=0.990
    #3 sec=6.3F.1.3 page=0 table=- score=0.989
    #4 sec=6.3D.1.3 page=0 table=- score=0.988
    #5 sec=6.3G.1.3 page=0 table=- score=0.987

## q05 — What is the transmit OFF power requirement for NR FR1 UE?
_expected_section = §6.3.2 · type = numeric · difficulty = easy_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.3.2.3 p0 table=-
    #1 sec=6.3.3.2.3 page=0 table=- score=-18.838
    #2 sec=6.3.2 page=544 table=- score=-16.186
    #3 sec=6.3A.2.0 page=0 table=- score=-15.984
    #4 sec=6.3.3.6 page=557 table=- score=-15.850
    #5 sec=6.3.2.3 page=0 table=- score=-15.612

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 2/2 (100%) · top-1 = §6.3E.2.0.1 p0 table=-
    #1 sec=6.3E.2.0.1 page=0 table=- score=0.312
    #2 sec=6.5.3.2.3 page=0 table=6.5.3.2.3-1 score=0.348
    #3 sec=6.5.3.2.3 page=0 table=6.5.3.2.3-2 score=0.356
    #4 sec=6.5.3.3.3.10 page=0 table=- score=0.356
    #5 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.359

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.029
    #2 sec=6.3E.2.0.1 page=0 table=- score=0.028
    #3 sec=6.3G.2.3 page=0 table=- score=0.027
    #4 sec=6.3.3.2.3 page=0 table=- score=0.016
    #5 sec=6.5.3.2.3 page=0 table=6.5.3.2.3-1 score=0.016

**reranked:bge** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 2/2 (100%) · top-1 = §6.3G.2.3 p0 table=-
    #1 sec=6.3G.2.3 page=0 table=- score=0.974
    #2 sec=6.3A.2.0 page=0 table=- score=0.941
    #3 sec=6.3.2.3 page=0 table=- score=0.941
    #4 sec=6.3F.2.3 page=0 table=- score=0.941
    #5 sec=6.3.2 page=544 table=- score=0.888

## q06 — What are the absolute and relative power tolerance requirements?
_expected_section = §6.3.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/2 (50%) · top-1 = §3.2 p0 table=-
  missing keywords: ['absolute power tolerance']
    #1 sec=3.2 page=0 table=- score=-14.597
    #2 sec=6.3.4.3.5 page=0 table=- score=-14.308
    #3 sec=6.3D.4.2.5 page=0 table=- score=-14.266
    #4 sec=6.3G.4.2.5 page=0 table=- score=-14.094
    #5 sec=6.3C.4.2.5 page=0 table=- score=-14.083

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.2.3 p0 table=-
    #1 sec=6.3.4.2.3 page=0 table=- score=0.282
    #2 sec=6.3A.4.1.0 page=0 table=- score=0.305
    #3 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=0.307
    #4 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=0.307
    #5 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.333

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/2 (50%) · top-1 = §6.3A.4.1.0 p0 table=-
  missing keywords: ['relative power tolerance']
    #1 sec=6.3A.4.1.0 page=0 table=- score=0.028
    #2 sec=6.3.4.2.3 page=0 table=- score=0.028
    #3 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=0.028
    #4 sec=6.3.4.1 page=567 table=- score=0.027
    #5 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=0.027

**reranked:bge** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3A.4.1.0 p0 table=-
    #1 sec=6.3A.4.1.0 page=0 table=- score=0.939
    #2 sec=6.3.4.2.3 page=0 table=- score=0.909
    #3 sec=6.3G.4.3.3 page=0 table=- score=0.839
    #4 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.825
    #5 sec=6.3.4.3.5 page=0 table=- score=0.800

## q07 — What is the configured transmitted power for UE in NR?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.12 · coverage = 1/1 (100%) · top-1 = §6.2A.1.0.3 p0 table=-
    #1 sec=6.2A.1.0.3 page=0 table=- score=-12.951
    #2 sec=6.2A.4.1.5 page=0 table=- score=-12.503
    #3 sec=6.2.1.3 page=0 table=- score=-12.064
    #4 sec=6.2G.1.3 page=0 table=- score=-11.433
    #5 sec=6.3.1 page=541 table=6.2I.4.5-0 score=-11.088

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 0/1 (0%) · top-1 = §6.2B.4.0.1.3 p0 table=-
  missing keywords: ['configured transmitted power']
    #1 sec=6.2B.4.0.1.3 page=0 table=- score=0.324
    #2 sec=6.2E.1.0.1 page=0 table=- score=0.333
    #3 sec=6.5.3.2.3 page=0 table=6.5.3.2.3-1 score=0.334
    #4 sec=6.5.3.2.3 page=0 table=6.5.3.2.3-2 score=0.341
    #5 sec=6.5E.2.2.1D.1 page=0 table=- score=0.348

**hybrid** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 1/1 (100%) · top-1 = §3.2 p0 table=-
    #1 sec=3.2 page=0 table=- score=0.029
    #2 sec=6.5E.2.2.1.1 page=0 table=- score=0.026
    #3 sec=6.2B.4.0.1.3 page=0 table=- score=0.026
    #4 sec=6.2C.1.3 page=0 table=- score=0.024
    #5 sec=6.2A.1.0.3 page=0 table=- score=0.016

**reranked:bge** — hit@1=N hit@3=N hit@5=N RR@10=0.14 · coverage = 0/1 (0%) · top-1 = §6.2C.1.3 p0 table=-
  missing keywords: ['configured transmitted power']
    #1 sec=6.2C.1.3 page=0 table=- score=0.970
    #2 sec=6.2B.4.0.1.3 page=0 table=- score=0.967
    #3 sec=6.2B.4.0.1.3 page=0 table=- score=0.945
    #4 sec=6.2E.1.0.1 page=0 table=- score=0.918
    #5 sec=6.3E.1.0.1 page=0 table=- score=0.873

## q08 — How are additional MPR (A-MPR) requirements defined for NR FR1?
_expected_section = §6.2.3 · type = procedure · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=Y RR@10=0.20 · coverage = 1/2 (50%) · top-1 = §6.2A.3.0.3 p0 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2A.3.0.3 page=0 table=- score=-18.294
    #2 sec=6.2B.3.0.3 page=0 table=- score=-17.852
    #3 sec=6.2B.3.1.1 page=0 table=- score=-16.903
    #4 sec=6.2F.3.3.1 page=0 table=- score=-16.648
    #5 sec=6.2.3.1 page=0 table=- score=-16.636

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 1/2 (50%) · top-1 = §6.2B.3.1.1 p0 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2B.3.1.1 page=0 table=- score=0.347
    #2 sec=6.2A.3.0.1 page=0 table=- score=0.351
    #3 sec=6.2.3.1 page=0 table=- score=0.355
    #4 sec=6.2F.3.3.1 page=0 table=- score=0.357
    #5 sec=6.2G.3.1 page=0 table=- score=0.359

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 1/2 (50%) · top-1 = §6.2B.3.1.1 p0 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2B.3.1.1 page=0 table=- score=0.032
    #2 sec=6.2A.3.0.1 page=0 table=- score=0.031
    #3 sec=6.2.3.1 page=0 table=- score=0.031
    #4 sec=6.2F.3.3.1 page=0 table=- score=0.031
    #5 sec=6.2G.3.1 page=0 table=- score=0.030

**reranked:bge** — hit@1=N hit@3=N hit@5=N RR@10=0.14 · coverage = 1/2 (50%) · top-1 = §6.2B.3.1.1 p0 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2B.3.1.1 page=0 table=- score=0.958
    #2 sec=6.2F.3.3.1 page=0 table=- score=0.955
    #3 sec=6.2G.3.1 page=0 table=- score=0.954
    #4 sec=6.2D.3_1.1 page=0 table=- score=0.950
    #5 sec=6.2D.3.1 page=0 table=- score=0.946

## q09 — What is the test purpose for the minimum output power conformance test?
_expected_section = §6.3.1 · type = section_summary · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=-18.061
    #2 sec=6.3.4.1 page=567 table=- score=-15.460
    #3 sec=6.3.4.2 page=567 table=- score=-15.460
    #4 sec=6.3.4.4 page=587 table=- score=-15.089
    #5 sec=6.3.4.3 page=570 table=- score=-15.086

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.1.1 p0 table=-
    #1 sec=6.3.1.1 page=0 table=- score=0.347
    #2 sec=6.3F.1.1 page=0 table=- score=0.347
    #3 sec=6.3.1 page=541 table=- score=0.348
    #4 sec=6.3D.1.1 page=0 table=- score=0.357
    #5 sec=6.3.4.4 page=587 table=- score=0.360

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.032
    #2 sec=6.3.4.1 page=567 table=- score=0.031
    #3 sec=6.3.4.4 page=587 table=- score=0.031
    #4 sec=6.3.4.2 page=567 table=- score=0.031
    #5 sec=6.3.4.3 page=570 table=- score=0.030

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.988
    #2 sec=6.3.4.1 page=567 table=- score=0.979
    #3 sec=6.3.4.2 page=567 table=- score=0.979
    #4 sec=6.3.4.4 page=587 table=- score=0.961
    #5 sec=6.3.4.3 page=570 table=- score=0.954

## q10 — Why does excess Transmit OFF power matter for cell coverage?
_expected_section = §6.3.2 · type = section_summary · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.2.1 p0 table=-
    #1 sec=6.3.2.1 page=0 table=- score=-29.889
    #2 sec=6.3E.2.1.1 page=0 table=- score=-29.889
    #3 sec=6.3E.2.1D.1 page=0 table=- score=-29.889
    #4 sec=6.3E.2.2.1 page=0 table=- score=-29.889
    #5 sec=6.3F.2.1 page=0 table=- score=-29.889

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.2.1 p0 table=-
    #1 sec=6.3.2.1 page=0 table=- score=0.261
    #2 sec=6.3E.2.1.1 page=0 table=- score=0.261
    #3 sec=6.3E.2.1D.1 page=0 table=- score=0.261
    #4 sec=6.3E.2.2.1 page=0 table=- score=0.261
    #5 sec=6.3F.2.1 page=0 table=- score=0.261

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.2.1 p0 table=-
    #1 sec=6.3.2.1 page=0 table=- score=0.033
    #2 sec=6.3E.2.1.1 page=0 table=- score=0.032
    #3 sec=6.3E.2.1D.1 page=0 table=- score=0.032
    #4 sec=6.3E.2.2.1 page=0 table=- score=0.031
    #5 sec=6.3F.2.1 page=0 table=- score=0.031

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.2.1 p0 table=-
    #1 sec=6.3.2.1 page=0 table=- score=0.986
    #2 sec=6.3E.2.1.1 page=0 table=- score=0.986
    #3 sec=6.3E.2.1D.1 page=0 table=- score=0.986
    #4 sec=6.3E.2.2.1 page=0 table=- score=0.986
    #5 sec=6.3F.2.1 page=0 table=- score=0.986

## q11 — What is the maximum output power for a Power Class 2 UE in NR band n78?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 3/3 (100%) · top-1 = §6.2A.3.1.5 p0 table=-
    #1 sec=6.2A.3.1.5 page=0 table=- score=-20.823
    #2 sec=6.2D.2.5 page=0 table=- score=-19.451
    #3 sec=6.2.1 page=97 table=6.2.1.5-2 score=-18.971
    #4 sec=6.2G.1.5 page=0 table=- score=-18.166
    #5 sec=6.2G.2.5 page=0 table=- score=-17.915

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p97 table=6.2.1.5-2
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.344
    #2 sec=6.2D.2.5 page=0 table=- score=0.351
    #3 sec=6.2D.2.5 page=0 table=- score=0.352
    #4 sec=6.2D.2.5 page=0 table=- score=0.356
    #5 sec=6.2G.1.5 page=0 table=6.2G.1.5-2 score=0.357

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p97 table=6.2.1.5-2
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.032
    #2 sec=6.2G.1.5 page=0 table=6.2G.1.5-2 score=0.029
    #3 sec=6.2D.2.5 page=0 table=- score=0.029
    #4 sec=6.2D.2_1.5 page=0 table=- score=0.027
    #5 sec=6.2.1.3 page=0 table=- score=0.026

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.973
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.940
    #3 sec=6.2A.1.1.5 page=0 table=6.2A.1.1.5-1a score=0.913
    #4 sec=6.2G.1.5 page=0 table=6.2G.1.5-2 score=0.870
    #5 sec=6.2.1.5 page=0 table=6.2.1.5-2 score=0.869

## q12 — What is the minimum output power limit and measurement bandwidth for a 10 MHz channel in FR1?
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.1.3 p0 table=6.3.1.3-1
    #1 sec=6.3.1.3 page=0 table=6.3.1.3-1 score=-18.040
    #2 sec=6.3E.1.0.1 page=0 table=6.3E.1.0.1-1 score=-17.433
    #3 sec=6.3F.3.2.5 page=0 table=6.3F.3.2.5-1 score=-17.395
    #4 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=-17.007
    #5 sec=6.3.4.2.5 page=0 table=6.3.4.2.5-1 score=-17.000

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.1.3 p0 table=6.3.1.3-1
    #1 sec=6.3.1.3 page=0 table=6.3.1.3-1 score=0.330
    #2 sec=6.3D.3_1.5 page=0 table=6.3D.3_1.5-1 score=0.330
    #3 sec=6.3G.3.2.5 page=0 table=6.3G.3.2.5-1 score=0.332
    #4 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=0.333
    #5 sec=6.3G.3.3.5 page=0 table=6.3G.3.3.5-1 score=0.334

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.1.3 p0 table=6.3.1.3-1
    #1 sec=6.3.1.3 page=0 table=6.3.1.3-1 score=0.033
    #2 sec=6.3F.3.2.5 page=0 table=6.3F.3.2.5-1 score=0.031
    #3 sec=6.3D.3_1.5 page=0 table=6.3D.3_1.5-1 score=0.029
    #4 sec=6.3.4.2.5 page=0 table=6.3.4.2.5-1 score=0.029
    #5 sec=6.3G.3.3.5 page=0 table=6.3G.3.3.5-1 score=0.029

**reranked:bge** — hit@1=N hit@3=N hit@5=N RR@10=0.10 · coverage = 2/3 (67%) · top-1 = §6.3F.3.2.5 p0 table=6.3F.3.2.5-1
  missing keywords: ['-40']
    #1 sec=6.3F.3.2.5 page=0 table=6.3F.3.2.5-1 score=0.938
    #2 sec=6.3D.3_1.5 page=0 table=6.3D.3_1.5-1 score=0.931
    #3 sec=6.3G.3.1.5 page=0 table=6.3G.3.1.5-1 score=0.926
    #4 sec=6.3.3.2.5 page=0 table=6.3.3.2.5-1 score=0.916
    #5 sec=6.3G.3.3.5 page=0 table=6.3G.3.3.5-1 score=0.909

## q13 — What is the absolute power tolerance for an NR UE under normal conditions?
_expected_section = §6.3.4.2 · type = numeric · difficulty = easy_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=-18.228
    #2 sec=6.3.4.2 page=567 table=- score=-18.228
    #3 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=-18.223
    #4 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=-18.223
    #5 sec=6.3.4.2.4.1 page=0 table=6.3.4.2.4.1-1 score=-14.159

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.14 · coverage = 0/2 (0%) · top-1 = §6.2B.4.0.1.3 p0 table=-
  missing keywords: ['absolute power tolerance', '9.0']
    #1 sec=6.2B.4.0.1.3 page=0 table=- score=0.315
    #2 sec=6.2B.1.1.5 page=0 table=- score=0.325
    #3 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.332
    #4 sec=6.5.3.2.3 page=0 table=6.5.3.2.3-1 score=0.344
    #5 sec=6.2D.1_1.5 page=0 table=- score=0.349

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.4.2.3 p0 table=-
  missing keywords: ['9.0']
    #1 sec=6.3.4.2.3 page=0 table=- score=0.028
    #2 sec=6.3A.4.1.0 page=0 table=- score=0.027
    #3 sec=6.3.4.1 page=567 table=- score=0.016
    #4 sec=6.2B.4.0.1.3 page=0 table=- score=0.016
    #5 sec=6.3.4.2 page=567 table=- score=0.016

**reranked:bge** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/2 (50%) · top-1 = §6.3.4.1 p567 table=-
  missing keywords: ['9.0']
    #1 sec=6.3.4.1 page=567 table=- score=0.955
    #2 sec=6.3.4.2 page=567 table=- score=0.955
    #3 sec=6.3.4.2.3 page=0 table=- score=0.766
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.747
    #5 sec=6.3A.4.1.0 page=0 table=- score=0.735

## q14 — What is the aggregate power tolerance for PUSCH transmissions with 0 dB TPC commands?
_expected_section = §6.3.4.4 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p588 table=6.3.4.4.3-1
    #1 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=-28.180
    #2 sec=6.3.4.4.3 page=0 table=6.3.4.4.3-1 score=-27.668
    #3 sec=6.3.4.4 page=587 table=- score=-24.929
    #4 sec=6.3.4.4.3 page=0 table=- score=-24.688
    #5 sec=6.3.4.4.4.2 page=0 table=- score=-20.585

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4.3 p0 table=6.3.4.4.3-1
    #1 sec=6.3.4.4.3 page=0 table=6.3.4.4.3-1 score=0.246
    #2 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=0.262
    #3 sec=6.3.4.3 page=576 table=- score=0.309
    #4 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.314
    #5 sec=6.3.4.4 page=590 table=- score=0.333

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p588 table=6.3.4.4.3-1
    #1 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=0.033
    #2 sec=6.3.4.4.3 page=0 table=6.3.4.4.3-1 score=0.033
    #3 sec=6.3.4.3 page=576 table=- score=0.031
    #4 sec=6.3D.4.3.5 page=0 table=6.3D.4.3.5-1 score=0.029
    #5 sec=6.3.4.4.4.2 page=0 table=- score=0.028

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p588 table=6.3.4.4.3-1
    #1 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=0.999
    #2 sec=6.3.4.4.3 page=0 table=6.3.4.4.3-1 score=0.998
    #3 sec=6.3.4.4.4.2 page=0 table=- score=0.981
    #4 sec=6.3.4.3 page=576 table=- score=0.974
    #5 sec=6.3.4.4 page=587 table=6.3.4.3.5-7 score=0.959

## q15 — What is the PCMAX tolerance when the configured maximum output power is between 21 and 23 dBm?
_expected_section = §6.2.4 · type = numeric · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2.2 p107 table=-
    #1 sec=6.2.2 page=107 table=- score=-26.524
    #2 sec=6.2.4 page=276 table=6.2.4.3-2 score=-23.970
    #3 sec=6.2.4 page=273 table=- score=-23.702
    #4 sec=6.2.3 page=263 table=6.2.3.5-29 score=-21.955
    #5 sec=6.2.4 page=278 table=6.2.4.5-1 score=-21.348

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p276 table=6.2.4.3-2
    #1 sec=6.2.4 page=276 table=6.2.4.3-2 score=0.228
    #2 sec=6.2B.4.0.1.3 page=0 table=- score=0.234
    #3 sec=6.2G.4.3 page=0 table=- score=0.293
    #4 sec=6.2.4 page=273 table=- score=0.310
    #5 sec=6.2A.3.1.5 page=0 table=6.2A.3.1.5-1 score=0.314

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p276 table=6.2.4.3-2
    #1 sec=6.2.4 page=276 table=6.2.4.3-2 score=0.033
    #2 sec=6.2.4 page=273 table=- score=0.031
    #3 sec=6.2.2.5 page=0 table=- score=0.025
    #4 sec=6.2.2 page=107 table=- score=0.016
    #5 sec=6.2B.4.0.1.3 page=0 table=- score=0.016

**reranked:bge** — hit@1=N hit@3=N hit@5=Y RR@10=0.20 · coverage = 3/3 (100%) · top-1 = §6.2.2.5 p0 table=6.2.2.5-1a
    #1 sec=6.2.2.5 page=0 table=6.2.2.5-1a score=0.984
    #2 sec=6.2G.2.5 page=0 table=6.2G.2.5-7 score=0.977
    #3 sec=6.2.2.5 page=0 table=6.2.2.5-2 score=0.975
    #4 sec=6.2.2.5 page=0 table=6.2.2.5-3 score=0.975
    #5 sec=6.2.4 page=276 table=6.2.4.3-2 score=0.973

## q16 — What is the allowed maximum power reduction for a power class 3 UE using DFT-s-OFDM 256 QAM modulation?
_expected_section = §6.2.2 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-2
    #1 sec=6.2.2 page=99 table=6.2.2.3-2 score=-29.609
    #2 sec=6.2.2 page=98 table=6.2.2.3-1 score=-24.418
    #3 sec=6.2.2.3 page=0 table=- score=-24.178
    #4 sec=6.5D.2.2.4.1 page=0 table=6.5D.2.2.4.1-3 score=-22.655
    #5 sec=6.2.2 page=99 table=6.2.2.3-5 score=-22.148

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p98 table=6.2.2.3-1
    #1 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.298
    #2 sec=6.2.2 page=99 table=6.2.2.3-2 score=0.326
    #3 sec=6.2.2.3 page=0 table=- score=0.339
    #4 sec=6.2.2 page=98 table=- score=0.341
    #5 sec=6.2.3 page=151 table=- score=0.361

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p98 table=6.2.2.3-1
    #1 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.033
    #2 sec=6.2.2 page=99 table=6.2.2.3-2 score=0.033
    #3 sec=6.2.2.3 page=0 table=- score=0.032
    #4 sec=6.2.2 page=98 table=- score=0.028
    #5 sec=6.2.3.3.20 page=0 table=6.2.3.3.21-2 score=0.026

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p98 table=6.2.2.3-1
    #1 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.994
    #2 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.988
    #3 sec=6.2.2.3 page=0 table=- score=0.985
    #4 sec=6.2.2 page=98 table=- score=0.978
    #5 sec=6.2.3 page=225 table=6.2.3.5-3 score=0.957

## q17 — Which test verifies the UE's ability to set its initial output power at the start of a transmission after a gap longer than 20ms?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.2.1 p0 table=-
    #1 sec=6.3.4.2.1 page=0 table=- score=-55.903
    #2 sec=6.3D.4.1.1 page=0 table=- score=-55.397
    #3 sec=6.3A.4.1.1.1 page=0 table=- score=-54.575
    #4 sec=6.3.4.1 page=567 table=- score=-50.391
    #5 sec=6.3.4.2 page=567 table=- score=-50.391

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.2.1 p0 table=-
    #1 sec=6.3.4.2.1 page=0 table=- score=0.207
    #2 sec=6.3D.4.1.1 page=0 table=- score=0.249
    #3 sec=6.3A.4.1.1.1 page=0 table=- score=0.276
    #4 sec=6.3D.4.2.1 page=0 table=- score=0.293
    #5 sec=6.3.4.3.1 page=0 table=- score=0.293

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.2.1 p0 table=-
    #1 sec=6.3.4.2.1 page=0 table=- score=0.033
    #2 sec=6.3D.4.1.1 page=0 table=- score=0.032
    #3 sec=6.3A.4.1.1.1 page=0 table=- score=0.032
    #4 sec=6.3.4.1 page=567 table=- score=0.031
    #5 sec=6.3.4.2 page=567 table=- score=0.030

**reranked:bge** — hit@1=N hit@3=N hit@5=Y RR@10=0.20 · coverage = 2/2 (100%) · top-1 = §6.3D.4.1.1 p0 table=-
    #1 sec=6.3D.4.1.1 page=0 table=- score=0.999
    #2 sec=6.3A.4.1.0 page=0 table=- score=0.995
    #3 sec=6.3A.4.1.1.1 page=0 table=- score=0.995
    #4 sec=6.3.4.1 page=567 table=- score=0.992
    #5 sec=6.3.4.2 page=567 table=- score=0.992

## q18 — What is the PRACH ON power measurement period for preamble format 0?
_expected_section = §6.3.3.4 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=-31.047
    #2 sec=6.3.3.3 page=550 table=- score=-30.617
    #3 sec=6.3.3.4 page=550 table=- score=-30.617
    #4 sec=6.3.3.4.3 page=0 table=- score=-30.537
    #5 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=-27.961

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4.3 p0 table=6.3.3.4.3-1
    #1 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.280
    #2 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.288
    #3 sec=6.3.3.3 page=550 table=- score=0.301
    #4 sec=6.3.3.4 page=550 table=- score=0.301
    #5 sec=6.3.3.4.3 page=0 table=- score=0.310

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.033
    #2 sec=6.3.3.3 page=550 table=- score=0.032
    #3 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.032
    #4 sec=6.3.3.4 page=550 table=- score=0.031
    #5 sec=6.3.3.4.3 page=0 table=- score=0.031

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.971
    #2 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.960
    #3 sec=6.3.3.4.3 page=0 table=- score=0.937
    #4 sec=6.3.3.3 page=550 table=- score=0.834
    #5 sec=6.3.3.4 page=550 table=- score=0.834

## q19 — Which power control commands does the SS send to drive the UE to its minimum output power during the conformance test?
_expected_section = §6.3.1 · type = procedure · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 2/2 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=-32.189
    #2 sec=6.3.4.4.3 page=0 table=- score=-26.783
    #3 sec=6.3.1.4.2 page=0 table=- score=-24.106
    #4 sec=6.3F.1.4.2 page=0 table=- score=-24.106
    #5 sec=6.3.4.4.1 page=0 table=- score=-22.963

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 1/2 (50%) · top-1 = §6.3.4.4 p587 table=-
  missing keywords: ['200ms']
    #1 sec=6.3.4.4 page=587 table=- score=0.378
    #2 sec=6.3A.4.2.1.4.2 page=0 table=- score=0.390
    #3 sec=6.3.4.3 page=576 table=- score=0.393
    #4 sec=6.3.4.3 page=576 table=- score=0.393
    #5 sec=6.3A.4.2.1.4.2 page=0 table=- score=0.396

**hybrid** — hit@1=N hit@3=N hit@5=Y RR@10=0.25 · coverage = 2/2 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=0.033
    #2 sec=6.3.4.1 page=567 table=- score=0.029
    #3 sec=6.3.4.2 page=567 table=- score=0.029
    #4 sec=6.3.1 page=543 table=- score=0.028
    #5 sec=6.4.2.1.4.2 page=0 table=- score=0.027

**reranked:bge** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 2/2 (100%) · top-1 = §6.4.2.1.4.2 p0 table=-
    #1 sec=6.4.2.1.4.2 page=0 table=- score=0.973
    #2 sec=6.3A.1.1.4.2 page=0 table=- score=0.965
    #3 sec=6.3.1 page=543 table=- score=0.964
    #4 sec=6.3D.1.4.2 page=0 table=- score=0.961
    #5 sec=6.3D.1_1.4.2 page=0 table=- score=0.960

## q20 — What is P-MPR in the PCMAX equation and what value must it take during UE conducted conformance testing?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4.3 p0 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4.3 page=0 table=- score=-34.722
    #2 sec=6.2.4 page=275 table=- score=-31.625
    #3 sec=H.2.2 page=0 table=- score=-29.092
    #4 sec=6.4.2.6.3 page=0 table=6.4.2.5-2 score=-20.752
    #5 sec=6.2.4.3 page=0 table=- score=-17.450

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4 p275 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4 page=275 table=- score=0.335
    #2 sec=6.2.4.3 page=0 table=- score=0.356
    #3 sec=6.2A.4.0.1.3 page=0 table=- score=0.363
    #4 sec=6.2B.4.0.1.3 page=0 table=- score=0.364
    #5 sec=6.2.4 page=273 table=- score=0.368

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4 p275 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4 page=275 table=- score=0.033
    #2 sec=6.2.4.3 page=0 table=- score=0.032
    #3 sec=6.2.4 page=273 table=- score=0.031
    #4 sec=6.2.4.3 page=0 table=- score=0.029
    #5 sec=6.2A.4.0.1.4 page=0 table=- score=0.028

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4.3 p0 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4.3 page=0 table=- score=0.962
    #2 sec=6.2.4 page=275 table=- score=0.941
    #3 sec=6.4.2.6.3 page=0 table=6.4.2.5-2 score=0.832
    #4 sec=6.2B.4.0.1.3 page=0 table=- score=0.831
    #5 sec=6.2A.4.0.1.4 page=0 table=- score=0.830

## q21 — In the UE Power Class table, what maximum output power and tolerance apply to band n14 for Power Class 1?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=-29.205
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=-27.957
    #3 sec=6.2A.1.1.5 page=0 table=- score=-26.916
    #4 sec=6.2.2 page=98 table=- score=-26.806
    #5 sec=6.2.2.5 page=0 table=- score=-26.176

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1.5 p0 table=6.2.1.5-2a
    #1 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.262
    #2 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.266
    #3 sec=6.2.2 page=118 table=6.2.2.5-6 score=0.279
    #4 sec=6.2.3 page=270 table=6.2.3.5-35 score=0.282
    #5 sec=6.2.2 page=110 table=6.2.2.5-1 score=0.287

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.033
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.031
    #3 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.030
    #4 sec=6.2.2.5 page=0 table=- score=0.030
    #5 sec=6.2.2.5 page=0 table=- score=0.029

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.998
    #2 sec=6.2.1.3 page=0 table=6.2.1.3-1 score=0.986
    #3 sec=6.2.3 page=270 table=6.2.3.5-35 score=0.973
    #4 sec=6.2.2 page=98 table=- score=0.968
    #5 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.967

## q22 — What is the allowed MPR for CP-OFDM 256 QAM modulation in outer RB allocations for a power class 3 UE?
_expected_section = §6.2.2 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-2
    #1 sec=6.2.2 page=99 table=6.2.2.3-2 score=-38.551
    #2 sec=6.2E.2.0.2 page=0 table=6.2E.2.0.2-1 score=-35.435
    #3 sec=6.2.2.3 page=0 table=6.2.2.3-2 score=-34.926
    #4 sec=6.2.2.3 page=0 table=6.2.2.3-5 score=-34.781
    #5 sec=6.2D.2.3 page=0 table=6.2D.2.3-1 score=-34.710

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p98 table=6.2.2.3-1
    #1 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.289
    #2 sec=6.2.2 page=99 table=6.2.2.3-2 score=0.299
    #3 sec=6.2.2.3 page=0 table=6.2.2.3-1 score=0.313
    #4 sec=6.2.3 page=151 table=- score=0.318
    #5 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.320

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-2
    #1 sec=6.2.2 page=99 table=6.2.2.3-2 score=0.033
    #2 sec=6.2E.2.0.2 page=0 table=6.2E.2.0.2-1 score=0.031
    #3 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.031
    #4 sec=6.2.2.3 page=0 table=6.2.2.3-1 score=0.031
    #5 sec=6.2.2.3 page=0 table=6.2.2.3-2 score=0.031

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-5
    #1 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.996
    #2 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.994
    #3 sec=6.2.2.3 page=0 table=- score=0.971
    #4 sec=6.2E.2.0.2 page=0 table=6.2E.2.0.2-1 score=0.962
    #5 sec=6.2.2 page=98 table=- score=0.959

## q23 — What is the PRACH ON power measurement period for preamble format C2 with 15 kHz SCS?
_expected_section = §6.3.3.4 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=-36.359
    #2 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=-33.799
    #3 sec=6.3.3.3 page=550 table=- score=-30.617
    #4 sec=6.3.3.4 page=550 table=- score=-30.617
    #5 sec=6.3.3.4.3 page=0 table=- score=-29.824

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4.3 p0 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.260
    #2 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.273
    #3 sec=6.3.3.4 page=554 table=6.3.3.4.4.3-2 score=0.339
    #4 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.350
    #5 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=0.356

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.033
    #2 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.033
    #3 sec=6.3.3.4 page=554 table=6.3.3.4.4.3-2 score=0.031
    #4 sec=6.3.3.3 page=550 table=- score=0.031
    #5 sec=6.3.3.4 page=550 table=- score=0.030

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.3.4.3 p0 table=6.3.3.4.3-1
    #1 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.903
    #2 sec=6.3.3.4 page=554 table=6.3.3.4.4.3-2 score=0.899
    #3 sec=6.3.3.4 page=551 table=- score=0.856
    #4 sec=6.3.3.4.3 page=0 table=- score=0.848
    #5 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.846

## q24 — What is the test requirement for measured UE output power at test point 2 in the configured transmitted power test?
_expected_section = §6.2.4 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=N hit@3=N hit@5=Y RR@10=0.25 · coverage = 2/2 (100%) · top-1 = §6.2D.4.5 p0 table=6.2D.4.5-1
    #1 sec=6.2D.4.5 page=0 table=6.2D.4.5-1 score=-27.568
    #2 sec=6.2D.4_1.5 page=0 table=6.2D.4_1.5-1 score=-27.568
    #3 sec=6.3.1 page=541 table=6.2I.4.5-1 score=-22.555
    #4 sec=6.2.4.5 page=0 table=- score=-22.341
    #5 sec=6.2G.4.5 page=0 table=- score=-22.311

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 1/2 (50%) · top-1 = §6.2D.4_1.5 p0 table=6.2D.4_1.5-1
  missing keywords: ['10 dbm']
    #1 sec=6.2D.4_1.5 page=0 table=6.2D.4_1.5-1 score=0.255
    #2 sec=6.2D.4.5 page=0 table=6.2D.4.5-1 score=0.263
    #3 sec=6.3A.2.1.1 page=0 table=- score=0.305
    #4 sec=6.3A.1.1.1 page=0 table=- score=0.315
    #5 sec=6.2B.4.1.1 page=0 table=- score=0.321

**hybrid** — hit@1=N hit@3=N hit@5=Y RR@10=0.25 · coverage = 2/2 (100%) · top-1 = §6.2D.4.5 p0 table=6.2D.4.5-1
    #1 sec=6.2D.4.5 page=0 table=6.2D.4.5-1 score=0.033
    #2 sec=6.2D.4_1.5 page=0 table=6.2D.4_1.5-1 score=0.033
    #3 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.029
    #4 sec=6.2.4.5 page=0 table=- score=0.029
    #5 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.028

**reranked:bge** — hit@1=N hit@3=N hit@5=Y RR@10=0.20 · coverage = 2/2 (100%) · top-1 = §6.2D.4.5 p0 table=6.2D.4.5-1
    #1 sec=6.2D.4.5 page=0 table=6.2D.4.5-1 score=0.997
    #2 sec=6.2D.4_1.5 page=0 table=6.2D.4_1.5-1 score=0.996
    #3 sec=6.2A.4.1.5 page=0 table=6.2A.4.1.5-1 score=0.979
    #4 sec=6.2B.4.1.5 page=0 table=6.2B.4.1.5-1 score=0.979
    #5 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.977

## q25 — In the 5 MHz ramp up sub-test, what is the expected power step size when the RB allocation changes from 1 RB to 15 RBs?
_expected_section = §6.3.4.3 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3 p579 table=6.3.4.3.5-1
    #1 sec=6.3.4.3 page=579 table=6.3.4.3.5-1 score=-38.985
    #2 sec=6.3.4.3 page=585 table=6.3.4.3.5-5 score=-36.677
    #3 sec=6.3.4.3 page=580 table=6.3.4.3.5-2 score=-36.065
    #4 sec=6.3.4.3 page=581 table=6.3.4.3.5-3 score=-34.516
    #5 sec=6.3.4.3 page=586 table=6.3.4.3.5-6 score=-34.442

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3 p579 table=6.3.4.3.5-1
    #1 sec=6.3.4.3 page=579 table=6.3.4.3.5-1 score=0.277
    #2 sec=6.3.4.3 page=580 table=6.3.4.3.5-2 score=0.282
    #3 sec=6.3.4.3 page=586 table=6.3.4.3.5-6 score=0.304
    #4 sec=6.3.4.3 page=585 table=6.3.4.3.5-5 score=0.307
    #5 sec=6.3.4.4 page=587 table=6.3.4.3.5-7 score=0.320

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3 p579 table=6.3.4.3.5-1
    #1 sec=6.3.4.3 page=579 table=6.3.4.3.5-1 score=0.033
    #2 sec=6.3.4.3 page=580 table=6.3.4.3.5-2 score=0.032
    #3 sec=6.3.4.3 page=585 table=6.3.4.3.5-5 score=0.032
    #4 sec=6.3.4.3 page=586 table=6.3.4.3.5-6 score=0.031
    #5 sec=6.3.4.3 page=581 table=6.3.4.3.5-3 score=0.031

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3 p579 table=6.3.4.3.5-1
    #1 sec=6.3.4.3 page=579 table=6.3.4.3.5-1 score=0.997
    #2 sec=6.3.4.3 page=581 table=6.3.4.3.5-3 score=0.993
    #3 sec=6.3.4.3 page=583 table=6.3.4.3.5-4 score=0.988
    #4 sec=6.3.4.3 page=585 table=6.3.4.3.5-5 score=0.987
    #5 sec=6.3.4.3 page=580 table=6.3.4.3.5-2 score=0.986

## q26 — Where is the Transmit OFF power requirement actually tested, given that clause 6.3.2 defines no standalone test procedure?
_expected_section = §6.3.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.10 · coverage = 1/2 (50%) · top-1 = §6.3.3.2.1 p0 table=-
  missing keywords: ['covered by']
    #1 sec=6.3.3.2.1 page=0 table=- score=-34.125
    #2 sec=6.3.3.1 page=545 table=- score=-32.607
    #3 sec=6.3.3.2 page=545 table=- score=-32.607
    #4 sec=6.3.3.1 page=545 table=- score=-31.712
    #5 sec=6.3.3.2 page=545 table=- score=-29.433

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.299
    #2 sec=6.3.2.5 page=0 table=- score=0.325
    #3 sec=6.3F.2.5 page=0 table=- score=0.328
    #4 sec=6.3E.2.2.5 page=0 table=- score=0.334
    #5 sec=6.3E.2.1.5 page=0 table=- score=0.334

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.031
    #2 sec=6.3.2.5 page=0 table=- score=0.029
    #3 sec=6.3.3.2 page=545 table=- score=0.029
    #4 sec=6.3.2 page=544 table=- score=0.028
    #5 sec=6.3.3.1 page=545 table=- score=0.027

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.2 p544 table=-
  missing keywords: ['covered by']
    #1 sec=6.3.2 page=544 table=- score=0.759
    #2 sec=6.3.2.3 page=0 table=- score=0.749
    #3 sec=6.3D.2.3 page=0 table=- score=0.728
    #4 sec=6.3A.2.0 page=0 table=- score=0.727
    #5 sec=6.3F.3.1 page=0 table=- score=0.723

## q27 — Which clauses define the MPR and A-MPR values used in the PCMAX_L formula for configured maximum output power?
_expected_section = §6.2.4 · type = section_summary · difficulty = hard_

**sparse** — hit@1=N hit@3=N hit@5=Y RR@10=0.20 · coverage = 3/3 (100%) · top-1 = §6.2A.4.0.1.4 p0 table=-
    #1 sec=6.2A.4.0.1.4 page=0 table=- score=-26.905
    #2 sec=6.2D.3.3 page=0 table=- score=-24.902
    #3 sec=6.2A.4.0.1.3 page=0 table=- score=-24.524
    #4 sec=6.2D.3_1.3 page=0 table=- score=-23.902
    #5 sec=6.2.4 page=275 table=6.2.4.3-1 score=-23.688

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.17 · coverage = 3/3 (100%) · top-1 = §6.2.3.3.2 p0 table=-
    #1 sec=6.2.3.3.2 page=0 table=- score=0.310
    #2 sec=6.2A.4.0.1.4 page=0 table=- score=0.313
    #3 sec=6.2A.4.0.1.3 page=0 table=- score=0.313
    #4 sec=6.2.3 page=129 table=- score=0.320
    #5 sec=6.2A.4.0.1.3 page=0 table=- score=0.321

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 3/3 (100%) · top-1 = §6.2A.4.0.1.4 p0 table=-
    #1 sec=6.2A.4.0.1.4 page=0 table=- score=0.033
    #2 sec=6.2A.4.0.1.3 page=0 table=- score=0.031
    #3 sec=6.2.4.3 page=0 table=- score=0.030
    #4 sec=6.2.4 page=273 table=- score=0.029
    #5 sec=6.2.3 page=222 table=- score=0.028

**reranked:bge** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 2/3 (67%) · top-1 = §6.2D.4.3 p0 table=-
  missing keywords: ['pcmax']
    #1 sec=6.2D.4.3 page=0 table=- score=0.985
    #2 sec=6.2A.4.0.1.4 page=0 table=- score=0.983
    #3 sec=6.2A.4.0.1.3 page=0 table=- score=0.961
    #4 sec=6.2.3 page=123 table=- score=0.960
    #5 sec=6.2A.3.0.3 page=0 table=- score=0.957

## q28 — What is the test purpose of the absolute power tolerance test?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=-13.445
    #2 sec=6.3.4.2 page=567 table=- score=-13.445
    #3 sec=6.3A.4.1.1.5 page=0 table=- score=-13.270
    #4 sec=6.3.4.2.5 page=0 table=- score=-12.680
    #5 sec=6.3C.4.1.5 page=0 table=- score=-12.680

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3A.4.1.0 p0 table=-
    #1 sec=6.3A.4.1.0 page=0 table=- score=0.334
    #2 sec=6.3.4.2.3 page=0 table=- score=0.341
    #3 sec=6.3.4.1 page=567 table=- score=0.349
    #4 sec=6.3.4.2 page=567 table=- score=0.349
    #5 sec=6.3.4.4 page=587 table=- score=0.378

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=0.032
    #2 sec=6.3.4.2 page=567 table=- score=0.032
    #3 sec=6.3A.4.1.0 page=0 table=- score=0.031
    #4 sec=6.3.4.2.3 page=0 table=- score=0.031
    #5 sec=6.3.4.2.5 page=0 table=- score=0.031

**reranked:bge** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=0.993
    #2 sec=6.3.4.2 page=567 table=- score=0.993
    #3 sec=6.3A.4.1.0 page=0 table=- score=0.966
    #4 sec=6.3.4.2.3 page=0 table=- score=0.872
    #5 sec=6.3G.4.3.3 page=0 table=- score=0.772

## q29 — What does the aggregate power tolerance test verify about UE transmitter behaviour?
_expected_section = §6.3.4.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=-19.876
    #2 sec=6.5.2.4.1.1 page=0 table=- score=-18.061
    #3 sec=6.5F.2.4.2.1 page=0 table=- score=-18.061
    #4 sec=6.5.2.4.2.1 page=0 table=- score=-18.061
    #5 sec=6.5C.2.4.1.1 page=0 table=- score=-18.061

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=0.271
    #2 sec=6.3.4.4.3 page=0 table=- score=0.278
    #3 sec=7.7A.1.4.2 page=0 table=- score=0.294
    #4 sec=6.3A.4.1.0 page=0 table=- score=0.295
    #5 sec=6.3.4.2.3 page=0 table=- score=0.306

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=0.033
    #2 sec=6.3.4.4.3 page=0 table=- score=0.016
    #3 sec=6.5.2.4.1.1 page=0 table=- score=0.016
    #4 sec=6.5F.2.4.2.1 page=0 table=- score=0.016
    #5 sec=7.7A.1.4.2 page=0 table=- score=0.016

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=0.991
    #2 sec=6.3.4.3 page=570 table=- score=0.884
    #3 sec=6.2F.1A.1 page=0 table=- score=0.878
    #4 sec=6.3.4.4.3 page=0 table=- score=0.877
    #5 sec=6.3.4.1 page=567 table=- score=0.874

## q30 — What is the test purpose of the relative power tolerance test, and within what transmission gap does it apply?
_expected_section = §6.3.4.3 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=Y RR@10=0.20 · coverage = 3/3 (100%) · top-1 = §6.4D.4.3 p0 table=-
    #1 sec=6.4D.4.3 page=0 table=- score=-25.498
    #2 sec=H.2.2 page=0 table=- score=-22.720
    #3 sec=6.3.4.1 page=567 table=- score=-21.818
    #4 sec=6.3.4.2 page=567 table=- score=-21.818
    #5 sec=6.3.4.3 page=570 table=- score=-21.026

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.3 p570 table=-
    #1 sec=6.3.4.3 page=570 table=- score=0.325
    #2 sec=6.3.4.1 page=567 table=- score=0.341
    #3 sec=6.3.4.2 page=567 table=- score=0.341
    #4 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.356
    #5 sec=6.3A.4.1.0 page=0 table=- score=0.360

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=0.032
    #2 sec=6.3.4.3 page=570 table=- score=0.032
    #3 sec=6.3.4.2 page=567 table=- score=0.031
    #4 sec=6.3.4.2.3 page=0 table=- score=0.030
    #5 sec=6.3.4.4 page=587 table=- score=0.029

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.3 p570 table=-
    #1 sec=6.3.4.3 page=570 table=- score=0.987
    #2 sec=6.3.4.1 page=567 table=- score=0.785
    #3 sec=6.3.4.2 page=567 table=- score=0.785
    #4 sec=6.3G.4.2.3 page=0 table=- score=0.737
    #5 sec=6.3A.4.3.0 page=0 table=- score=0.631
