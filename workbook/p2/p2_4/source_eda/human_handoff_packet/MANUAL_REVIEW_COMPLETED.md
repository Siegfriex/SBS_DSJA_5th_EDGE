# P2-G4 Manual Review Completed

- 완료시각: `2026-07-13T13:29:07`
- 검토자: `Codex DS manual review`
- 검토일: `2026-07-13`

## 결론

원천을 임의 생성하지 않는 원칙으로 직접 판단을 완료했다. 이번 strict-clean 모델링에서는 all-null 변수, 부재 panel 트랙, D05 직접 조인, 2023 all-null 타깃을 제외한다. target leakage FAIL 조합은 모두 차단 유지한다. 삭제된 2,650행은 복구하지 않는다.

## 수작업 결정 요약

| area | issue_type | manual_decision | rows | status |
| --- | --- | --- | --- | --- |
| human_required | bridge_design_required | drop_D05_scope | 1 | approved |
| human_required | historical_2023_target_unavailable | exclude_2023_target | 8 | approved |
| human_required | missing_panel_source | drop_panel_track | 2 | approved |
| human_required | source_unavailable_all_null | exclude_from_features | 2 | approved |
| target_leakage | leakage_fail_pairs | keep_blocked | 16 | approved |
| deleted_row_recovery | strict_deleted_rows | no_deleted_rows_recovered | 2650 | approved |

## 13건 필수 판단 결과

| review_id | priority | issue_type | item | human_decision | source_fix_path_or_evidence | final_status |
| --- | --- | --- | --- | --- | --- | --- |
| HR-001 | P1 | source_unavailable_all_null | ctx24_industry_hhi (datasets=D04,D08_v2; missing_n_sum=10256) | exclude_from_features | 02_EVIDENCE/strict_model_feature_registry.csv | approved |
| HR-002 | P1 | source_unavailable_all_null | ctx24_industry_top3_pct (datasets=D04,D08_v2; missing_n_sum=10256) | exclude_from_features | 02_EVIDENCE/strict_model_feature_registry.csv | approved |
| HR-003 | P1 | missing_panel_source | mart_department_panel_2023_2025 | drop_panel_track | 02_EVIDENCE/strict_target_sample_counts.csv | approved |
| HR-004 | P1 | missing_panel_source | mart_A_rate_transition_2023_2025 | drop_panel_track | 02_EVIDENCE/strict_target_sample_counts.csv | approved |
| HR-005 | P2 | bridge_design_required | D05 job_cert columns | drop_D05_scope | 02_EVIDENCE/strict_model_feature_registry.csv | approved |
| HR-006 | P2 | historical_2023_target_unavailable | domestic_progression_rate_pct | exclude_2023_target | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | approved |
| HR-007 | P2 | historical_2023_target_unavailable | graduate_school_progression_rate_pct | exclude_2023_target | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | approved |
| HR-008 | P2 | historical_2023_target_unavailable | health_employment_rate_pct | exclude_2023_target | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | approved |
| HR-009 | P2 | historical_2023_target_unavailable | overseas_progression_rate_pct | exclude_2023_target | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | approved |
| HR-010 | P2 | historical_2023_target_unavailable | progression_rate_pct | exclude_2023_target | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | approved |
| HR-011 | P2 | historical_2023_target_unavailable | selectivity_proxy_pct | exclude_2023_target | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | approved |
| HR-012 | P2 | historical_2023_target_unavailable | university_progression_rate_pct | exclude_2023_target | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | approved |
| HR-013 | P2 | historical_2023_target_unavailable | vocational_college_progression_rate_pct | exclude_2023_target | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | approved |

## Target Leakage 결정

- leakage FAIL 조합 `16`건: 전부 `keep_blocked`
- 근거: same target, same target family, deterministic equality, employment/progression lineage audit FAIL.

## 삭제 행 복구 결정

| policy_id | decision | affected_rows | reason | evidence | reviewer | review_date | final_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DR-000 | no_deleted_rows_recovered | 2650 | strict 삭제 행은 구조 매칭 미해결, 캠퍼스 충돌, major_group_7 미확정, duplicate key/name, 소표본 0/100 극단 비율 중 하나 이상에 걸린 행이다. 복구할 개별 원천 증빙이 없으므로 전부 삭제 유지한다. | 02_EVIDENCE/strict_deleted_rows_detail.csv | Codex DS manual review | 2026-07-13 | approved |

## strict 모델링 입력

- `03_MODEL_INPUT/mart_department_model_base_2024_strict_drop.parquet`
- `03_MODEL_INPUT/mart_department_model_base_2024_strict_drop.csv`
- `03_MODEL_INPUT/manual_approved_feature_registry.csv`
- `03_MODEL_INPUT/manual_approved_target_and_scope_policy.csv`
- `03_MODEL_INPUT/manual_approved_scope_policy.json`

## 타깃별 현재 사용 가능 표본

| target_candidate | strict_target_keep_n | total_n | common_structural_drop_n | target_missing_drop_n | target_extreme_small_denom_drop_n | strict_target_drop_n |
| --- | --- | --- | --- | --- | --- | --- |
| a_rate_pct | 7592 | 10242 | 2650 | 0 | 236 | 2650 |
| cd_rate_pct | 7592 | 10242 | 2650 | 0 | 297 | 2650 |
| f_rate_pct | 7592 | 10242 | 2650 | 0 | 683 | 2650 |
| graduate_school_progression_rate_pct | 5674 | 10242 | 2650 | 2655 | 346 | 4568 |
| health_employment_rate_pct | 5600 | 10242 | 2650 | 2765 | 190 | 4642 |
| selectivity_proxy_pct | 3119 | 10242 | 2650 | 6505 | 0 | 7123 |

## 후속 작업 규칙

1. 모델링은 strict-clean 입력만 사용한다.
2. `human_required_decision_sheet.csv`의 `approved` 결정은 현재 P4 범위의 확정 정책으로 본다.
3. `source_fix_path_or_evidence`가 실제 신규 원천 파일이 아닌 항목은 재빌드 없이 제외/차단 유지한다.
4. 나중에 원천 파일이 생기면 그때 D08, registry, strict policy audit을 다시 생성한다.
