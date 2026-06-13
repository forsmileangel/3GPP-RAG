# Retrieval Benchmark

_scored at k=10 (hit@1/3/5, MRR@10); detail rows show top 5; source_format = tspec_md; backends = sparse, dense, hybrid_

## Aggregate

| backend | hit@1 | hit@3 | hit@5 | MRR@10 | mean coverage |
|---|---|---|---|---|---|
| sparse | 23/30 | 28/30 | 30/30 | 0.86 | 76% |
| dense | 22/30 | 26/30 | 28/30 | 0.81 | 79% |
| hybrid | 26/30 | 27/30 | 27/30 | 0.89 | 79% |

## By question type

| backend | type | n | hit@1 | hit@3 | hit@5 | MRR@10 | coverage |
|---|---|---|---|---|---|---|---|
| sparse | numeric | 9 | 89% | 100% | 100% | 0.94 | 80% |
| sparse | procedure | 3 | 33% | 100% | 100% | 0.67 | 61% |
| sparse | section_summary | 11 | 82% | 82% | 100% | 0.86 | 70% |
| sparse | table_lookup | 7 | 71% | 100% | 100% | 0.83 | 86% |
| dense | numeric | 9 | 67% | 67% | 78% | 0.71 | 76% |
| dense | procedure | 3 | 67% | 100% | 100% | 0.78 | 61% |
| dense | section_summary | 11 | 73% | 91% | 100% | 0.83 | 88% |
| dense | table_lookup | 7 | 86% | 100% | 100% | 0.93 | 79% |
| hybrid | numeric | 9 | 78% | 78% | 78% | 0.81 | 87% |
| hybrid | procedure | 3 | 67% | 67% | 67% | 0.71 | 61% |
| hybrid | section_summary | 11 | 91% | 100% | 100% | 0.94 | 73% |
| hybrid | table_lookup | 7 | 100% | 100% | 100% | 1.00 | 86% |

## q01 — What is the maximum output power tolerance for FR1 PC3 UE?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1.3 p0 table=-
  missing keywords: ['23', 'dbm']
    #1 sec=6.2.1.3 page=0 table=- score=-12.464
    #2 sec=6.2.1.1 page=0 table=- score=-11.688
    #3 sec=6.2.3.5 page=0 table=- score=-11.432
    #4 sec=6.2.1.5 page=0 table=- score=-11.375
    #5 sec=6.2.2.5 page=0 table=- score=-11.296

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.11 · coverage = 2/3 (67%) · top-1 = §6.2.3.5 p0 table=-
  missing keywords: ['23']
    #1 sec=6.2.3.5 page=0 table=- score=0.356
    #2 sec=6.2.2.5 page=0 table=- score=0.379
    #3 sec=6.3.4.2.3 page=0 table=- score=0.380
    #4 sec=6.2.4.3 page=0 table=- score=0.380
    #5 sec=6.3.4.4.3 page=0 table=- score=0.381

**hybrid** — hit@1=N hit@3=N hit@5=N RR@10=0.17 · coverage = 2/3 (67%) · top-1 = §6.2.3.5 p0 table=-
  missing keywords: ['23']
    #1 sec=6.2.3.5 page=0 table=- score=0.032
    #2 sec=6.2.2.5 page=0 table=- score=0.032
    #3 sec=6.3.4.2.3 page=0 table=- score=0.031
    #4 sec=6.3.4.4.3 page=0 table=- score=0.030
    #5 sec=6.2.4.3 page=0 table=- score=0.030

## q02 — How is the test procedure defined for UE maximum output power across power classes?
_expected_section = §6.2.1 · type = procedure · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1.3 p0 table=-
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2.1.3 page=0 table=- score=-17.984
    #2 sec=6.2.1.3 page=0 table=- score=-11.783
    #3 sec=6.2.1.5 page=0 table=- score=-11.565
    #4 sec=6.2.3.1 page=0 table=- score=-10.818
    #5 sec=6.2.4.5 page=0 table=6.2.4.5-1 score=-10.533

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1.3 p0 table=-
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2.1.3 page=0 table=- score=0.292
    #2 sec=6.2.2.5 page=0 table=- score=0.326
    #3 sec=6.2.4.5 page=0 table=6.2.4.5-1 score=0.329
    #4 sec=6.2.3.5 page=0 table=- score=0.334
    #5 sec=6.2.4.5 page=0 table=- score=0.335

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1.3 p0 table=-
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2.1.3 page=0 table=- score=0.033
    #2 sec=6.2.4.5 page=0 table=6.2.4.5-1 score=0.031
    #3 sec=6.2.1.3 page=0 table=- score=0.030
    #4 sec=6.2.1.5 page=0 table=- score=0.030
    #5 sec=6.2.4.5 page=0 table=- score=0.030

## q03 — What are the test conditions and channel bandwidth for inner / outer maximum output power?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 3/3 (100%) · top-1 = §6.2.2.4.1 p0 table=6.2.2.4.1-2c
    #1 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-2c score=-15.071
    #2 sec=6.2.2.3 page=0 table=- score=-14.607
    #3 sec=6.2.1.4.1 page=0 table=6.2.1.4.1-1 score=-13.977
    #4 sec=6.2.2.3 page=0 table=- score=-13.807
    #5 sec=6.2.2.3 page=0 table=- score=-12.301

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1.4.1 p0 table=6.2.1.4.1-1
    #1 sec=6.2.1.4.1 page=0 table=6.2.1.4.1-1 score=0.312
    #2 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-3 score=0.315
    #3 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-2c score=0.319
    #4 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-1 score=0.328
    #5 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-2a score=0.331

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1.4.1 p0 table=6.2.1.4.1-1
    #1 sec=6.2.1.4.1 page=0 table=6.2.1.4.1-1 score=0.032
    #2 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-2c score=0.032
    #3 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-3 score=0.031
    #4 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-2 score=0.029
    #5 sec=6.3.1.4.1 page=0 table=6.3.1.4.1-1 score=0.029

## q04 — Define UE output power dynamics — minimum output power requirement.
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1.3 p0 table=-
    #1 sec=6.3.1.3 page=0 table=- score=-18.854
    #2 sec=6.3.4.2.3 page=0 table=- score=-17.442
    #3 sec=6.3.4.4.3 page=0 table=- score=-16.904
    #4 sec=6.2.1.3 page=0 table=- score=-16.693
    #5 sec=6.3.1.1 page=0 table=- score=-16.496

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1.3 p0 table=-
    #1 sec=6.3.1.3 page=0 table=- score=0.235
    #2 sec=6.3.1.1 page=0 table=- score=0.309
    #3 sec=6.2.1.1 page=0 table=- score=0.339
    #4 sec=6.3.4.4.3 page=0 table=- score=0.345
    #5 sec=6.3.4.2.3 page=0 table=- score=0.347

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1.3 p0 table=-
    #1 sec=6.3.1.3 page=0 table=- score=0.033
    #2 sec=6.3.1.1 page=0 table=- score=0.032
    #3 sec=6.3.4.2.3 page=0 table=- score=0.032
    #4 sec=6.3.4.4.3 page=0 table=- score=0.031
    #5 sec=6.2.1.3 page=0 table=- score=0.030

## q05 — What is the transmit OFF power requirement for NR FR1 UE?
_expected_section = §6.3.2 · type = numeric · difficulty = easy_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.3.2.3 p0 table=-
    #1 sec=6.3.3.2.3 page=0 table=- score=-18.946
    #2 sec=6.3.2.3 page=0 table=- score=-15.304
    #3 sec=6.3.2.2 page=0 table=- score=-15.020
    #4 sec=6.3.2.1 page=0 table=- score=-14.640
    #5 sec=6.3.2.5 page=0 table=- score=-14.199

**dense** — hit@1=N hit@3=N hit@5=Y RR@10=0.25 · coverage = 0/2 (0%) · top-1 = §6.2.1.5 p0 table=6.2.1.5-2a
  missing keywords: ['transmit off', 'off power']
    #1 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.359
    #2 sec=6.2.1.3 page=0 table=6.2.1.3-1 score=0.371
    #3 sec=6.2.1.5 page=0 table=6.2.1.5-1 score=0.388
    #4 sec=6.3.2.2 page=0 table=- score=0.389
    #5 sec=6.2.1.5 page=0 table=6.2.1.5-2 score=0.391

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2.2 p0 table=-
    #1 sec=6.3.2.2 page=0 table=- score=0.031
    #2 sec=6.3.2.3 page=0 table=- score=0.031
    #3 sec=6.3.2.1 page=0 table=- score=0.030
    #4 sec=6.3.3.2.3 page=0 table=- score=0.029
    #5 sec=6.2.1.3 page=0 table=- score=0.028

## q06 — What are the absolute and relative power tolerance requirements?
_expected_section = §6.3.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3.5 p0 table=-
    #1 sec=6.3.4.3.5 page=0 table=- score=-15.379
    #2 sec=6.3.4.3.3 page=0 table=- score=-13.943
    #3 sec=6.3.4.3.5 page=0 table=- score=-13.571
    #4 sec=6.3.4.3.5 page=0 table=- score=-13.233
    #5 sec=6.3.4.2.5 page=0 table=- score=-11.781

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.2.3 p0 table=-
    #1 sec=6.3.4.2.3 page=0 table=- score=0.282
    #2 sec=6.3.4.4.3 page=0 table=- score=0.337
    #3 sec=6.3.4.3.3 page=0 table=- score=0.342
    #4 sec=6.3.4.1 page=0 table=- score=0.346
    #5 sec=6.3.4.2.5 page=0 table=- score=0.347

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3.3 p0 table=-
    #1 sec=6.3.4.3.3 page=0 table=- score=0.032
    #2 sec=6.3.4.2.3 page=0 table=- score=0.032
    #3 sec=6.3.4.3.5 page=0 table=- score=0.031
    #4 sec=6.3.4.2.5 page=0 table=- score=0.031
    #5 sec=6.3.4.3.5 page=0 table=- score=0.029

## q07 — What is the configured transmitted power for UE in NR?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.2.4.5 p0 table=-
    #1 sec=6.2.4.5 page=0 table=- score=-14.693
    #2 sec=6.2.1.3 page=0 table=- score=-14.599
    #3 sec=6.2.4.3 page=0 table=- score=-13.321
    #4 sec=6.2.1.3 page=0 table=- score=-10.132
    #5 sec=6.2.4.3 page=0 table=- score=-9.355

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 1/1 (100%) · top-1 = §6.2.1.3 p0 table=-
    #1 sec=6.2.1.3 page=0 table=- score=0.359
    #2 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.375
    #3 sec=6.2.4.5 page=0 table=- score=0.395
    #4 sec=6.2.4.3 page=0 table=- score=0.402
    #5 sec=6.2.1.5 page=0 table=6.2.1.5-2 score=0.405

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.2.4.5 p0 table=-
    #1 sec=6.2.4.5 page=0 table=- score=0.032
    #2 sec=6.2.1.3 page=0 table=- score=0.032
    #3 sec=6.2.4.3 page=0 table=- score=0.031
    #4 sec=6.2.4.3 page=0 table=- score=0.028
    #5 sec=6.2.4.3 page=0 table=- score=0.028

## q08 — How are additional MPR (A-MPR) requirements defined for NR FR1?
_expected_section = §6.2.3 · type = procedure · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/2 (50%) · top-1 = §6.2.4.3 p0 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2.4.3 page=0 table=- score=-14.477
    #2 sec=6.2.3.1 page=0 table=- score=-14.033
    #3 sec=6.2.3 page=0 table=- score=-11.054
    #4 sec=6.2.3.3.1 page=0 table=- score=-11.014
    #5 sec=6.2.3.2 page=0 table=- score=-10.767

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.2.3.1 p0 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2.3.1 page=0 table=- score=0.355
    #2 sec=6.2.3.3.1 page=0 table=- score=0.377
    #3 sec=6.2.3.3.2 page=0 table=- score=0.406
    #4 sec=6.2.3.3.1 page=0 table=- score=0.409
    #5 sec=6.2.3.4.1 page=0 table=6.2.3.4.1-8 score=0.414

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.2.3.1 p0 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2.3.1 page=0 table=- score=0.033
    #2 sec=6.2.3.3.1 page=0 table=- score=0.032
    #3 sec=6.2.4.3 page=0 table=- score=0.016
    #4 sec=6.2.3 page=0 table=- score=0.016
    #5 sec=6.2.3.3.2 page=0 table=- score=0.016

## q09 — What is the test purpose for the minimum output power conformance test?
_expected_section = §6.3.1 · type = section_summary · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.1.3 p0 table=-
  missing keywords: ['test purpose']
    #1 sec=6.3.1.3 page=0 table=- score=-11.300
    #2 sec=6.3.1.5 page=0 table=- score=-10.785
    #3 sec=6.3.1.3 page=0 table=6.3.1.3-1 score=-9.984
    #4 sec=6.3.4.2.3 page=0 table=- score=-9.832
    #5 sec=6.3.4.4.3 page=0 table=- score=-9.464

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.1.1 p0 table=-
  missing keywords: ['test purpose']
    #1 sec=6.3.1.1 page=0 table=- score=0.347
    #2 sec=6.3.1.5 page=0 table=- score=0.396
    #3 sec=6.3.4.4.3 page=0 table=- score=0.422
    #4 sec=6.3.1.3 page=0 table=- score=0.423
    #5 sec=6.2.1.1 page=0 table=- score=0.424

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.1.5 p0 table=-
  missing keywords: ['test purpose']
    #1 sec=6.3.1.5 page=0 table=- score=0.032
    #2 sec=6.3.1.3 page=0 table=- score=0.032
    #3 sec=6.3.1.1 page=0 table=- score=0.032
    #4 sec=6.3.4.4.3 page=0 table=- score=0.031
    #5 sec=6.3.4.3.3 page=0 table=- score=0.030

## q10 — Why does excess Transmit OFF power matter for cell coverage?
_expected_section = §6.3.2 · type = section_summary · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.2.1 p0 table=-
    #1 sec=6.3.2.1 page=0 table=- score=-31.308
    #2 sec=6.2.1.1 page=0 table=- score=-24.436
    #3 sec=6.3.2.3 page=0 table=- score=-12.207
    #4 sec=6.3.3.2.1 page=0 table=- score=-12.147
    #5 sec=6.3.2.5 page=0 table=- score=-11.939

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.2.1 p0 table=-
    #1 sec=6.3.2.1 page=0 table=- score=0.261
    #2 sec=6.3.3.2.1 page=0 table=- score=0.388
    #3 sec=6.3.2.3 page=0 table=- score=0.389
    #4 sec=6.3.3.4.1 page=0 table=- score=0.421
    #5 sec=6.3.2.5 page=0 table=- score=0.422

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.2.1 p0 table=-
    #1 sec=6.3.2.1 page=0 table=- score=0.033
    #2 sec=6.3.3.2.1 page=0 table=- score=0.032
    #3 sec=6.3.2.3 page=0 table=- score=0.032
    #4 sec=6.2.1.1 page=0 table=- score=0.031
    #5 sec=6.3.2.5 page=0 table=- score=0.031

## q11 — What is the maximum output power for a Power Class 2 UE in NR band n78?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1.5 p0 table=6.2.1.5-2
    #1 sec=6.2.1.5 page=0 table=6.2.1.5-2 score=-19.039
    #2 sec=6.2.2.5 page=0 table=- score=-18.763
    #3 sec=6.2.1.3 page=0 table=6.2.1.3-1 score=-17.394
    #4 sec=6.2.1.5 page=0 table=- score=-17.389
    #5 sec=6.2.1.5 page=0 table=6.2.1.5-1 score=-16.805

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1.5 p0 table=6.2.1.5-2a
    #1 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.364
    #2 sec=6.2.3.5 page=0 table=- score=0.372
    #3 sec=6.2.1.3 page=0 table=- score=0.373
    #4 sec=6.2.3.5 page=0 table=- score=0.380
    #5 sec=6.2.1.3 page=0 table=6.2.1.3-1 score=0.385

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1.5 p0 table=6.2.1.5-2
    #1 sec=6.2.1.5 page=0 table=6.2.1.5-2 score=0.032
    #2 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.031
    #3 sec=6.2.1.3 page=0 table=6.2.1.3-1 score=0.031
    #4 sec=6.2.1.3 page=0 table=- score=0.031
    #5 sec=6.2.2.5 page=0 table=- score=0.030

## q12 — What is the minimum output power limit and measurement bandwidth for a 10 MHz channel in FR1?
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.1.3 p0 table=6.3.1.3-1
    #1 sec=6.3.1.3 page=0 table=6.3.1.3-1 score=-20.145
    #2 sec=6.3.3.2.5 page=0 table=6.3.3.2.5-1 score=-18.976
    #3 sec=6.3.3.6.5 page=0 table=6.3.3.6.5-1 score=-17.661
    #4 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=-17.577
    #5 sec=6.3.1.5 page=0 table=6.3.1.5-1 score=-17.314

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.1.3 p0 table=6.3.1.3-1
    #1 sec=6.3.1.3 page=0 table=6.3.1.3-1 score=0.330
    #2 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=0.333
    #3 sec=6.3.3.2.5 page=0 table=6.3.3.2.5-1 score=0.341
    #4 sec=6.3.4.2.5 page=0 table=6.3.4.2.5-1 score=0.358
    #5 sec=6.3.4.2.5 page=0 table=6.3.4.2.5-2 score=0.370

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.1.3 p0 table=6.3.1.3-1
    #1 sec=6.3.1.3 page=0 table=6.3.1.3-1 score=0.033
    #2 sec=6.3.3.2.5 page=0 table=6.3.3.2.5-1 score=0.032
    #3 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=0.032
    #4 sec=6.3.3.6.5 page=0 table=6.3.3.6.5-1 score=0.031
    #5 sec=6.3.4.2.5 page=0 table=6.3.4.2.5-1 score=0.031

## q13 — What is the absolute power tolerance for an NR UE under normal conditions?
_expected_section = §6.3.4.2 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.4.2.4.1 p0 table=6.3.4.2.4.1-1
  missing keywords: ['9.0']
    #1 sec=6.3.4.2.4.1 page=0 table=6.3.4.2.4.1-1 score=-16.073
    #2 sec=6.3.4.1 page=0 table=- score=-14.988
    #3 sec=6.3.4.2.3 page=0 table=- score=-11.553
    #4 sec=6.3.4.2.5 page=0 table=- score=-11.481
    #5 sec=6.3.4.4.4.1 page=0 table=6.3.4.4.4.1-2 score=-10.967

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.4.2.3 p0 table=-
  missing keywords: ['9.0']
    #1 sec=6.3.4.2.3 page=0 table=- score=0.352
    #2 sec=6.2.1.5 page=0 table=- score=0.355
    #3 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.375
    #4 sec=6.2.1.3 page=0 table=- score=0.376
    #5 sec=6.2.4.5 page=0 table=- score=0.380

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.4.2.3 p0 table=-
  missing keywords: ['9.0']
    #1 sec=6.3.4.2.3 page=0 table=- score=0.032
    #2 sec=6.2.1.5 page=0 table=- score=0.030
    #3 sec=6.2.4.5 page=0 table=- score=0.029
    #4 sec=6.2.3.1 page=0 table=- score=0.028
    #5 sec=6.3.4.3.5 page=0 table=- score=0.028

## q14 — What is the aggregate power tolerance for PUSCH transmissions with 0 dB TPC commands?
_expected_section = §6.3.4.4 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4.3 p0 table=-
    #1 sec=6.3.4.4.3 page=0 table=- score=-23.258
    #2 sec=6.3.4.4.3 page=0 table=6.3.4.4.3-1 score=-22.416
    #3 sec=6.3.4.4.4.2 page=0 table=- score=-20.170
    #4 sec=6.3.4.4.4.2 page=0 table=- score=-18.362
    #5 sec=6.3.4.3.4.2 page=0 table=- score=-18.032

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4.3 p0 table=6.3.4.4.3-1
    #1 sec=6.3.4.4.3 page=0 table=6.3.4.4.3-1 score=0.246
    #2 sec=6.3.4.3.3 page=0 table=6.3.4.3.3-1 score=0.349
    #3 sec=6.3.4.4.4.2 page=0 table=- score=0.367
    #4 sec=6.3.4.4.4.2 page=0 table=- score=0.367
    #5 sec=6.3.4.4.5 page=0 table=6.3.4.4.5-1 score=0.368

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4.3 p0 table=6.3.4.4.3-1
    #1 sec=6.3.4.4.3 page=0 table=6.3.4.4.3-1 score=0.033
    #2 sec=6.3.4.4.4.2 page=0 table=- score=0.032
    #3 sec=6.3.4.4.4.2 page=0 table=- score=0.031
    #4 sec=6.3.4.4.3 page=0 table=- score=0.031
    #5 sec=6.3.4.4.5 page=0 table=6.3.4.4.5-1 score=0.030

## q15 — What is the PCMAX tolerance when the configured maximum output power is between 21 and 23 dBm?
_expected_section = §6.2.4 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4.3 p0 table=-
  missing keywords: ['2.0']
    #1 sec=6.2.4.3 page=0 table=- score=-20.573
    #2 sec=6.2.4.5 page=0 table=- score=-17.129
    #3 sec=6.2.4.3 page=0 table=- score=-16.951
    #4 sec=6.2.4.3 page=0 table=- score=-15.612
    #5 sec=6.2.1.3 page=0 table=- score=-15.093

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 2/3 (67%) · top-1 = §6.2.2.5 p0 table=6.2.2.5-1a
  missing keywords: ['pcmax']
    #1 sec=6.2.2.5 page=0 table=6.2.2.5-1a score=0.327
    #2 sec=6.2.2.5 page=0 table=6.2.2.5-8 score=0.327
    #3 sec=6.2.2.5 page=0 table=6.2.2.5-2 score=0.327
    #4 sec=6.2.2.5 page=0 table=- score=0.327
    #5 sec=6.2.3.5 page=0 table=6.2.3.5-27b score=0.328

**hybrid** — hit@1=N hit@3=N hit@5=N RR@10=0.17 · coverage = 2/3 (67%) · top-1 = §6.2.2.5 p0 table=6.2.2.5-8
  missing keywords: ['pcmax']
    #1 sec=6.2.2.5 page=0 table=6.2.2.5-8 score=0.030
    #2 sec=6.2.2.5 page=0 table=- score=0.030
    #3 sec=6.2.2.5 page=0 table=6.2.2.5-7b score=0.029
    #4 sec=6.2.3.5 page=0 table=6.2.3.5-29 score=0.028
    #5 sec=6.2.2.5 page=0 table=- score=0.028

## q16 — What is the allowed maximum power reduction for a power class 3 UE using DFT-s-OFDM 256 QAM modulation?
_expected_section = §6.2.2 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.2.3 p0 table=-
  missing keywords: ['4.5']
    #1 sec=6.2.2.3 page=0 table=- score=-22.357
    #2 sec=6.2.3.5 page=0 table=- score=-18.059
    #3 sec=6.2.3.1 page=0 table=- score=-16.779
    #4 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-2 score=-16.028
    #5 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-1 score=-15.894

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2.3 p0 table=-
    #1 sec=6.2.2.3 page=0 table=- score=0.339
    #2 sec=6.2.3.3.20 page=0 table=6.2.3.3.21-2 score=0.370
    #3 sec=6.2.3.3.1 page=0 table=6.2.3.3.1-2 score=0.371
    #4 sec=6.2.3.3.23 page=0 table=6.2.3.3.23-2 score=0.376
    #5 sec=6.2.3.3.22 page=0 table=6.2.3.3.22-2 score=0.379

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2.3 p0 table=-
    #1 sec=6.2.2.3 page=0 table=- score=0.033
    #2 sec=6.2.3.3.20 page=0 table=6.2.3.3.21-2 score=0.029
    #3 sec=6.2.2.3 page=0 table=6.2.2.3-1 score=0.029
    #4 sec=6.2.3.3.23 page=0 table=6.2.3.3.23-2 score=0.029
    #5 sec=6.2.3.3.1 page=0 table=6.2.3.3.1-2 score=0.028

## q17 — Which test verifies the UE's ability to set its initial output power at the start of a transmission after a gap longer than 20ms?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.2.1 p0 table=-
    #1 sec=6.3.4.2.1 page=0 table=- score=-60.350
    #2 sec=6.3.4.2.3 page=0 table=- score=-50.446
    #3 sec=6.3.4.3.1 page=0 table=- score=-44.531
    #4 sec=6.2.2.3 page=0 table=- score=-27.934
    #5 sec=6.3.4.2.4.2 page=0 table=- score=-22.304

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.2.1 p0 table=-
    #1 sec=6.3.4.2.1 page=0 table=- score=0.207
    #2 sec=6.3.4.3.1 page=0 table=- score=0.293
    #3 sec=6.3.4.4.1 page=0 table=- score=0.333
    #4 sec=6.3.4.2.3 page=0 table=- score=0.338
    #5 sec=6.3.1.1 page=0 table=- score=0.347

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.2.1 p0 table=-
    #1 sec=6.3.4.2.1 page=0 table=- score=0.033
    #2 sec=6.3.4.3.1 page=0 table=- score=0.032
    #3 sec=6.3.4.2.3 page=0 table=- score=0.032
    #4 sec=6.3.4.4.1 page=0 table=- score=0.031
    #5 sec=6.3.4.2.4.2 page=0 table=- score=0.030

## q18 — What is the PRACH ON power measurement period for preamble format 0?
_expected_section = §6.3.3.4 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4.3 p0 table=-
    #1 sec=6.3.3.4.3 page=0 table=- score=-30.986
    #2 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=-26.378
    #3 sec=6.3.3.4.4.2 page=0 table=- score=-23.323
    #4 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=-18.892
    #5 sec=6.3.3.4.3 page=0 table=- score=-16.894

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4.3 p0 table=6.3.3.4.3-1
    #1 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.280
    #2 sec=6.3.3.4.3 page=0 table=- score=0.310
    #3 sec=6.3.3.4.4.2 page=0 table=- score=0.390
    #4 sec=6.3.3.4.3 page=0 table=- score=0.395
    #5 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=0.418

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4.3 p0 table=-
    #1 sec=6.3.3.4.3 page=0 table=- score=0.033
    #2 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.033
    #3 sec=6.3.3.4.4.2 page=0 table=- score=0.032
    #4 sec=6.3.3.4.3 page=0 table=- score=0.031
    #5 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=0.031

## q19 — Which power control commands does the SS send to drive the UE to its minimum output power during the conformance test?
_expected_section = §6.3.1 · type = procedure · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.4.3 p0 table=-
    #1 sec=6.3.4.4.3 page=0 table=- score=-32.895
    #2 sec=6.3.1.4.2 page=0 table=- score=-31.925
    #3 sec=6.3.3.2.4.2 page=0 table=- score=-28.910
    #4 sec=6.3.3.6.4.2 page=0 table=- score=-28.888
    #5 sec=6.3.4.4.1 page=0 table=- score=-27.747

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 2/2 (100%) · top-1 = §6.3.4.3.4.2 p0 table=-
    #1 sec=6.3.4.3.4.2 page=0 table=- score=0.404
    #2 sec=6.3.3.6.4.2 page=0 table=- score=0.413
    #3 sec=6.3.1.1 page=0 table=- score=0.417
    #4 sec=6.3.4.3.4.2 page=0 table=- score=0.427
    #5 sec=6.3.4.4.4.2 page=0 table=- score=0.429

**hybrid** — hit@1=N hit@3=N hit@5=N RR@10=0.14 · coverage = 2/2 (100%) · top-1 = §6.3.3.6.4.2 p0 table=-
    #1 sec=6.3.3.6.4.2 page=0 table=- score=0.032
    #2 sec=6.3.4.4.3 page=0 table=- score=0.031
    #3 sec=6.3.4.3.4.2 page=0 table=- score=0.031
    #4 sec=6.3.3.2.4.2 page=0 table=- score=0.031
    #5 sec=6.3.4.3.4.2 page=0 table=- score=0.031

## q20 — What is P-MPR in the PCMAX equation and what value must it take during UE conducted conformance testing?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4.3 p0 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4.3 page=0 table=- score=-36.800
    #2 sec=6.2.4.3 page=0 table=- score=-17.704
    #3 sec=6.2.3.3.7 page=0 table=- score=-10.141
    #4 sec=6.2.4.3 page=0 table=- score=-9.109
    #5 sec=6.3.3.2.4.2 page=0 table=- score=-8.265

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4.3 p0 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4.3 page=0 table=- score=0.356
    #2 sec=6.2.4.3 page=0 table=- score=0.397
    #3 sec=6.2.4.1 page=0 table=- score=0.405
    #4 sec=6.2.3.4.3.4 page=0 table=- score=0.410
    #5 sec=6.2.3.3.2 page=0 table=- score=0.413

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4.3 p0 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4.3 page=0 table=- score=0.033
    #2 sec=6.2.4.3 page=0 table=- score=0.033
    #3 sec=6.2.4.3 page=0 table=- score=0.031
    #4 sec=6.2.3.3.7 page=0 table=- score=0.016
    #5 sec=6.2.4.1 page=0 table=- score=0.016

## q21 — In the UE Power Class table, what maximum output power and tolerance apply to band n14 for Power Class 1?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2.3.5 p0 table=-
    #1 sec=6.2.3.5 page=0 table=- score=-27.052
    #2 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=-25.983
    #3 sec=6.2.2.5 page=0 table=- score=-24.550
    #4 sec=6.2.1.3 page=0 table=- score=-23.333
    #5 sec=6.2.2.5 page=0 table=- score=-22.867

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1.5 p0 table=6.2.1.5-2a
    #1 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.262
    #2 sec=6.2.2.5 page=0 table=- score=0.288
    #3 sec=6.2.2.5 page=0 table=- score=0.293
    #4 sec=6.2.1.3 page=0 table=6.2.1.3-1 score=0.301
    #5 sec=6.2.3.5 page=0 table=- score=0.322

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1.5 p0 table=6.2.1.5-2a
    #1 sec=6.2.1.5 page=0 table=6.2.1.5-2a score=0.033
    #2 sec=6.2.2.5 page=0 table=- score=0.032
    #3 sec=6.2.2.5 page=0 table=- score=0.032
    #4 sec=6.2.1.3 page=0 table=6.2.1.3-1 score=0.030
    #5 sec=6.2.1.5 page=0 table=- score=0.030

## q22 — What is the allowed MPR for CP-OFDM 256 QAM modulation in outer RB allocations for a power class 3 UE?
_expected_section = §6.2.2 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2.3 p0 table=6.2.2.3-2
    #1 sec=6.2.2.3 page=0 table=6.2.2.3-2 score=-24.599
    #2 sec=6.2.2.3 page=0 table=6.2.2.3-5 score=-24.522
    #3 sec=6.2.2.3 page=0 table=6.2.2.3-1 score=-24.420
    #4 sec=6.2.2.3 page=0 table=6.2.2.3-4b score=-22.895
    #5 sec=6.2.2.4.1 page=0 table=6.2.2.4.1-2c score=-19.972

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2.3 p0 table=6.2.2.3-1
    #1 sec=6.2.2.3 page=0 table=6.2.2.3-1 score=0.313
    #2 sec=6.2.2.3 page=0 table=6.2.2.3-2 score=0.324
    #3 sec=6.2.2.3 page=0 table=6.2.2.3-4b score=0.328
    #4 sec=6.2.2.3 page=0 table=6.2.2.3-5 score=0.335
    #5 sec=6.2.2.3 page=0 table=- score=0.343

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2.3 p0 table=6.2.2.3-2
    #1 sec=6.2.2.3 page=0 table=6.2.2.3-2 score=0.033
    #2 sec=6.2.2.3 page=0 table=6.2.2.3-1 score=0.032
    #3 sec=6.2.2.3 page=0 table=6.2.2.3-5 score=0.032
    #4 sec=6.2.2.3 page=0 table=6.2.2.3-4b score=0.031
    #5 sec=6.2.3.3.1 page=0 table=- score=0.029

## q23 — What is the PRACH ON power measurement period for preamble format C2 with 15 kHz SCS?
_expected_section = §6.3.3.4 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4.3 p0 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=-31.616
    #2 sec=6.3.3.4.3 page=0 table=- score=-30.879
    #3 sec=6.3.3.4.4.2 page=0 table=- score=-23.323
    #4 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=-21.635
    #5 sec=6.3.3.4.4.3 page=0 table=6.3.3.4.4.3-2 score=-20.681

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4.3 p0 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.260
    #2 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=0.356
    #3 sec=6.3.3.4.3 page=0 table=- score=0.381
    #4 sec=6.3.3.4.4.2 page=0 table=- score=0.395
    #5 sec=6.3.3.4.4.3 page=0 table=6.3.3.4.4.3-2 score=0.396

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4.3 p0 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4.3 page=0 table=6.3.3.4.3-1 score=0.033
    #2 sec=6.3.3.4.3 page=0 table=- score=0.032
    #3 sec=6.3.3.4.5 page=0 table=6.3.3.4.5-1 score=0.032
    #4 sec=6.3.3.4.4.2 page=0 table=- score=0.031
    #5 sec=6.3.3.4.4.3 page=0 table=6.3.3.4.4.3-2 score=0.031

## q24 — What is the test requirement for measured UE output power at test point 2 in the configured transmitted power test?
_expected_section = §6.2.4 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.2.4.5 p0 table=-
    #1 sec=6.2.4.5 page=0 table=- score=-25.835
    #2 sec=6.2.1.3 page=0 table=- score=-20.769
    #3 sec=6.2.4.5 page=0 table=6.2.4.5-1 score=-19.952
    #4 sec=6.2.4.1 page=0 table=- score=-18.043
    #5 sec=6.2.1.3 page=0 table=- score=-16.100

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.1.1 p0 table=-
    #1 sec=6.3.1.1 page=0 table=- score=0.331
    #2 sec=6.2.4.5 page=0 table=- score=0.338
    #3 sec=6.2.4.1 page=0 table=- score=0.340
    #4 sec=6.3.4.2.1 page=0 table=- score=0.345
    #5 sec=6.2.4.5 page=0 table=6.2.4.5-1 score=0.346

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.2.4.5 p0 table=-
    #1 sec=6.2.4.5 page=0 table=- score=0.033
    #2 sec=6.2.4.1 page=0 table=- score=0.031
    #3 sec=6.2.4.5 page=0 table=6.2.4.5-1 score=0.031
    #4 sec=6.2.1.3 page=0 table=- score=0.029
    #5 sec=6.3.4.2.1 page=0 table=- score=0.029

## q25 — In the 5 MHz ramp up sub-test, what is the expected power step size when the RB allocation changes from 1 RB to 15 RBs?
_expected_section = §6.3.4.3 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3.5 p0 table=-
    #1 sec=6.3.4.3.5 page=0 table=- score=-32.764
    #2 sec=6.3.4.3.5 page=0 table=6.3.4.3.5-1 score=-26.979
    #3 sec=6.3.4.3.5 page=0 table=6.3.4.3.5-5 score=-26.021
    #4 sec=6.3.4.3.5 page=0 table=6.3.4.3.5-3 score=-25.251
    #5 sec=6.3.4.3.5 page=0 table=6.3.4.3.5-2 score=-23.676

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.4.3.5 p0 table=6.3.4.3.5-3
  missing keywords: ['ramp up']
    #1 sec=6.3.4.3.5 page=0 table=6.3.4.3.5-3 score=0.358
    #2 sec=6.3.4.3.5 page=0 table=6.3.4.3.5-2 score=0.359
    #3 sec=6.3.4.3.5 page=0 table=6.3.4.3.5-5 score=0.360
    #4 sec=6.3.4.3.5 page=0 table=6.3.4.3.5-1 score=0.361
    #5 sec=6.3.4.3.5 page=0 table=6.3.4.3.5-4 score=0.364

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3.5 p0 table=6.3.4.3.5-3
    #1 sec=6.3.4.3.5 page=0 table=6.3.4.3.5-3 score=0.032
    #2 sec=6.3.4.3.5 page=0 table=6.3.4.3.5-1 score=0.032
    #3 sec=6.3.4.3.5 page=0 table=6.3.4.3.5-5 score=0.032
    #4 sec=6.3.4.3.5 page=0 table=6.3.4.3.5-2 score=0.032
    #5 sec=6.3.4.3.5 page=0 table=- score=0.031

## q26 — Where is the Transmit OFF power requirement actually tested, given that clause 6.3.2 defines no standalone test procedure?
_expected_section = §6.3.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=Y RR@10=0.20 · coverage = 0/2 (0%) · top-1 = §6.3.3.2.1 p0 table=-
  missing keywords: ['covered by', 'transmit on/off time mask']
    #1 sec=6.3.3.2.1 page=0 table=- score=-34.457
    #2 sec=6.3.3.1 page=0 table=- score=-32.253
    #3 sec=6.3.3.4.1 page=0 table=- score=-24.934
    #4 sec=6.3.3.6.1 page=0 table=- score=-24.934
    #5 sec=6.3.2.3 page=0 table=- score=-23.722

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2.5 p0 table=-
    #1 sec=6.3.2.5 page=0 table=- score=0.325
    #2 sec=6.3.2.4 page=0 table=- score=0.360
    #3 sec=6.3.2.3 page=0 table=- score=0.382
    #4 sec=6.3.2.2 page=0 table=- score=0.384
    #5 sec=6.3.3.2.5 page=0 table=- score=0.406

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.2.5 p0 table=-
  missing keywords: ['covered by', 'transmit on/off time mask']
    #1 sec=6.3.2.5 page=0 table=- score=0.032
    #2 sec=6.3.2.3 page=0 table=- score=0.031
    #3 sec=6.3.3.2.1 page=0 table=- score=0.030
    #4 sec=6.3.2.1 page=0 table=- score=0.030
    #5 sec=6.3.2.2 page=0 table=- score=0.030

## q27 — Which clauses define the MPR and A-MPR values used in the PCMAX_L formula for configured maximum output power?
_expected_section = §6.2.4 · type = section_summary · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4.3 p0 table=-
  missing keywords: ['6.2.2.3']
    #1 sec=6.2.4.3 page=0 table=- score=-23.452
    #2 sec=6.2.4.5 page=0 table=- score=-23.186
    #3 sec=6.2.4.3 page=0 table=- score=-19.816
    #4 sec=6.2.4.3 page=0 table=- score=-18.182
    #5 sec=6.2.3.5 page=0 table=- score=-14.514

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2.3.3.2 p0 table=-
    #1 sec=6.2.3.3.2 page=0 table=- score=0.310
    #2 sec=6.2.4.3 page=0 table=- score=0.347
    #3 sec=6.2.3.3.1 page=0 table=- score=0.367
    #4 sec=6.2.4.3 page=0 table=- score=0.379
    #5 sec=6.2.3.4.1 page=0 table=- score=0.403

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4.3 p0 table=-
    #1 sec=6.2.4.3 page=0 table=- score=0.033
    #2 sec=6.2.4.3 page=0 table=- score=0.031
    #3 sec=6.2.4.3 page=0 table=- score=0.031
    #4 sec=6.2.3.3.2 page=0 table=- score=0.030
    #5 sec=6.2.3.3.1 page=0 table=- score=0.030

## q28 — What is the test purpose of the absolute power tolerance test?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.4.2.5 p0 table=-
  missing keywords: ['set its initial output power']
    #1 sec=6.3.4.2.5 page=0 table=- score=-12.508
    #2 sec=6.3.4.2.3 page=0 table=- score=-12.019
    #3 sec=6.3.4.2.4.1 page=0 table=6.3.4.2.4.1-1 score=-8.960
    #4 sec=6.2.4.3 page=0 table=- score=-8.810
    #5 sec=6.3.4.4.4.2 page=0 table=- score=-8.462

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.4.2.3 p0 table=-
  missing keywords: ['set its initial output power']
    #1 sec=6.3.4.2.3 page=0 table=- score=0.341
    #2 sec=6.3.4.2.5 page=0 table=- score=0.387
    #3 sec=6.3.4.4.3 page=0 table=- score=0.403
    #4 sec=6.3.4.1 page=0 table=- score=0.451
    #5 sec=6.2.3.5 page=0 table=6.2.3.5-38 score=0.455

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.4.2.3 p0 table=-
  missing keywords: ['set its initial output power']
    #1 sec=6.3.4.2.3 page=0 table=- score=0.033
    #2 sec=6.3.4.2.5 page=0 table=- score=0.033
    #3 sec=6.3.4.4.3 page=0 table=- score=0.029
    #4 sec=6.3.4.3.5 page=0 table=- score=0.029
    #5 sec=6.3.4.3.3 page=0 table=- score=0.029

## q29 — What does the aggregate power tolerance test verify about UE transmitter behaviour?
_expected_section = §6.3.4.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4.3 p0 table=-
    #1 sec=6.3.4.4.3 page=0 table=- score=-17.498
    #2 sec=6.2.1.1 page=0 table=- score=-16.033
    #3 sec=6.3.4.4.1 page=0 table=- score=-13.441
    #4 sec=6.3.4.2.1 page=0 table=- score=-13.213
    #5 sec=6.3.4.3.1 page=0 table=- score=-13.211

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4.3 p0 table=-
    #1 sec=6.3.4.4.3 page=0 table=- score=0.278
    #2 sec=6.3.4.2.3 page=0 table=- score=0.306
    #3 sec=6.3.1.1 page=0 table=- score=0.343
    #4 sec=6.3.4.3.5 page=0 table=- score=0.346
    #5 sec=6.2.4.5 page=0 table=- score=0.366

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4.3 p0 table=-
    #1 sec=6.3.4.4.3 page=0 table=- score=0.033
    #2 sec=6.2.1.1 page=0 table=- score=0.031
    #3 sec=6.3.4.2.3 page=0 table=- score=0.031
    #4 sec=6.3.4.4.1 page=0 table=- score=0.031
    #5 sec=6.3.4.2.1 page=0 table=- score=0.031

## q30 — What is the test purpose of the relative power tolerance test, and within what transmission gap does it apply?
_expected_section = §6.3.4.3 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=Y RR@10=0.25 · coverage = 1/3 (33%) · top-1 = §6.3.4.4.4.2 p0 table=-
  missing keywords: ['target sub-frame', 'less than or equal']
    #1 sec=6.3.4.4.4.2 page=0 table=- score=-19.983
    #2 sec=6.3.4.2.3 page=0 table=- score=-18.892
    #3 sec=6.3.4.4.4.2 page=0 table=- score=-16.685
    #4 sec=6.3.4.3.3 page=0 table=- score=-15.858
    #5 sec=6.3.4.4.3 page=0 table=- score=-15.478

**dense** — hit@1=N hit@3=N hit@5=Y RR@10=0.25 · coverage = 3/3 (100%) · top-1 = §6.3.4.2.3 p0 table=-
    #1 sec=6.3.4.2.3 page=0 table=- score=0.364
    #2 sec=6.3.4.2.1 page=0 table=- score=0.387
    #3 sec=6.3.4.4.3 page=0 table=- score=0.398
    #4 sec=6.3.4.3.3 page=0 table=- score=0.402
    #5 sec=6.3.4.3.1 page=0 table=- score=0.414

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 1/3 (33%) · top-1 = §6.3.4.2.3 p0 table=-
  missing keywords: ['target sub-frame', 'less than or equal']
    #1 sec=6.3.4.2.3 page=0 table=- score=0.033
    #2 sec=6.3.4.4.3 page=0 table=- score=0.031
    #3 sec=6.3.4.3.3 page=0 table=- score=0.031
    #4 sec=6.3.4.2.1 page=0 table=- score=0.031
    #5 sec=6.3.4.3.5 page=0 table=- score=0.030
