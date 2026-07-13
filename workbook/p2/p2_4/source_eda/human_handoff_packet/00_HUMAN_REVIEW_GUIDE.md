# P2-G4 Human Review Handoff Guide

- 생성시각: `2026-07-13T11:37:48`
- 패킷 루트: `workbook/p2/p2_4/source_eda/human_handoff_packet`
- strict-clean 기준 보고서: `workbook/p2/p2_4/source_eda/reports/P2_G4_STRICT_DROP_AND_REVIEW_UPDATE.md`

## 1. 검토 목표

이 패킷은 P2-G4 모델링 전 단계에서 사람이 반드시 판단해야 하는 잔여 항목만 넘기기 위한 것이다. 구조적으로 애매한 학과행, 캠퍼스 충돌, major_group_7 미확정, duplicate key/name, 소표본 0/100 극단 비율 행은 이미 strict-clean 산출물에서 삭제했다.

따라서 사람 검토자는 삭제된 2,650행 전체를 다시 라벨링할 필요가 없다. 기본 원칙은 `삭제 유지`이며, 특정 행을 반드시 살려야 할 근거가 있을 때만 `deleted_row_recovery_sheet.csv`에 승인 내용을 쓴다.

## 2. 먼저 열 파일

1. `01_DECISION_SHEETS/human_required_decision_sheet.csv`
2. `01_DECISION_SHEETS/decision_codebook.csv`
3. 필요할 때만 `02_EVIDENCE/strict_deleted_rows_detail.csv`
4. target leakage 예외 검토가 필요할 때만 `01_DECISION_SHEETS/target_leakage_override_sheet.csv`

사람이 직접 채워야 하는 파일은 `01_DECISION_SHEETS/` 아래 파일뿐이다. `02_EVIDENCE/`와 `03_MODEL_INPUT/` 파일은 증빙/입력 파일이므로 직접 수정하지 않는다.

## 3. 이번에 사람이 판단할 항목 요약

| priority | issue_type | agent_default_decision | items |
| --- | --- | --- | --- |
| P1 | missing_panel_source | keep_panel_blocked | 2 |
| P1 | source_unavailable_all_null | exclude_from_features | 2 |
| P2 | bridge_design_required | keep_D05_excluded | 1 |
| P2 | historical_2023_target_unavailable | exclude_2023_target | 8 |

전체 사람 판단 항목은 `13`건이다. 우선순위 `P1`은 원천 부재라서 모델링 범위를 바로 막는 항목이고, `P2`는 확장 분석 또는 추가 feature 편입 여부를 결정하는 항목이다.

## 4. 결정값 작성 규칙

### 4.1 공통 컬럼

- `human_decision`: 반드시 `allowed_human_decisions` 중 하나만 입력한다.
- `human_decision_detail`: 사람이 판단한 근거를 한 문장 이상으로 적는다.
- `source_fix_path_or_evidence`: 원천 파일을 새로 주거나 수정했다면 실제 경로를 적는다. 제외 결정이면 `not_applicable`로 둔다.
- `reviewer`: 검토자 이름 또는 이니셜.
- `review_date`: `YYYY-MM-DD` 형식.
- `final_status`: `approved`, `rejected`, `deferred` 중 하나로 마감한다.

빈칸으로 두면 후속 자동화에서 승인된 결정으로 보지 않는다.

### 4.2 source_unavailable_all_null

대상: `ctx24_industry_hhi`, `ctx24_industry_top3_pct`.

문제: D04/D08 관련 산출물에서 해당 변수가 전부 비어 있다. 일부 행 결측이 아니라 변수 원천 자체가 비어 있으므로 행 삭제로 해결되지 않는다.

허용 결정값:

- `exclude_from_features`: 현재 P4에서는 feature에서 제외한다. 기본 권장값이다.
- `rebuild_source`: 이 변수를 만들 원천과 산식을 사람이 제공한다.
- `defer`: 이번 모델링에서는 보류한다.

`rebuild_source`를 고르면 `source_fix_path_or_evidence`에 실제 원천 파일 경로를 적고, `human_decision_detail`에 산식과 key grain을 적어야 한다.

### 4.3 missing_panel_source

대상: `mart_department_panel_2023_2025.parquet`, `mart_A_rate_transition_2023_2025.parquet`.

문제: panel/transition parquet 자체가 없다. 현재 파일 경로가 비어 있으므로 자동 보정이 불가능하다.

허용 결정값:

- `keep_panel_blocked`: panel 트랙은 막고 2024 단년도 strict-clean 모델링만 진행한다. 기본 권장값이다.
- `build_panel_sources`: panel parquet를 새로 만든다.
- `drop_panel_track`: 이번 P4 범위에서 panel 트랙을 제외한다.

`build_panel_sources`를 고르면 생성될 parquet의 key grain, 기간, target 컬럼, 담당자를 적는다.

### 4.4 bridge_design_required

대상: D05 job_cert columns.

문제: D05는 직무분류 축 데이터라 학과행에 직접 붙이면 분석 단위가 맞지 않는다. 직접 조인은 금지한다.

허용 결정값:

- `keep_D05_excluded`: 이번 모델링에서는 제외한다. 기본 권장값이다.
- `design_bridge_and_aggregate`: 직무분류->계열/학과 bridge와 집계 규칙을 설계한다.
- `drop_D05_scope`: 이번 P4 전체 범위에서 D05를 제외한다.

`design_bridge_and_aggregate`를 고르면 매핑 키, 다대다 처리, 가중치, 집계 함수, 검증 기준을 적어야 한다.

### 4.5 historical_2023_target_unavailable

대상: `dept_outcomes_2023_sample.csv`의 8개 target-like 컬럼.

문제: 2023 확장 표본 11,287행에서 해당 컬럼이 전부 비어 있다. 현재 상태에서는 2023 확장 타깃으로 사용할 수 없다.

허용 결정값:

- `exclude_2023_target`: 해당 2023 타깃 컬럼을 분석에서 제외한다. 기본 권장값이다.
- `provide_2023_source`: 2023 원천 파일과 산식을 제공한다.
- `drop_2023_extension`: 2023 확장 분석 자체를 제외한다.

`provide_2023_source`를 고르면 원천 파일 경로, 컬럼명, 산식, 결측 허용 기준을 적어야 한다.

## 5. 삭제 행 복구 규칙

strict-clean에서 삭제된 행은 `02_EVIDENCE/strict_deleted_rows_detail.csv`에 남아 있다. 기본 원칙은 삭제 유지다.

특정 행을 복구하려면 `01_DECISION_SHEETS/deleted_row_recovery_sheet.csv`에 아래를 모두 채운다.

- `outcome_row_id`: 복구할 행 ID
- `recover_yn`: `Y` 또는 `N`
- `recovery_reason`: 왜 삭제 정책보다 복구가 맞는지
- `corrected_school_name`, `corrected_campus_name`, `corrected_dept_name`, `corrected_major_group_7`: 사람이 확정한 값
- `corrected_match_status`: 복구 후 기대 상태. 원칙적으로 `auto_high_confidence` 또는 그에 준하는 승인 상태여야 한다.
- `corrected_source_path_or_rule`: 수정 근거 파일 또는 규칙

복구 행은 단순히 `살림`으로 처리하지 않는다. 수정 근거가 없는 행은 계속 삭제 유지한다.

## 6. Target leakage 예외 규칙

`01_DECISION_SHEETS/target_leakage_override_sheet.csv`에는 16개의 leakage FAIL 조합이 들어 있다. 기본 결정은 모두 `keep_blocked`다.

예외적으로 허용하려면 `override_with_written_justification`을 쓰고, 왜 해당 feature가 타깃 누수가 아닌지 데이터 생성 시점과 산식 기준으로 설명해야 한다. 상관계수가 높다는 이유만으로 허용할 수 없다.

## 7. 검토 완료 기준

검토 완료로 인정하려면 다음 조건을 만족해야 한다.

1. `human_required_decision_sheet.csv`의 13행 모두 `human_decision`, `human_decision_detail`, `reviewer`, `review_date`, `final_status`가 채워져 있다.
2. `human_decision`은 각 행의 `allowed_human_decisions` 중 하나다.
3. source를 새로 제공하는 결정은 실제 파일 경로와 산식이 있다.
4. D05 bridge 설계 결정은 key grain과 집계 규칙이 있다.
5. deleted row 복구가 있으면 `deleted_row_recovery_sheet.csv`에 outcome_row_id와 수정 근거가 있다.
6. target leakage override가 있으면 데이터 생성 시점 기준의 비누수 근거가 있다.

## 8. 사람이 결정한 뒤 엔지니어가 할 일

- 제외 결정만 있으면 strict-clean 입력을 그대로 쓴다.
- 원천 재생성 또는 2023 source 제공이 있으면 해당 원천을 반영해 D08/registry/target sample을 재빌드한다.
- D05 bridge 설계가 승인되면 직접 조인이 아니라 bridge 집계 산출물을 만든 뒤 feature registry에 편입한다.
- deleted row recovery가 승인되면 복구 overlay를 만든 뒤 strict row policy audit을 다시 생성한다.
- target leakage override가 승인되면 target별 모델 스펙에만 반영하고 전역 feature 허용으로 처리하지 않는다.

## 9. 패킷 파일 맵

- `00_HUMAN_REVIEW_GUIDE.md`: 이 문서
- `01_DECISION_SHEETS/human_required_decision_sheet.csv`: 사람이 반드시 채울 13건
- `01_DECISION_SHEETS/decision_codebook.csv`: issue_type별 허용 결정값
- `01_DECISION_SHEETS/deleted_row_recovery_sheet.csv`: 삭제 행 복구 요청용 빈 템플릿
- `01_DECISION_SHEETS/target_leakage_override_sheet.csv`: leakage FAIL 예외 승인용
- `02_EVIDENCE/strict_deleted_rows_detail.csv`: 삭제된 2,650행 상세
- `02_EVIDENCE/strict_row_policy_audit.csv`: 전체 10,242행의 strict 삭제 정책 플래그
- `02_EVIDENCE/strict_drop_reason_counts.csv`: 삭제 사유별 건수
- `02_EVIDENCE/strict_target_sample_counts.csv`: 타깃별 사용 가능 표본 수
- `02_EVIDENCE/strict_model_feature_registry.csv`: strict feature registry
- `03_MODEL_INPUT/mart_department_model_base_2024_strict_drop.parquet`: 모델링 기본 입력
- `03_MODEL_INPUT/mart_department_model_base_2024_strict_drop.csv`: CSV 버전 모델링 기본 입력
- `04_REPORTS/P2_G4_STRICT_DROP_AND_REVIEW_UPDATE.md`: strict 삭제 정책 보고서

## 10. 현재 판단 대상 13건

| review_id | priority | issue_type | path | item | agent_default_decision |
| --- | --- | --- | --- | --- | --- |
| HR-001 | P1 | source_unavailable_all_null | workbook/p2/p2_3/p4_handoff_candidate/shared/department_model_column_registry.csv | ctx24_industry_hhi (datasets=D04,D08_v2; missing_n_sum=10256) | exclude_from_features |
| HR-002 | P1 | source_unavailable_all_null | workbook/p2/p2_3/p4_handoff_candidate/shared/department_model_column_registry.csv | ctx24_industry_top3_pct (datasets=D04,D08_v2; missing_n_sum=10256) | exclude_from_features |
| HR-003 | P1 | missing_panel_source | workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_panel_2023_2025.parquet | mart_department_panel_2023_2025 | keep_panel_blocked |
| HR-004 | P1 | missing_panel_source | workbook/p2/p2_3/p4_handoff_candidate/shared/mart_A_rate_transition_2023_2025.parquet | mart_A_rate_transition_2023_2025 | keep_panel_blocked |
| HR-005 | P2 | bridge_design_required | workbook/p2/p2_3/p4_handoff_candidate/shared/department_model_column_registry.csv | D05 job_cert columns | keep_D05_excluded |
| HR-006 | P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | domestic_progression_rate_pct | exclude_2023_target |
| HR-007 | P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | graduate_school_progression_rate_pct | exclude_2023_target |
| HR-008 | P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | health_employment_rate_pct | exclude_2023_target |
| HR-009 | P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | overseas_progression_rate_pct | exclude_2023_target |
| HR-010 | P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | progression_rate_pct | exclude_2023_target |
| HR-011 | P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | selectivity_proxy_pct | exclude_2023_target |
| HR-012 | P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | university_progression_rate_pct | exclude_2023_target |
| HR-013 | P2 | historical_2023_target_unavailable | workbook/p2/p2_4/dept_outcomes_2023_sample.csv | vocational_college_progression_rate_pct | exclude_2023_target |
