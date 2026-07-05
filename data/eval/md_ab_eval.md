# Retrieval Benchmark

_scored at k=10 (hit@1/3/5, MRR@10); detail rows show top 5; source_format = tspec_md; backends = sparse, dense, hybrid_

## Aggregate

| backend | hit@1 | hit@3 | hit@5 | MRR@10 | mean coverage |
|---|---|---|---|---|---|
| sparse | 9/30 | 17/30 | 20/30 | 0.47 | 62% |
| dense | 14/30 | 19/30 | 20/30 | 0.56 | 68% |
| hybrid | 13/30 | 21/30 | 22/30 | 0.58 | 70% |

## By question type

| backend | type | n | hit@1 | hit@3 | hit@5 | MRR@10 | coverage |
|---|---|---|---|---|---|---|---|
| sparse | numeric | 9 | 44% | 67% | 78% | 0.58 | 80% |
| sparse | procedure | 3 | 0% | 67% | 100% | 0.34 | 61% |
| sparse | section_summary | 11 | 27% | 45% | 45% | 0.42 | 48% |
| sparse | table_lookup | 7 | 29% | 57% | 71% | 0.47 | 62% |
| dense | numeric | 9 | 33% | 44% | 44% | 0.42 | 78% |
| dense | procedure | 3 | 0% | 67% | 67% | 0.28 | 44% |
| dense | section_summary | 11 | 64% | 73% | 82% | 0.70 | 61% |
| dense | table_lookup | 7 | 57% | 71% | 71% | 0.64 | 79% |
| hybrid | numeric | 9 | 44% | 56% | 67% | 0.54 | 83% |
| hybrid | procedure | 3 | 33% | 67% | 67% | 0.48 | 44% |
| hybrid | section_summary | 11 | 55% | 73% | 73% | 0.64 | 56% |
| hybrid | table_lookup | 7 | 29% | 86% | 86% | 0.56 | 86% |

## q01 — What is the maximum output power tolerance for FR1 PC3 UE?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 2/3 (67%) · top-1 = §6.2A.2.1.5 p0 table=-
  missing keywords: ['23']
    #1 sec=6.2A.2.1.5 page=0 table=- score=-19.083
    #2 sec=6.2A.2.1.5 page=0 table=- score=-19.031
    #3 sec=6.2A.3.1.5 page=0 table=- score=-17.481
    #4 sec=6.2A.2.1.5 page=0 table=- score=-13.839
    #5 sec=6.2G.1.5 page=0 table=- score=-13.439

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 2/3 (67%) · top-1 = §6.2A.2.1.5 p0 table=-
  missing keywords: ['23']
    #1 sec=6.2A.2.1.5 page=0 table=- score=0.340
    #2 sec=6.2A.3.1.5 page=0 table=- score=0.342
    #3 sec=6.2.3.5 page=0 table=- score=0.356
    #4 sec=6.2G.2.3 page=0 table=- score=0.360
    #5 sec=6.2A.2.1.5 page=0 table=- score=0.364

**hybrid** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 2/3 (67%) · top-1 = §6.2A.2.1.5 p0 table=-
  missing keywords: ['23']
    #1 sec=6.2A.2.1.5 page=0 table=- score=0.033
    #2 sec=6.2A.3.1.5 page=0 table=- score=0.032
    #3 sec=6.2A.2.1.5 page=0 table=- score=0.032
    #4 sec=6.2A.4.1.5 page=0 table=- score=0.027
    #5 sec=6.2E.2.1D.5 page=0 table=- score=0.027

## q02 — How is the test procedure defined for UE maximum output power across power classes?
_expected_section = §6.2.1 · type = procedure · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 1/3 (33%) · top-1 = §6.2A.1.0.4 p0 table=-
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2A.1.0.4 page=0 table=- score=-17.575
    #2 sec=6.2A.1.0.3 page=0 table=- score=-16.882
    #3 sec=6.2.1.3 page=0 table=- score=-16.390
    #4 sec=6.2A.1.0.5 page=0 table=- score=-16.293
    #5 sec=6.2A.2.0.4 page=0 table=- score=-16.215

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/3 (33%) · top-1 = §6.2G.1.3 p0 table=-
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2G.1.3 page=0 table=- score=0.268
    #2 sec=6.2.1.3 page=0 table=- score=0.292
    #3 sec=6.2D.2.5 page=0 table=- score=0.293
    #4 sec=6.2G.1.5 page=0 table=- score=0.304
    #5 sec=6.2D.2_1.5 page=0 table=- score=0.312

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1.3 p0 table=-
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2.1.3 page=0 table=- score=0.032
    #2 sec=6.2G.2.3 page=0 table=- score=0.029
    #3 sec=6.2G.1.3 page=0 table=- score=0.028
    #4 sec=6.2G.1.5 page=0 table=- score=0.028
    #5 sec=6.2F.1.3 page=0 table=- score=0.027

## q03 — What are the test conditions and channel bandwidth for inner / outer maximum output power?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.11 · coverage = 3/3 (100%) · top-1 = §6.2E.2.0.2 p0 table=-
    #1 sec=6.2E.2.0.2 page=0 table=- score=-18.471
    #2 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-2c score=-15.488
    #3 sec=6.2A.2.1.4.1 page=0 table=6.2A.2.1.4.1-2b score=-15.366
    #4 sec=6.2A.2.1.4.1 page=0 table=6.2A.2.1.4.1-2a score=-15.189
    #5 sec=6.4.2.1.4.1 page=0 table=6.4.2.1.4.1-1 score=-14.947

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2A.2.1.4.1 p0 table=6.2A.2.1.4.1-3a
    #1 sec=6.2A.2.1.4.1 page=0 table=6.2A.2.1.4.1-3a score=0.299
    #2 sec=6.2.1.4.1 page=0 table=6.2.1.4.1-1 score=0.312
    #3 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-3 score=0.315
    #4 sec=6.2G.2.4.1 page=0 table=6.2G.2.4.1-3 score=0.316
    #5 sec=6.2C.1.5 page=0 table=6.2C.1.5-1 score=0.319

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2.2.4.1 p0 table=6.2.2.4.1-2c
    #1 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-2c score=0.031
    #2 sec=6.2.1.4.1 page=0 table=6.2.1.4.1-1 score=0.031
    #3 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-3 score=0.030
    #4 sec=6.2G.2.4.1 page=0 table=6.2G.2.4.1-3 score=0.029
    #5 sec=6.2G.2.4.1 page=0 table=6.2G.2.4.1-2 score=0.028

## q04 — Define UE output power dynamics — minimum output power requirement.
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/1 (100%) · top-1 = §6.3B p0 table=-
    #1 sec=6.3B page=0 table=- score=-19.065
    #2 sec=6.3.1.3 page=0 table=- score=-17.914
    #3 sec=6.3F.1.3 page=0 table=- score=-17.849
    #4 sec=6.3A.1.0 page=0 table=- score=-17.425
    #5 sec=6.3D.1.3 page=0 table=- score=-17.410

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/1 (100%) · top-1 = §6.3F.1.3 p0 table=-
    #1 sec=6.3F.1.3 page=0 table=- score=0.231
    #2 sec=6.3.1.3 page=0 table=- score=0.235
    #3 sec=6.3G.1.3 page=0 table=- score=0.257
    #4 sec=6.3D.1.3 page=0 table=- score=0.295
    #5 sec=6.3E.1.0.1 page=0 table=- score=0.304

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/1 (100%) · top-1 = §6.3F.1.3 p0 table=-
    #1 sec=6.3F.1.3 page=0 table=- score=0.032
    #2 sec=6.3.1.3 page=0 table=- score=0.032
    #3 sec=6.3D.1.3 page=0 table=- score=0.031
    #4 sec=6.3G.1.3 page=0 table=- score=0.031
    #5 sec=6.3.1.1 page=0 table=- score=0.029

## q05 — What is the transmit OFF power requirement for NR FR1 UE?
_expected_section = §6.3.2 · type = numeric · difficulty = easy_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 2/2 (100%) · top-1 = §6.3.3.2.3 p0 table=-
    #1 sec=6.3.3.2.3 page=0 table=- score=-18.838
    #2 sec=6.3A.2.0 page=0 table=- score=-15.984
    #3 sec=6.3.2.3 page=0 table=- score=-15.612
    #4 sec=6.3F.2.3 page=0 table=- score=-15.542
    #5 sec=6.3D.2.5 page=0 table=- score=-15.407

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 2/2 (100%) · top-1 = §6.3E.2.0.1 p0 table=-
    #1 sec=6.3E.2.0.1 page=0 table=- score=0.312
    #2 sec=6.5.3.2.3 page=0 table=6.5.3.2.3-1 score=0.348
    #3 sec=6.5.3.2.3 page=0 table=6.5.3.2.3-2 score=0.356
    #4 sec=6.5.3.3.3.10 page=0 table=- score=0.356
    #5 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.359

**hybrid** — hit@1=N hit@3=N hit@5=N RR@10=0.14 · coverage = 2/2 (100%) · top-1 = §6.3E.2.0.1 p0 table=-
    #1 sec=6.3E.2.0.1 page=0 table=- score=0.028
    #2 sec=6.3G.2.3 page=0 table=- score=0.027
    #3 sec=6.3A.2.1.1 page=0 table=- score=0.023
    #4 sec=6.3.3.2.3 page=0 table=- score=0.016
    #5 sec=6.3A.2.0 page=0 table=- score=0.016

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
    #3 sec=6.3.4.4.3 page=0 table=- score=0.337
    #4 sec=6.3.4.3.3 page=0 table=- score=0.342
    #5 sec=6.3G.4.3.3 page=0 table=- score=0.343

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3A.4.1.0 p0 table=-
    #1 sec=6.3A.4.1.0 page=0 table=- score=0.028
    #2 sec=6.3.4.2.3 page=0 table=- score=0.028
    #3 sec=6.3.4.2.5 page=0 table=- score=0.028
    #4 sec=6.3.4.3.3 page=0 table=- score=0.028
    #5 sec=6.3D.4.2.5 page=0 table=- score=0.027

## q07 — What is the configured transmitted power for UE in NR?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.11 · coverage = 1/1 (100%) · top-1 = §6.2A.1.0.3 p0 table=-
    #1 sec=6.2A.1.0.3 page=0 table=- score=-12.951
    #2 sec=6.2A.4.1.5 page=0 table=- score=-12.503
    #3 sec=6.2.1.3 page=0 table=- score=-12.064
    #4 sec=6.2G.1.3 page=0 table=- score=-11.433
    #5 sec=3.2 page=0 table=- score=-11.041

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 0/1 (0%) · top-1 = §6.2B.4.0.1.3 p0 table=-
  missing keywords: ['configured transmitted power']
    #1 sec=6.2B.4.0.1.3 page=0 table=- score=0.324
    #2 sec=6.2E.1.0.1 page=0 table=- score=0.333
    #3 sec=6.5.3.2.3 page=0 table=6.5.3.2.3-1 score=0.334
    #4 sec=6.5.3.2.3 page=0 table=6.5.3.2.3-2 score=0.341
    #5 sec=6.5E.2.2.1D.1 page=0 table=- score=0.348

**hybrid** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 0/1 (0%) · top-1 = §3.2 p0 table=-
  missing keywords: ['configured transmitted power']
    #1 sec=3.2 page=0 table=- score=0.029
    #2 sec=6.5E.2.2.1D.1 page=0 table=- score=0.027
    #3 sec=6.5E.2.2.1.1 page=0 table=- score=0.027
    #4 sec=6.2B.4.0.1.3 page=0 table=- score=0.026
    #5 sec=6.2C.1.3 page=0 table=- score=0.025

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

## q09 — What is the test purpose for the minimum output power conformance test?
_expected_section = §6.3.1 · type = section_summary · difficulty = easy_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 1/2 (50%) · top-1 = §6.4G.2.1.4.2 p0 table=-
  missing keywords: ['test purpose']
    #1 sec=6.4G.2.1.4.2 page=0 table=- score=-11.095
    #2 sec=6.4F.2.2.4.2 page=0 table=- score=-10.847
    #3 sec=6.4D.2.1_1.4.2 page=0 table=- score=-10.746
    #4 sec=6.4D.2.1.4.2 page=0 table=- score=-10.746
    #5 sec=6.4.2.2.4.2 page=0 table=- score=-10.539

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.1.1 p0 table=-
  missing keywords: ['test purpose']
    #1 sec=6.3.1.1 page=0 table=- score=0.347
    #2 sec=6.3F.1.1 page=0 table=- score=0.347
    #3 sec=6.3D.1.1 page=0 table=- score=0.357
    #4 sec=6.3A.1.1.1 page=0 table=- score=0.387
    #5 sec=6.3G.1.3 page=0 table=- score=0.390

**hybrid** — hit@1=N hit@3=N hit@5=N RR@10=0.12 · coverage = 1/2 (50%) · top-1 = §6.2B.3.1.3 p0 table=-
  missing keywords: ['test purpose']
    #1 sec=6.2B.3.1.3 page=0 table=- score=0.029
    #2 sec=6.2A.3.1.3 page=0 table=- score=0.028
    #3 sec=7.3C.2.3 page=0 table=- score=0.027
    #4 sec=7.3C.3.3 page=0 table=- score=0.026
    #5 sec=7.5A.1.3 page=0 table=- score=0.024

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

## q11 — What is the maximum output power for a Power Class 2 UE in NR band n78?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.14 · coverage = 2/3 (67%) · top-1 = §6.2A.3.1.5 p0 table=-
  missing keywords: ['26']
    #1 sec=6.2A.3.1.5 page=0 table=- score=-20.823
    #2 sec=6.2D.2.5 page=0 table=- score=-19.451
    #3 sec=6.2G.1.5 page=0 table=- score=-18.166
    #4 sec=6.2G.2.5 page=0 table=- score=-17.915
    #5 sec=6.2A.1.0.4 page=0 table=- score=-16.941

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.14 · coverage = 2/3 (67%) · top-1 = §6.2D.2.5 p0 table=-
  missing keywords: ['26']
    #1 sec=6.2D.2.5 page=0 table=- score=0.351
    #2 sec=6.2D.2.5 page=0 table=- score=0.352
    #3 sec=6.2D.2.5 page=0 table=- score=0.356
    #4 sec=6.2G.1.5 page=0 table=6.2G.1.5-2 score=0.357
    #5 sec=6.2D.3.5 page=0 table=- score=0.358

**hybrid** — hit@1=N hit@3=N hit@5=Y RR@10=0.25 · coverage = 3/3 (100%) · top-1 = §6.2G.1.5 p0 table=6.2G.1.5-2
    #1 sec=6.2G.1.5 page=0 table=6.2G.1.5-2 score=0.030
    #2 sec=6.2D.2.5 page=0 table=- score=0.029
    #3 sec=6.2D.2_1.5 page=0 table=- score=0.028
    #4 sec=6.2.1.3 page=0 table=- score=0.027
    #5 sec=6.2.1.5 page=0 table=6.2.1.5-2 score=0.027

## q12 — What is the minimum output power limit and measurement bandwidth for a 10 MHz channel in FR1?
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.1.3 p0 table=6.3.1.3-1
    #1 sec=6.3.1.3 page=0 table=6.3.1.3-1 score=-18.040
    #2 sec=6.3E.1.0.1 page=0 table=6.3E.1.0.1-1 score=-17.433
    #3 sec=6.3F.3.2.5 page=0 table=6.3F.3.2.5-1 score=-17.395
    #4 sec=6.3.4.2.5 page=0 table=6.3.4.2.5-1 score=-17.000
    #5 sec=6.3D.4.1.5 page=0 table=6.3D.4.1.5-1 score=-17.000

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
    #4 sec=6.3G.3.3.5 page=0 table=6.3G.3.3.5-1 score=0.029
    #5 sec=6.3.4.2.5 page=0 table=6.3.4.2.5-1 score=0.029

## q13 — What is the absolute power tolerance for an NR UE under normal conditions?
_expected_section = §6.3.4.2 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.4.2.4.1 p0 table=6.3.4.2.4.1-1
  missing keywords: ['9.0']
    #1 sec=6.3.4.2.4.1 page=0 table=6.3.4.2.4.1-1 score=-14.159
    #2 sec=6.3D.4.1.4.1 page=0 table=6.3D.4.1.4.1-1 score=-13.869
    #3 sec=6.3.4.1 page=0 table=- score=-13.814
    #4 sec=6.3A.4.1.1.5 page=0 table=- score=-12.880
    #5 sec=F.1.0 page=0 table=- score=-12.733

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.17 · coverage = 0/2 (0%) · top-1 = §6.2B.4.0.1.3 p0 table=-
  missing keywords: ['absolute power tolerance', '9.0']
    #1 sec=6.2B.4.0.1.3 page=0 table=- score=0.315
    #2 sec=6.2B.1.1.5 page=0 table=- score=0.325
    #3 sec=6.5.3.2.3 page=0 table=6.5.3.2.3-1 score=0.344
    #4 sec=6.2D.1_1.5 page=0 table=- score=0.349
    #5 sec=6.2D.1.5 page=0 table=- score=0.349

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.4.2.3 p0 table=-
  missing keywords: ['9.0']
    #1 sec=6.3.4.2.3 page=0 table=- score=0.029
    #2 sec=6.3A.4.1.0 page=0 table=- score=0.029
    #3 sec=6.2B.4.0.1.3 page=0 table=- score=0.016
    #4 sec=6.3.4.2.4.1 page=0 table=6.3.4.2.4.1-1 score=0.016
    #5 sec=6.2B.1.1.5 page=0 table=- score=0.016

## q14 — What is the aggregate power tolerance for PUSCH transmissions with 0 dB TPC commands?
_expected_section = §6.3.4.4 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4.3 p0 table=6.3.4.4.3-1
    #1 sec=6.3.4.4.3 page=0 table=6.3.4.4.3-1 score=-27.668
    #2 sec=6.3.4.4.3 page=0 table=- score=-24.688
    #3 sec=6.3.4.4.4.2 page=0 table=- score=-20.585
    #4 sec=6.3D.4.2_1.4.2 page=0 table=- score=-20.270
    #5 sec=6.3.4.4.4.2 page=0 table=- score=-19.697

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4.3 p0 table=6.3.4.4.3-1
    #1 sec=6.3.4.4.3 page=0 table=6.3.4.4.3-1 score=0.246
    #2 sec=6.3.4.3.3 page=0 table=6.3.4.3.3-1 score=0.349
    #3 sec=6.3D.4.3.5 page=0 table=6.3D.4.3.5-1 score=0.357
    #4 sec=6.3C.4.3.5 page=0 table=6.3C.4.3.5-1 score=0.358
    #5 sec=6.3D.4.3_1.5 page=0 table=6.3D.4.3_1.5-1 score=0.358

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4.3 p0 table=6.3.4.4.3-1
    #1 sec=6.3.4.4.3 page=0 table=6.3.4.4.3-1 score=0.033
    #2 sec=6.3D.4.3.5 page=0 table=6.3D.4.3.5-1 score=0.031
    #3 sec=6.3.4.4.4.2 page=0 table=- score=0.030
    #4 sec=6.3.4.4.4.2 page=0 table=- score=0.029
    #5 sec=6.3A.4.3.1.5 page=0 table=6.3A.4.3.1.5-1 score=0.029

## q15 — What is the PCMAX tolerance when the configured maximum output power is between 21 and 23 dBm?
_expected_section = §6.2.4 · type = numeric · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=Y RR@10=0.25 · coverage = 2/3 (67%) · top-1 = §6.2E.1.0.1 p0 table=-
  missing keywords: ['pcmax']
    #1 sec=6.2E.1.0.1 page=0 table=- score=-19.261
    #2 sec=6.2A.4.0.1.4 page=0 table=- score=-17.650
    #3 sec=6.2A.4.0.1.3 page=0 table=- score=-17.490
    #4 sec=6.2.4.3 page=0 table=- score=-17.226
    #5 sec=6.2.2.5 page=0 table=- score=-16.982

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 2/3 (67%) · top-1 = §6.2B.4.0.1.3 p0 table=-
  missing keywords: ['pcmax']
    #1 sec=6.2B.4.0.1.3 page=0 table=- score=0.234
    #2 sec=6.2G.4.3 page=0 table=- score=0.293
    #3 sec=6.2A.3.1.5 page=0 table=6.2A.3.1.5-1 score=0.314
    #4 sec=6.2G.2.5 page=0 table=6.2G.2.5-7 score=0.322
    #5 sec=6.2G.2.5 page=0 table=6.2G.2.5-6 score=0.323

**hybrid** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 2/3 (67%) · top-1 = §6.2.2.5 p0 table=-
  missing keywords: ['pcmax']
    #1 sec=6.2.2.5 page=0 table=- score=0.030
    #2 sec=6.2A.2.1.5 page=0 table=- score=0.027
    #3 sec=6.2.3.5 page=0 table=6.2.3.5-29 score=0.027
    #4 sec=6.2.3.5 page=0 table=6.2.3.5-12 score=0.026
    #5 sec=6.2C.5.5 page=0 table=6.2C.5.5-7 score=0.026

## q16 — What is the allowed maximum power reduction for a power class 3 UE using DFT-s-OFDM 256 QAM modulation?
_expected_section = §6.2.2 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.2.3 p0 table=-
  missing keywords: ['4.5']
    #1 sec=6.2.2.3 page=0 table=- score=-24.178
    #2 sec=6.5D.2.2.4.1 page=0 table=6.5D.2.2.4.1-3 score=-22.655
    #3 sec=6.5D.2.2.4.1 page=0 table=6.5D.2.2.4.1-2 score=-22.128
    #4 sec=6.2D.2.4.1 page=0 table=6.2D.2.4.1-2a score=-22.053
    #5 sec=6.2D.2.4.1 page=0 table=6.2D.2.4.1-3a score=-22.053

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2.3 p0 table=-
    #1 sec=6.2.2.3 page=0 table=- score=0.339
    #2 sec=6.2.3.3.20 page=0 table=6.2.3.3.21-2 score=0.370
    #3 sec=6.2.3.3.1 page=0 table=6.2.3.3.1-2 score=0.371
    #4 sec=6.4.2.1a.4.2 page=0 table=- score=0.374
    #5 sec=6.4.2.1.4.2 page=0 table=- score=0.375

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.2.3 p0 table=-
  missing keywords: ['4.5']
    #1 sec=6.2.2.3 page=0 table=- score=0.033
    #2 sec=6.2.3.3.20 page=0 table=6.2.3.3.21-2 score=0.029
    #3 sec=6.2.3.3.23 page=0 table=6.2.3.3.23-2 score=0.027
    #4 sec=6.2D.2.3 page=0 table=- score=0.026
    #5 sec=6.5D.2.2.4.1 page=0 table=6.5D.2.2.4.1-3 score=0.016

## q17 — Which test verifies the UE's ability to set its initial output power at the start of a transmission after a gap longer than 20ms?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.2.1 p0 table=-
    #1 sec=6.3.4.2.1 page=0 table=- score=-55.903
    #2 sec=6.3D.4.1.1 page=0 table=- score=-55.397
    #3 sec=6.3A.4.1.1.1 page=0 table=- score=-54.575
    #4 sec=6.3.4.2.3 page=0 table=- score=-44.863
    #5 sec=6.3A.4.1.0 page=0 table=- score=-43.165

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
    #4 sec=6.3.4.3.1 page=0 table=- score=0.031
    #5 sec=6.3D.4.2.1 page=0 table=- score=0.030

## q18 — What is the PRACH ON power measurement period for preamble format 0?
_expected_section = §6.3.3.4 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4.3 p0 table=-
    #1 sec=6.3.3.4.3 page=0 table=- score=-30.537
    #2 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=-27.961
    #3 sec=6.3.3.4.4.2 page=0 table=- score=-24.692
    #4 sec=E.6.2 page=0 table=- score=-20.646
    #5 sec=E.6.3 page=0 table=- score=-19.700

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4.3 p0 table=6.3.3.4.3-1
    #1 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.280
    #2 sec=6.3.3.4.3 page=0 table=- score=0.310
    #3 sec=6.4.2.1.4.3 page=0 table=- score=0.334
    #4 sec=E.6.3 page=0 table=- score=0.365
    #5 sec=6.4.2.1.4.3 page=0 table=- score=0.383

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4.3 p0 table=-
    #1 sec=6.3.3.4.3 page=0 table=- score=0.033
    #2 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.033
    #3 sec=E.6.3 page=0 table=- score=0.031
    #4 sec=6.3.3.4.4.2 page=0 table=- score=0.031
    #5 sec=E.6.2 page=0 table=- score=0.031

## q19 — Which power control commands does the SS send to drive the UE to its minimum output power during the conformance test?
_expected_section = §6.3.1 · type = procedure · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.4.3 p0 table=-
    #1 sec=6.3.4.4.3 page=0 table=- score=-26.783
    #2 sec=6.3.1.4.2 page=0 table=- score=-24.106
    #3 sec=6.3F.1.4.2 page=0 table=- score=-24.106
    #4 sec=6.3.4.4.1 page=0 table=- score=-22.963
    #5 sec=6.3D.4.3.1 page=0 table=- score=-22.815

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 1/2 (50%) · top-1 = §6.3A.4.2.1.4.2 p0 table=-
  missing keywords: ['200ms']
    #1 sec=6.3A.4.2.1.4.2 page=0 table=- score=0.390
    #2 sec=6.3A.4.2.1.4.2 page=0 table=- score=0.396
    #3 sec=6.3A.4.3.1.4.2 page=0 table=- score=0.400
    #4 sec=6.3.4.3.4.2 page=0 table=- score=0.404
    #5 sec=6.3A.4.2.1.4.2 page=0 table=- score=0.407

**hybrid** — hit@1=N hit@3=N hit@5=N RR@10=0.10 · coverage = 1/2 (50%) · top-1 = §6.4.2.1.4.2 p0 table=-
  missing keywords: ['down']
    #1 sec=6.4.2.1.4.2 page=0 table=- score=0.029
    #2 sec=6.3.3.6.4.2 page=0 table=- score=0.029
    #3 sec=6.4F.2.1.4.2 page=0 table=- score=0.029
    #4 sec=6.3D.4.3.1 page=0 table=- score=0.027
    #5 sec=6.4.2.1.4.2 page=0 table=- score=0.027

## q20 — What is P-MPR in the PCMAX equation and what value must it take during UE conducted conformance testing?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4.3 p0 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4.3 page=0 table=- score=-34.722
    #2 sec=H.2.2 page=0 table=- score=-29.092
    #3 sec=6.4.2.6.3 page=0 table=6.4.2.5-2 score=-20.752
    #4 sec=6.2.4.3 page=0 table=- score=-17.450
    #5 sec=H.2.6 page=0 table=- score=-13.023

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4.3 p0 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4.3 page=0 table=- score=0.356
    #2 sec=6.2A.4.0.1.3 page=0 table=- score=0.363
    #3 sec=6.2B.4.0.1.3 page=0 table=- score=0.364
    #4 sec=6.2G.4.3 page=0 table=- score=0.374
    #5 sec=6.2A.4.0.1.4 page=0 table=- score=0.380

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4.3 p0 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4.3 page=0 table=- score=0.032
    #2 sec=6.2.4.3 page=0 table=- score=0.030
    #3 sec=6.2A.4.0.1.4 page=0 table=- score=0.029
    #4 sec=6.2B.4.0.1.3 page=0 table=- score=0.028
    #5 sec=6.2A.4.0.1.3 page=0 table=- score=0.016

## q21 — In the UE Power Class table, what maximum output power and tolerance apply to band n14 for Power Class 1?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.12 · coverage = 1/3 (33%) · top-1 = §6.2A.1.1.5 p0 table=-
  missing keywords: ['31', 'public safety']
    #1 sec=6.2A.1.1.5 page=0 table=- score=-26.916
    #2 sec=6.2.2.5 page=0 table=- score=-26.176
    #3 sec=6.2G.1.5 page=0 table=- score=-25.767
    #4 sec=6.2A.3.1.5 page=0 table=- score=-25.670
    #5 sec=6.2.3.5 page=0 table=- score=-25.436

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1.5 p0 table=6.2.1.5-2a
    #1 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.262
    #2 sec=6.2.2.5 page=0 table=- score=0.288
    #3 sec=6.5.2.4.1.3 page=0 table=6.5.2.4.1.3-2 score=0.290
    #4 sec=6.2.2.5 page=0 table=- score=0.293
    #5 sec=6.2.1.3 page=0 table=6.2.1.3-1 score=0.301

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2.2.5 p0 table=-
    #1 sec=6.2.2.5 page=0 table=- score=0.032
    #2 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.031
    #3 sec=6.2.2.5 page=0 table=- score=0.031
    #4 sec=6.2A.3.1.5 page=0 table=- score=0.030
    #5 sec=6.2D.2.5 page=0 table=- score=0.028

## q22 — What is the allowed MPR for CP-OFDM 256 QAM modulation in outer RB allocations for a power class 3 UE?
_expected_section = §6.2.2 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2E.2.0.2 p0 table=6.2E.2.0.2-1
    #1 sec=6.2E.2.0.2 page=0 table=6.2E.2.0.2-1 score=-35.435
    #2 sec=6.2.2.3 page=0 table=6.2.2.3-2 score=-34.926
    #3 sec=6.2.2.3 page=0 table=6.2.2.3-5 score=-34.781
    #4 sec=6.2D.2.3 page=0 table=6.2D.2.3-1 score=-34.710
    #5 sec=6.2D.2.3 page=0 table=6.2D.2.3-2 score=-33.742

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2.3 p0 table=6.2.2.3-1
    #1 sec=6.2.2.3 page=0 table=6.2.2.3-1 score=0.313
    #2 sec=6.2E.2.0.2 page=0 table=6.2E.2.0.2-1 score=0.320
    #3 sec=6.2D.2.3 page=0 table=6.2D.2.3-2 score=0.324
    #4 sec=6.2.2.3 page=0 table=6.2.2.3-2 score=0.324
    #5 sec=6.2D.2.3 page=0 table=6.2D.2.3-1 score=0.325

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2E.2.0.2 p0 table=6.2E.2.0.2-1
    #1 sec=6.2E.2.0.2 page=0 table=6.2E.2.0.2-1 score=0.033
    #2 sec=6.2.2.3 page=0 table=6.2.2.3-2 score=0.032
    #3 sec=6.2.2.3 page=0 table=6.2.2.3-1 score=0.031
    #4 sec=6.2D.2.3 page=0 table=6.2D.2.3-2 score=0.031
    #5 sec=6.2D.2.3 page=0 table=6.2D.2.3-1 score=0.031

## q23 — What is the PRACH ON power measurement period for preamble format C2 with 15 kHz SCS?
_expected_section = §6.3.3.4 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4.3 p0 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=-33.799
    #2 sec=6.3.3.4.3 page=0 table=- score=-29.824
    #3 sec=6.3.3.4.4.2 page=0 table=- score=-24.692
    #4 sec=6.3.3.4.4.3 page=0 table=6.3.3.4.4.3-2 score=-24.526
    #5 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=-21.543

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4.3 p0 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.260
    #2 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=0.356
    #3 sec=6.3G.3.2.5 page=0 table=6.3G.3.2.5-1 score=0.359
    #4 sec=6.3.3.4.3 page=0 table=- score=0.381
    #5 sec=6.3.3.4.4.2 page=0 table=- score=0.395

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4.3 p0 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.033
    #2 sec=6.3.3.4.3 page=0 table=- score=0.032
    #3 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=0.032
    #4 sec=6.3.3.4.4.2 page=0 table=- score=0.031
    #5 sec=6.3G.3.2.5 page=0 table=6.3G.3.2.5-1 score=0.031

## q24 — What is the test requirement for measured UE output power at test point 2 in the configured transmitted power test?
_expected_section = §6.2.4 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 1/2 (50%) · top-1 = §6.2D.4.5 p0 table=6.2D.4.5-1
  missing keywords: ['10 dbm']
    #1 sec=6.2D.4.5 page=0 table=6.2D.4.5-1 score=-27.568
    #2 sec=6.2D.4_1.5 page=0 table=6.2D.4_1.5-1 score=-27.568
    #3 sec=6.2.4.5 page=0 table=- score=-22.341
    #4 sec=6.2G.4.5 page=0 table=- score=-22.311
    #5 sec=6.4G.2.1.4.2 page=0 table=- score=-20.239

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 1/2 (50%) · top-1 = §6.2D.4_1.5 p0 table=6.2D.4_1.5-1
  missing keywords: ['10 dbm']
    #1 sec=6.2D.4_1.5 page=0 table=6.2D.4_1.5-1 score=0.255
    #2 sec=6.2D.4.5 page=0 table=6.2D.4.5-1 score=0.263
    #3 sec=6.3A.2.1.1 page=0 table=- score=0.305
    #4 sec=6.3A.1.1.1 page=0 table=- score=0.315
    #5 sec=6.2B.4.1.1 page=0 table=- score=0.321

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 2/2 (100%) · top-1 = §6.2D.4.5 p0 table=6.2D.4.5-1
    #1 sec=6.2D.4.5 page=0 table=6.2D.4.5-1 score=0.033
    #2 sec=6.2D.4_1.5 page=0 table=6.2D.4_1.5-1 score=0.033
    #3 sec=6.2.4.5 page=0 table=- score=0.029
    #4 sec=6.2G.4.5 page=0 table=6.2G.4.5-1 score=0.028
    #5 sec=6.2.4.5 page=0 table=6.2.4.5-1 score=0.027

## q25 — In the 5 MHz ramp up sub-test, what is the expected power step size when the RB allocation changes from 1 RB to 15 RBs?
_expected_section = §6.3.4.3 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=N hit@3=N hit@5=Y RR@10=0.25 · coverage = 1/2 (50%) · top-1 = §6.3C.4.2.5 p0 table=-
  missing keywords: ['12.76']
    #1 sec=6.3C.4.2.5 page=0 table=- score=-33.873
    #2 sec=6.3G.4.2.5 page=0 table=- score=-32.292
    #3 sec=6.3D.4.2.5 page=0 table=- score=-32.230
    #4 sec=6.3.4.3.5 page=0 table=- score=-32.169
    #5 sec=6.3D.4.2_1.5 page=0 table=- score=-31.334

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 2/2 (100%) · top-1 = §6.3C.4.2.5 p0 table=-
    #1 sec=6.3C.4.2.5 page=0 table=- score=0.347
    #2 sec=6.3C.4.2.5 page=0 table=6.3C.4.2.5-2 score=0.349
    #3 sec=6.3D.4.2_1.5 page=0 table=6.3D.4.2_1.5-4 score=0.351
    #4 sec=6.3D.4.2_1.5 page=0 table=6.3D.4.2_1.5-1 score=0.351
    #5 sec=6.3C.4.2.5 page=0 table=6.3C.4.2.5-1 score=0.351

**hybrid** — hit@1=N hit@3=N hit@5=N RR@10=0.10 · coverage = 2/2 (100%) · top-1 = §6.3C.4.2.5 p0 table=-
    #1 sec=6.3C.4.2.5 page=0 table=- score=0.033
    #2 sec=6.3D.4.2_1.5 page=0 table=6.3D.4.2_1.5-1 score=0.031
    #3 sec=6.3C.4.2.5 page=0 table=6.3C.4.2.5-1 score=0.031
    #4 sec=6.3C.4.2.5 page=0 table=6.3C.4.2.5-2 score=0.030
    #5 sec=6.3C.4.2.5 page=0 table=6.3C.4.2.5-3 score=0.029

## q26 — Where is the Transmit OFF power requirement actually tested, given that clause 6.3.2 defines no standalone test procedure?
_expected_section = §6.3.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.17 · coverage = 0/2 (0%) · top-1 = §6.3.3.2.1 p0 table=-
  missing keywords: ['covered by', 'transmit on/off time mask']
    #1 sec=6.3.3.2.1 page=0 table=- score=-34.125
    #2 sec=6.3.3.1 page=0 table=- score=-29.290
    #3 sec=6.3F.3.2.1 page=0 table=- score=-27.613
    #4 sec=6.3D.3.1 page=0 table=- score=-27.496
    #5 sec=6.3A.3.1.1 page=0 table=- score=-25.958

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.2.5 p0 table=-
  missing keywords: ['covered by', 'transmit on/off time mask']
    #1 sec=6.3.2.5 page=0 table=- score=0.325
    #2 sec=6.3F.2.5 page=0 table=- score=0.328
    #3 sec=6.3E.2.2.5 page=0 table=- score=0.334
    #4 sec=6.3E.2.1.5 page=0 table=- score=0.334
    #5 sec=6.3E.2.1D.5 page=0 table=- score=0.337

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.2.5 p0 table=-
  missing keywords: ['covered by', 'transmit on/off time mask']
    #1 sec=6.3.2.5 page=0 table=- score=0.031
    #2 sec=6.3.2.3 page=0 table=- score=0.028
    #3 sec=6.3A.3.1.5 page=0 table=- score=0.028
    #4 sec=6.3F.2.5 page=0 table=- score=0.027
    #5 sec=6.3F.2.3 page=0 table=- score=0.027

## q27 — Which clauses define the MPR and A-MPR values used in the PCMAX_L formula for configured maximum output power?
_expected_section = §6.2.4 · type = section_summary · difficulty = hard_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.17 · coverage = 2/3 (67%) · top-1 = §6.2A.4.0.1.4 p0 table=-
  missing keywords: ['pcmax']
    #1 sec=6.2A.4.0.1.4 page=0 table=- score=-26.905
    #2 sec=6.2D.3.3 page=0 table=- score=-24.902
    #3 sec=6.2A.4.0.1.3 page=0 table=- score=-24.524
    #4 sec=6.2D.3_1.3 page=0 table=- score=-23.902
    #5 sec=6.2G.3.3 page=0 table=- score=-23.383

**dense** — hit@1=N hit@3=N hit@5=Y RR@10=0.20 · coverage = 3/3 (100%) · top-1 = §6.2.3.3.2 p0 table=-
    #1 sec=6.2.3.3.2 page=0 table=- score=0.310
    #2 sec=6.2A.4.0.1.4 page=0 table=- score=0.313
    #3 sec=6.2A.4.0.1.3 page=0 table=- score=0.313
    #4 sec=6.2A.4.0.1.3 page=0 table=- score=0.321
    #5 sec=6.2.4.3 page=0 table=- score=0.347

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 3/3 (100%) · top-1 = §6.2A.4.0.1.4 p0 table=-
    #1 sec=6.2A.4.0.1.4 page=0 table=- score=0.033
    #2 sec=6.2A.4.0.1.3 page=0 table=- score=0.031
    #3 sec=6.2.4.3 page=0 table=- score=0.031
    #4 sec=6.2D.4.3 page=0 table=- score=0.028
    #5 sec=6.2G.3.3 page=0 table=- score=0.028

## q28 — What is the test purpose of the absolute power tolerance test?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 0/2 (0%) · top-1 = §6.3A.4.1.1.5 p0 table=-
  missing keywords: ['set its initial output power', 'larger than 20ms']
    #1 sec=6.3A.4.1.1.5 page=0 table=- score=-13.270
    #2 sec=6.3.4.2.5 page=0 table=- score=-12.680
    #3 sec=6.3C.4.1.5 page=0 table=- score=-12.680
    #4 sec=6.3D.4.1.5 page=0 table=- score=-12.680
    #5 sec=6.3D.4.1_1.5 page=0 table=- score=-12.571

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/2 (50%) · top-1 = §6.3A.4.1.0 p0 table=-
  missing keywords: ['set its initial output power']
    #1 sec=6.3A.4.1.0 page=0 table=- score=0.334
    #2 sec=6.3.4.2.3 page=0 table=- score=0.341
    #3 sec=6.3D.4.1_1.5 page=0 table=- score=0.383
    #4 sec=6.3.4.2.5 page=0 table=- score=0.387
    #5 sec=6.3C.4.1.5 page=0 table=- score=0.389

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.4.2.5 p0 table=-
  missing keywords: ['set its initial output power', 'larger than 20ms']
    #1 sec=6.3.4.2.5 page=0 table=- score=0.032
    #2 sec=6.3A.4.1.0 page=0 table=- score=0.032
    #3 sec=6.3C.4.1.5 page=0 table=- score=0.031
    #4 sec=6.3D.4.1_1.5 page=0 table=- score=0.031
    #5 sec=6.3A.4.1.1.5 page=0 table=- score=0.031

## q29 — What does the aggregate power tolerance test verify about UE transmitter behaviour?
_expected_section = §6.3.4.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 0/3 (0%) · top-1 = §6.5.2.4.1.1 p0 table=-
  missing keywords: ['maintain its power', 'non-contiguous transmissions', '0 db commands']
    #1 sec=6.5.2.4.1.1 page=0 table=- score=-18.061
    #2 sec=6.5F.2.4.2.1 page=0 table=- score=-18.061
    #3 sec=6.5.2.4.2.1 page=0 table=- score=-18.061
    #4 sec=6.5C.2.4.1.1 page=0 table=- score=-18.061
    #5 sec=6.5C.2.4.2.1 page=0 table=- score=-18.061

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4.3 p0 table=-
    #1 sec=6.3.4.4.3 page=0 table=- score=0.278
    #2 sec=7.7A.1.4.2 page=0 table=- score=0.294
    #3 sec=6.3A.4.1.0 page=0 table=- score=0.295
    #4 sec=6.3.4.2.3 page=0 table=- score=0.306
    #5 sec=6.3G.4.3.3 page=0 table=- score=0.310

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4.3 p0 table=-
    #1 sec=6.3.4.4.3 page=0 table=- score=0.028
    #2 sec=6.5.2.4.1.1 page=0 table=- score=0.016
    #3 sec=6.5F.2.4.2.1 page=0 table=- score=0.016
    #4 sec=7.7A.1.4.2 page=0 table=- score=0.016
    #5 sec=6.3A.4.1.0 page=0 table=- score=0.016

## q30 — What is the test purpose of the relative power tolerance test, and within what transmission gap does it apply?
_expected_section = §6.3.4.3 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.12 · coverage = 0/3 (0%) · top-1 = §6.4D.4.3 p0 table=-
  missing keywords: ['target sub-frame', 'reference sub-frame', 'less than or equal']
    #1 sec=6.4D.4.3 page=0 table=- score=-25.498
    #2 sec=H.2.2 page=0 table=- score=-22.720
    #3 sec=6.5A.3.1.0 page=0 table=- score=-19.226
    #4 sec=E.3.1 page=0 table=- score=-17.970
    #5 sec=6.3.4.4.4.2 page=0 table=- score=-17.224

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 0/3 (0%) · top-1 = §6.3A.4.1.0 p0 table=-
  missing keywords: ['target sub-frame', 'reference sub-frame', 'less than or equal']
    #1 sec=6.3A.4.1.0 page=0 table=- score=0.360
    #2 sec=6.3.4.2.3 page=0 table=- score=0.364
    #3 sec=6.3A.4.3.0 page=0 table=- score=0.373
    #4 sec=7.6C.2_1.1.4.2 page=0 table=- score=0.377
    #5 sec=6.3G.4.2.3 page=0 table=- score=0.384

**hybrid** — hit@1=N hit@3=N hit@5=N RR@10=0.12 · coverage = 0/3 (0%) · top-1 = §6.3.4.2.3 p0 table=-
  missing keywords: ['target sub-frame', 'reference sub-frame', 'less than or equal']
    #1 sec=6.3.4.2.3 page=0 table=- score=0.031
    #2 sec=6.3G.4.2.5 page=0 table=- score=0.029
    #3 sec=6.3A.4.1.0 page=0 table=- score=0.028
    #4 sec=6.3D.4.2_1.5 page=0 table=- score=0.026
    #5 sec=6.3G.4.2.5 page=0 table=- score=0.026
