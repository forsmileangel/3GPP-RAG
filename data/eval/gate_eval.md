# Evidence Gate

_backend = hybrid; mode = balanced; source_format = tspec_md; 30 answerable + 12 out-of-scope; REFUSE = positive class_

## Confusion matrix

| | gate REFUSE | gate ANSWER |
|---|---|---|
| out_of_scope (should refuse) | 2 (TP) | 10 (FN) |
| answerable (should answer) | 0 (FP) | 30 (TN) |

refusal precision = 100% · refusal recall = 17% · F1 = 0.29

## Acceptance

- out-of-scope refusal correctness (recall) = 17% (2/12 OOS refused)
- citation accuracy = 87% (FAIL vs >= 90%)
- mean coverage (answered) = 79% (PASS vs >= 70%)

## Out-of-scope refusal by kind

| oos_kind | n | refused | refusal rate |
|---|---|---|---|
| hard | 8 | 2 | 25% |
| scope_boundary | 4 | 0 | 0% |

## Gate detail

- **q01** [answerable] [TN] answer (conf 0.70) — evidence 0.704 >= answer_floor 0.650
- **q02** [answerable] [TN] answer (conf 0.79) — evidence 0.785 >= answer_floor 0.650
- **q03** [answerable] [TN] answer (conf 0.92) — evidence 0.916 >= answer_floor 0.650
- **q04** [answerable] [TN] answer (conf 0.68) — evidence 0.679 >= answer_floor 0.650
- **q05** [answerable] [TN] answer (conf 0.91) — evidence 0.911 >= answer_floor 0.650
- **q06** [answerable] [TN] answer (conf 0.99) — evidence 0.994 >= answer_floor 0.650
- **q07** [answerable] [TN] answer (conf 0.96) — evidence 0.956 >= answer_floor 0.650
- **q08** [answerable] [TN] answer (conf 0.96) — evidence 0.957 >= answer_floor 0.650
- **q09** [answerable] [TN] answer (conf 0.72) — evidence 0.716 >= answer_floor 0.650
- **q10** [answerable] [TN] answer (conf 0.83) — evidence 0.833 >= answer_floor 0.650
- **q11** [answerable] [TN] answer (conf 0.95) — evidence 0.951 >= answer_floor 0.650
- **q12** [answerable] [TN] answer (conf 0.86) — evidence 0.859 >= answer_floor 0.650
- **q13** [answerable] [TN] answer (conf 0.70) — evidence 0.704 >= answer_floor 0.650
- **q14** [answerable] [TN] answer (conf 1.00) — evidence 0.997 >= answer_floor 0.650
- **q15** [answerable] [TN] answer (conf 0.70) — evidence 0.704 >= answer_floor 0.650
- **q16** [answerable] [TN] answer (conf 0.87) — evidence 0.869 >= answer_floor 0.650
- **q17** [answerable] [TN] answer (conf 0.87) — evidence 0.870 >= answer_floor 0.650
- **q18** [answerable] [TN] answer (conf 1.00) — evidence 0.997 >= answer_floor 0.650
- **q19** [answerable] [TN] answer (conf 0.80) — evidence 0.803 >= answer_floor 0.650
- **q20** [answerable] [TN] answer (conf 0.96) — evidence 0.957 >= answer_floor 0.650
- **q21** [answerable] [TN] answer (conf 0.92) — evidence 0.917 >= answer_floor 0.650
- **q22** [answerable] [TN] answer (conf 0.96) — evidence 0.957 >= answer_floor 0.650
- **q23** [answerable] [TN] answer (conf 0.94) — evidence 0.939 >= answer_floor 0.650
- **q24** [answerable] [TN] answer (conf 0.92) — evidence 0.917 >= answer_floor 0.650
- **q25** [answerable] [TN] answer (conf 0.91) — evidence 0.908 >= answer_floor 0.650
- **q26** [answerable] [TN] answer (conf 0.75) — evidence 0.751 >= answer_floor 0.650
- **q27** [answerable] [TN] answer (conf 0.78) — evidence 0.784 >= answer_floor 0.650
- **q28** [answerable] [TN] answer (conf 0.88) — evidence 0.877 >= answer_floor 0.650
- **q29** [answerable] [TN] answer (conf 0.76) — evidence 0.759 >= answer_floor 0.650
- **q30** [answerable] [TN] answer (conf 0.91) — evidence 0.911 >= answer_floor 0.650
- **q31** [out_of_scope/hard] [FN] answer (conf 0.83) — evidence 0.830 >= answer_floor 0.650
- **q32** [out_of_scope/hard] [FN] low_confidence (conf 0.65) — evidence 0.648 in [0.500, 0.650)
- **q33** [out_of_scope/hard] [FN] low_confidence (conf 0.52) — evidence 0.518 in [0.500, 0.650)
- **q34** [out_of_scope/hard] [TP] refuse (conf 0.51) — evidence 0.489 < low_floor 0.500
- **q35** [out_of_scope/hard] [FN] low_confidence (conf 0.62) — evidence 0.617 in [0.500, 0.650)
- **q36** [out_of_scope/hard] [FN] low_confidence (conf 0.62) — evidence 0.617 in [0.500, 0.650)
- **q37** [out_of_scope/hard] [TP] refuse (conf 0.73) — evidence 0.265 < low_floor 0.500
- **q38** [out_of_scope/hard] [FN] low_confidence (conf 0.61) — evidence 0.611 in [0.500, 0.650)
- **q39** [out_of_scope/scope_boundary] [FN] answer (conf 0.81) — evidence 0.807 >= answer_floor 0.650
- **q40** [out_of_scope/scope_boundary] [FN] answer (conf 0.77) — evidence 0.774 >= answer_floor 0.650
- **q41** [out_of_scope/scope_boundary] [FN] answer (conf 0.72) — evidence 0.716 >= answer_floor 0.650
- **q42** [out_of_scope/scope_boundary] [FN] answer (conf 0.74) — evidence 0.740 >= answer_floor 0.650
