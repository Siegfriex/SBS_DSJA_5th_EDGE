# P4 Cleaning Final Report

## Final Status

`P4_CLEANING_READY_WITH_WARNINGS`

## Sample Registry

| sample_id | status | total_n | school_n | train_n | validation_n | test_n |
| --- | --- | --- | --- | --- | --- | --- |
| GRADE_ALL | READY | 10099 | 200 | 7417 | 1504 | 1178 |
| GRADE_SELECTIVITY | READY | 3707 | 151 | 2760 | 585 | 362 |
| EMPLOYMENT_HEALTH | READY | 7389 | 188 | 5428 | 1121 | 840 |
| PROGRESSION_GRADSCHOOL | READY | 7498 | 197 | 5499 | 1141 | 858 |
| JOINT_EMP_PROG | READY | 7389 | 188 | 5428 | 1121 | 840 |
| GRADE_STRUCTURE | READY | 8561 | 198 | 6302 | 1263 | 996 |
| GRADE_SELECTIVITY_STRUCTURE | READY | 3198 | 146 | 2355 | 522 | 321 |
| JOINT_EMP_PROG_STRUCTURE | READY | 6270 | 186 | 4623 | 932 | 715 |
| JOINT_EMP_PROG_SELECTIVITY | READY | 2805 | 138 | 2097 | 415 | 293 |
| P1_SIGNAL_ALIGNMENT_CORE | READY | 7389 | 188 | 5428 | 1121 | 840 |
| P1_SIGNAL_ALIGNMENT_SELECTIVITY | READY | 2805 | 138 | 2097 | 415 | 293 |
| P2_STRUCTURE_READY | READY | 8561 | 198 | 6302 | 1263 | 996 |
| P2_SELECTIVITY_READY | READY | 3198 | 146 | 2355 | 522 | 321 |
| P3_STRUCTURE_READY | READY | 8561 | 198 | 6302 | 1263 | 996 |
| P3_SELECTIVITY_READY | READY | 3198 | 146 | 2355 | 522 | 321 |
| P4_STRUCTURE_READY | READY | 6366 | 195 | 4687 | 949 | 730 |
| P4_SELECTIVITY_READY | READY | 2439 | 136 | 1805 | 372 | 262 |
| COUNT_RETENTION_READY | NOT_AVAILABLE | 0 | 0 | 0 | 0 | 0 |
| COUNT_PROGRESSION_READY | NOT_AVAILABLE | 0 | 0 | 0 | 0 | 0 |
| TYPE_READY | PENDING_P3_P4 | 0 | 0 | 0 | 0 | 0 |
| PANEL_READY | PENDING_2023_2025 | 0 | 0 | 0 | 0 | 0 |

## Leakage FAIL Reclassification

| class | n |
| --- | --- |
| INTENDED_EXCLUSION | 14 |
| REGISTRY_MISCLASSIFICATION | 2 |

## Count Readiness

| readiness_id | status | usable_n | reason |
| --- | --- | --- | --- |
| GRADE_COUNT_READY | NOT_AVAILABLE | 0 | No source numerator/denominator pair is present in D08/D01/D02/D03/source registry. |
| EMPLOYMENT_COUNT_READY | NOT_AVAILABLE | 0 | No source numerator/denominator pair is present in D08/D01/D02/D03/source registry. |
| RETENTION_1_COUNT_READY | NOT_AVAILABLE | 0 | No source numerator/denominator pair is present in D08/D01/D02/D03/source registry. |
| RETENTION_2_COUNT_READY | NOT_AVAILABLE | 0 | No source numerator/denominator pair is present in D08/D01/D02/D03/source registry. |
| RETENTION_3_COUNT_READY | NOT_AVAILABLE | 0 | No source numerator/denominator pair is present in D08/D01/D02/D03/source registry. |
| RETENTION_4_COUNT_READY | NOT_AVAILABLE | 0 | No source numerator/denominator pair is present in D08/D01/D02/D03/source registry. |
| PROGRESSION_COUNT_READY | NOT_AVAILABLE | 0 | No source numerator/denominator pair is present in D08/D01/D02/D03/source registry. |
| P4_2024_RATE_MODEL_READY | READY | 10242 | Stored 2024 rate targets/signals are available; count binomial readiness is independent. |
| P4_COUNT_BINOMIAL_READY | NOT_AVAILABLE | 0 | Count numerator/denominator pairs are not in active handoff. |
