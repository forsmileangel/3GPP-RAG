# Retrieval Benchmark

_scored at k=10 (hit@1/3/5, MRR@10); detail rows show top 5; source_format = pdf_pymupdf; backends = sparse, dense, hybrid_

## Aggregate

| backend | hit@1 | hit@3 | hit@5 | MRR@10 | mean coverage |
|---|---|---|---|---|---|
| sparse | 22/30 | 29/30 | 29/30 | 0.85 | 88% |
| dense | 21/30 | 27/30 | 28/30 | 0.80 | 84% |
| hybrid | 22/30 | 29/30 | 30/30 | 0.85 | 89% |

## By question type

| backend | type | n | hit@1 | hit@3 | hit@5 | MRR@10 | coverage |
|---|---|---|---|---|---|---|---|
| sparse | numeric | 9 | 89% | 100% | 100% | 0.94 | 100% |
| sparse | procedure | 3 | 67% | 100% | 100% | 0.83 | 61% |
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

## q01 — What is the maximum output power tolerance for FR1 PC3 UE?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=-13.266
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=-11.692
    #3 sec=6.2.1 page=92 table=- score=-10.858
    #4 sec=6.2.3 page=222 table=- score=-10.771
    #5 sec=6.2.1 page=95 table=- score=-10.725

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
    #5 sec=6.2.1 page=96 table=6.2.1.5-1 score=0.030

## q02 — How is the test procedure defined for UE maximum output power across power classes?
_expected_section = §6.2.1 · type = procedure · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1 p92 table=-
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2.1 page=92 table=- score=-16.590
    #2 sec=6.2.3 page=123 table=- score=-10.903
    #3 sec=6.2.1 page=93 table=6.2.1.3-1 score=-10.901
    #4 sec=6.2.2 page=98 table=- score=-10.790
    #5 sec=6.3.4.3 page=570 table=- score=-10.742

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
    #3 sec=6.2.2 page=98 table=- score=0.030
    #4 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.030
    #5 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.029

## q03 — What are the test conditions and channel bandwidth for inner / outer maximum output power?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-5
    #1 sec=6.2.2 page=99 table=6.2.2.3-5 score=-17.958
    #2 sec=6.2.1 page=94 table=6.2.1.4.1-1 score=-15.283
    #3 sec=6.3.1 page=541 table=- score=-13.793
    #4 sec=6.2.3 page=123 table=- score=-12.714
    #5 sec=6.3.3.2 page=546 table=6.3.3.2.4.1-1 score=-12.460

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
    #3 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.030
    #4 sec=6.2.1 page=92 table=- score=0.029
    #5 sec=6.3.3.2 page=546 table=6.3.3.2.4.1-1 score=0.028

## q04 — Define UE output power dynamics — minimum output power requirement.
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=-26.330
    #2 sec=6.2.1 page=92 table=- score=-20.851
    #3 sec=6.3.4.1 page=567 table=- score=-16.566
    #4 sec=6.3.4.2 page=567 table=- score=-16.566
    #5 sec=6.3.4.4 page=587 table=- score=-15.530

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

## q05 — What is the transmit OFF power requirement for NR FR1 UE?
_expected_section = §6.3.2 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=-17.234
    #2 sec=6.3.3.1 page=545 table=- score=-15.122
    #3 sec=6.3.3.6 page=557 table=- score=-15.049
    #4 sec=6.3.3.2 page=545 table=- score=-14.911
    #5 sec=6.3.2 page=544 table=- score=-13.934

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 2/2 (100%) · top-1 = §6.2.3 p123 table=-
    #1 sec=6.2.3 page=123 table=- score=0.367
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.367
    #3 sec=6.3.2 page=544 table=- score=0.374
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.378
    #5 sec=6.3.4.3 page=570 table=- score=0.383

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.032
    #2 sec=6.3.3.2 page=546 table=- score=0.029
    #3 sec=6.3.3.2 page=546 table=6.3.3.2.4.1-1 score=0.028
    #4 sec=6.2.2 page=98 table=- score=0.026
    #5 sec=6.3.1 page=541 table=- score=0.025

## q06 — What are the absolute and relative power tolerance requirements?
_expected_section = §6.3.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3 p576 table=-
    #1 sec=6.3.4.3 page=576 table=- score=-13.362
    #2 sec=6.3.4.3 page=570 table=- score=-13.196
    #3 sec=6.3.4.1 page=567 table=- score=-12.631
    #4 sec=6.3.4.2 page=567 table=- score=-12.631
    #5 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=-10.561

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

## q07 — What is the configured transmitted power for UE in NR?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.2.4 p279 table=6.2.4.5-2
    #1 sec=6.2.4 page=279 table=6.2.4.5-2 score=-14.125
    #2 sec=6.2.4 page=274 table=- score=-13.698
    #3 sec=6.2.4 page=273 table=- score=-13.618
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=-13.365
    #5 sec=6.3.1 page=541 table=6.2I.4.5-0 score=-12.671

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

## q08 — How are additional MPR (A-MPR) requirements defined for NR FR1?
_expected_section = §6.2.3 · type = procedure · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.2.3 p123 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2.3 page=123 table=- score=-14.383
    #2 sec=6.2.3 page=123 table=- score=-11.927
    #3 sec=6.2.3 page=125 table=6.2.3.3.1-1 score=-11.086
    #4 sec=6.2.4 page=274 table=- score=-10.997
    #5 sec=6.2.2 page=98 table=- score=-10.970

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
    #3 sec=6.2.3 page=125 table=6.2.3.3.1-1 score=0.029
    #4 sec=6.2.3 page=127 table=6.2.3.3.1-2 score=0.029
    #5 sec=6.2.3 page=140 table=- score=0.028

## q09 — What is the test purpose for the minimum output power conformance test?
_expected_section = §6.3.1 · type = section_summary · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=-20.163
    #2 sec=6.3.4.1 page=567 table=- score=-17.604
    #3 sec=6.3.4.2 page=567 table=- score=-17.604
    #4 sec=6.3.4.3 page=570 table=- score=-17.243
    #5 sec=6.3.4.4 page=587 table=- score=-17.213

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

## q10 — Why does excess Transmit OFF power matter for cell coverage?
_expected_section = §6.3.2 · type = section_summary · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=-26.495
    #2 sec=6.2.1 page=92 table=- score=-17.758
    #3 sec=6.3.3.1 page=545 table=- score=-12.279
    #4 sec=6.3.3.2 page=545 table=- score=-12.073
    #5 sec=6.3.3.1 page=545 table=- score=-11.196

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
    #4 sec=6.3.3.1 page=545 table=- score=0.030
    #5 sec=6.3.2 page=544 table=- score=0.030

## q11 — What is the maximum output power for a Power Class 2 UE in NR band n78?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p97 table=6.2.1.5-2
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=-21.420
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=-18.939
    #3 sec=6.2.1 page=93 table=6.2.1.3-1 score=-18.384
    #4 sec=6.2.1 page=96 table=6.2.1.5-1 score=-17.994
    #5 sec=6.2.2 page=98 table=- score=-17.435

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

## q12 — What is the minimum output power limit and measurement bandwidth for a 10 MHz channel in FR1?
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.1 p542 table=6.3.1.3-1
    #1 sec=6.3.1 page=542 table=6.3.1.3-1 score=-18.916
    #2 sec=6.3.1 page=543 table=6.3.1.5-1 score=-18.466
    #3 sec=6.3.3.6 page=565 table=6.3.3.6.5-1 score=-17.890
    #4 sec=6.3.3.3 page=550 table=6.3.3.2.5-1 score=-17.357
    #5 sec=6.3.3.4 page=550 table=6.3.3.2.5-1 score=-17.357

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

## q13 — What is the absolute power tolerance for an NR UE under normal conditions?
_expected_section = §6.3.4.2 · type = numeric · difficulty = easy_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=-21.266
    #2 sec=6.3.4.2 page=567 table=- score=-21.266
    #3 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=-17.760
    #4 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=-17.760
    #5 sec=6.3.4.2 page=568 table=6.3.4.2.4.1-1 score=-13.959

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
    #5 sec=6.2.4 page=279 table=6.2.4.5-2 score=0.028

## q14 — What is the aggregate power tolerance for PUSCH transmissions with 0 dB TPC commands?
_expected_section = §6.3.4.4 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=-23.858
    #2 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=-23.239
    #3 sec=6.3.4.3 page=576 table=- score=-20.980
    #4 sec=6.3.4.4 page=590 table=- score=-18.212
    #5 sec=6.3.4.4 page=590 table=- score=-17.190

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

## q15 — What is the PCMAX tolerance when the configured maximum output power is between 21 and 23 dBm?
_expected_section = §6.2.4 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p273 table=-
    #1 sec=6.2.4 page=273 table=- score=-23.921
    #2 sec=6.2.2 page=107 table=- score=-21.230
    #3 sec=6.3.1 page=541 table=6.2I.4.5-1 score=-20.781
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=-20.526
    #5 sec=6.2.1 page=93 table=6.2.1.3-1 score=-19.765

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p276 table=6.2.4.3-2
    #1 sec=6.2.4 page=276 table=6.2.4.3-2 score=0.228
    #2 sec=6.2.4 page=273 table=- score=0.310
    #3 sec=6.2.4 page=275 table=6.2.4.3-1 score=0.336
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.336

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p273 table=-
    #1 sec=6.2.4 page=273 table=- score=0.033
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.031
    #3 sec=6.2.4 page=275 table=6.2.4.3-1 score=0.031
    #4 sec=6.2.2 page=107 table=- score=0.031
    #5 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.030

## q16 — What is the allowed maximum power reduction for a power class 3 UE using DFT-s-OFDM 256 QAM modulation?
_expected_section = §6.2.2 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-2
    #1 sec=6.2.2 page=99 table=6.2.2.3-2 score=-22.410
    #2 sec=6.2.2 page=98 table=6.2.2.3-1 score=-19.981
    #3 sec=6.2.2 page=98 table=- score=-19.510
    #4 sec=6.2.2 page=99 table=6.2.2.3-5 score=-19.370
    #5 sec=6.2.2 page=98 table=- score=-19.186

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
    #5 sec=6.2.3 page=151 table=- score=0.029

## q17 — Which test verifies the UE's ability to set its initial output power at the start of a transmission after a gap longer than 20ms?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=-56.728
    #2 sec=6.3.4.2 page=567 table=- score=-56.728
    #3 sec=6.3.4.3 page=570 table=- score=-32.639
    #4 sec=6.3.4.4 page=587 table=- score=-23.467
    #5 sec=6.2.2 page=99 table=6.2.2.3-5 score=-21.978

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

## q18 — What is the PRACH ON power measurement period for preamble format 0?
_expected_section = §6.3.3.4 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.3.3.3 p550 table=-
    #1 sec=6.3.3.3 page=550 table=- score=-31.185
    #2 sec=6.3.3.4 page=550 table=- score=-31.185
    #3 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=-30.645
    #4 sec=6.3.3.4 page=553 table=- score=-22.470
    #5 sec=6.3.3.3 page=550 table=- score=-19.009

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

## q19 — Which power control commands does the SS send to drive the UE to its minimum output power during the conformance test?
_expected_section = §6.3.1 · type = procedure · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=-39.473
    #2 sec=6.3.1 page=543 table=- score=-30.461
    #3 sec=6.3.3.6 page=561 table=- score=-28.712
    #4 sec=6.3.4.1 page=567 table=- score=-28.393
    #5 sec=6.3.4.2 page=567 table=- score=-28.393

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
    #3 sec=6.3.4.2 page=567 table=- score=0.031
    #4 sec=6.3.1 page=543 table=- score=0.030
    #5 sec=6.3.3.6 page=561 table=- score=0.030

## q20 — What is P-MPR in the PCMAX equation and what value must it take during UE conducted conformance testing?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4 p275 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4 page=275 table=- score=-30.587
    #2 sec=6.2.4 page=273 table=- score=-13.216
    #3 sec=6.3.4.4 page=587 table=- score=-11.717
    #4 sec=6.3.3.6 page=558 table=- score=-9.428
    #5 sec=6.2.3 page=135 table=6.2.3.3.7-1 score=-8.988

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
    #3 sec=6.2.2 page=98 table=- score=0.028
    #4 sec=6.2.1 page=95 table=6.2.1.4.3-2 score=0.016
    #5 sec=6.3.4.4 page=587 table=- score=0.016

## q21 — In the UE Power Class table, what maximum output power and tolerance apply to band n14 for Power Class 1?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=-30.611
    #2 sec=6.2.2 page=98 table=- score=-28.914
    #3 sec=6.2.1 page=97 table=6.2.1.5-2 score=-27.428
    #4 sec=6.2.3 page=123 table=- score=-25.775
    #5 sec=6.2.1 page=96 table=6.2.1.5-1 score=-23.626

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

## q22 — What is the allowed MPR for CP-OFDM 256 QAM modulation in outer RB allocations for a power class 3 UE?
_expected_section = §6.2.2 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-2
    #1 sec=6.2.2 page=99 table=6.2.2.3-2 score=-27.379
    #2 sec=6.2.2 page=99 table=6.2.2.3-5 score=-25.185
    #3 sec=6.2.2 page=98 table=6.2.2.3-1 score=-24.879
    #4 sec=6.2.3 page=123 table=- score=-20.515
    #5 sec=6.2.3 page=139 table=6.2.3.3.15-2 score=-20.057

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

## q23 — What is the PRACH ON power measurement period for preamble format C2 with 15 kHz SCS?
_expected_section = §6.3.3.4 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=-35.537
    #2 sec=6.3.3.3 page=550 table=- score=-31.185
    #3 sec=6.3.3.4 page=550 table=- score=-31.185
    #4 sec=6.3.3.4 page=553 table=- score=-24.288
    #5 sec=6.3.3.4 page=554 table=6.3.3.4.4.3-2 score=-23.234

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

## q24 — What is the test requirement for measured UE output power at test point 2 in the configured transmitted power test?
_expected_section = §6.2.4 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=6.2I.4.5-1
    #1 sec=6.3.1 page=541 table=6.2I.4.5-1 score=-24.583
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=-21.343
    #3 sec=6.2.1 page=93 table=6.2.1.3-1 score=-17.831
    #4 sec=6.2.4 page=273 table=- score=-17.304
    #5 sec=6.3.4.3 page=570 table=- score=-14.796

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.2.4 p278 table=6.2.4.5-1
    #1 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.333
    #2 sec=6.3.4.3 page=570 table=- score=0.337
    #3 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.337
    #4 sec=6.3.4.4 page=587 table=- score=0.340
    #5 sec=6.3.4.1 page=567 table=- score=0.344

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.2.4 p278 table=6.2.4.5-1
    #1 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.033
    #2 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.032
    #3 sec=6.3.4.3 page=570 table=- score=0.032
    #4 sec=6.3.4.1 page=567 table=- score=0.030
    #5 sec=6.3.4.2 page=567 table=- score=0.029

## q25 — In the 5 MHz ramp up sub-test, what is the expected power step size when the RB allocation changes from 1 RB to 15 RBs?
_expected_section = §6.3.4.3 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.3 p579 table=6.3.4.3.5-1
    #1 sec=6.3.4.3 page=579 table=6.3.4.3.5-1 score=-39.397
    #2 sec=6.3.4.3 page=585 table=6.3.4.3.5-5 score=-37.983
    #3 sec=6.3.4.3 page=581 table=6.3.4.3.5-3 score=-35.671
    #4 sec=6.3.4.3 page=580 table=6.3.4.3.5-2 score=-35.334
    #5 sec=6.3.4.3 page=586 table=6.3.4.3.5-6 score=-34.550

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

## q26 — Where is the Transmit OFF power requirement actually tested, given that clause 6.3.2 defines no standalone test procedure?
_expected_section = §6.3.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=N RR@10=0.11 · coverage = 1/2 (50%) · top-1 = §6.3.3.1 p545 table=-
  missing keywords: ['covered by']
    #1 sec=6.3.3.1 page=545 table=- score=-34.844
    #2 sec=6.3.3.2 page=545 table=- score=-34.844
    #3 sec=6.3.3.1 page=545 table=- score=-32.161
    #4 sec=6.3.3.2 page=545 table=- score=-30.326
    #5 sec=6.3.3.3 page=550 table=- score=-26.854

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

## q27 — Which clauses define the MPR and A-MPR values used in the PCMAX_L formula for configured maximum output power?
_expected_section = §6.2.4 · type = section_summary · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.4 p275 table=6.2.4.3-1
  missing keywords: ['6.2.2.3', '6.2.3.3']
    #1 sec=6.2.4 page=275 table=6.2.4.3-1 score=-22.263
    #2 sec=6.2.4 page=273 table=- score=-21.030
    #3 sec=6.2.4 page=275 table=- score=-20.383
    #4 sec=6.3.1 page=541 table=6.2I.4.5-1 score=-17.013
    #5 sec=6.2.3 page=123 table=- score=-16.582

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

## q28 — What is the test purpose of the absolute power tolerance test?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=-14.768
    #2 sec=6.3.4.2 page=567 table=- score=-14.768
    #3 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=-10.577
    #4 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=-10.577
    #5 sec=6.2.4 page=275 table=6.2.4.3-1 score=-9.868

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

## q29 — What does the aggregate power tolerance test verify about UE transmitter behaviour?
_expected_section = §6.3.4.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=-20.742
    #2 sec=6.2.1 page=92 table=- score=-16.920
    #3 sec=6.3.4.1 page=567 table=- score=-13.848
    #4 sec=6.3.4.2 page=567 table=- score=-13.848
    #5 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=-12.145

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=0.271
    #2 sec=6.3.4.3 page=570 table=- score=0.308
    #3 sec=6.3.4.1 page=567 table=- score=0.322
    #4 sec=6.3.4.2 page=567 table=- score=0.322
    #5 sec=6.3.4.3 page=576 table=- score=0.333

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=0.033
    #2 sec=6.3.4.1 page=567 table=- score=0.032
    #3 sec=6.3.4.3 page=570 table=- score=0.031
    #4 sec=6.3.4.2 page=567 table=- score=0.031
    #5 sec=6.2.1 page=92 table=- score=0.031

## q30 — What is the test purpose of the relative power tolerance test, and within what transmission gap does it apply?
_expected_section = §6.3.4.3 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.3 p570 table=-
    #1 sec=6.3.4.3 page=570 table=- score=-25.376
    #2 sec=6.3.4.1 page=567 table=- score=-24.837
    #3 sec=6.3.4.2 page=567 table=- score=-24.837
    #4 sec=6.3.4.4 page=587 table=- score=-19.675
    #5 sec=6.2.1 page=92 table=- score=-19.185

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
    #5 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.030
