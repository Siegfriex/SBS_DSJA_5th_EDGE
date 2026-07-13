# DATA PREPROCESSING INTEGRITY REPORT

## 1. Executive Status

- final_status: `READY_WITH_WARNINGS`
- run_id: `20260713T044343Z_5b1a3d5`
- critical_fail_counts: `{"required_input_fail_n": 0, "outcome_row_id_null_n": 0, "outcome_row_id_duplicate_n": 0, "exact_duplicate_n": 0, "unapproved_many_to_many_n": 0, "row_expansion_unexplained_n": 0, "domain_fail_anomaly_n": 0, "rate_reconciliation_fail_n": 0, "sample_registry_mismatch_n": 0, "school_split_leakage_n": 0, "target_self_leakage_n": 0, "active_id_metadata_feature_n": 0, "unresolved_other_role_n": 0, "active_all_null_feature_n": 0, "row_lineage_missing_n": 0}`
- warning_counts: `{"hash_or_shape_warning_n": 0, "ledgered_duplicate_conflict_rows": 36, "count_ready_not_observed_families": ["GRADE", "PROGRESSION", "RETENTION"], "high_missing_selectivity_n": 6505, "major7_mapping_warn_n": 1}`

## 2. Run Provenance

```json
{
  "run_id": "20260713T044343Z_5b1a3d5",
  "utc_started_at": "2026-07-13T04:43:43.295882+00:00",
  "utc_finished_at": "2026-07-13T04:43:49.064824+00:00",
  "execution_seconds": 5.769,
  "project_root": "/home/sieg/projects-wsl/SBS_dataScience",
  "git_commit_full": "5b1a3d54266d881a839ad9a3cec750da66e94bc7",
  "git_commit_short": "5b1a3d5",
  "git_dirty": true,
  "python_version": "3.12.3 (main, Jun 19 2026, 12:46:00) [GCC 13.3.0]",
  "platform": "Linux-6.18.33.2-microsoft-standard-WSL2-x86_64-with-glibc2.39",
  "pandas_version": "3.0.3",
  "numpy_version": "2.5.0",
  "pyarrow_version": "24.0.0",
  "sklearn_version": "1.9.0",
  "selected_notebook_path": "/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_4/p4_modeling_readiness_v4/p2_G4_dataset_cell_inspection.ipynb",
  "selected_notebook_sha256": "cf980e2962e6906853d49cf71c46d6062e07be897d23a72f01070f0e6bcc790b",
  "random_seed_used": false,
  "execution_command": "python workbook/p2/p2_4/p4_preprocessing_integrity_v1/run_preprocessing_integrity_v1.py",
  "execution_success": true,
  "warning_count": 5,
  "error_count": 0
}
```

## 3. Input File Inventory

| label | exists | actual_shape | expected_shape | hash_match | shape_match | status | warning_code |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mart_department_model_base_2024 | True | [10242, 151] | [10242, 151] | True | True | PASS |  |
| P4_PHASE_SAMPLE_MEMBERSHIP_FINAL | True | [10242, 21] | [10242, 21] | True | True | PASS |  |
| P4_PHASE_SAMPLE_REGISTRY_FINAL | True | [12, 11] | [12, 11] | True | True | PASS |  |
| department_model_column_registry_v4 | True | [151, 22] | [151, 22] | True | True | PASS |  |
| P4_PHASE_FEATURE_SET_FINAL | True | [250, 11] | [250, 11] | True | True | PASS |  |
| P4_PHASE_MODEL_SPEC_FINAL | True | [18, 10] | [18, 10] | True | True | PASS |  |
| P4_DUPLICATE_CONFLICT_RESOLUTION | True | [36, 14] | [36, 14] | True | True | PASS |  |
| P4_TARGET_PROFILE_BY_PHASE | True | [396, 20] | [396, 20] | True | True | PASS |  |
| P4_FINAL_MODELING_READINESS | True | [24, 2] | null | True |  | PASS |  |
| P4_MODELING_REVIEW_BUNDLE_MANIFEST | True | [15, 9] | null |  |  | PASS |  |
| P4_HANDOFF_MANIFEST | True | [29, 2] | null |  |  | PASS |  |
| dim_school_split | True | [200, 6] | null |  |  | PASS |  |
| shared_model_sample_membership | True | [10242, 17] | null |  |  | PASS |  |
| shared_model_sample_registry | True | [5, 12] | null |  |  | PASS |  |
| shared_column_registry | True | [198, 6] | null |  |  | PASS |  |
| shared_feature_registry | True | [4, 7] | null |  |  | PASS |  |
| shared_target_registry | True | [6, 4] | null |  |  | PASS |  |
| cleaning_derived_formula_reconstruction | True | [8, 7] | null |  |  | PASS |  |
| cleaning_split_integrity_audit | True | [6, 3] | null |  |  | PASS |  |
| cleaning_target_leakage_audit_by_phase | True | [31, 11] | null |  |  | PASS |  |
| cleaning_count_denominator_inventory | True | [72, 13] | null |  |  | PASS |  |
| cleaning_context_grain_audit | True | [43, 8] | null |  |  | PASS |  |

## 4. Dataset Row/Column Counts

- base shape: `(10242, 184)`
- unique schools: `200`
- unique campuses: `452`
- unique departments: `10222`

## 5. Grain and Key Audit

| key_candidate | exists | null_key_rows | duplicate_key_rows | duplicate_key_groups | unique_key_n | value_conflict_group_n | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| outcome_row_id | True | 0 | 0 | 0 | 10242 | 0 | PASS |
| analysis_year+school_uid+campus_uid+dept_uid | True | 0 | 36 | 18 | 10224 | 18 | WARN |
| analysis_year+school_uid+campus_uid+dept_uid+outcome_row_id | True | 0 | 0 | 0 | 10242 | 0 | PASS |
| school_uid | True | 0 | 10235 | 193 | 200 | 0 | PASS |
| campus_uid | True | 0 | 10200 | 410 | 452 | 0 | PASS |
| dept_uid | True | 0 | 40 | 20 | 10222 | 0 | PASS |

Grain summary:

| metric | value |
| --- | --- |
| row_n | 10242 |
| school_n | 200 |
| campus_n | 452 |
| department_entity_n | 10222 |
| year_n | 1 |
| same_dept_uid_multi_school_n | 0 |
| same_dept_uid_multi_campus_n | 2 |
| school_dept_name_multi_entity_n | 40 |
| degree_course_non_null_n | 8561 |

## 6. Join Cardinality Audit

| left_dataset | right_dataset | join_key | expected_cardinality | actual_cardinality | left_row_count_before | right_row_count | output_row_count | row_expansion_factor | matched_rows | left_only_rows | right_only_rows | duplicate_key_count_left | duplicate_key_count_right | many_to_many | approved_many_to_many | match_method | match_confidence | review_needed | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D08 | P4_PHASE_SAMPLE_MEMBERSHIP_FINAL | outcome_row_id | one_to_one | one_to_one | 10242 | 10242 | 10242 | 1.0 | 10242 | 0 |  | 0 | 0 | False | False | exact/stable_key | stable_key | False | PASS |
| D08 | dim_school_split | school_uid | many_to_one | many_to_one | 10242 | 200 | 10242 | 1.0 | 10242 | 0 |  | 10235 | 0 | False | False | exact/stable_key | stable_key | False | PASS |
| D08_conflict_subset | P4_DUPLICATE_CONFLICT_RESOLUTION | outcome_row_id | many_to_one | one_to_one | 36 | 10242 | 36 | 1.0 | 36 | 0 |  | 0 | 0 | False | False | exact/stable_key | stable_key | False | PASS |

## 7. Duplicate/Conflict Audit

- conflict rows: `36`
- conflict groups: `32`

| classification | status | rows |
| --- | --- | --- |
| CAMPUS_CONFLICT | LEDGERED_EXCLUSION | 2 |
| PARENT_HEADCOUNT_REUSED | LEDGERED_WARN | 56 |
| TRUE_DUPLICATE | LEDGERED_EXCLUSION | 6 |

## 8. Schema/Dtype Audit

- columns profiled: `164`
- dtype mismatch rows: `0`
- coercion failure columns: `0`

## 9. Missingness Audit

- selectivity missing: `6505` / `10242`
- health employment missing: `2765` / `10242`
- graduate school progression missing: `2655` / `10242`

## 10. Domain/Range Audit

- explicit rule anomaly rows: `5043`
- fail severity rows: `0`

## 11. Count/Denominator/Rate Audit

Count inventory:

| family | column | exists | non_null_n | missing_n | status |
| --- | --- | --- | --- | --- | --- |
| GRADE | a_grade_students_n | False | 0 | 10242 | not_observed |
| GRADE | graded_students_n | False | 0 | 10242 | not_observed |
| GRADE | a_rate_pct | True | 10242 | 0 | observed |
| GRADE | a_rate_prop | False | 0 | 10242 | not_observed |
| RETENTION | initial_employed_n | False | 0 | 10242 | not_observed |
| RETENTION | retained_1_n | False | 0 | 10242 | not_observed |
| RETENTION | retained_2_n | False | 0 | 10242 | not_observed |
| RETENTION | retained_3_n | False | 0 | 10242 | not_observed |
| RETENTION | retained_4_n | False | 0 | 10242 | not_observed |
| PROGRESSION | graduate_school_progressors_n | False | 0 | 10242 | not_observed |
| PROGRESSION | graduates_n | True | 8561 | 1681 | observed |
| PROGRESSION | graduate_school_progression_rate_pct | True | 7587 | 2655 | observed |
| PROGRESSION | graduate_school_progression_prop | False | 0 | 10242 | not_observed |

Rate reconciliation:

| rate_name | status | audited_n | violation_n | max_abs_diff | tolerance |
| --- | --- | --- | --- | --- | --- |
| competition_ratio | PASS | 5257 | 0 | 3.711597344135953e-06 | 0.001 |
| admission_yield_ratio | PASS | 5257 | 0 | 3.8146972691777137e-07 | 0.001 |
| admit_per_applicant_ratio | PASS | 5260 | 0 | 2.938257137596878e-08 | 0.001 |
| leave_rate_pct | PASS | 8441 | 0 | 3.691642518788285e-06 | 0.001 |
| female_student_share_pct | PASS | 8441 | 0 | 3.796268771338873e-06 | 0.001 |
| international_student_share_pct | PASS | 8441 | 0 | 3.7368463097209315e-06 | 0.001 |
| fulltime_faculty_share_pct | PASS | 6379 | 0 | 3.6831559810934777e-06 | 0.001 |

## 12. Major7/Category Mapping Audit

| audit | key | row_n | school_n | status |
| --- | --- | --- | --- | --- |
| major_group_7_distribution | ART | 1566 | 166.0 | PASS |
| major_group_7_distribution | EDU | 728 | 130.0 | PASS |
| major_group_7_distribution | ENG | 2642 | 157.0 | PASS |
| major_group_7_distribution | HUM | 1108 | 157.0 | PASS |
| major_group_7_distribution | MED | 632 | 126.0 | PASS |
| major_group_7_distribution | NAT | 1258 | 142.0 | PASS |
| major_group_7_distribution | SOC | 2165 | 172.0 | PASS |
| major_group_7_distribution |  | 143 | 45.0 | WARN |
| major7_mapping_method | inherited_headcount | 8561 |  | PASS |
| major7_mapping_method | keyword_rule | 859 |  | PASS |
| major7_mapping_method | exact_dictionary | 679 |  | PASS |
| major7_mapping_method | ambiguous | 85 |  | PASS |
| major7_mapping_method | unknown | 58 |  | PASS |
| major7_mapping_confidence | high | 8561 |  | PASS |
| major7_mapping_confidence | medium | 1538 |  | PASS |
| major7_mapping_confidence | low | 85 |  | PASS |
| major7_mapping_confidence | unknown | 58 |  | PASS |
| major7_review_needed | False | 10099 |  | PASS |
| major7_review_needed | True | 143 |  | PASS |
| major7_candidate_count | 1 | 10121 |  | PASS |
| major7_candidate_count | 0 | 58 |  | PASS |
| major7_candidate_count | 2 | 58 |  | PASS |
| major7_candidate_count | 3 | 3 |  | PASS |
| major7_candidate_count | 4 | 2 |  | PASS |
| same_school_dept_multiple_major7 | ALL | 0 |  | PASS |

## 13. Sample Membership Audit

| sample_id | registry_row_n | actual_row_n | diff_row_n | registry_school_n | actual_school_n | diff_school_n | train_n | validation_n | test_n | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1_STRUCTURE_READY | 6270 | 6270 | 0 | 186 | 186 | 0 | 4623 | 932 | 715 | PASS |
| P1_SELECTIVITY_READY | 2416 | 2416 | 0 | 130 | 130 | 0 | 1789 | 367 | 260 | PASS |
| P2_STRUCTURE_READY | 8561 | 8561 | 0 | 198 | 198 | 0 | 6302 | 1263 | 996 | PASS |
| P2_SELECTIVITY_READY | 3198 | 3198 | 0 | 146 | 146 | 0 | 2355 | 522 | 321 | PASS |
| P3_STRUCTURE_READY | 8561 | 8561 | 0 | 198 | 198 | 0 | 6302 | 1263 | 996 | PASS |
| P3_SELECTIVITY_READY | 3198 | 3198 | 0 | 146 | 146 | 0 | 2355 | 522 | 321 | PASS |
| P4_E_STRUCTURE_READY | 6270 | 6270 | 0 | 186 | 186 | 0 | 4623 | 932 | 715 | PASS |
| P4_P_STRUCTURE_READY | 6366 | 6366 | 0 | 195 | 195 | 0 | 4687 | 949 | 730 | PASS |
| P4_JOINT_STRUCTURE_READY | 6270 | 6270 | 0 | 186 | 186 | 0 | 4623 | 932 | 715 | PASS |
| P4_E_SELECTIVITY_READY | 2416 | 2416 | 0 | 130 | 130 | 0 | 1789 | 367 | 260 | PASS |
| P4_P_SELECTIVITY_READY | 2439 | 2439 | 0 | 136 | 136 | 0 | 1805 | 372 | 262 | PASS |
| P4_JOINT_SELECTIVITY_READY | 2416 | 2416 | 0 | 130 | 130 | 0 | 1789 | 367 | 260 | PASS |

## 14. Split Leakage Audit

| split_a | split_b | overlap_school_n | overlap_schools | status |
| --- | --- | --- | --- | --- |
| test | train | 0 |  | PASS |
| test | val | 0 |  | PASS |
| train | val | 0 |  | PASS |

## 15. Feature Role/Leakage Audit

- target self leakage rows: `0`
- active ID/metadata feature rows: `0`
- unresolved OTHER rows: `0`

## 16. Clean Mart Outputs

```json
{
  "p2_structure_ready_2024.parquet": {
    "status": "CREATED",
    "rows": 8561,
    "reason": "sample_P2_STRUCTURE_READY"
  },
  "p2_selectivity_ready_2024.parquet": {
    "status": "CREATED",
    "rows": 3198,
    "reason": "sample_P2_SELECTIVITY_READY"
  },
  "p4_employment_rate_ready_2024.parquet": {
    "status": "CREATED",
    "rows": 6270,
    "reason": "sample_P4_E_STRUCTURE_READY"
  },
  "p4_progression_rate_ready_2024.parquet": {
    "status": "CREATED",
    "rows": 6366,
    "reason": "sample_P4_P_STRUCTURE_READY"
  },
  "p4_joint_rate_ready_2024.parquet": {
    "status": "CREATED",
    "rows": 6270,
    "reason": "sample_P4_JOINT_STRUCTURE_READY"
  },
  "retention_count_ready_2024.parquet": {
    "status": "NOT_AVAILABLE",
    "rows": 0,
    "reason": "retention numerator/denominator columns not observed"
  },
  "progression_count_ready_2024.parquet": {
    "status": "NOT_AVAILABLE",
    "rows": 0,
    "reason": "graduate_school_progressors_n not observed"
  }
}
```

## 17. Exclusion Ledger

- excluded rows: `8`
- ledger path: `data/excluded_rows.parquet`

## 18. Unresolved Blockers

- BLOCKED_INTEGRITY critical count total: `0`
- COUNT_READY grade/retention/progression: `not_observed` where numerator/denominator columns are absent.

## 19. Preprocessing Contract

- Completed: provenance, key/grain, join cardinality, duplicate ledger, schema, missingness, domain/range, count inventory, major7, samples, split, role/leakage, lineage, clean marts.
- Not performed: imputation, scaling, one-hot encoding, model fitting, residual generation, bootstrap inference.
- Future fold-local only: imputer/scaler/encoder fitting.

## 20. Final PASS/WARN/FAIL Matrix

| Gate | Status | Key Count | Output |
|---|---|---:|---|
| Gate 0 inventory | PASS | 0 | qa/dataset_inventory.csv |
| Gate 1 key/grain | PASS | 0 | qa/key_grain_audit.csv |
| Gate 2 join | PASS | 0 | qa/join_cardinality_audit.csv |
| Gate 3 schema | PASS | 0 | qa/column_schema_profile.csv |
| Gate 4 missingness | WARN | 6505 | qa/missingness_profile.csv |
| Gate 5 domain/range | PASS | 0 | qa/domain_range_audit.csv |
| Gate 6 count/rate | WARN | 3 | qa/count_denominator_audit.csv |
| Gate 7 major7 | WARN | 1 | qa/major7_mapping_audit.csv |
| Gate 8 samples/split | PASS | 0 | qa/sample_membership_audit.csv |
| Gate 9 feature roles | PASS | 0 | qa/feature_role_leakage_audit.csv |
