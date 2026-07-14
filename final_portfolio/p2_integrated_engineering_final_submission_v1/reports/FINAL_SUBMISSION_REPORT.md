# P2 최종 제출 패키지 보고서

- FINAL_STATUS: `PASS_WITH_WARNINGS`
- RUN_ID: `20260714T062549Z`
- submission_root: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_integrated_engineering_final_submission_v1`
- active D08: `data/derived/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet`
- active D08 shape: `10242 x 151`
- active D08 sha256: `598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962`
- raw source files: `30`
- derived/provenance files: `136 / 11`

## Gate Matrix

| gate | status | evidence |
| --- | --- | --- |
| G01_raw_data_clone | PASS | qa/raw_data_integrity.csv |
| G02_derived_data_clone | PASS | qa/derived_data_integrity.csv |
| G03_active_mart_integrity | PASS | qa/active_mart_integrity.csv |
| G04_source_lineage | PASS | qa/source_lineage_summary.csv |
| G05_registry_coverage | WARN | qa/registry_audit.csv |
| G06_sample_split | PASS | qa/sample_split_integrity.csv |
| G07_target_coverage | PASS | qa/target_coverage_profile.csv |
| G08_phase_result_readout | PASS | qa/phase_result_readout.csv |

## Issue Register

| issue_id | severity | evidence | submission_handling |
| --- | --- | --- | --- |
| WARN_D08_SPLIT_EXTERNAL | WARN | D08 has no direct split column; use school_uid merge to dim_school_split | sample/split integrity gate verifies the external split merge |
| WARN_DIRECT_URL_LIMIT | WARN | some source direct download URLs are portal-level in the local source catalog | local file hashes and official portal URLs are retained as provenance anchors |
| WARN_Q_BRANCH_BLOCKED | WARN | P6 Q/selectivity branch is not interpreted as launch-ready | final report restricts claims to validated D08 and strict-chain readout |
| WARN_REGISTRY_COVERAGE | WARN | registry and D08 columns are not perfectly symmetric | missing/unregistered columns are written to qa/ |

## Key Evidence Files

- `qa/raw_data_integrity.csv`
- `qa/derived_data_integrity.csv`
- `qa/active_mart_integrity.csv`
- `qa/sample_split_integrity.csv`
- `qa/target_coverage_profile.csv`
- `qa/final_status_matrix.csv`
- `FINAL_SUBMISSION_PACKAGE_MANIFEST.csv`

## Re-run

```bash
MPLCONFIGDIR=/tmp/mplconfig .venv/bin/jupyter nbconvert --to notebook --execute workbook/p2/p2_integrated_engineering_final_submission_v1/P2_FINAL_SUBMISSION.ipynb --inplace --ExecutePreprocessor.timeout=900
```