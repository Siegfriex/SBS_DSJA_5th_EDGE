# P2-G4 Human Handoff Packet

사람 검토자에게 넘길 파일 묶음이다.

먼저 `00_HUMAN_REVIEW_GUIDE.md`를 읽고, 실제 입력은 `01_DECISION_SHEETS/` 아래 CSV에만 작성한다.

## File Manifest

| relative_path | size_kb |
| --- | --- |
| 00_HUMAN_REVIEW_GUIDE.md | 11.1 |
| 01_DECISION_SHEETS/decision_codebook.csv | 1.4 |
| 01_DECISION_SHEETS/deleted_row_recovery_sheet.csv | 0.2 |
| 01_DECISION_SHEETS/human_required_decision_sheet.csv | 8.7 |
| 01_DECISION_SHEETS/human_required_summary_by_issue.csv | 0.3 |
| 01_DECISION_SHEETS/target_leakage_override_sheet.csv | 4.6 |
| 02_EVIDENCE/strict_deleted_rows_detail.csv | 3586.7 |
| 02_EVIDENCE/strict_drop_deleted_rows_review_reference.csv | 1042.5 |
| 02_EVIDENCE/strict_drop_reason_counts.csv | 0.2 |
| 02_EVIDENCE/strict_model_feature_registry.csv | 17.3 |
| 02_EVIDENCE/strict_row_policy_audit.csv | 3521.7 |
| 02_EVIDENCE/strict_target_sample_counts.csv | 0.4 |
| 02_EVIDENCE/target_feature_exclusion_policy.csv | 3.3 |
| 03_MODEL_INPUT/MODEL_INPUT_PATHS.md | 0.8 |
| 03_MODEL_INPUT/mart_department_model_base_2024_strict_drop.csv | 11111.6 |
| 03_MODEL_INPUT/mart_department_model_base_2024_strict_drop.parquet | 1528.7 |
| 03_MODEL_INPUT/strict_clean_manifest.json | 0.9 |
| 04_REPORTS/P2_G4_HUMAN_REVIEW_ACTIONS_FULL_PRIOR.md | 22.9 |
| 04_REPORTS/P2_G4_STRICT_DROP_AND_REVIEW_UPDATE.md | 14.2 |
## Manual Review Status

- 상태: `completed_by_codex_manual_review`
- 완료 보고서: `MANUAL_REVIEW_COMPLETED.md`
- 필수 판단 시트: `01_DECISION_SHEETS/human_required_decision_sheet.csv`
- 결정 요약: `01_DECISION_SHEETS/manual_review_decision_summary.csv`
- 원칙: 신규 원천을 임의 생성하지 않고, 증빙 없는 항목은 제외/차단 유지.
