# P4 Final Modeling Readiness

## Status

`READY_WITH_WARNINGS`

## Phase Status

| status_key | value |
| --- | --- |
| overall_status | READY_WITH_WARNINGS |
| P1_MODELING_STATUS | READY_WITH_WARNINGS |
| P2_S_MODELING_STATUS | READY_WITH_WARNINGS |
| P2_Q_MODELING_STATUS | READY_WITH_WARNINGS |
| P3_S_MODELING_STATUS | READY_WITH_WARNINGS |
| P3_Q_MODELING_STATUS | READY_WITH_WARNINGS |
| P4_E_STRUCTURE_STATUS | READY_WITH_WARNINGS |
| P4_P_STRUCTURE_STATUS | READY_WITH_WARNINGS |
| P4_JOINT_STRUCTURE_STATUS | READY_WITH_WARNINGS |
| P4_E_SELECTIVITY_STATUS | READY_WITH_WARNINGS |
| P4_P_SELECTIVITY_STATUS | READY_WITH_WARNINGS |
| P4_JOINT_SELECTIVITY_STATUS | READY_WITH_WARNINGS |
| P5_2024_EXPLORATORY_STATUS | READY |
| P7_STATUS | PENDING_TASK_MATRIX |
| P8_STATUS | NOT_AVAILABLE |
| rank_block | False |
| sample_block | False |
| pending_residual_spec_n | 4 |
| created_at | 2026-07-13T05:06:13.174377+00:00 |
| active_d08_sha256 | 5f56e375fd1c0474a5e55652859ae007e2f45becd6d3350ee4c82e21fab8df9b |
| active_d08_shape | [7592, 151] |
| active_d08_policy | strict_clean_manual_approved |
| manual_approved_feature_registry_shape | [198, 11] |
| manual_approved_p4_use_true_n | 131 |
| target_specific_keep_blocked_n | 16 |
| input_file_n | 13 |
| duplicate_conflict_excluded_row_n | 0 |
| strict_deleted_rows_preserved_n | 2650 |
| OTHER_after_resolution | 0 |

## Input Policy

- Active model input: `workbook/p2/p2_4/source_eda/strict_clean_v1/mart_department_model_base_2024_strict_drop.parquet`
- Active policy: strict-clean D08 plus manual-approved feature registry.
- Deleted strict rows are not recovered; target samples use `strict_target_sample_membership.csv`.
- Target-specific leakage rows remain `keep_blocked` denylist entries, not global feature drops.

## Final Samples

| sample_id | row_n | school_n | train_n | validation_n | test_n | excluded_conflict_n | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1_STRUCTURE_READY | 5600 | 185 | 4080 | 871 | 649 | 0 | READY |
| P1_SELECTIVITY_READY | 2355 | 130 | 1742 | 360 | 253 | 0 | READY |
| P2_STRUCTURE_READY | 7592 | 197 | 5534 | 1168 | 890 | 0 | READY |
| P2_SELECTIVITY_READY | 3119 | 146 | 2293 | 514 | 312 | 0 | READY |
| P3_STRUCTURE_READY | 7592 | 197 | 5534 | 1168 | 890 | 0 | READY |
| P3_SELECTIVITY_READY | 3119 | 146 | 2293 | 514 | 312 | 0 | READY |
| P4_E_STRUCTURE_READY | 5600 | 185 | 4080 | 871 | 649 | 0 | READY |
| P4_P_STRUCTURE_READY | 5674 | 194 | 4129 | 884 | 661 | 0 | READY |
| P4_JOINT_STRUCTURE_READY | 5600 | 185 | 4080 | 871 | 649 | 0 | READY |
| P4_E_SELECTIVITY_READY | 2355 | 130 | 1742 | 360 | 253 | 0 | READY |
| P4_P_SELECTIVITY_READY | 2376 | 136 | 1756 | 365 | 255 | 0 | READY |
| P4_JOINT_SELECTIVITY_READY | 2355 | 130 | 1742 | 360 | 253 | 0 | READY |

## Treatment-Coded Rank Audit

| model_id | sample_id | train_n | raw_feature_count | encoded_feature_count | rank | rank_deficiency | condition_number | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1_STRUCTURE | P1_STRUCTURE_READY | 4080 | 13 | 32.0 | 32.0 | 0.0 | 26.89350559821392 | PASS |
| P1_SELECTIVITY | P1_SELECTIVITY_READY | 1742 | 16 | 33.0 | 33.0 | 0.0 | 47.075691585511215 | PASS |
| P2_S | P2_STRUCTURE_READY | 5534 | 11 | 32.0 | 32.0 | 0.0 | 94.82564013081095 | PASS |
| P2_Q | P2_SELECTIVITY_READY | 2293 | 14 | 32.0 | 32.0 | 0.0 | 70.4266578528154 | PASS |
| P3_S | P3_STRUCTURE_READY | 5534 | 11 | 32.0 | 32.0 | 0.0 | 94.82564013081095 | PASS |
| P3_Q | P3_SELECTIVITY_READY | 2293 | 14 | 32.0 | 32.0 | 0.0 | 70.4266578528154 | PASS |
| P4_E_STRUCTURE_A_RATE | P4_E_STRUCTURE_READY | 4080 | 12 | 31.0 | 31.0 | 0.0 | 26.765002143847916 | PASS |
| P4_E_STRUCTURE_RESIDUAL | P4_E_STRUCTURE_READY | 4080 | 12 |  |  |  |  | PENDING_UPSTREAM_RESIDUAL |
| P4_E_SELECTIVITY_A_RATE | P4_E_SELECTIVITY_READY | 1742 | 15 | 32.0 | 32.0 | 0.0 | 48.064342050456 | PASS |
| P4_E_SELECTIVITY_RESIDUAL | P4_E_SELECTIVITY_READY | 1742 | 15 |  |  |  |  | PENDING_UPSTREAM_RESIDUAL |
| P4_P_STRUCTURE_A_RATE | P4_P_STRUCTURE_READY | 4129 | 12 | 33.0 | 33.0 | 0.0 | 84.41952739666249 | PASS |
| P4_P_STRUCTURE_RESIDUAL | P4_P_STRUCTURE_READY | 4129 | 12 |  |  |  |  | PENDING_UPSTREAM_RESIDUAL |
| P4_P_SELECTIVITY_A_RATE | P4_P_SELECTIVITY_READY | 1756 | 15 | 33.0 | 33.0 | 0.0 | 69.10836864452585 | PASS |
| P4_P_SELECTIVITY_RESIDUAL | P4_P_SELECTIVITY_READY | 1756 | 15 |  |  |  |  | PENDING_UPSTREAM_RESIDUAL |
| P4_E_JOINT_STRUCTURE_A_RATE | P4_JOINT_STRUCTURE_READY | 4080 | 12 | 31.0 | 31.0 | 0.0 | 26.765002143847916 | PASS |
| P4_P_JOINT_STRUCTURE_A_RATE | P4_JOINT_STRUCTURE_READY | 4080 | 12 | 31.0 | 31.0 | 0.0 | 26.765002143847916 | PASS |
| P4_E_JOINT_SELECTIVITY_A_RATE | P4_JOINT_SELECTIVITY_READY | 1742 | 15 | 32.0 | 32.0 | 0.0 | 48.064342050456 | PASS |
| P4_P_JOINT_SELECTIVITY_A_RATE | P4_JOINT_SELECTIVITY_READY | 1742 | 15 | 32.0 | 32.0 | 0.0 | 48.064342050456 | PASS |

## Review Bundle

`/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_4/p4_modeling_readiness_v4/P4_MODELING_REVIEW_BUNDLE.zip`
