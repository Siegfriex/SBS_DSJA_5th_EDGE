# HANDOFF TO CHATGPT

## A. 실행 정보

- run_id: `20260713T044343Z_5b1a3d5`
- commit: `5b1a3d54266d881a839ad9a3cec750da66e94bc7`
- notebook path/hash: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_4/p4_modeling_readiness_v4/p2_G4_dataset_cell_inspection.ipynb` / `cf980e2962e6906853d49cf71c46d6062e07be897d23a72f01070f0e6bcc790b`
- input data path/hash: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet` / `598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962`
- execution_seconds: `5.769`
- final_status: `READY_WITH_WARNINGS`

## B. 핵심 데이터 개수

- base shape: `10242 x 184`
- unique schools/campuses/departments: `200 / 452 / 10222`

### sample counts

| sample_id | actual_row_n | actual_school_n | train_n | validation_n | test_n |
| --- | --- | --- | --- | --- | --- |
| P1_STRUCTURE_READY | 6270 | 186 | 4623 | 932 | 715 |
| P1_SELECTIVITY_READY | 2416 | 130 | 1789 | 367 | 260 |
| P2_STRUCTURE_READY | 8561 | 198 | 6302 | 1263 | 996 |
| P2_SELECTIVITY_READY | 3198 | 146 | 2355 | 522 | 321 |
| P3_STRUCTURE_READY | 8561 | 198 | 6302 | 1263 | 996 |
| P3_SELECTIVITY_READY | 3198 | 146 | 2355 | 522 | 321 |
| P4_E_STRUCTURE_READY | 6270 | 186 | 4623 | 932 | 715 |
| P4_P_STRUCTURE_READY | 6366 | 195 | 4687 | 949 | 730 |
| P4_JOINT_STRUCTURE_READY | 6270 | 186 | 4623 | 932 | 715 |
| P4_E_SELECTIVITY_READY | 2416 | 130 | 1789 | 367 | 260 |
| P4_P_SELECTIVITY_READY | 2439 | 136 | 1805 | 372 | 262 |
| P4_JOINT_SELECTIVITY_READY | 2416 | 130 | 1789 | 367 | 260 |

### split counts

| split | row_n |
| --- | --- |
| train | 7529 |
| val | 1514 |
| test | 1199 |

### target non-null counts

| target | non_null_n | missing_n |
| --- | --- | --- |
| a_rate_pct | 10242 | 0 |
| health_employment_rate_pct | 7477 | 2765 |
| graduate_school_progression_rate_pct | 7587 | 2655 |

- major7 coverage: `10099 / 10242`
- count-ready grade/retention/progression: `not_observed / not_observed / not_observed`

## C. Gate 결과

| Gate | PASS/WARN/FAIL | 핵심 수치 | 산출 파일 |
|---|---|---:|---|
| Gate 0 inventory | PASS | 0 required fail | qa/dataset_inventory.csv |
| Gate 1 key/grain | PASS | 0 key dup | qa/key_grain_audit.csv |
| Gate 2 join | PASS | 0 unapproved m:m | qa/join_cardinality_audit.csv |
| Gate 3 schema | PASS | 164 columns | qa/column_schema_profile.csv |
| Gate 4 missingness | WARN | selectivity missing 6505 | qa/missingness_profile.csv |
| Gate 5 domain/range | PASS | 0 fail anomalies | qa/domain_range_audit.csv |
| Gate 6 count/rate | WARN | 3 count families not observed | qa/count_denominator_audit.csv |
| Gate 7 major7 | WARN | 1 warnings | qa/major7_mapping_audit.csv |
| Gate 8 sample/split | PASS | 0 sample mismatch, 0 school overlap | qa/sample_membership_audit.csv |
| Gate 9 feature roles | PASS | 0 target self leakage | qa/feature_role_leakage_audit.csv |

## D. 발견된 문제

| issue_id | severity | affected rows | evidence file | preprocessing impact | required decision |
|---|---|---:|---|---|---|
| WARN_COUNT_NOT_OBSERVED | WARN | 10242 | qa/count_denominator_audit.csv | count-binomial marts not created | obtain numerator/denominator source or keep rate-only |
| WARN_DUPLICATE_CONFLICT_LEDGERED | WARN | 36 | qa/duplicate_conflict_audit.csv | rows ledgered; primary conflict exclusions preserved | reviewer may inspect excluded_rows.parquet |
| WARN_SELECTIVITY_MISSING | WARN | 6505 | qa/missingness_profile.csv | selectivity branch sample smaller | no imputation here; fold-local later |

## E. 생성 데이터

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/clean_department_model_base_2024.parquet`
  - shape: `(10242, 184)`
  - SHA256: `dc4d320a44c2e6a109e4da58c8ee3aefaf98572e99d53f13daa804a8f2ca79a2`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `analysis_year, outcome_row_id, school_name_raw, school_name_base_raw, school_name_std, campus_name_raw_x, campus_seq, campus_branch, campus_name_std_x, dept_name_raw, dept_name_std, dept_field_raw`
  - 사용 가능 단계: preprocessing/integrity review

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/count_integrity_anomaly_rows.parquet`
  - shape: `(0, 5)`
  - SHA256: `caf0c44e480d79f404f8f46cb51c93366dec95bf7b9e0058bb93b1aaec5bfc5b`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `outcome_row_id, family, issue, severity, detail`
  - 사용 가능 단계: preprocessing/integrity review

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/count_ready_rows.parquet`
  - shape: `(10242, 7)`
  - SHA256: `64781788884788a7ed750265e7e1387a4dd3db8828b0ab7fb52862bb8b8a686b`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `outcome_row_id, GRADE_COUNT_READY, RETENTION_COUNT_READY, PROGRESSION_COUNT_READY, COUNT_RELATION_VALID, RATE_RECONCILED, DENOMINATOR_VALID`
  - 사용 가능 단계: preprocessing/integrity review

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/domain_anomaly_rows.parquet`
  - shape: `(5043, 8)`
  - SHA256: `2239b56373eaf0b5a892d9d878115b4c3f441e288179904bed0c0cb4c076fba4`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `outcome_row_id, column, observed_value, rule_id, severity, reason, source_dataset, recommended_action`
  - 사용 가능 단계: preprocessing/integrity review

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/dtype_coercion_review_rows.parquet`
  - shape: `(0, 3)`
  - SHA256: `42e9e10b7ceb9ee8797dfdd1af5ca6114c0e6279a68e58c65b444372a4950cfa`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `outcome_row_id, column, raw_value`
  - 사용 가능 단계: preprocessing/integrity review

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/duplicate_conflict_rows.parquet`
  - shape: `(64, 22)`
  - SHA256: `3b20f608668606841a31fc1053d51bda630ab966621b9cf672ef8c850775f7d5`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `outcome_row_id, analysis_year, school_uid, school_name_std, campus_uid, campus_branch, dept_uid, dept_name_std, degree_course, headcount_grain_uid, match_method, match_score`
  - 사용 가능 단계: preprocessing/integrity review

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/excluded_rows.parquet`
  - shape: `(8, 5)`
  - SHA256: `a857d4301ba2fcf1f15655a059b61f6a7396517a794ce6824a49e252ddd038e7`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `outcome_row_id, school_name_std, dept_name_std, integrity_exclusion_reason, exclusion_rule_id`
  - 사용 가능 단계: preprocessing/integrity review

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/join_review_rows.parquet`
  - shape: `(1681, 7)`
  - SHA256: `48a165efb4f8c8d25c41029dae8ff40b2247e4c52766a15a5344e9e25ba02ff3`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `outcome_row_id, school_name_std, dept_name_std, match_method, match_score, candidate_count, review_reason`
  - 사용 가능 단계: preprocessing/integrity review

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/p2_selectivity_ready_2024.parquet`
  - shape: `(3198, 184)`
  - SHA256: `a61f5fc9f6306cc310b09bd3fb4d292337f13b820ea0d028ac79aae3b8f38f96`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `analysis_year, outcome_row_id, school_name_raw, school_name_base_raw, school_name_std, campus_name_raw_x, campus_seq, campus_branch, campus_name_std_x, dept_name_raw, dept_name_std, dept_field_raw`
  - 사용 가능 단계: preprocessing/integrity review

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/p2_structure_ready_2024.parquet`
  - shape: `(8561, 184)`
  - SHA256: `1dc4ce02999478f2ab5a10f2290e3bbd9148ea7986fcd3b5eed6d36029627baf`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `analysis_year, outcome_row_id, school_name_raw, school_name_base_raw, school_name_std, campus_name_raw_x, campus_seq, campus_branch, campus_name_std_x, dept_name_raw, dept_name_std, dept_field_raw`
  - 사용 가능 단계: preprocessing/integrity review

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/p4_employment_rate_ready_2024.parquet`
  - shape: `(6270, 184)`
  - SHA256: `9b543685c62eb212d78271fdd34725ea34d0d6ee383a96c60b0734d0b3ec2d5a`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `analysis_year, outcome_row_id, school_name_raw, school_name_base_raw, school_name_std, campus_name_raw_x, campus_seq, campus_branch, campus_name_std_x, dept_name_raw, dept_name_std, dept_field_raw`
  - 사용 가능 단계: preprocessing/integrity review

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/p4_joint_rate_ready_2024.parquet`
  - shape: `(6270, 184)`
  - SHA256: `9b543685c62eb212d78271fdd34725ea34d0d6ee383a96c60b0734d0b3ec2d5a`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `analysis_year, outcome_row_id, school_name_raw, school_name_base_raw, school_name_std, campus_name_raw_x, campus_seq, campus_branch, campus_name_std_x, dept_name_raw, dept_name_std, dept_field_raw`
  - 사용 가능 단계: preprocessing/integrity review

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/p4_progression_rate_ready_2024.parquet`
  - shape: `(6366, 184)`
  - SHA256: `6760bc705cb17b1873d42ae78bddbed9a9267290a7da54cde1b38b2ea5186a22`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `analysis_year, outcome_row_id, school_name_raw, school_name_base_raw, school_name_std, campus_name_raw_x, campus_seq, campus_branch, campus_name_std_x, dept_name_raw, dept_name_std, dept_field_raw`
  - 사용 가능 단계: preprocessing/integrity review

- `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/row_lineage.parquet`
  - shape: `(10242, 10)`
  - SHA256: `9e5589586932ce8bdc72ec395144ea3386d4ef0784079d6283f7704abd4a1113`
  - grain: `outcome_row_id` or row-level lineage depending on file
  - inclusion rule: see manifest/clean_mart_output_status.json
  - 주요 컬럼: `output_row_id, source_dataset, source_row_id, source_row_hash, join_method, join_key, conflict_group_id, inclusion_status, exclusion_rule_id, transformation_rule_ids`
  - 사용 가능 단계: preprocessing/integrity review

## F. 최종 전처리 계약

- 변환 완료 항목: deterministic proportions, recomputed log checks, integrity flags, lineage hash, sample-ready mart slicing.
- 미수행 항목: imputation, scaling, one-hot encoding, model fitting, residual generation, bootstrap inference.
- 향후 fold 안에서 수행할 항목: train-only imputer/scaler/encoder fitting.
- 모델링 전에 해결해야 할 blocker: none if final_status is READY_WITH_WARNINGS; count models require external numerator/denominator data.

## G. 복사 가능한 최종 브리핑

```text
FINAL_STATUS: READY_WITH_WARNINGS
BASE_DATA: 10242 rows x 184 columns, sha256=598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962
GRAIN: outcome_row_id plus analysis_year + school_uid + campus_uid + dept_uid verified
KEY_DUPLICATE: outcome_row_id duplicate=0
JOIN_EXPANSION: unexplained=0
MISSINGNESS: selectivity missing=6505 / 10242
COUNT_READY: grade=not_observed, retention=not_observed, progression=not_observed
MAPPING: major7 non-null=10099 / 10242
SAMPLE_REGISTRY: mismatch=0
SPLIT_LEAKAGE: school_overlap=0
FEATURE_LEAKAGE: target_self=0, id_metadata=0
OUTPUT_DATA: data/clean_department_model_base_2024.parquet and phase-specific ready marts
BLOCKERS: no critical integrity blocker; count models require numerator/denominator source
```

## H. File Evidence Index

- mart_department_model_base_2024: shape=[10242, 151] sha256=598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962 status=PASS
- P4_PHASE_SAMPLE_MEMBERSHIP_FINAL: shape=[10242, 21] sha256=58d0308aa92f04badea3c7fc2db44fc28d0d93580db9bff4f16d47d870ebc7c6 status=PASS
- P4_PHASE_SAMPLE_REGISTRY_FINAL: shape=[12, 11] sha256=6483fdf67cca469ed7bd2500e5ef917ffd01007194c83461f5c827b03f16805e status=PASS
- department_model_column_registry_v4: shape=[151, 22] sha256=ab75225547d42ddc8e6cdf686be61ecc8bf87512729d8d9d053652b521093b94 status=PASS
- P4_PHASE_FEATURE_SET_FINAL: shape=[250, 11] sha256=dc851803d22a22e891a7fdd9a31dbe0c3d2ac56421a9798e06a9e87e20ce2320 status=PASS
- P4_PHASE_MODEL_SPEC_FINAL: shape=[18, 10] sha256=d7f560167ec752938b73dbee3c5f9dddc84fbc009d9eeaa3905b20946cc7dc48 status=PASS
- P4_DUPLICATE_CONFLICT_RESOLUTION: shape=[36, 14] sha256=24d2e000661b3e67a353877383c7ef68b8e156f52bd11ac22f4b1fd724be8d4f status=PASS
- P4_TARGET_PROFILE_BY_PHASE: shape=[396, 20] sha256=6f3fdb25676ccfdf59b0b2f458e5cdb5dd66dfb6f61e037b2e711418efffc25a status=PASS
- P4_FINAL_MODELING_READINESS: shape=[24, 2] sha256=8fcd0df2cee25f2b31ba498806ea5956e82e5da74580ce01573aa01c201ffbea status=PASS
- P4_MODELING_REVIEW_BUNDLE_MANIFEST: shape=[15, 9] sha256=9afa80278fcec363790fb844c056b78c623ac98f46a5556e0049aae24615da79 status=PASS
- P4_HANDOFF_MANIFEST: shape=[29, 2] sha256=b9ea9528b24630f15be8913012b40df81692d16e849120bb825f29ef35c01661 status=PASS
- dim_school_split: shape=[200, 6] sha256=85c2c851ddcfd02d5ead41dbd9424124e4ef1993347842c031e487e8f2a13583 status=PASS
- shared_model_sample_membership: shape=[10242, 17] sha256=ef7eb73a35e9a058959747272d1b1e832622c415adeb363754dcb0fcb507c830 status=PASS
- shared_model_sample_registry: shape=[5, 12] sha256=b3389c0051d9b9eeca555f43cd8194d99574c2444df68cd8273232f7f9a553f8 status=PASS
- shared_column_registry: shape=[198, 6] sha256=5871ec9ae36dd0e078eed403c67322784e3880d2fa82849671be45a6d252e126 status=PASS
- shared_feature_registry: shape=[4, 7] sha256=776c7072444b5abee02f9a20942ca24cff5ec5c684593299a2c8c43dbf7a6529 status=PASS
- shared_target_registry: shape=[6, 4] sha256=3e48aaea329c4df989af2e078635fd7d7cd1677d5afd6c99d5f106e6313b5247 status=PASS
- cleaning_derived_formula_reconstruction: shape=[8, 7] sha256=4c64021289618d58b469179e47f6a5b34946d5a0b16bb24d97975bb591e00be5 status=PASS
- cleaning_split_integrity_audit: shape=[6, 3] sha256=828c5dfcca39b7edf532a868d55077cf96057087e0c80337c01605613d103964 status=PASS
- cleaning_target_leakage_audit_by_phase: shape=[31, 11] sha256=460718776978168fb812a2a134dc7641d41077e31ba7451dbe9b1b4c4ea23939 status=PASS
- cleaning_count_denominator_inventory: shape=[72, 13] sha256=e5f98113264ea1d5cce968e3864651295b71a13e2e087804023e23c47af09ae4 status=PASS
- cleaning_context_grain_audit: shape=[43, 8] sha256=3aaabb7042202aa085bc22b12fed632749515365a46bc48eb30c491c96ce3cb2 status=PASS

## I. QA Output Evidence Index

- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/clean_department_model_base_2024.parquet`
  - shape: `[10242, 184]`
  - sha256: `dc4d320a44c2e6a109e4da58c8ee3aefaf98572e99d53f13daa804a8f2ca79a2`
  - size_bytes: `2953708`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/count_integrity_anomaly_rows.parquet`
  - shape: `[0, 5]`
  - sha256: `caf0c44e480d79f404f8f46cb51c93366dec95bf7b9e0058bb93b1aaec5bfc5b`
  - size_bytes: `2691`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/count_ready_rows.parquet`
  - shape: `[10242, 7]`
  - sha256: `64781788884788a7ed750265e7e1387a4dd3db8828b0ab7fb52862bb8b8a686b`
  - size_bytes: `74767`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/domain_anomaly_rows.parquet`
  - shape: `[5043, 8]`
  - sha256: `2239b56373eaf0b5a892d9d878115b4c3f441e288179904bed0c0cb4c076fba4`
  - size_bytes: `21410`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/dtype_coercion_review_rows.parquet`
  - shape: `[0, 3]`
  - sha256: `42e9e10b7ceb9ee8797dfdd1af5ca6114c0e6279a68e58c65b444372a4950cfa`
  - size_bytes: `1920`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/duplicate_conflict_rows.parquet`
  - shape: `[64, 22]`
  - sha256: `3b20f608668606841a31fc1053d51bda630ab966621b9cf672ef8c850775f7d5`
  - size_bytes: `15515`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/excluded_rows.parquet`
  - shape: `[8, 5]`
  - sha256: `a857d4301ba2fcf1f15655a059b61f6a7396517a794ce6824a49e252ddd038e7`
  - size_bytes: `4254`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/join_review_rows.parquet`
  - shape: `[1681, 7]`
  - sha256: `48a165efb4f8c8d25c41029dae8ff40b2247e4c52766a15a5344e9e25ba02ff3`
  - size_bytes: `40847`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/p2_selectivity_ready_2024.parquet`
  - shape: `[3198, 184]`
  - sha256: `a61f5fc9f6306cc310b09bd3fb4d292337f13b820ea0d028ac79aae3b8f38f96`
  - size_bytes: `1029334`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/p2_structure_ready_2024.parquet`
  - shape: `[8561, 184]`
  - sha256: `1dc4ce02999478f2ab5a10f2290e3bbd9148ea7986fcd3b5eed6d36029627baf`
  - size_bytes: `2443944`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/p4_employment_rate_ready_2024.parquet`
  - shape: `[6270, 184]`
  - sha256: `9b543685c62eb212d78271fdd34725ea34d0d6ee383a96c60b0734d0b3ec2d5a`
  - size_bytes: `1826832`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/p4_joint_rate_ready_2024.parquet`
  - shape: `[6270, 184]`
  - sha256: `9b543685c62eb212d78271fdd34725ea34d0d6ee383a96c60b0734d0b3ec2d5a`
  - size_bytes: `1826832`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/p4_progression_rate_ready_2024.parquet`
  - shape: `[6366, 184]`
  - sha256: `6760bc705cb17b1873d42ae78bddbed9a9267290a7da54cde1b38b2ea5186a22`
  - size_bytes: `1847111`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/data/row_lineage.parquet`
  - shape: `[10242, 10]`
  - sha256: `9e5589586932ce8bdc72ec395144ea3386d4ef0784079d6283f7704abd4a1113`
  - size_bytes: `824045`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/manifest/PREPROCESSING_INTEGRITY_MANIFEST.json`
  - shape: `[53, 6]`
  - sha256: `60682ff7a0672d9d64c3420ada793829965c6aa511735f0deac69a099877cacb`
  - size_bytes: `28539`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/manifest/clean_mart_output_status.json`
  - shape: `[7, 2]`
  - sha256: `b627f34686e5a08efecb60b92e1b4b1f465707ba03656d541695cd958fd0c1e6`
  - size_bytes: `991`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/manifest/integrity_summary.json`
  - shape: `[7, 2]`
  - sha256: `9f64bf6337112dd079f6544731cf362d5d4201929cbf43beb28d1ffe84592af9`
  - size_bytes: `3191`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/all_null_constant_audit.csv`
  - shape: `[164, 7]`
  - sha256: `f3bbfcb86ccb5c97315d9b3a5a85955f15a17351699f5fd71f83025b888f20b8`
  - size_bytes: `11026`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/column_schema_profile.csv`
  - shape: `[164, 23]`
  - sha256: `0f1643dc37cf4103f680c2de39094c8b721e8cede0dcfe0e7a103058795f5ec3`
  - size_bytes: `34702`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/count_denominator_audit.csv`
  - shape: `[13, 6]`
  - sha256: `28cba31f8405ddae2e79aa0db54b72db005e6d32e7b72d87a33a8a3cfc7ecbc1`
  - size_bytes: `757`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/dataset_inventory.csv`
  - shape: `[22, 20]`
  - sha256: `87bd587872a02114fea6ce5c3c21d93324d449a4b363111088e3009fde5c56e4`
  - size_bytes: `18817`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/derived_formula_registry.csv`
  - shape: `[5, 4]`
  - sha256: `204d9c887164514d762b671b7a49b00e57e5617144725f5e95fff843909072f9`
  - size_bytes: `526`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/derived_rate_reconciliation.csv`
  - shape: `[7, 6]`
  - sha256: `6a0edfa0cc8baa46488988ca7379d193f08b6e6ddcf2d992b827b883bb2bd3dd`
  - size_bytes: `513`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/domain_range_audit.csv`
  - shape: `[5043, 8]`
  - sha256: `ff52d86c3a7fee3b722807a85f2614fe57d069b20b634c3a77a50b6c36a5365b`
  - size_bytes: `843960`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/domain_rule_registry.csv`
  - shape: `[87, 5]`
  - sha256: `b2fdb21b583546a8ab6329860181d04ba94d497bc4c44ae6a0524137a91f3d3c`
  - size_bytes: `7647`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/dtype_mismatch_audit.csv`
  - shape: `[0, 23]`
  - sha256: `de7f7033eaa0b7bfc9034acd3192a4cb71b4dae53ec4fe14907e5c79dd5bb739`
  - size_bytes: `242`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/duplicate_conflict_audit.csv`
  - shape: `[64, 9]`
  - sha256: `e3e2addf8090cd9117154d49689b9c4c56af5abe3c59a53b81888debd48821f3`
  - size_bytes: `8279`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/feature_role_leakage_audit.csv`
  - shape: `[250, 12]`
  - sha256: `a65b38f7025edb9be31558e6f7f882f183b20275103711231a5bfa6d9239e7f7`
  - size_bytes: `27766`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/file_provenance_audit.csv`
  - shape: `[22, 20]`
  - sha256: `87bd587872a02114fea6ce5c3c21d93324d449a4b363111088e3009fde5c56e4`
  - size_bytes: `18817`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/grain_summary.csv`
  - shape: `[9, 2]`
  - sha256: `280a16dae5b2c58c99a7b8a6a6b2bc5779afc77c982030008b222a4e17ebd095`
  - size_bytes: `216`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/join_cardinality_audit.csv`
  - shape: `[3, 20]`
  - sha256: `ea5c2d8831a17d9334e99d0693345bce01a3ed7f7752f1e4ea2b7318dd7d2a52`
  - size_bytes: `808`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/join_unmatched_summary.csv`
  - shape: `[0, 2]`
  - sha256: `7f4920e32a6bc944dfbbbc4c47aacfd223058de9de360f5113947fb2c613baa5`
  - size_bytes: `30`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/key_grain_audit.csv`
  - shape: `[6, 8]`
  - sha256: `faedd22444174f09db0207944958fdfd17ccfa3acbcd5650ddfabc8f3c1f5943`
  - size_bytes: `429`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/major7_mapping_audit.csv`
  - shape: `[25, 5]`
  - sha256: `8a11bab4765ec62cd9a5862e98f4301a5d487cfbeba11ca4455cd5bbe9b3dddb`
  - size_bytes: `1090`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/missingness_by_major7.csv`
  - shape: `[1312, 5]`
  - sha256: `9e407397fbbd21780252e303d8cdfb2ac73d1097f5d5b32d1460c3597d2ec315`
  - size_bytes: `53611`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/missingness_by_sample.csv`
  - shape: `[912, 5]`
  - sha256: `2b50812c4f6855e788de5e46ade418ac95df9df5d973ad66d122b5a316c1fd2e`
  - size_bytes: `52671`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/missingness_by_split.csv`
  - shape: `[492, 5]`
  - sha256: `446769e3e756c8d8cdb645893ca0627f5f74d342c0f6f09025ab5946a1793fa8`
  - size_bytes: `23318`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/missingness_cooccurrence.csv`
  - shape: `[4, 5]`
  - sha256: `89ee23c17de439f7d2a7543476ccf15944fa8214bee204c9fbaa573f693807ec`
  - size_bytes: `343`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/missingness_profile.csv`
  - shape: `[164, 6]`
  - sha256: `12699b702c6279e97ee2322911a3e05f5a1d347596cf9a422d1fe570acc06c90`
  - size_bytes: `9137`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/notebook_discovery.csv`
  - shape: `[2, 8]`
  - sha256: `a216dc006fd951adf93a303667cd2c1b491dce638bc719d859c8005d75043aeb`
  - size_bytes: `758`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/notebook_execution_audit.csv`
  - shape: `[19, 11]`
  - sha256: `d7e2d94eacec9a99d41a44359d0b9ae37e28c257bba555184b835aabfddb9c26`
  - size_bytes: `1894`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/row_split_leakage_audit.csv`
  - shape: `[0, 2]`
  - sha256: `ef6e13214e821ed9e30cfa357eccd4e76b116fc2d92477ed9ad1729b0bed0639`
  - size_bytes: `26`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/sample_membership_audit.csv`
  - shape: `[12, 11]`
  - sha256: `1d886a2419eb34a81a3e863bb8c5a082a7b4f12667f43753e689f1efbac5ffa3`
  - size_bytes: `877`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/split_leakage_audit.csv`
  - shape: `[3, 5]`
  - sha256: `6092119f562222171774771ba5a1331796c907d66eec966ca15c72a0a5e50a8f`
  - size_bytes: `113`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/stored_notebook_output_reconciliation.csv`
  - shape: `[22, 5]`
  - sha256: `6d34be41b7f2282c44a6c6349945efa08c9c3d6d95b59c02692431f2fea5b5b1`
  - size_bytes: `1621`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/transformation_decision_ledger.csv`
  - shape: `[5, 4]`
  - sha256: `aaa2a3f0194878feb4ab9e33ef4692f46820ce54ffa5a18455c60d744ad0f229`
  - size_bytes: `593`
- path: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/reports/DATA_PREPROCESSING_INTEGRITY_REPORT.md`
  - shape: `None`
  - sha256: `ea1f7abbdf130725b57b213c90ded70398d60c3c6953b140f8f221e09fb61f96`
  - size_bytes: `14016`

## J. Critical Assertion Matrix

- `required_input_fail_n` = `0`
- `outcome_row_id_null_n` = `0`
- `outcome_row_id_duplicate_n` = `0`
- `exact_duplicate_n` = `0`
- `unapproved_many_to_many_n` = `0`
- `row_expansion_unexplained_n` = `0`
- `domain_fail_anomaly_n` = `0`
- `rate_reconciliation_fail_n` = `0`
- `sample_registry_mismatch_n` = `0`
- `school_split_leakage_n` = `0`
- `target_self_leakage_n` = `0`
- `active_id_metadata_feature_n` = `0`
- `unresolved_other_role_n` = `0`
- `active_all_null_feature_n` = `0`
- `row_lineage_missing_n` = `0`

## K. Warning Ledger Matrix

- `hash_or_shape_warning_n` = `0`
- `ledgered_duplicate_conflict_rows` = `36`
- `count_ready_not_observed_families` = `['GRADE', 'PROGRESSION', 'RETENTION']`
- `high_missing_selectivity_n` = `6505`
- `major7_mapping_warn_n` = `1`