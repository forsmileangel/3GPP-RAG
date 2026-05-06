# Week 2 Retrieval Benchmark

_top_k = 5; backends = sparse, dense_

## Aggregate

| backend | hit@K | mean coverage |
|---|---|---|
| sparse | 10/10 | 92% |
| dense | 10/10 | 82% |

## q01 — What is the maximum output power tolerance for FR1 PC3 UE?
_expected_section = §6.2.1 · type = numeric · difficulty = easy_

**sparse** — HIT · coverage = 3/3 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=-12.033
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=-10.144
    #3 sec=6.2.1 page=92 table=- score=-9.732
    #4 sec=6.2.3 page=222 table=- score=-9.621
    #5 sec=6.2.1 page=95 table=- score=-9.556

**dense** — HIT · coverage = 3/3 (100%) · top-1 = §6.2.4 p273 table=-
    #1 sec=6.2.4 page=273 table=- score=0.332
    #2 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.334
    #3 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.347
    #4 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.353
    #5 sec=6.2.1 page=96 table=6.2.1.5-1 score=0.364

## q02 — How is the test procedure defined for UE maximum output power across power classes?
_expected_section = §6.2.1 · type = procedure · difficulty = medium_

**sparse** — HIT · coverage = 2/3 (67%) · top-1 = §6.2.1 p92 table=-
  missing keywords: ['pc3']
    #1 sec=6.2.1 page=92 table=- score=-15.284
    #2 sec=6.2.3 page=123 table=- score=-9.528
    #3 sec=6.3.1 page=541 table=- score=-9.517
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=-9.502
    #5 sec=6.2.2 page=98 table=- score=-9.396

**dense** — HIT · coverage = 1/3 (33%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
  missing keywords: ['test procedure', 'pc3']
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.294
    #2 sec=6.2.1 page=92 table=- score=0.314
    #3 sec=6.2.4 page=273 table=- score=0.316
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.319
    #5 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.331

## q03 — What are the test conditions and channel bandwidth for inner / outer maximum output power?
_expected_section = §6.2.1 · type = table_lookup · difficulty = medium_

**sparse** — HIT · coverage = 3/3 (100%) · top-1 = §6.2.2 p99 table=6.2.2.3-5
    #1 sec=6.2.2 page=99 table=6.2.2.3-5 score=-17.068
    #2 sec=6.2.1 page=94 table=6.2.1.4.1-1 score=-14.296
    #3 sec=6.3.1 page=541 table=- score=-12.264
    #4 sec=6.2.3 page=123 table=- score=-12.097
    #5 sec=6.2.3 page=135 table=6.2.3.3.8-1 score=-11.369

**dense** — HIT · coverage = 1/3 (33%) · top-1 = §6.2.1 p97 table=6.2.1.5-2
  missing keywords: ['inner', 'outer']
    #1 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.332
    #2 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=0.341
    #3 sec=6.2.4 page=273 table=- score=0.341
    #4 sec=6.2.4 page=278 table=6.2.4.5-1 score=0.343
    #5 sec=6.2.1 page=97 table=6.2.1.5-3 score=0.345

## q04 — Define UE output power dynamics — minimum output power requirement.
_expected_section = §6.3.1 · type = numeric · difficulty = easy_

**sparse** — HIT · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=-22.816
    #2 sec=6.2.1 page=92 table=- score=-18.922
    #3 sec=6.3.4.1 page=567 table=- score=-14.262
    #4 sec=6.3.4.2 page=567 table=- score=-14.262
    #5 sec=6.3.4.4 page=587 table=- score=-13.331

**dense** — HIT · coverage = 1/1 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.252
    #2 sec=6.3.4.3 page=570 table=- score=0.351
    #3 sec=6.3.4.4 page=587 table=- score=0.356
    #4 sec=6.3.4.4 page=590 table=- score=0.363
    #5 sec=6.3.1 page=541 table=6.2I.4.5-1 score=0.376

## q05 — What is the transmit OFF power requirement for NR FR1 UE?
_expected_section = §6.3.2 · type = numeric · difficulty = easy_

**sparse** — HIT · coverage = 2/2 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=-14.803
    #2 sec=6.3.3.1 page=545 table=- score=-13.521
    #3 sec=6.3.3.2 page=545 table=- score=-13.134
    #4 sec=6.3.3.6 page=557 table=- score=-13.111
    #5 sec=6.3.2 page=544 table=- score=-11.536

**dense** — HIT · coverage = 2/2 (100%) · top-1 = §6.2.3 p123 table=-
    #1 sec=6.2.3 page=123 table=- score=0.367
    #2 sec=6.2.1 page=97 table=6.2.1.5-2 score=0.367
    #3 sec=6.3.2 page=544 table=- score=0.374
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.378
    #5 sec=6.3.4.3 page=570 table=- score=0.383

## q06 — What are the absolute and relative power tolerance requirements?
_expected_section = §6.3.4 · type = section_summary · difficulty = medium_

**sparse** — HIT · coverage = 2/2 (100%) · top-1 = §6.3.4.3 p576 table=-
    #1 sec=6.3.4.3 page=576 table=- score=-11.708
    #2 sec=6.3.4.3 page=570 table=- score=-11.376
    #3 sec=6.3.4.1 page=567 table=- score=-10.699
    #4 sec=6.3.4.2 page=567 table=- score=-10.699
    #5 sec=6.3.4.2 page=569 table=6.3.4.2.5-1 score=-8.972

**dense** — HIT · coverage = 2/2 (100%) · top-1 = §6.3.4.1 p567 table=6.3.4.2.3-1
    #1 sec=6.3.4.1 page=567 table=6.3.4.2.3-1 score=0.307
    #2 sec=6.3.4.2 page=567 table=6.3.4.2.3-1 score=0.307
    #3 sec=6.3.4.3 page=570 table=6.3.4.3.3-1 score=0.333
    #4 sec=6.3.4.1 page=567 table=- score=0.341
    #5 sec=6.3.4.2 page=567 table=- score=0.341

## q07 — What is the configured transmitted power for UE in NR?
_expected_section = §6.2.4 · type = section_summary · difficulty = medium_

**sparse** — HIT · coverage = 1/1 (100%) · top-1 = §6.2.4 p279 table=6.2.4.5-2
    #1 sec=6.2.4 page=279 table=6.2.4.5-2 score=-13.080
    #2 sec=6.2.4 page=273 table=- score=-12.524
    #3 sec=6.2.4 page=274 table=- score=-12.465
    #4 sec=6.2.1 page=93 table=6.2.1.3-1 score=-12.283
    #5 sec=6.3.1 page=541 table=6.2I.4.5-0 score=-11.728

**dense** — HIT · coverage = 1/1 (100%) · top-1 = §6.2.1 p93 table=6.2.1.3-1
    #1 sec=6.2.1 page=93 table=6.2.1.3-1 score=0.379
    #2 sec=6.2.3 page=123 table=- score=0.389
    #3 sec=6.3.4.3 page=570 table=- score=0.391
    #4 sec=6.2.4 page=273 table=- score=0.391
    #5 sec=6.2.3 page=123 table=- score=0.392

## q08 — How are additional MPR (A-MPR) requirements defined for NR FR1?
_expected_section = §6.2.3 · type = procedure · difficulty = medium_

**sparse** — HIT · coverage = 1/2 (50%) · top-1 = §6.2.3 p123 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2.3 page=123 table=- score=-12.766
    #2 sec=6.3.3.2 page=546 table=- score=-10.336
    #3 sec=6.2.3 page=123 table=- score=-10.329
    #4 sec=6.2.4 page=274 table=- score=-10.233
    #5 sec=6.2.2 page=98 table=- score=-9.821

**dense** — HIT · coverage = 1/2 (50%) · top-1 = §6.2.3 p123 table=-
  missing keywords: ['additional mpr']
    #1 sec=6.2.3 page=123 table=- score=0.361
    #2 sec=6.2.3 page=127 table=6.2.3.3.1-2 score=0.378
    #3 sec=6.2.3 page=123 table=6.2.3.3.1-1 score=0.398
    #4 sec=6.2.3 page=137 table=6.2.3.3.11-1 score=0.406
    #5 sec=6.2.3 page=129 table=- score=0.409

## q09 — What is the test purpose for the minimum output power conformance test?
_expected_section = §6.3.1 · type = section_summary · difficulty = easy_

**sparse** — HIT · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=-16.958
    #2 sec=6.3.4.1 page=567 table=- score=-14.910
    #3 sec=6.3.4.2 page=567 table=- score=-14.910
    #4 sec=6.3.4.4 page=587 table=- score=-14.591
    #5 sec=6.3.4.3 page=570 table=- score=-14.575

**dense** — HIT · coverage = 2/2 (100%) · top-1 = §6.3.1 p541 table=-
    #1 sec=6.3.1 page=541 table=- score=0.348
    #2 sec=6.3.4.4 page=587 table=- score=0.360
    #3 sec=6.3.4.1 page=567 table=- score=0.371
    #4 sec=6.3.4.2 page=567 table=- score=0.371
    #5 sec=6.3.4.3 page=570 table=- score=0.371

## q10 — Why does excess Transmit OFF power matter for cell coverage?
_expected_section = §6.3.2 · type = section_summary · difficulty = hard_

**sparse** — HIT · coverage = 3/3 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=-24.756
    #2 sec=6.2.1 page=92 table=- score=-17.183
    #3 sec=6.3.3.1 page=545 table=- score=-10.813
    #4 sec=6.3.3.2 page=545 table=- score=-10.640
    #5 sec=6.3.3.2 page=546 table=6.3.3.2.4.1-1 score=-9.895

**dense** — HIT · coverage = 3/3 (100%) · top-1 = §6.3.2 p544 table=-
    #1 sec=6.3.2 page=544 table=- score=0.334
    #2 sec=6.3.3.1 page=545 table=- score=0.411
    #3 sec=6.3.3.2 page=545 table=- score=0.413
    #4 sec=6.3.3.3 page=550 table=6.3.3.2.5-1 score=0.422
    #5 sec=6.3.3.4 page=550 table=6.3.3.2.5-1 score=0.422
