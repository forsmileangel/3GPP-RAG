# Retrieval Benchmark

_scored at k=10 (hit@1/3/5, MRR@10); detail rows show top 5; source_format = pdf_pymupdf; backends = sparse, dense, hybrid_

## Aggregate

| backend | hit@1 | hit@3 | hit@5 | MRR@10 | mean coverage |
|---|---|---|---|---|---|
| sparse | 19/30 | 28/30 | 30/30 | 0.79 | 89% |
| dense | 21/30 | 26/30 | 26/30 | 0.78 | 82% |
| hybrid | 23/30 | 29/30 | 30/30 | 0.88 | 89% |

## By question type

| backend | type | n | hit@1 | hit@3 | hit@5 | MRR@10 | coverage |
|---|---|---|---|---|---|---|---|
| sparse | numeric | 9 | 67% | 100% | 100% | 0.83 | 100% |
| sparse | procedure | 3 | 67% | 100% | 100% | 0.83 | 61% |
| sparse | section_summary | 11 | 55% | 91% | 100% | 0.73 | 89% |
| sparse | table_lookup | 7 | 71% | 86% | 100% | 0.82 | 86% |
| dense | numeric | 9 | 56% | 78% | 78% | 0.64 | 81% |
| dense | procedure | 3 | 67% | 67% | 67% | 0.70 | 44% |
| dense | section_summary | 11 | 64% | 91% | 91% | 0.77 | 97% |
| dense | table_lookup | 7 | 100% | 100% | 100% | 1.00 | 76% |
| hybrid | numeric | 9 | 78% | 100% | 100% | 0.89 | 94% |
| hybrid | procedure | 3 | 67% | 67% | 100% | 0.75 | 61% |
| hybrid | section_summary | 11 | 64% | 100% | 100% | 0.82 | 94% |
| hybrid | table_lookup | 7 | 100% | 100% | 100% | 1.00 | 86% |

## q01 — What is the maximum output power tolerance for FR1 PC3 UE?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=-13.600
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=-12.548
    #3 sec=6.2.1 page=95 table=- score=-12.222
    #4 sec=6.2.3 page=222 table=- score=-11.595
    #5 sec=6.2.1 page=92 table=- score=-11.278

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
    #4 sec=6.2.4 page=273 table=- score=0.030
    #5 sec=6.2.1 page=96 table=6.2.1.5-1 score=0.030

## q02 — How is the test procedure defined for UE maximum output power across power classes?
_expected_section = §6.2.1 · type = procedure · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1 p92 table=-
  missing keywords: ['pc2', 'pc3']
    #1 sec=6.2.1 page=92 table=- score=-16.397
    #2 sec=6.3.1 page=541 table=6.2I.4.5-1 score=-10.821
    #3 sec=6.3.1 page=541 table=- score=-10.551
    #4 sec=6.2.1 page=95 table=- score=-10.196
    #5 sec=6.2.3 page=222 table=- score=-10.154

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
    #2 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.031
    #3 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.031
    #4 sec=6.2.4 page=273 table=- score=0.030
    #5 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.030

## q03 — What are the test conditions and channel bandwidth for inner / outer maximum output power?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=Y RR@10=0.25 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-5
    #1 sec=6.2.2 page=99 table=6.2.2.3-5 score=-16.742
    #2 sec=6.2.3 page=123 table=- score=-13.952
    #3 sec=6.2.2 page=104 table=6.2.2.4.1-3 score=-13.566
    #4 sec=6.2.1 page=94 table=6.2.1.4.1-1 score=-13.046
    #5 sec=6.2.2 page=102 table=6.2.2.4.1-2 score=-12.954

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/3 (33%) · top-1 = §6.2.1 p97 table=6.2.1.5-2
  missing keywords: ['inner', 'outer']
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.332
    #2 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=0.341
    #3 sec=6.2.4 page=273 table=- score=0.341
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.343

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p94 table=6.2.1.4.1-1
    #1 sec=6.2.1 page=94 table=6.2.1.4.1-1 score=0.030
    #2 sec=6.2.1 page=92 table=- score=0.026
    #3 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.016
    #4 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.016
    #5 sec=6.2.3 page=123 table=- score=0.016

## q04 — Define UE output power dynamics — minimum output power requirement.
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=-25.551
    #2 sec=6.2.1 page=92 table=- score=-20.074
    #3 sec=6.3.4.1 page=567 table=- score=-15.221
    #4 sec=6.3.4.2 page=567 table=- score=-15.221
    #5 sec=6.3.1 page=543 table=- score=-15.162

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.252
    #2 sec=6.3.4.3 page=570 table=- score=0.351
    #3 sec=6.3.4.4 page=587 table=- score=0.356
    #4 sec=6.3.4.4 page=590 table=- score=0.363

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.033
    #2 sec=6.3.4.3 page=570 table=- score=0.031
    #3 sec=6.3.4.1 page=567 table=- score=0.031
    #4 sec=6.3.4.4 page=587 table=- score=0.031
    #5 sec=6.2.1 page=92 table=- score=0.031

## q05 — What is the transmit OFF power requirement for NR FR1 UE?
_expected_section = §6.3.2 · type = numeric · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=-16.186
    #2 sec=6.3.3.6 page=557 table=- score=-15.850
    #3 sec=6.3.2 page=544 table=- score=-14.685
    #4 sec=6.3.3.1 page=545 table=- score=-14.494
    #5 sec=6.3.3.2 page=545 table=- score=-14.148

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 2/2 (100%) · top-1 = §6.2.3 p123 table=-
    #1 sec=6.2.3 page=123 table=- score=0.367
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.367
    #3 sec=6.3.2 page=544 table=- score=0.374
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.378
    #5 sec=6.3.4.3 page=570 table=- score=0.383

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.032
    #2 sec=6.3.3.2 page=546 table=- score=0.028
    #3 sec=6.3.3.2 page=546 table=6.3.3.2.4.1-1 score=0.027
    #4 sec=6.2.3 page=123 table=- score=0.016
    #5 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.016

## q06 — What are the absolute and relative power tolerance requirements?
_expected_section = §6.3.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.3.4.1 p567 table=-
  missing keywords: ['relative power tolerance']
    #1 sec=6.3.4.1 page=567 table=- score=-12.002
    #2 sec=6.3.4.2 page=567 table=- score=-12.002
    #3 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=-11.290
    #4 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=-11.290
    #5 sec=6.3.4.3 page=576 table=- score=-11.172

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=6.3.4.2.3-1
    #1 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=0.307
    #2 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=0.307
    #3 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.333
    #4 sec=6.3.4.1 page=567 table=- score=0.341
    #5 sec=6.3.4.2 page=567 table=- score=0.341

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=6.3.4.2.3-1
    #1 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=0.032
    #2 sec=6.3.4.1 page=567 table=- score=0.032
    #3 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=0.032
    #4 sec=6.3.4.2 page=567 table=- score=0.032
    #5 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.030

## q07 — What is the configured transmitted power for UE in NR?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=6.2I.4.5-0
    #1 sec=6.3.1 page=541 table=6.2I.4.5-0 score=-11.088
    #2 sec=6.2.4 page=274 table=- score=-10.841
    #3 sec=6.2.4 page=279 table=6.2.4.5-2 score=-10.109
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=-10.061
    #5 sec=6.2.4 page=273 table=- score=-9.672

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 1/1 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.379

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 1/1 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.032
    #2 sec=6.2.4 page=273 table=- score=0.031
    #3 sec=6.3.4.3 page=570 table=- score=0.030
    #4 sec=6.2.3 page=123 table=- score=0.028
    #5 sec=6.2.3 page=123 table=- score=0.027

## q08 — How are additional MPR (A-MPR) requirements defined for NR FR1?
_expected_section = §6.2.3 · type = procedure · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 1/2 (50%) · top-1 = §6.2.3 p123 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2.3 page=123 table=- score=-16.517
    #2 sec=6.2.3 page=125 table=6.2.3.3.1-1 score=-14.579
    #3 sec=6.2.3 page=123 table=6.2.3.3.1-1 score=-12.834
    #4 sec=6.2.3 page=140 table=- score=-10.764
    #5 sec=6.2.3 page=222 table=- score=-10.527

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
    #2 sec=6.2.3 page=123 table=6.2.3.3.1-1 score=0.032
    #3 sec=6.2.3 page=140 table=- score=0.031
    #4 sec=6.2.3 page=129 table=- score=0.030
    #5 sec=6.2.3 page=125 table=6.2.3.3.1-1 score=0.029

## q09 — What is the test purpose for the minimum output power conformance test?
_expected_section = §6.3.1 · type = section_summary · difficulty = easy_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=-18.061
    #2 sec=6.3.4.1 page=567 table=- score=-15.460
    #3 sec=6.3.4.2 page=567 table=- score=-15.460
    #4 sec=6.3.4.4 page=587 table=- score=-15.089
    #5 sec=6.3.4.3 page=570 table=- score=-15.086

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
    #1 sec=6.3.2 page=544 table=- score=-24.780
    #2 sec=6.2.1 page=92 table=- score=-14.361
    #3 sec=6.3.3.1 page=545 table=- score=-13.191
    #4 sec=6.3.3.2 page=545 table=- score=-12.930
    #5 sec=6.3.3.1 page=545 table=- score=-11.737

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
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=-18.971
    #2 sec=6.2.1 page=93 table=6.2.1.3-1 score=-16.753
    #3 sec=6.2.1 page=96 table=6.2.1.5-1 score=-15.948
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=-15.916
    #5 sec=6.2.2 page=98 table=- score=-15.237

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p97 table=6.2.1.5-2
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.344
    #2 sec=6.2.2 page=118 table=6.2.2.5-6 score=0.374
    #3 sec=6.2.3 page=224 table=6.2.3.5-2 score=0.381
    #4 sec=6.2.2 page=110 table=6.2.2.5-1 score=0.383
    #5 sec=6.2.3 page=236 table=6.2.3.5-12 score=0.385

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p97 table=6.2.1.5-2
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.033
    #2 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.031
    #3 sec=6.2.1 page=96 table=6.2.1.5-1 score=0.030
    #4 sec=6.2.2 page=98 table=- score=0.029
    #5 sec=6.2.4 page=274 table=- score=0.028

## q12 — What is the minimum output power limit and measurement bandwidth for a 10 MHz channel in FR1?
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.3.4.2 p569 table=6.3.4.2.5-1
    #1 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=-17.007
    #2 sec=6.3.1 page=542 table=6.3.1.3-1 score=-16.771
    #3 sec=6.3.1 page=543 table=6.3.1.5-1 score=-16.270
    #4 sec=6.3.3.6 page=565 table=6.3.3.6.5-1 score=-15.056
    #5 sec=6.3.3.3 page=550 table=6.3.3.2.5-1 score=-14.502

**dense** — hit@1=N hit@3=N hit@5=N RR@10=0.00 · coverage = 1/3 (33%) · top-1 = §6.3.3.4 p556 table=6.3.3.4.5-1
  missing keywords: ['-40', '9.375']
    #1 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.370

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.3.4.2 p569 table=6.3.4.2.5-1
    #1 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=0.032
    #2 sec=6.3.1 page=542 table=6.3.1.3-1 score=0.032
    #3 sec=6.3.3.6 page=565 table=6.3.3.6.5-1 score=0.032
    #4 sec=6.3.1 page=543 table=6.3.1.5-1 score=0.032
    #5 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.031

## q13 — What is the absolute power tolerance for an NR UE under normal conditions?
_expected_section = §6.3.4.2 · type = numeric · difficulty = easy_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=-18.228
    #2 sec=6.3.4.2 page=567 table=- score=-18.228
    #3 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=-18.223
    #4 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=-18.223
    #5 sec=6.3.4.2 page=568 table=6.3.4.2.4.1-1 score=-11.057

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
    #3 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.030
    #4 sec=6.2.3 page=123 table=- score=0.028
    #5 sec=6.2.1 page=92 table=- score=0.028

## q14 — What is the aggregate power tolerance for PUSCH transmissions with 0 dB TPC commands?
_expected_section = §6.3.4.4 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p588 table=6.3.4.4.3-1
    #1 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=-28.180
    #2 sec=6.3.4.4 page=587 table=- score=-24.929
    #3 sec=6.3.4.3 page=576 table=- score=-19.954
    #4 sec=6.3.4.4 page=590 table=- score=-18.361
    #5 sec=6.3.4.4 page=590 table=- score=-17.390

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

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2.2 p107 table=-
    #1 sec=6.2.2 page=107 table=- score=-26.524
    #2 sec=6.2.4 page=276 table=6.2.4.3-2 score=-23.970
    #3 sec=6.2.4 page=273 table=- score=-23.702
    #4 sec=6.2.3 page=263 table=6.2.3.5-29 score=-21.955
    #5 sec=6.2.4 page=278 table=6.2.4.5-1 score=-21.348

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p276 table=6.2.4.3-2
    #1 sec=6.2.4 page=276 table=6.2.4.3-2 score=0.228
    #2 sec=6.2.4 page=273 table=- score=0.310
    #3 sec=6.2.4 page=275 table=6.2.4.3-1 score=0.336

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.4 p276 table=6.2.4.3-2
    #1 sec=6.2.4 page=276 table=6.2.4.3-2 score=0.033
    #2 sec=6.2.4 page=273 table=- score=0.032
    #3 sec=6.2.4 page=275 table=6.2.4.3-1 score=0.031
    #4 sec=6.2.2 page=107 table=- score=0.016
    #5 sec=6.2.3 page=263 table=6.2.3.5-29 score=0.016

## q16 — What is the allowed maximum power reduction for a power class 3 UE using DFT-s-OFDM 256 QAM modulation?
_expected_section = §6.2.2 · type = numeric · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-2
    #1 sec=6.2.2 page=99 table=6.2.2.3-2 score=-29.609
    #2 sec=6.2.2 page=98 table=6.2.2.3-1 score=-24.418
    #3 sec=6.2.2 page=99 table=6.2.2.3-5 score=-22.148
    #4 sec=6.2.2 page=102 table=6.2.2.4.1-2 score=-21.774
    #5 sec=6.2.2 page=101 table=6.2.2.4.1-1 score=-21.597

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
    #5 sec=6.2.3 page=129 table=6.2.3.3.1-2 score=0.028

## q17 — Which test verifies the UE's ability to set its initial output power at the start of a transmission after a gap longer than 20ms?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=-50.391
    #2 sec=6.3.4.2 page=567 table=- score=-50.391
    #3 sec=6.3.4.3 page=570 table=- score=-27.748
    #4 sec=6.3.4.4 page=587 table=- score=-19.392
    #5 sec=6.3.1 page=541 table=- score=-17.173

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

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=-31.047
    #2 sec=6.3.3.3 page=550 table=- score=-30.617
    #3 sec=6.3.3.4 page=550 table=- score=-30.617
    #4 sec=6.3.3.4 page=553 table=- score=-23.617
    #5 sec=6.3.3.3 page=550 table=- score=-18.019

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.288
    #2 sec=6.3.3.3 page=550 table=- score=0.301
    #3 sec=6.3.3.4 page=550 table=- score=0.301
    #4 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.374
    #5 sec=6.3.3.4 page=551 table=- score=0.389

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=0.033
    #2 sec=6.3.3.3 page=550 table=- score=0.032
    #3 sec=6.3.3.4 page=550 table=- score=0.032
    #4 sec=6.3.3.4 page=553 table=- score=0.031
    #5 sec=6.3.3.4 page=556 table=6.3.3.4.5-1 score=0.031

## q19 — Which power control commands does the SS send to drive the UE to its minimum output power during the conformance test?
_expected_section = §6.3.1 · type = procedure · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=-32.189
    #2 sec=6.3.1 page=543 table=- score=-22.642
    #3 sec=6.3.4.1 page=567 table=- score=-22.571
    #4 sec=6.3.4.2 page=567 table=- score=-22.571
    #5 sec=6.3.3.6 page=561 table=- score=-22.273

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
    #5 sec=6.3.4.3 page=576 table=- score=0.030

## q20 — What is P-MPR in the PCMAX equation and what value must it take during UE conducted conformance testing?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4 p275 table=-
  missing keywords: ['electromagnetic energy absorption']
    #1 sec=6.2.4 page=275 table=- score=-31.625
    #2 sec=6.2.4 page=273 table=- score=-13.831
    #3 sec=6.2.4 page=275 table=6.2.4.3-1 score=-10.886
    #4 sec=6.2.4 page=276 table=6.2.4.3-2 score=-9.658
    #5 sec=6.3.4.4 page=587 table=- score=-9.460

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
    #3 sec=6.2.2 page=119 table=6.2.2.5-7 score=0.028
    #4 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.025
    #5 sec=6.2.3 page=254 table=6.2.3.5-23 score=0.025

## q21 — In the UE Power Class table, what maximum output power and tolerance apply to band n14 for Power Class 1?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=-29.205
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=-27.957
    #3 sec=6.2.2 page=98 table=- score=-26.806
    #4 sec=6.2.1 page=96 table=6.2.1.5-1 score=-24.147
    #5 sec=6.2.1 page=95 table=- score=-22.374

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.266
    #2 sec=6.2.2 page=118 table=6.2.2.5-6 score=0.279
    #3 sec=6.2.3 page=270 table=6.2.3.5-35 score=0.282
    #4 sec=6.2.2 page=110 table=6.2.2.5-1 score=0.287
    #5 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.288

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.033
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.032
    #3 sec=6.2.1 page=96 table=6.2.1.5-1 score=0.030
    #4 sec=6.2.2 page=98 table=- score=0.029
    #5 sec=6.2.2 page=98 table=- score=0.028

## q22 — What is the allowed MPR for CP-OFDM 256 QAM modulation in outer RB allocations for a power class 3 UE?
_expected_section = §6.2.2 · type = table_lookup · difficulty = medium_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-2
    #1 sec=6.2.2 page=99 table=6.2.2.3-2 score=-38.551
    #2 sec=6.2.2 page=98 table=6.2.2.3-1 score=-32.576
    #3 sec=6.2.2 page=99 table=6.2.2.3-5 score=-31.522
    #4 sec=6.2.3 page=139 table=6.2.3.3.15-2 score=-29.434
    #5 sec=6.2.3 page=147 table=6.2.3.3.26-2 score=-26.209

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p98 table=6.2.2.3-1
    #1 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.289
    #2 sec=6.2.2 page=99 table=6.2.2.3-2 score=0.299
    #3 sec=6.2.3 page=151 table=- score=0.318
    #4 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.320
    #5 sec=6.2.2 page=98 table=- score=0.338

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.2.2 p98 table=6.2.2.3-1
    #1 sec=6.2.2 page=98 table=6.2.2.3-1 score=0.033
    #2 sec=6.2.2 page=99 table=6.2.2.3-2 score=0.033
    #3 sec=6.2.2 page=99 table=6.2.2.3-5 score=0.031
    #4 sec=6.2.3 page=147 table=6.2.3.3.26-2 score=0.030
    #5 sec=6.2.3 page=151 table=- score=0.030

## q23 — What is the PRACH ON power measurement period for preamble format C2 with 15 kHz SCS?
_expected_section = §6.3.3.4 · type = table_lookup · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 0/2 (0%) · top-1 = §6.3.3.4 p551 table=6.3.3.4.3-1
  missing keywords: ['c2', '0.333333']
    #1 sec=6.3.3.4 page=551 table=6.3.3.4.3-1 score=-36.359
    #2 sec=6.3.3.3 page=550 table=- score=-30.617
    #3 sec=6.3.3.4 page=550 table=- score=-30.617
    #4 sec=6.3.3.4 page=554 table=6.3.3.4.4.3-2 score=-25.885
    #5 sec=6.3.3.4 page=553 table=- score=-24.318

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
    #1 sec=6.3.1 page=541 table=6.2I.4.5-1 score=-22.555
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=-19.154
    #3 sec=6.2.1 page=93 table=6.2.1.3-1 score=-15.143
    #4 sec=6.3.4.2 page=569 table=6.3.4.2.5-2 score=-14.437
    #5 sec=6.2.4 page=273 table=- score=-13.854

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
    #5 sec=6.3.1 page=541 table=- score=0.029

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

## q26 — Where is the Transmit OFF power requirement actually tested, given that clause 6.3.2 defines no standalone test procedure?
_expected_section = §6.3.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=N hit@5=Y RR@10=0.20 · coverage = 2/2 (100%) · top-1 = §6.3.3.1 p545 table=-
    #1 sec=6.3.3.1 page=545 table=- score=-32.607
    #2 sec=6.3.3.2 page=545 table=- score=-32.607
    #3 sec=6.3.3.1 page=545 table=- score=-31.712
    #4 sec=6.3.3.2 page=545 table=- score=-29.433
    #5 sec=6.3.2 page=544 table=- score=-25.724

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.299
    #2 sec=6.3.2 page=544 table=- score=0.347
    #3 sec=6.3.3.2 page=545 table=- score=0.375
    #4 sec=6.3.3.1 page=545 table=- score=0.393
    #5 sec=6.3.3.4 page=553 table=- score=0.406

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.032
    #2 sec=6.3.3.1 page=545 table=- score=0.031
    #3 sec=6.3.3.2 page=545 table=- score=0.031
    #4 sec=6.3.2 page=544 table=- score=0.031
    #5 sec=6.3.3.4 page=550 table=- score=0.029

## q27 — Which clauses define the MPR and A-MPR values used in the PCMAX_L formula for configured maximum output power?
_expected_section = §6.2.4 · type = section_summary · difficulty = hard_

**sparse** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4 p275 table=6.2.4.3-1
  missing keywords: ['6.2.2.3']
    #1 sec=6.2.4 page=275 table=6.2.4.3-1 score=-23.688
    #2 sec=6.2.4 page=273 table=- score=-22.222
    #3 sec=6.2.4 page=275 table=- score=-21.673
    #4 sec=6.2.3 page=222 table=- score=-19.660
    #5 sec=6.2.3 page=123 table=- score=-19.599

**dense** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.2.3 p129 table=-
    #1 sec=6.2.3 page=129 table=- score=0.320
    #2 sec=6.2.4 page=273 table=- score=0.357
    #3 sec=6.2.3 page=222 table=- score=0.368
    #4 sec=6.2.3 page=139 table=6.2.3.3.15-2 score=0.382
    #5 sec=6.2.3 page=123 table=- score=0.386

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 2/3 (67%) · top-1 = §6.2.4 p273 table=-
  missing keywords: ['6.2.2.3']
    #1 sec=6.2.4 page=273 table=- score=0.032
    #2 sec=6.2.3 page=222 table=- score=0.031
    #3 sec=6.2.3 page=129 table=- score=0.031
    #4 sec=6.2.4 page=275 table=- score=0.031
    #5 sec=6.2.3 page=123 table=- score=0.031

## q28 — What is the test purpose of the absolute power tolerance test?
_expected_section = §6.3.4.2 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=-13.445
    #2 sec=6.3.4.2 page=567 table=- score=-13.445
    #3 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=-11.386
    #4 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=-11.386
    #5 sec=6.3.4.2 page=569 table=6.3.4.2.5-2 score=-10.180

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
    #1 sec=6.3.4.4 page=587 table=- score=-19.876
    #2 sec=6.3.4.4 page=588 table=6.3.4.4.3-1 score=-15.281
    #3 sec=6.2.1 page=92 table=- score=-13.962
    #4 sec=6.3.4.1 page=567 table=- score=-12.285
    #5 sec=6.3.4.2 page=567 table=- score=-12.285

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=0.271
    #2 sec=6.3.4.3 page=570 table=- score=0.308
    #3 sec=6.3.4.1 page=567 table=- score=0.322
    #4 sec=6.3.4.2 page=567 table=- score=0.322
    #5 sec=6.3.4.3 page=576 table=- score=0.333

**hybrid** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.4 p587 table=-
    #1 sec=6.3.4.4 page=587 table=- score=0.033
    #2 sec=6.3.4.1 page=567 table=- score=0.031
    #3 sec=6.3.4.3 page=570 table=- score=0.031
    #4 sec=6.3.4.2 page=567 table=- score=0.031
    #5 sec=6.2.1 page=92 table=- score=0.031

## q30 — What is the test purpose of the relative power tolerance test, and within what transmission gap does it apply?
_expected_section = §6.3.4.3 · type = section_summary · difficulty = medium_

**sparse** — hit@1=N hit@3=Y hit@5=Y RR@10=0.33 · coverage = 3/3 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=-21.818
    #2 sec=6.3.4.2 page=567 table=- score=-21.818
    #3 sec=6.3.4.3 page=570 table=- score=-21.026
    #4 sec=6.3.4.4 page=587 table=- score=-16.417
    #5 sec=6.2.1 page=92 table=- score=-15.243

**dense** — hit@1=Y hit@3=Y hit@5=Y RR@10=1.00 · coverage = 3/3 (100%) · top-1 = §6.3.4.3 p570 table=-
    #1 sec=6.3.4.3 page=570 table=- score=0.325
    #2 sec=6.3.4.1 page=567 table=- score=0.341
    #3 sec=6.3.4.2 page=567 table=- score=0.341
    #4 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.356
    #5 sec=6.3.4.4 page=587 table=- score=0.375

**hybrid** — hit@1=N hit@3=Y hit@5=Y RR@10=0.50 · coverage = 3/3 (100%) · top-1 = §6.3.4.1 p567 table=-
    #1 sec=6.3.4.1 page=567 table=- score=0.033
    #2 sec=6.3.4.3 page=570 table=- score=0.032
    #3 sec=6.3.4.2 page=567 table=- score=0.032
    #4 sec=6.3.4.4 page=587 table=- score=0.031
    #5 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.030
