# Retrieval Benchmark

_scored at k=10 (hit@1/3/5, MRR@10); detail rows show top 5; backends = sparse, dense, hybrid, reranked:bge_

## Aggregate

| backend | hit@1 | hit@3 | hit@5 | MRR@10 | mean coverage |
|---|---|---|---|---|---|
| sparse | 22/30 | 29/30 | 29/30 | 0.85 | 89% |
| dense | 21/30 | 27/30 | 28/30 | 0.80 | 84% |
| hybrid | 22/30 | 29/30 | 30/30 | 0.85 | 89% |
| reranked:bge | 22/30 | 28/30 | 29/30 | 0.84 | 93% |

## By question type

| backend | type | n | hit@1 | hit@3 | hit@5 | MRR@10 | coverage |
|---|---|---|---|---|---|---|---|
| sparse | numeric | 9 | 89% | 100% | 100% | 0.94 | 100% |
| sparse | procedure | 3 | 67% | 100% | 100% | 0.83 | 72% |
| sparse | section_summary | 11 | 73% | 91% | 91% | 0.83 | 86% |
| sparse | table_lookup | 7 | 57% | 100% | 100% | 0.79 | 86% |
| dense | numeric | 9 | 56% | 89% | 89% | 0.68 | 89% |
| dense | procedure | 3 | 67% | 67% | 67% | 0.70 | 44% |
| dense | section_summary | 11 | 64% | 91% | 100% | 0.80 | 97% |
| dense | table_lookup | 7 | 100% | 100% | 100% | 1.00 | 76% |
| hybrid | numeric | 9 | 89% | 100% | 100% | 0.94 | 94% |
| hybrid | procedure | 3 | 67% | 67% | 100% | 0.75 | 61% |
| hybrid | section_summary | 11 | 64% | 100% | 100% | 0.80 | 94% |
| hybrid | table_lookup | 7 | 71% | 100% | 100% | 0.86 | 86% |
| reranked:bge | numeric | 9 | 67% | 100% | 100% | 0.81 | 94% |
| reranked:bge | procedure | 3 | 100% | 100% | 100% | 1.00 | 61% |
| reranked:bge | section_summary | 11 | 64% | 91% | 91% | 0.79 | 97% |
| reranked:bge | table_lookup | 7 | 86% | 86% | 100% | 0.89 | 100% |

## q01 — What is the maximum output power tolerance for FR1 PC3 UE?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=-12.033
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=-10.144
    #3 sec=6.2.1 page=92 table=- score=-9.732
    #4 sec=6.2.3 page=222 table=- score=-9.621
    #5 sec=6.2.1 page=95 table=- score=-9.556

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 3/3 (100%) · top-1 = §6.2.4 p273 table=-
    #1 sec=6.2.4 page=273 table=- score=0.332
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.334
    #3 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.347
    #4 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.353
    #5 sec=6.2.1 page=96 table=6.2.1.5-1 score=0.364

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.032
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.032
    #3 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.031
    #4 sec=6.2.4 page=273 table=- score=0.031
    #5 sec=6.2.1 page=96 table=6.2.1.5-1 score=0.029

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.972
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.857
    #3 sec=6.2.4 page=273 table=- score=0.819
    #4 sec=6.2.1 page=97 table=6.2.1.5-3 score=0.760
    #5 sec=6.2.3 page=222 table=6.2.3.5-0 score=0.694

## q02 — How is the test procedure defined for UE maximum output power across power classes?
_expected_section = §6.2.1 · type = procedure · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.1 p92 table=-
  missing keywords: ['pc3']
    #1 sec=6.2.1 page=92 table=- score=-15.284
    #2 sec=6.2.3 page=123 table=- score=-9.528
    #3 sec=6.3.1 page=541 table=- score=-9.517
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=-9.502
    #5 sec=6.2.2 page=98 table=- score=-9.396

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.294
    #2 sec=6.2.1 page=92 table=- score=0.314
    #3 sec=6.2.4 page=273 table=- score=0.316
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.319
    #5 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.331

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1 p92 table=-
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2.1 page=92 table=- score=0.033
    #2 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.032
    #3 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.030
    #4 sec=6.2.2 page=98 table=- score=0.029
    #5 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.029

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.966
    #2 sec=6.2.4 page=273 table=- score=0.939
    #3 sec=6.2.2 page=121 table=6.2.2.5-9 score=0.939
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.923
    #5 sec=6.2.1 page=92 table=- score=0.914

## q03 — What are the test conditions and channel bandwidth for inner / outer maximum output power?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-5
    #1 sec=6.2.2 page=99 table=6.2.2.3-5 score=-17.068
    #2 sec=6.2.1 page=94 table=6.2.1.4.1-1 score=-14.296
    #3 sec=6.3.1 page=541 table=- score=-12.264
    #4 sec=6.2.3 page=123 table=- score=-12.097
    #5 sec=6.2.3 page=135 table=6.2.3.3.8-1 score=-11.369

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1 p97 table=6.2.1.5-2
  missing keywords: ['inner', 'outer']
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.332
    #2 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=0.341
    #3 sec=6.2.4 page=273 table=- score=0.341
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.343
    #5 sec=6.2.1 page=97 table=6.2.1.5-3 score=0.345

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-5
    #1 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.031
    #2 sec=6.2.1 page=94 table=6.2.1.4.1-1 score=0.030
    #3 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.029
    #4 sec=6.3.3.2 page=546 table=6.3.3.2.4.1-1 score=0.028
    #5 sec=6.2.1 page=92 table=- score=0.028

**reranked:bge** — hit@1=N hit@3=N hit@5=Y RR@10=0.20 · coverage = 3/3 (100%) · top-1 = §6.2.2 p101 table=6.2.2.4.1-1
    #1 sec=6.2.2 page=101 table=6.2.2.4.1-1 score=0.848
    #2 sec=6.2.2 page=102 table=6.2.2.4.1-2 score=0.811
    #3 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.807
    #4 sec=6.2.2 page=104 table=6.2.2.4.1-3 score=0.790
    #5 sec=6.2.1 page=94 table=6.2.1.4.1-1 score=0.751

## q04 — Define UE output power dynamics — minimum output power requirement.
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=-22.816
    #2 sec=6.2.1 page=92 table=- score=-18.922
    #3 sec=6.3.4.1 page=567 table=- score=-14.262
    #4 sec=6.3.4.2 page=567 table=- score=-14.262
    #5 sec=6.3.4.4 page=587 table=- score=-13.331

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.252
    #2 sec=6.3.4.3 page=570 table=- score=0.351
    #3 sec=6.3.4.4 page=587 table=- score=0.356
    #4 sec=6.3.4.4 page=590 table=- score=0.363
    #5 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.376

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.033
    #2 sec=6.3.4.3 page=570 table=- score=0.031
    #3 sec=6.3.4.4 page=587 table=- score=0.031
    #4 sec=6.3.4.1 page=567 table=- score=0.031
    #5 sec=6.2.1 page=92 table=- score=0.031

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.992
    #2 sec=6.3.4.1 page=567 table=- score=0.861
    #3 sec=6.3.4.2 page=567 table=- score=0.861
    #4 sec=6.3.4.4 page=587 table=- score=0.821
    #5 sec=6.3.4.3 page=570 table=- score=0.678

## q05 — What is the transmit OFF power requirement for NR FR1 UE?
_expected_section = §6.3.2 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=-14.803
    #2 sec=6.3.3.1 page=545 table=- score=-13.521
    #3 sec=6.3.3.2 page=545 table=- score=-13.134
    #4 sec=6.3.3.6 page=557 table=- score=-13.111
    #5 sec=6.3.2 page=544 table=- score=-11.536

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 2/2 (100%) · top-1 = §6.2.3 p123 table=-
    #1 sec=6.2.3 page=123 table=- score=0.367
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.367
    #3 sec=6.3.2 page=544 table=- score=0.374
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.378
    #5 sec=6.3.4.3 page=570 table=- score=0.383

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.032
    #2 sec=6.3.3.2 page=546 table=- score=0.029
    #3 sec=6.3.3.2 page=546 table=6.3.3.2.4.1-1 score=0.027
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.027
    #5 sec=6.2.2 page=98 table=- score=0.026

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.888
    #2 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.844
    #3 sec=6.3.3.2 page=546 table=6.3.3.2.4.1-1 score=0.836
    #4 sec=6.3.3.6 page=557 table=- score=0.828
    #5 sec=6.3.3.2 page=545 table=- score=0.727

## q06 — What are the absolute and relative power tolerance requirements?
_expected_section = §6.3.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3 p576 table=-
    #1 sec=6.3.4.3 page=576 table=- score=-11.708
    #2 sec=6.3.4.3 page=570 table=- score=-11.376
    #3 sec=6.3.4.1 page=567 table=- score=-10.699
    #4 sec=6.3.4.2 page=567 table=- score=-10.699
    #5 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=-8.972

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=6.3.4.2.3-1
    #1 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=0.307
    #2 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=0.307
    #3 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.333
    #4 sec=6.3.4.1 page=567 table=- score=0.341
    #5 sec=6.3.4.2 page=567 table=- score=0.341

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=6.3.4.2.3-1
    #1 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=0.032
    #2 sec=6.3.4.1 page=567 table=- score=0.031
    #3 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=0.031
    #4 sec=6.3.4.2 page=567 table=- score=0.031
    #5 sec=6.3.4.3 page=570 table=- score=0.031

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3 p570 table=6.3.4.3.3-1
    #1 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.825
    #2 sec=6.3.4.1 page=567 table=- score=0.790
    #3 sec=6.3.4.2 page=567 table=- score=0.790
    #4 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=0.756
    #5 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=0.756

## q07 — What is the configured transmitted power for UE in NR?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.2.4 p279 table=6.2.4.5-2
    #1 sec=6.2.4 page=279 table=6.2.4.5-2 score=-13.080
    #2 sec=6.2.4 page=273 table=- score=-12.524
    #3 sec=6.2.4 page=274 table=- score=-12.465
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=-12.283
    #5 sec=6.3.1 page=541 table=6.2I.4.5-0 score=-11.728

**dense** — hit@1=N hit@3=N hit@5=Y RR@10=0.25 · coverage = 1/1 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.379
    #2 sec=6.2.3 page=123 table=- score=0.389
    #3 sec=6.3.4.3 page=570 table=- score=0.391
    #4 sec=6.2.4 page=273 table=- score=0.391
    #5 sec=6.2.3 page=123 table=- score=0.392

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/1 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.032
    #2 sec=6.2.4 page=273 table=- score=0.031
    #3 sec=6.3.4.3 page=570 table=- score=0.030
    #4 sec=6.2.4 page=274 table=- score=0.030
    #5 sec=6.2.4 page=279 table=6.2.4.5-2 score=0.030

**reranked:bge** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/1 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.960
    #2 sec=6.2.4 page=273 table=- score=0.937
    #3 sec=6.2.4 page=273 table=- score=0.844
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.815
    #5 sec=6.2.4 page=279 table=6.2.4.5-2 score=0.792

## q08 — How are additional MPR (A-MPR) requirements defined for NR FR1?
_expected_section = §6.2.3 · type = procedure · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.2.3 p123 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2.3 page=123 table=- score=-12.766
    #2 sec=6.3.3.2 page=546 table=- score=-10.336
    #3 sec=6.2.3 page=123 table=- score=-10.329
    #4 sec=6.2.4 page=274 table=- score=-10.233
    #5 sec=6.2.2 page=98 table=- score=-9.821

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.2.3 p123 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2.3 page=123 table=- score=0.361
    #2 sec=6.2.3 page=127 table=6.2.3.3.1-2 score=0.378
    #3 sec=6.2.3 page=123 table=6.2.3.3.1-1 score=0.398
    #4 sec=6.2.3 page=137 table=6.2.3.3.11-1 score=0.406
    #5 sec=6.2.3 page=129 table=- score=0.409

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.2.3 p123 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2.3 page=123 table=- score=0.033
    #2 sec=6.2.3 page=123 table=6.2.3.3.1-1 score=0.031
    #3 sec=6.2.3 page=127 table=6.2.3.3.1-2 score=0.029
    #4 sec=6.2.3 page=125 table=6.2.3.3.1-1 score=0.028
    #5 sec=6.2.3 page=140 table=- score=0.028

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.2.3 p123 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2.3 page=123 table=- score=0.931
    #2 sec=6.2.3 page=123 table=6.2.3.3.1-1 score=0.644
    #3 sec=6.2.3 page=127 table=6.2.3.3.1-2 score=0.630
    #4 sec=6.2.1 page=94 table=6.2.1.4.1-1 score=0.366
    #5 sec=6.2.3 page=148 table=- score=0.283

## q09 — What is the test purpose for the minimum output power conformance test?
_expected_section = §6.3.1 · type = section_summary · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=-16.958
    #2 sec=6.3.4.1 page=567 table=- score=-14.910
    #3 sec=6.3.4.2 page=567 table=- score=-14.910
    #4 sec=6.3.4.4 page=587 table=- score=-14.591
    #5 sec=6.3.4.3 page=570 table=- score=-14.575

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.348
    #2 sec=6.3.4.4 page=587 table=- score=0.360
    #3 sec=6.3.4.1 page=567 table=- score=0.371
    #4 sec=6.3.4.2 page=567 table=- score=0.371
    #5 sec=6.3.4.3 page=570 table=- score=0.371

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.033
    #2 sec=6.3.4.1 page=567 table=- score=0.032
    #3 sec=6.3.4.4 page=587 table=- score=0.032
    #4 sec=6.3.4.2 page=567 table=- score=0.031
    #5 sec=6.3.4.3 page=570 table=- score=0.031

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.988
    #2 sec=6.3.4.1 page=567 table=- score=0.979
    #3 sec=6.3.4.2 page=567 table=- score=0.979
    #4 sec=6.3.4.4 page=587 table=- score=0.961
    #5 sec=6.3.4.3 page=570 table=- score=0.954

## q10 — Why does excess Transmit OFF power matter for cell coverage?
_expected_section = §6.3.2 · type = section_summary · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=-24.756
    #2 sec=6.2.1 page=92 table=- score=-17.183
    #3 sec=6.3.3.1 page=545 table=- score=-10.813
    #4 sec=6.3.3.2 page=545 table=- score=-10.640
    #5 sec=6.3.3.2 page=546 table=6.3.3.2.4.1-1 score=-9.895

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.334
    #2 sec=6.3.3.1 page=545 table=- score=0.411
    #3 sec=6.3.3.2 page=545 table=- score=0.413
    #4 sec=6.3.3.3 page=550 table=6.3.3.2.5-1 score=0.422
    #5 sec=6.3.3.4 page=550 table=6.3.3.2.5-1 score=0.422

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.033
    #2 sec=6.3.3.1 page=545 table=- score=0.032
    #3 sec=6.3.3.2 page=545 table=- score=0.031
    #4 sec=6.3.2 page=544 table=- score=0.030
    #5 sec=6.3.3.1 page=545 table=- score=0.030

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.945
    #2 sec=6.3.3.2 page=545 table=- score=0.049
    #3 sec=6.3.3.1 page=545 table=- score=0.044
    #4 sec=6.3.3.5 page=557 table=- score=0.040
    #5 sec=6.3.3.6 page=557 table=- score=0.040

## q11 — What is the maximum output power for a Power Class 2 UE in NR band n78?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p97 table=6.2.1.5-2
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=-19.697
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=-17.504
    #3 sec=6.2.1 page=93 table=6.2.1.3-1 score=-16.857
    #4 sec=6.2.1 page=96 table=6.2.1.5-1 score=-16.620
    #5 sec=6.2.2 page=98 table=- score=-15.828

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p97 table=6.2.1.5-2
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.344
    #2 sec=6.2.2 page=118 table=6.2.2.5-6 score=0.374
    #3 sec=6.2.3 page=224 table=6.2.3.5-2 score=0.381
    #4 sec=6.2.2 page=110 table=6.2.2.5-1 score=0.383
    #5 sec=6.2.3 page=236 table=6.2.3.5-12 score=0.385

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p97 table=6.2.1.5-2
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.033
    #2 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.031
    #3 sec=6.2.1 page=96 table=6.2.1.5-1 score=0.029
    #4 sec=6.2.2 page=98 table=- score=0.029
    #5 sec=6.2.4 page=274 table=- score=0.028

**reranked:bge** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2.2 p121 table=6.2.2.5-9
    #1 sec=6.2.2 page=121 table=6.2.2.5-9 score=0.983
    #2 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.973
    #3 sec=6.2.3 page=127 table=6.2.3.3.1-2 score=0.966
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.962
    #5 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.940

## q12 — What is the minimum output power limit and measurement bandwidth for a 10 MHz channel in FR1?
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.1 p542 table=6.3.1.3-1
    #1 sec=6.3.1 page=542 table=6.3.1.3-1 score=-16.954
    #2 sec=6.3.1 page=543 table=6.3.1.5-1 score=-16.575
    #3 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=-15.989
    #4 sec=6.3.3.6 page=565 table=6.3.3.6.5-1 score=-15.974
    #5 sec=6.3.3.3 page=550 table=6.3.3.2.5-1 score=-15.501

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 3/3 (100%) · top-1 = §6.3.3.4 p556 table=6.3.3.4.5-1
    #1 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.370
    #2 sec=6.3.3.6 page=565 table=6.3.3.6.5-1 score=0.375
    #3 sec=6.3.1 page=543 table=6.3.1.5-1 score=0.376
    #4 sec=6.3.1 page=542 table=6.3.1.3-1 score=0.383
    #5 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=0.388

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.1 p542 table=6.3.1.3-1
    #1 sec=6.3.1 page=542 table=6.3.1.3-1 score=0.032
    #2 sec=6.3.1 page=543 table=6.3.1.5-1 score=0.032
    #3 sec=6.3.3.6 page=565 table=6.3.3.6.5-1 score=0.032
    #4 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.031
    #5 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=0.031

**reranked:bge** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 3/3 (100%) · top-1 = §6.3.3.4 p556 table=6.3.3.4.5-1
    #1 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.829
    #2 sec=6.3.3.6 page=565 table=6.3.3.6.5-1 score=0.805
    #3 sec=6.3.1 page=542 table=6.3.1.3-1 score=0.785
    #4 sec=6.3.1 page=543 table=6.3.1.5-1 score=0.781
    #5 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=0.777

## q13 — What is the absolute power tolerance for an NR UE under normal conditions?
_expected_section = §6.3.4.2 · type = numeric · difficulty = easy_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=-19.084
    #2 sec=6.3.4.2 page=567 table=- score=-19.084
    #3 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=-15.285
    #4 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=-15.285
    #5 sec=6.3.4.2 page=568 table=6.3.4.2.4.1-1 score=-12.446

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.10 · coverage = 0/2 (0%) · top-1 = §6.2.1 p97 table=6.2.1.5-2
  missing keywords: ['absolute power tolerance', '9.0']
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.332
    #2 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.354
    #3 sec=6.3.4.3 page=570 table=- score=0.355
    #4 sec=6.3.4.4 page=587 table=- score=0.357
    #5 sec=6.2.1 page=97 table=6.2.1.5-3 score=0.369

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/2 (50%) · top-1 = §6.3.4.1 p567 table=-
  missing keywords: ['9.0']
    #1 sec=6.3.4.1 page=567 table=- score=0.031
    #2 sec=6.3.4.2 page=567 table=- score=0.030
    #3 sec=6.2.3 page=123 table=- score=0.030
    #4 sec=6.2.1 page=97 table=6.2.1.5-3 score=0.029
    #5 sec=6.2.1 page=92 table=- score=0.028

**reranked:bge** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/2 (50%) · top-1 = §6.3.4.1 p567 table=-
  missing keywords: ['9.0']
    #1 sec=6.3.4.1 page=567 table=- score=0.955
    #2 sec=6.3.4.2 page=567 table=- score=0.955
    #3 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.755
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.747
    #5 sec=6.3.4.2 page=568 table=6.3.4.2.4.1-1 score=0.711

## q14 — What is the aggregate power tolerance for PUSCH transmissions with 0 dB TPC commands?
_expected_section = §6.3.4.4 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=-21.799
    #2 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=-21.433
    #3 sec=6.3.4.3 page=576 table=- score=-19.213
    #4 sec=6.3.4.4 page=590 table=- score=-16.491
    #5 sec=6.3.4.4 page=590 table=- score=-15.670

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p588 table=6.3.4.4.3-1
    #1 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=0.262
    #2 sec=6.3.4.3 page=576 table=- score=0.309
    #3 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.314
    #4 sec=6.3.4.4 page=590 table=- score=0.333
    #5 sec=6.3.4.4 page=587 table=6.3.4.3.5-7 score=0.344

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p588 table=6.3.4.4.3-1
    #1 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=0.033
    #2 sec=6.3.4.3 page=576 table=- score=0.032
    #3 sec=6.3.4.4 page=590 table=- score=0.031
    #4 sec=6.3.4.4 page=590 table=- score=0.031
    #5 sec=6.3.4.4 page=590 table=- score=0.031

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p588 table=6.3.4.4.3-1
    #1 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=0.999
    #2 sec=6.3.4.3 page=576 table=- score=0.974
    #3 sec=6.3.4.4 page=587 table=6.3.4.3.5-7 score=0.959
    #4 sec=6.3.4.4 page=590 table=- score=0.948
    #5 sec=6.3.4.3 page=586 table=6.3.4.3.5-6 score=0.930

## q15 — What is the PCMAX tolerance when the configured maximum output power is between 21 and 23 dBm?
_expected_section = §6.2.4 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p273 table=-
    #1 sec=6.2.4 page=273 table=- score=-20.162
    #2 sec=6.2.2 page=107 table=- score=-19.144
    #3 sec=6.2.4 page=278 table=6.2.4.5-1 score=-18.539
    #4 sec=6.3.1 page=541 table=6.2I.4.5-1 score=-18.351
    #5 sec=6.2.1 page=93 table=6.2.1.3-1 score=-17.945

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p276 table=6.2.4.3-2
    #1 sec=6.2.4 page=276 table=6.2.4.3-2 score=0.228
    #2 sec=6.2.4 page=273 table=- score=0.310
    #3 sec=6.2.4 page=275 table=6.2.4.3-1 score=0.336
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.336
    #5 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=0.337

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p273 table=-
    #1 sec=6.2.4 page=273 table=- score=0.033
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.031
    #3 sec=6.2.2 page=107 table=- score=0.031
    #4 sec=6.2.4 page=275 table=6.2.4.3-1 score=0.031
    #5 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.030

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p276 table=6.2.4.3-2
    #1 sec=6.2.4 page=276 table=6.2.4.3-2 score=0.973
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.972
    #3 sec=6.2.3 page=258 table=6.2.3.5-26 score=0.957
    #4 sec=6.2.3 page=251 table=6.2.3.5-21 score=0.949
    #5 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.933

## q16 — What is the allowed maximum power reduction for a power class 3 UE using DFT-s-OFDM 256 QAM modulation?
_expected_section = §6.2.2 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-2
    #1 sec=6.2.2 page=99 table=6.2.2.3-2 score=-21.952
    #2 sec=6.2.2 page=98 table=6.2.2.3-1 score=-19.439
    #3 sec=6.2.2 page=99 table=6.2.2.3-5 score=-18.738
    #4 sec=6.2.2 page=98 table=- score=-17.730
    #5 sec=6.2.2 page=98 table=- score=-17.597

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p98 table=6.2.2.3-1
    #1 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.298
    #2 sec=6.2.2 page=99 table=6.2.2.3-2 score=0.326
    #3 sec=6.2.2 page=98 table=- score=0.341
    #4 sec=6.2.3 page=151 table=- score=0.361
    #5 sec=6.2.3 page=129 table=6.2.3.3.1-2 score=0.371

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p98 table=6.2.2.3-1
    #1 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.033
    #2 sec=6.2.2 page=99 table=6.2.2.3-2 score=0.033
    #3 sec=6.2.2 page=98 table=- score=0.031
    #4 sec=6.2.3 page=147 table=6.2.3.3.26-2 score=0.029
    #5 sec=6.2.3 page=151 table=- score=0.028

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p98 table=6.2.2.3-1
    #1 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.994
    #2 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.988
    #3 sec=6.2.2 page=98 table=- score=0.978
    #4 sec=6.2.3 page=225 table=6.2.3.5-3 score=0.957
    #5 sec=6.2.2 page=101 table=6.2.2.4.1-1 score=0.907

## q17 — Which test verifies the UE's ability to set its initial output power at the start of a transmission after a gap longer than 20ms?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=-54.624
    #2 sec=6.3.4.2 page=567 table=- score=-54.624
    #3 sec=6.3.4.3 page=570 table=- score=-31.057
    #4 sec=6.3.4.4 page=587 table=- score=-22.060
    #5 sec=6.2.2 page=99 table=6.2.2.3-5 score=-21.098

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=0.325
    #2 sec=6.3.4.2 page=567 table=- score=0.325
    #3 sec=6.3.4.3 page=570 table=- score=0.341
    #4 sec=6.3.4.4 page=587 table=- score=0.351
    #5 sec=6.2.1 page=92 table=- score=0.365

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=0.033
    #2 sec=6.3.4.2 page=567 table=- score=0.032
    #3 sec=6.3.4.3 page=570 table=- score=0.032
    #4 sec=6.3.4.4 page=587 table=- score=0.031
    #5 sec=6.3.1 page=541 table=- score=0.030

**reranked:bge** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=0.992
    #2 sec=6.3.4.2 page=567 table=- score=0.992
    #3 sec=6.3.4.3 page=570 table=- score=0.936
    #4 sec=6.3.4.4 page=590 table=- score=0.918
    #5 sec=6.3.4.4 page=587 table=- score=0.901

## q18 — What is the PRACH ON power measurement period for preamble format 0?
_expected_section = §6.3.3.4 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.3.3.3 p550 table=-
    #1 sec=6.3.3.3 page=550 table=- score=-28.069
    #2 sec=6.3.3.4 page=550 table=- score=-28.069
    #3 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=-27.728
    #4 sec=6.3.3.4 page=553 table=- score=-20.617
    #5 sec=6.3.3.3 page=550 table=- score=-16.729

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.288
    #2 sec=6.3.3.3 page=550 table=- score=0.301
    #3 sec=6.3.3.4 page=550 table=- score=0.301
    #4 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.374
    #5 sec=6.3.3.4 page=551 table=- score=0.389

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.3.3.3 p550 table=-
    #1 sec=6.3.3.3 page=550 table=- score=0.033
    #2 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.032
    #3 sec=6.3.3.4 page=550 table=- score=0.032
    #4 sec=6.3.3.4 page=553 table=- score=0.031
    #5 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.031

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.971
    #2 sec=6.3.3.3 page=550 table=- score=0.834
    #3 sec=6.3.3.4 page=550 table=- score=0.834
    #4 sec=6.3.3.4 page=554 table=6.3.3.4.4.3-2 score=0.775
    #5 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.596

## q19 — Which power control commands does the SS send to drive the UE to its minimum output power during the conformance test?
_expected_section = §6.3.1 · type = procedure · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=-36.315
    #2 sec=6.3.1 page=543 table=- score=-28.448
    #3 sec=6.3.3.6 page=561 table=- score=-26.868
    #4 sec=6.3.3.2 page=547 table=- score=-26.073
    #5 sec=6.3.4.1 page=567 table=- score=-25.607

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.10 · coverage = 1/2 (50%) · top-1 = §6.3.4.4 p587 table=-
  missing keywords: ['200ms']
    #1 sec=6.3.4.4 page=587 table=- score=0.378
    #2 sec=6.3.4.3 page=576 table=- score=0.393
    #3 sec=6.3.4.3 page=576 table=- score=0.393
    #4 sec=6.3.4.4 page=590 table=- score=0.399
    #5 sec=6.3.4.1 page=567 table=- score=0.399

**hybrid** — hit@1=N hit@3=N hit@5=Y RR@10=0.25 · coverage = 2/2 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=0.033
    #2 sec=6.3.4.1 page=567 table=- score=0.031
    #3 sec=6.3.3.2 page=547 table=- score=0.031
    #4 sec=6.3.1 page=543 table=- score=0.030
    #5 sec=6.3.3.6 page=561 table=- score=0.030

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.1 p543 table=-
    #1 sec=6.3.1 page=543 table=- score=0.964
    #2 sec=6.3.4.4 page=590 table=- score=0.925
    #3 sec=6.3.4.3 page=576 table=- score=0.916
    #4 sec=6.3.4.4 page=589 table=- score=0.912
    #5 sec=6.3.4.3 page=577 table=- score=0.882

## q20 — What is P-MPR in the PCMAX equation and what value must it take during UE conducted conformance testing?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4 p275 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4 page=275 table=- score=-27.022
    #2 sec=6.3.4.4 page=587 table=- score=-10.325
    #3 sec=6.2.4 page=273 table=- score=-9.915
    #4 sec=6.3.3.6 page=558 table=- score=-8.607
    #5 sec=6.2.3 page=135 table=6.2.3.3.7-1 score=-8.134

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4 p275 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4 page=275 table=- score=0.335
    #2 sec=6.2.4 page=273 table=- score=0.368
    #3 sec=6.2.1 page=95 table=6.2.1.4.3-2 score=0.411
    #4 sec=6.2.3 page=129 table=- score=0.416
    #5 sec=6.2.3 page=123 table=- score=0.418

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4 p275 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4 page=275 table=- score=0.033
    #2 sec=6.2.4 page=273 table=- score=0.032
    #3 sec=6.3.4.4 page=587 table=- score=0.016
    #4 sec=6.2.1 page=95 table=6.2.1.4.3-2 score=0.016
    #5 sec=6.2.3 page=129 table=- score=0.016

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4 p275 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4 page=275 table=- score=0.941
    #2 sec=6.2.4 page=273 table=- score=0.829
    #3 sec=6.2.3 page=254 table=6.2.3.5-23 score=0.711
    #4 sec=6.2.3 page=244 table=6.2.3.5-18 score=0.666
    #5 sec=6.2.2 page=115 table=6.2.2.5-4 score=0.608

## q21 — In the UE Power Class table, what maximum output power and tolerance apply to band n14 for Power Class 1?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=-27.900
    #2 sec=6.2.2 page=98 table=- score=-26.354
    #3 sec=6.2.1 page=97 table=6.2.1.5-2 score=-24.737
    #4 sec=6.2.3 page=123 table=- score=-23.613
    #5 sec=6.2.1 page=96 table=6.2.1.5-1 score=-21.395

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.266
    #2 sec=6.2.2 page=118 table=6.2.2.5-6 score=0.279
    #3 sec=6.2.3 page=270 table=6.2.3.5-35 score=0.282
    #4 sec=6.2.2 page=110 table=6.2.2.5-1 score=0.287
    #5 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.288

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.033
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.031
    #3 sec=6.2.1 page=96 table=6.2.1.5-1 score=0.030
    #4 sec=6.2.2 page=98 table=- score=0.028
    #5 sec=6.2.2 page=98 table=- score=0.028

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.998
    #2 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.984
    #3 sec=6.2.4 page=273 table=- score=0.982
    #4 sec=6.2.3 page=270 table=6.2.3.5-35 score=0.973
    #5 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.972

## q22 — What is the allowed MPR for CP-OFDM 256 QAM modulation in outer RB allocations for a power class 3 UE?
_expected_section = §6.2.2 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-2
    #1 sec=6.2.2 page=99 table=6.2.2.3-2 score=-28.327
    #2 sec=6.2.2 page=99 table=6.2.2.3-5 score=-25.909
    #3 sec=6.2.2 page=98 table=6.2.2.3-1 score=-25.538
    #4 sec=6.2.3 page=139 table=6.2.3.3.15-2 score=-20.555
    #5 sec=6.2.3 page=123 table=- score=-20.488

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p98 table=6.2.2.3-1
    #1 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.289
    #2 sec=6.2.2 page=99 table=6.2.2.3-2 score=0.299
    #3 sec=6.2.3 page=151 table=- score=0.318
    #4 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.320
    #5 sec=6.2.2 page=98 table=- score=0.338

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-2
    #1 sec=6.2.2 page=99 table=6.2.2.3-2 score=0.033
    #2 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.032
    #3 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.032
    #4 sec=6.2.3 page=151 table=- score=0.031
    #5 sec=6.2.3 page=147 table=6.2.3.3.26-2 score=0.029

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-5
    #1 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.996
    #2 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.994
    #3 sec=6.2.2 page=101 table=6.2.2.4.1-1 score=0.966
    #4 sec=6.2.2 page=98 table=- score=0.959
    #5 sec=6.2.3 page=135 table=6.2.3.3.7-1 score=0.937

## q23 — What is the PRACH ON power measurement period for preamble format C2 with 15 kHz SCS?
_expected_section = §6.3.3.4 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=-33.585
    #2 sec=6.3.3.3 page=550 table=- score=-28.069
    #3 sec=6.3.3.4 page=550 table=- score=-28.069
    #4 sec=6.3.3.4 page=554 table=6.3.3.4.4.3-2 score=-23.116
    #5 sec=6.3.3.4 page=553 table=- score=-22.250

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.273
    #2 sec=6.3.3.4 page=554 table=6.3.3.4.4.3-2 score=0.339
    #3 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.350
    #4 sec=6.3.3.3 page=550 table=- score=0.378
    #5 sec=6.3.3.4 page=550 table=- score=0.378

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.033
    #2 sec=6.3.3.3 page=550 table=- score=0.032
    #3 sec=6.3.3.4 page=554 table=6.3.3.4.4.3-2 score=0.032
    #4 sec=6.3.3.4 page=550 table=- score=0.031
    #5 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.031

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.3.4 p554 table=6.3.3.4.4.3-2
    #1 sec=6.3.3.4 page=554 table=6.3.3.4.4.3-2 score=0.899
    #2 sec=6.3.3.4 page=551 table=- score=0.856
    #3 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.846
    #4 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.676
    #5 sec=6.3.3.3 page=550 table=- score=0.589

## q24 — What is the test requirement for measured UE output power at test point 2 in the configured transmitted power test?
_expected_section = §6.2.4 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=6.2I.4.5-1
    #1 sec=6.3.1 page=541 table=6.2I.4.5-1 score=-22.960
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=-19.804
    #3 sec=6.2.1 page=93 table=6.2.1.3-1 score=-15.854
    #4 sec=6.2.4 page=273 table=- score=-15.840
    #5 sec=6.3.4.2 page=569 table=6.3.4.2.5-2 score=-13.810

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.2.4 p278 table=6.2.4.5-1
    #1 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.333
    #2 sec=6.3.4.3 page=570 table=- score=0.337
    #3 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.337
    #4 sec=6.3.4.4 page=587 table=- score=0.340
    #5 sec=6.3.4.1 page=567 table=- score=0.344

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.2.4 p278 table=6.2.4.5-1
    #1 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.033
    #2 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.032
    #3 sec=6.3.4.3 page=570 table=- score=0.031
    #4 sec=6.3.4.1 page=567 table=- score=0.029
    #5 sec=6.3.4.2 page=567 table=- score=0.028

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.2.4 p278 table=6.2.4.5-1
    #1 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.977
    #2 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.963
    #3 sec=6.3.4.4 page=590 table=- score=0.948
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.939
    #5 sec=6.3.4.4 page=590 table=- score=0.895

## q25 — In the 5 MHz ramp up sub-test, what is the expected power step size when the RB allocation changes from 1 RB to 15 RBs?
_expected_section = §6.3.4.3 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3 p579 table=6.3.4.3.5-1
    #1 sec=6.3.4.3 page=579 table=6.3.4.3.5-1 score=-39.306
    #2 sec=6.3.4.3 page=585 table=6.3.4.3.5-5 score=-37.896
    #3 sec=6.3.4.3 page=581 table=6.3.4.3.5-3 score=-35.893
    #4 sec=6.3.4.3 page=580 table=6.3.4.3.5-2 score=-35.255
    #5 sec=6.3.4.3 page=586 table=6.3.4.3.5-6 score=-34.428

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

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.11 · coverage = 1/2 (50%) · top-1 = §6.3.3.1 p545 table=-
  missing keywords: ['covered by']
    #1 sec=6.3.3.1 page=545 table=- score=-31.556
    #2 sec=6.3.3.2 page=545 table=- score=-31.556
    #3 sec=6.3.3.1 page=545 table=- score=-29.081
    #4 sec=6.3.3.2 page=545 table=- score=-27.280
    #5 sec=6.3.3.3 page=550 table=- score=-24.102

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.299
    #2 sec=6.3.2 page=544 table=- score=0.347
    #3 sec=6.3.3.2 page=545 table=- score=0.375
    #4 sec=6.3.3.1 page=545 table=- score=0.393
    #5 sec=6.3.3.4 page=553 table=- score=0.406

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 2/2 (100%) · top-1 = §6.3.3.1 p545 table=-
    #1 sec=6.3.3.1 page=545 table=- score=0.031
    #2 sec=6.3.3.2 page=545 table=- score=0.031
    #3 sec=6.3.2 page=544 table=- score=0.031
    #4 sec=6.3.2 page=544 table=- score=0.030
    #5 sec=6.3.3.3 page=550 table=- score=0.030

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.759
    #2 sec=6.3.2 page=544 table=- score=0.705
    #3 sec=6.3.3.2 page=545 table=- score=0.614
    #4 sec=6.3.3.1 page=545 table=- score=0.532
    #5 sec=6.3.3.3 page=550 table=- score=0.449

## q27 — Which clauses define the MPR and A-MPR values used in the PCMAX_L formula for configured maximum output power?
_expected_section = §6.2.4 · type = section_summary · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.4 p275 table=6.2.4.3-1
  missing keywords: ['6.2.2.3', '6.2.3.3']
    #1 sec=6.2.4 page=275 table=6.2.4.3-1 score=-20.222
    #2 sec=6.2.4 page=275 table=- score=-19.123
    #3 sec=6.2.4 page=273 table=- score=-18.903
    #4 sec=6.2.3 page=123 table=- score=-15.855
    #5 sec=6.3.1 page=541 table=6.2I.4.5-1 score=-14.747

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2.3 p129 table=-
    #1 sec=6.2.3 page=129 table=- score=0.320
    #2 sec=6.2.4 page=273 table=- score=0.357
    #3 sec=6.2.3 page=222 table=- score=0.368
    #4 sec=6.2.3 page=139 table=6.2.3.3.15-2 score=0.382
    #5 sec=6.2.3 page=123 table=- score=0.386

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4 p273 table=-
  missing keywords: ['6.2.2.3']
    #1 sec=6.2.4 page=273 table=- score=0.032
    #2 sec=6.2.4 page=275 table=- score=0.031
    #3 sec=6.2.3 page=123 table=- score=0.031
    #4 sec=6.2.3 page=222 table=- score=0.031
    #5 sec=6.2.4 page=275 table=6.2.4.3-1 score=0.030

**reranked:bge** — hit@1=N hit@3=N hit@5=N RR@10=0.17 · coverage = 3/3 (100%) · top-1 = §6.2.3 p123 table=-
    #1 sec=6.2.3 page=123 table=- score=0.960
    #2 sec=6.2.3 page=140 table=- score=0.939
    #3 sec=6.2.3 page=222 table=- score=0.924
    #4 sec=6.2.3 page=139 table=6.2.3.3.15-2 score=0.902
    #5 sec=6.2.3 page=129 table=- score=0.820

## q28 — What is the test purpose of the absolute power tolerance test?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=-12.501
    #2 sec=6.3.4.2 page=567 table=- score=-12.501
    #3 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=-8.877
    #4 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=-8.877
    #5 sec=6.2.4 page=275 table=6.2.4.3-1 score=-8.303

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=0.349
    #2 sec=6.3.4.2 page=567 table=- score=0.349
    #3 sec=6.3.4.4 page=587 table=- score=0.378
    #4 sec=6.3.4.3 page=570 table=- score=0.412
    #5 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=0.418

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=0.033
    #2 sec=6.3.4.2 page=567 table=- score=0.032
    #3 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=0.031
    #4 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=0.031
    #5 sec=6.3.4.4 page=587 table=- score=0.031

**reranked:bge** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=0.993
    #2 sec=6.3.4.2 page=567 table=- score=0.993
    #3 sec=6.3.4.3 page=570 table=- score=0.499
    #4 sec=6.3.4.2 page=568 table=6.3.4.2.4.1-1 score=0.408
    #5 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=0.364

## q29 — What does the aggregate power tolerance test verify about UE transmitter behaviour?
_expected_section = §6.3.4.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=-19.355
    #2 sec=6.2.1 page=92 table=- score=-15.929
    #3 sec=6.3.4.1 page=567 table=- score=-12.783
    #4 sec=6.3.4.2 page=567 table=- score=-12.783
    #5 sec=6.3.2 page=544 table=- score=-11.082

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=0.271
    #2 sec=6.3.4.3 page=570 table=- score=0.308
    #3 sec=6.3.4.1 page=567 table=- score=0.322
    #4 sec=6.3.4.2 page=567 table=- score=0.322
    #5 sec=6.3.4.3 page=576 table=- score=0.333

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=0.033
    #2 sec=6.3.4.1 page=567 table=- score=0.032
    #3 sec=6.3.4.2 page=567 table=- score=0.031
    #4 sec=6.3.4.3 page=570 table=- score=0.031
    #5 sec=6.2.1 page=92 table=- score=0.031

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=0.991
    #2 sec=6.3.4.3 page=570 table=- score=0.884
    #3 sec=6.3.4.1 page=567 table=- score=0.874
    #4 sec=6.3.4.2 page=567 table=- score=0.874
    #5 sec=6.3.4.4 page=589 table=- score=0.713

## q30 — What is the test purpose of the relative power tolerance test, and within what transmission gap does it apply?
_expected_section = §6.3.4.3 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.3 p570 table=-
    #1 sec=6.3.4.3 page=570 table=- score=-22.924
    #2 sec=6.3.4.1 page=567 table=- score=-22.190
    #3 sec=6.3.4.2 page=567 table=- score=-22.190
    #4 sec=6.3.4.4 page=587 table=- score=-17.411
    #5 sec=6.2.1 page=92 table=- score=-17.363

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.3 p570 table=-
    #1 sec=6.3.4.3 page=570 table=- score=0.325
    #2 sec=6.3.4.1 page=567 table=- score=0.341
    #3 sec=6.3.4.2 page=567 table=- score=0.341
    #4 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.356
    #5 sec=6.3.4.4 page=587 table=- score=0.375

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.3 p570 table=-
    #1 sec=6.3.4.3 page=570 table=- score=0.033
    #2 sec=6.3.4.1 page=567 table=- score=0.032
    #3 sec=6.3.4.2 page=567 table=- score=0.032
    #4 sec=6.3.4.4 page=587 table=- score=0.031
    #5 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.029

**reranked:bge** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.3 p570 table=-
    #1 sec=6.3.4.3 page=570 table=- score=0.987
    #2 sec=6.3.4.1 page=567 table=- score=0.785
    #3 sec=6.3.4.2 page=567 table=- score=0.785
    #4 sec=6.3.4.4 page=587 table=6.3.4.3.5-7 score=0.598
    #5 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.580
