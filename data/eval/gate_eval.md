# Evidence Gate

_backend = hybrid; mode = balanced; source_format = tspec_md; 30 answerable + 12 out-of-scope; REFUSE = positive class_

## Confusion matrix

| | gate REFUSE | gate ANSWER |
|---|---|---|
| out_of_scope (should refuse) | 3 (TP) | 9 (FN) |
| answerable (should answer) | 1 (FP) | 29 (TN) |

refusal precision = 75% · refusal recall = 25% · F1 = 0.38

## Acceptance

- out-of-scope refusal correctness (recall) = 25% (3/12 OOS refused)
- citation accuracy = 45% (FAIL vs >= 90%)
- mean coverage (answered) = 71% (PASS vs >= 70%)

## Out-of-scope refusal by kind

| oos_kind | n | refused | refusal rate |
|---|---|---|---|
| hard | 8 | 3 | 38% |
| scope_boundary | 4 | 0 | 0% |

## Gate detail

- **q01** [answerable] [TN] answer (conf 0.79) — evidence 0.793 >= answer_floor 0.650
- **q02** [answerable] [TN] answer (conf 0.74) — evidence 0.741 >= answer_floor 0.650
- **q03** [answerable] [TN] answer (conf 0.87) — evidence 0.870 >= answer_floor 0.650
- **q04** [answerable] [TN] answer (conf 0.68) — evidence 0.676 >= answer_floor 0.650
- **q05** [answerable] [TN] answer (conf 0.85) — evidence 0.852 >= answer_floor 0.650
- **q06** [answerable] [TN] answer (conf 0.89) — evidence 0.893 >= answer_floor 0.650
- **q07** [answerable] [TN] answer (conf 0.86) — evidence 0.857 >= answer_floor 0.650
- **q08** [answerable] [TN] answer (conf 0.75) — evidence 0.750 >= answer_floor 0.650
- **q09** [answerable] [FP] refuse (conf 0.59) — evidence 0.413 < low_floor 0.500
- **q10** [answerable] [TN] answer (conf 0.83) — evidence 0.833 >= answer_floor 0.650
- **q11** [answerable] [TN] answer (conf 0.86) — evidence 0.861 >= answer_floor 0.650
- **q12** [answerable] [TN] answer (conf 0.78) — evidence 0.779 >= answer_floor 0.650
- **q13** [answerable] [TN] answer (conf 0.86) — evidence 0.856 >= answer_floor 0.650
- **q14** [answerable] [TN] answer (conf 0.92) — evidence 0.919 >= answer_floor 0.650
- **q15** [answerable] [TN] low_confidence (conf 0.62) — evidence 0.620 in [0.500, 0.650)
- **q16** [answerable] [TN] answer (conf 0.83) — evidence 0.829 >= answer_floor 0.650
- **q17** [answerable] [TN] answer (conf 0.71) — evidence 0.707 >= answer_floor 0.650
- **q18** [answerable] [TN] answer (conf 0.92) — evidence 0.917 >= answer_floor 0.650
- **q19** [answerable] [TN] answer (conf 0.75) — evidence 0.749 >= answer_floor 0.650
- **q20** [answerable] [TN] answer (conf 0.87) — evidence 0.874 >= answer_floor 0.650
- **q21** [answerable] [TN] answer (conf 0.87) — evidence 0.872 >= answer_floor 0.650
- **q22** [answerable] [TN] answer (conf 0.78) — evidence 0.785 >= answer_floor 0.650
- **q23** [answerable] [TN] answer (conf 0.90) — evidence 0.899 >= answer_floor 0.650
- **q24** [answerable] [TN] answer (conf 0.82) — evidence 0.817 >= answer_floor 0.650
- **q25** [answerable] [TN] answer (conf 0.87) — evidence 0.873 >= answer_floor 0.650
- **q26** [answerable] [TN] answer (conf 0.67) — evidence 0.670 >= answer_floor 0.650
- **q27** [answerable] [TN] answer (conf 0.74) — evidence 0.744 >= answer_floor 0.650
- **q28** [answerable] [TN] answer (conf 0.75) — evidence 0.752 >= answer_floor 0.650
- **q29** [answerable] [TN] answer (conf 0.67) — evidence 0.673 >= answer_floor 0.650
- **q30** [answerable] [TN] answer (conf 0.78) — evidence 0.784 >= answer_floor 0.650
- **q31** [out_of_scope/hard] [FN] answer (conf 0.71) — evidence 0.707 >= answer_floor 0.650
- **q32** [out_of_scope/hard] [FN] low_confidence (conf 0.59) — evidence 0.593 in [0.500, 0.650)
- **q33** [out_of_scope/hard] [TP] refuse (conf 0.52) — evidence 0.482 < low_floor 0.500
- **q34** [out_of_scope/hard] [TP] refuse (conf 0.58) — evidence 0.419 < low_floor 0.500
- **q35** [out_of_scope/hard] [FN] low_confidence (conf 0.54) — evidence 0.536 in [0.500, 0.650)
- **q36** [out_of_scope/hard] [FN] low_confidence (conf 0.54) — evidence 0.539 in [0.500, 0.650)
- **q37** [out_of_scope/hard] [TP] refuse (conf 0.60) — evidence 0.396 < low_floor 0.500
- **q38** [out_of_scope/hard] [FN] answer (conf 0.69) — evidence 0.688 >= answer_floor 0.650
- **q39** [out_of_scope/scope_boundary] [FN] low_confidence (conf 0.65) — evidence 0.649 in [0.500, 0.650)
- **q40** [out_of_scope/scope_boundary] [FN] answer (conf 0.74) — evidence 0.739 >= answer_floor 0.650
- **q41** [out_of_scope/scope_boundary] [FN] answer (conf 0.72) — evidence 0.721 >= answer_floor 0.650
- **q42** [out_of_scope/scope_boundary] [FN] answer (conf 0.83) — evidence 0.828 >= answer_floor 0.650
