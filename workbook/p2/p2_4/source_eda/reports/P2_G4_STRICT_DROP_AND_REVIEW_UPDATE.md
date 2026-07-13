# P2-G4 Strict Drop And Review Update

- 생성시각: `2026-07-13T11:10:43`
- 원본 D08: `workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet`
- strict 삭제 적용 Parquet: `workbook/p2/p2_4/source_eda/strict_clean_v1/mart_department_model_base_2024_strict_drop.parquet`
- strict 삭제 적용 CSV: `workbook/p2/p2_4/source_eda/strict_clean_v1/mart_department_model_base_2024_strict_drop.csv`
- 최신 리뷰 폴더: `workbook/p2/p2_4/source_eda/review_queues`

## 처리 원칙

사용자 지시에 따라 애매하거나 구조적으로 문제가 있는 행은 일단 삭제 처리했다. 원본 파일은 보존했고, 삭제 적용본은 `source_eda/strict_clean_v1/`에 별도 저장했다.

삭제한 행은 복구 불가능하게 지운 것이 아니라 `strict_deleted_rows_detail.csv`와 `strict_row_policy_audit.csv`에 이유와 함께 남겼다. 이후 사람이 특정 행을 살리기로 결정하면 해당 행만 승인 overlay로 복구할 수 있다.

## 결과 요약

- 원본 행 수: `10242`
- strict 유지 행 수: `7592`
- strict 삭제 행 수: `2650`
- strict 유지율: `74.13%`

## 삭제 사유별 건수

| drop_flag | rows |
| --- | --- |
| drop_structure_unresolved | 1681 |
| drop_rate_extreme_small_denominator | 941 |
| drop_campus_conflict | 236 |
| drop_major7_unresolved | 143 |
| drop_d08_key_duplicate | 36 |
| drop_normalized_name_duplicate | 8 |
| drop_core_identity_missing | 0 |

## 타깃별 strict 샘플

타깃 결측은 임의 대체하지 않고 해당 타깃 샘플에서 삭제했다.

| target_candidate | strict_target_keep_n | total_n | common_structural_drop_n | target_missing_drop_n | target_extreme_small_denom_drop_n | strict_target_drop_n |
| --- | --- | --- | --- | --- | --- | --- |
| a_rate_pct | 7592 | 10242 | 2650 | 0 | 236 | 2650 |
| cd_rate_pct | 7592 | 10242 | 2650 | 0 | 297 | 2650 |
| f_rate_pct | 7592 | 10242 | 2650 | 0 | 683 | 2650 |
| graduate_school_progression_rate_pct | 5674 | 10242 | 2650 | 2655 | 346 | 4568 |
| health_employment_rate_pct | 5600 | 10242 | 2650 | 2765 | 190 | 4642 |
| selectivity_proxy_pct | 3119 | 10242 | 2650 | 6505 | 0 | 7123 |

## 최신 리뷰 액션 레지스터

| id | status | action | rows | artifact | note |
| --- | --- | --- | --- | --- | --- |
| STRICT-001 | agent_applied | drop structurally unresolved rows | 1681 | workbook/p2/p2_4/source_eda/strict_clean_v1/strict_deleted_rows_detail.csv | manual_pending/unmatched/non-ok row_qa rows are excluded from strict analysis base |
| STRICT-002 | agent_applied | drop campus conflict rows | 236 | workbook/p2/p2_4/source_eda/strict_clean_v1/strict_deleted_rows_detail.csv | campus_conflict_flag rows are excluded pending alias/campus policy rebuild |
| STRICT-003 | agent_applied | drop unresolved major_group_7 rows | 143 | workbook/p2/p2_4/source_eda/strict_clean_v1/strict_deleted_rows_detail.csv | ambiguous/unknown/low confidence major labels are excluded |
| STRICT-004 | agent_applied | drop duplicate key/name rows | 36 | workbook/p2/p2_4/source_eda/strict_clean_v1/strict_deleted_rows_detail.csv | duplicate carried D08 key and normalized department duplicate rows are excluded |
| STRICT-005 | agent_applied | drop small-denominator 0/100 percent extreme rows | 941 | workbook/p2/p2_4/source_eda/strict_clean_v1/strict_deleted_rows_detail.csv | extreme ratio with graduates<=5 or enrolled_students<=20 is excluded under strict policy |
| STRICT-006 | agent_applied | exclude target-missing rows per target sample | 11925 | workbook/p2/p2_4/source_eda/strict_clean_v1/strict_target_sample_membership.csv | target missing is not imputed; it is deleted from the relevant target sample |
| STRICT-007 | agent_applied | write target-specific leakage denylist | 16 | workbook/p2/p2_4/source_eda/strict_clean_v1/target_feature_exclusion_policy.csv | leakage FAIL pairs are blocked at target-model level |
| HUMAN-001 | human_required | decide truly missing/source-unavailable items | 13 | workbook/p2/p2_4/source_eda/strict_clean_v1/human_required_after_strict_drop.csv | cannot be solved by row deletion; needs source rebuild or analysis exclusion decision |

## 사람이 아직 명시적으로 판단해야 하는 항목

행 삭제로 해결되는 구조 문제는 strict 산출물에서 제거했다. 아래는 행 삭제로 해결되지 않는 진짜 빈 값/원천 부재/설계 판단 항목이다.

| priority | issue_type | path | item | why_not_auto_fixed | human_needed | recommended_default |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | source_unavailable_all_null | workbook/p2/p2_3/p4_handoff_candidate/shared/department_model_column_registry.csv | ctx24_industry_hhi (datasets=D04,D08_v2; missing_n_sum=10256) | 원천 변수 자체가 관련 산출물에서 전부 비어 있어 행 삭제로 해결되지 않는다. | 해당 변수를 재수집/재생성할지, 분석 범위에서 영구 제외할지 결정 | exclude_from_features_until_source_exists |
| P1 | source_unavailable_all_null | workbook/p2/p2_3/p4_handoff_candidate/shared/department_model_column_registry.csv | ctx24_industry_top3_pct (datasets=D04,D08_v2; missing_n_sum=10256) | 원천 변수 자체가 관련 산출물에서 전부 비어 있어 행 삭제로 해결되지 않는다. | 해당 변수를 재수집/재생성할지, 분석 범위에서 영구 제외할지 결정 | exclude_from_features_until_source_exists |
| P1 | missing_panel_source | workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_panel_2023_2025.parquet | mart_department_panel_2023_2025 | 2023-2025 panel/transition parquet 자체가 존재하지 않는다. | 패널 트랙을 만들지, 이번 P4에서 제외할지 결정 | keep_panel_track_blocked |
| P1 | missing_panel_source | workbook/p2/p2_3/p4_handoff_candidate/shared/mart_A_rate_transition_2023_2025.parquet | mart_A_rate_transition_2023_2025 | 2023-2025 panel/transition parquet 자체가 존재하지 않는다. | 패널 트랙을 만들지, 이번 P4에서 제외할지 결정 | keep_panel_track_blocked |
| P2 | bridge_design_required | workbook/p2/p2_3/p4_handoff_candidate/shared/department_model_column_registry.csv | D05 job_cert columns | 직무분류 기반 데이터라 학과행에 직접 조인하면 축이 맞지 않는다. | 직무분류->계열/학과 브리지 키와 집계 수준 설계 | do_not_join_D05_directly |
| P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | domestic_progression_rate_pct | 2023 확장 표본 11287행에서 해당 타깃 컬럼이 전부 비어 있다. | 2023 원천에서 해당 변수를 만들 수 있는지 확인하거나 2023 분석에서 제외 | exclude_2023_column_from_target_analysis |
| P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | graduate_school_progression_rate_pct | 2023 확장 표본 11287행에서 해당 타깃 컬럼이 전부 비어 있다. | 2023 원천에서 해당 변수를 만들 수 있는지 확인하거나 2023 분석에서 제외 | exclude_2023_column_from_target_analysis |
| P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | health_employment_rate_pct | 2023 확장 표본 11287행에서 해당 타깃 컬럼이 전부 비어 있다. | 2023 원천에서 해당 변수를 만들 수 있는지 확인하거나 2023 분석에서 제외 | exclude_2023_column_from_target_analysis |
| P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | overseas_progression_rate_pct | 2023 확장 표본 11287행에서 해당 타깃 컬럼이 전부 비어 있다. | 2023 원천에서 해당 변수를 만들 수 있는지 확인하거나 2023 분석에서 제외 | exclude_2023_column_from_target_analysis |
| P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | progression_rate_pct | 2023 확장 표본 11287행에서 해당 타깃 컬럼이 전부 비어 있다. | 2023 원천에서 해당 변수를 만들 수 있는지 확인하거나 2023 분석에서 제외 | exclude_2023_column_from_target_analysis |
| P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | selectivity_proxy_pct | 2023 확장 표본 11287행에서 해당 타깃 컬럼이 전부 비어 있다. | 2023 원천에서 해당 변수를 만들 수 있는지 확인하거나 2023 분석에서 제외 | exclude_2023_column_from_target_analysis |
| P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | university_progression_rate_pct | 2023 확장 표본 11287행에서 해당 타깃 컬럼이 전부 비어 있다. | 2023 원천에서 해당 변수를 만들 수 있는지 확인하거나 2023 분석에서 제외 | exclude_2023_column_from_target_analysis |
| P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | vocational_college_progression_rate_pct | 2023 확장 표본 11287행에서 해당 타깃 컬럼이 전부 비어 있다. | 2023 원천에서 해당 변수를 만들 수 있는지 확인하거나 2023 분석에서 제외 | exclude_2023_column_from_target_analysis |

## Target Leakage 처리

누수 실패 조합은 사람이 다시 고를 때까지 target-specific denylist로 막았다. 전역 컬럼 삭제가 아니라 타깃별 모델 스펙에서 제외해야 한다.

| target | blocked_feature | reasons | abs_corr_train_validation | deterministic_equal_rate | policy_action | agent_decision |
| --- | --- | --- | --- | --- | --- | --- |
| health_employment_rate_pct | employment_rate_pct | same_target_family_outcome\|employment_lineage_name | 0.8102478276975554 | 0.254493278960882 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| health_employment_rate_pct | has_employment | employment_lineage_name |  | 0.0 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| employment_rate_pct | employment_rate_pct | same_as_target\|corr_abs_gt_0.995\|deterministic_equality | 1.0 | 1.0 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| employment_rate_pct | has_employment | employment_lineage_name |  | 0.0 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| graduate_school_progression_rate_pct | progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.9947958618143944 | 0.9058543125279308 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| graduate_school_progression_rate_pct | vocational_college_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.0230136402500334 | 0.4275286757038581 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| graduate_school_progression_rate_pct | university_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.0240808251406509 | 0.422910770147475 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| graduate_school_progression_rate_pct | domestic_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.9938044852313588 | 0.8912557723819455 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| graduate_school_progression_rate_pct | overseas_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.1173446512741289 | 0.4361686280351556 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| graduate_school_progression_rate_pct | has_progression | progression_lineage_name |  | 0.0001489646953671 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| progression_rate_pct | progression_rate_pct | same_as_target\|corr_abs_gt_0.995\|deterministic_equality | 1.0 | 1.0 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| progression_rate_pct | vocational_college_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.0475804611375327 | 0.4136749590347088 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| progression_rate_pct | university_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.0975347058503601 | 0.4214211231938031 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| progression_rate_pct | domestic_progression_rate_pct | same_target_family_outcome\|progression_lineage_name\|corr_abs_gt_0.995 | 0.9988130355127952 | 0.9754208252644124 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| progression_rate_pct | overseas_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.1218384021958973 | 0.4057798301802472 | exclude blocked_feature from this target model | auto_block_from_fail_audit |
| progression_rate_pct | has_progression | progression_lineage_name |  | 0.0001489646953671 | exclude blocked_feature from this target model | auto_block_from_fail_audit |

## 산출 파일

- 삭제 적용 D08 Parquet: `workbook/p2/p2_4/source_eda/strict_clean_v1/mart_department_model_base_2024_strict_drop.parquet`
- 삭제 적용 D08 CSV: `workbook/p2/p2_4/source_eda/strict_clean_v1/mart_department_model_base_2024_strict_drop.csv`
- 전체 행별 삭제 정책: `workbook/p2/p2_4/source_eda/strict_clean_v1/strict_row_policy_audit.csv`
- 삭제된 행 상세: `workbook/p2/p2_4/source_eda/strict_clean_v1/strict_deleted_rows_detail.csv`
- 타깃별 샘플 멤버십: `workbook/p2/p2_4/source_eda/strict_clean_v1/strict_target_sample_membership.csv`
- 타깃별 샘플 카운트: `workbook/p2/p2_4/source_eda/strict_clean_v1/strict_target_sample_counts.csv`
- strict feature registry: `workbook/p2/p2_4/source_eda/strict_clean_v1/strict_model_feature_registry.csv`
- target leakage denylist: `workbook/p2/p2_4/source_eda/strict_clean_v1/target_feature_exclusion_policy.csv`
- 사람이 필요한 항목: `workbook/p2/p2_4/source_eda/strict_clean_v1/human_required_after_strict_drop.csv`
- 최신 리뷰 레지스터: `workbook/p2/p2_4/source_eda/review_queues/human_review_action_register.csv`

## 이후 재실행 기준

1. 모델링/EDA는 strict D08를 입력으로 쓴다.
2. `strict_target_sample_membership.csv`에서 타깃별 `strict_target_keep=True`만 사용한다.
3. target-specific feature denylist를 모델 스펙에 반영한다.
4. `human_required_after_strict_drop.csv` 항목은 사람이 원천 제공 또는 제외 결정을 내리기 전까지 자동 보정하지 않는다.
