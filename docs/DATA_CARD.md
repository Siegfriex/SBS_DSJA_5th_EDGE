# Data Card

## Dataset Shapes

| dataset | row_count | column_count | sha256 |
| --- | --- | --- | --- |
| D01 | 34969 | 186 | 2f187b5af44c828d4107af12368029caf6b83b6254af75b9653b6402b8f1b0ce |
| D02 | 10242 | 37 | 45f8aa40f31e14b83b5d97f594abf89bb4a5aaa4bc67735767e19077d189f493 |
| D03 | 10242 | 108 | c6fd569052684502e5bab5758510d3cd945f68ddeaa47fdfb3e9bab803889dca |
| D04 | 14 | 87 | 489caf15edbefa1ed0c30fdfa98dbe31096b36c219f6610dae69a2d5e49c47e5 |
| D05 | 24 | 32 | f4447cf519bdf366e36851a68e6ec6b6605f9c9a591d96c911de4eece2327246 |
| D06 | 91 | 45 | 75d8bc34a0bf092c3e2c4332fd213d4a01f5a86252b6f6b4ac6f29709b3202c3 |
| D07 | 7 | 29 | f44c6f9e7a7539361dce301686144780e0ce588deb929b625ebe811674bb621f |
| D08 | 10242 | 151 | 598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962 |

## Final Mart

- 파일: `workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet`
- shape: `10,242 x 151`
- sha256: `598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962`
- key: `outcome_row_id`
- 학교 수: 200

## P4 Sample Registry

| sample_id | actual_n | registry_n | actual_train_n | actual_val_n | actual_test_n | status |
| --- | --- | --- | --- | --- | --- | --- |
| GRADE_ALL | 10099 | 10099 | 7417 | 1504 | 1178 | PASS |
| GRADE_SELECTIVITY | 3707 | 3707 | 2760 | 585 | 362 | PASS |
| EMPLOYMENT_HEALTH | 7389 | 7389 | 5428 | 1121 | 840 | PASS |
| PROGRESSION_GRADSCHOOL | 7498 | 7498 | 5499 | 1141 | 858 | PASS |
| JOINT_EMP_PROG | 7389 | 7389 | 5428 | 1121 | 840 | PASS |

## Known Boundaries

- `manual_pending` 및 `unmatched` 구조 row는 삭제하지 않고 sample mask에서 제외/보존한다.
- GOMS는 계열별 context라서 학과 고유 성과로 해석하면 안 된다.
- 공개 포트폴리오에는 full parquet와 raw CSV를 올리지 않는다.
