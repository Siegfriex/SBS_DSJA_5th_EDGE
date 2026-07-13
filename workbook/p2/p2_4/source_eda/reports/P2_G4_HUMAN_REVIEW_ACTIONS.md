# P2-G4 Human Review Action Report

- 생성시각: `2026-07-13T10:56:16`
- 기준 모델 테이블: `workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet`
- 검토 큐 폴더: `workbook/p2/p2_4/source_eda/review_queues`
- 액션 레지스터: `workbook/p2/p2_4/source_eda/review_queues/human_review_action_register.csv`

## 핵심 결론

현재 자동 파이프라인이 더 진행되기 전에 사람이 판단해야 할 항목은 있다. 특히 `target leakage`, 구조 매칭 미확정, D08 key duplicate, `major_group_7` 미확정 라벨은 모델링 게이트를 직접 막거나 표본 정의를 흔드는 P0 항목이다.

자동으로 `drop_duplicates()` 하거나 결측을 0으로 채우면 안 된다. 아래 큐에서 사람이 승인값을 채운 뒤, 브리지/레지스트리/모델 스펙을 갱신하고 D08 계열 산출물을 재빌드하는 순서가 맞다.

## 액션 레지스터

| id | priority | review_area | rows_or_items | queue_path | source_path | required_human_decision |
| --- | --- | --- | --- | --- | --- | --- |
| HR-001 | P0 | target leakage | 16 | workbook/p2/p2_4/source_eda/review_queues/target_leakage_feature_exclusion_review.csv | workbook/p2/p2_4/p4_2_model_readiness/qa/target_leakage_audit.csv | 타깃별로 금지 피처인지 확정하고 모델 스펙/레지스트리에 target-specific exclusion을 반영 |
| HR-002 | P0 | structure match manual/unmatched | 1681 | workbook/p2/p2_4/source_eda/review_queues/structure_match_human_review_queue.csv | workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_outcome_headcount_v2.csv | outcome_row_id별 승인 headcount_row_id 또는 unmatched/exclude 판정 |
| HR-003 | P0 | D08 duplicate key/campus identity | 36 | workbook/p2/p2_4/source_eda/review_queues/d08_key_duplicate_human_review_queue.csv | workbook/p2/p2_4/p4_2_model_readiness/qa/d08_key_duplicate_detail.csv | 동일 headcount UID 중복이 실제 중복인지 캠퍼스/학과 분리인지 판정 |
| HR-004 | P0 | major_group_7 human labeling | 143 | workbook/p2/p2_4/source_eda/review_queues/major7_human_label_review_queue.csv | workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_department_major7_v2.csv | HUM/SOC/EDU/ENG/NAT/MED/ART 중 하나 또는 샘플 제외 라벨 확정 |
| HR-005 | P1 | special-term major rules | 67 | workbook/p2/p2_4/source_eda/review_queues/major7_special_term_review_queue.csv | workbook/p2/p2_4/p4_1_data_contract/qa/major7_special_term_search.csv | 자유전공/융합/AI/바이오 등 특수명칭의 전공계열 규칙 확정 |
| HR-006 | P1 | missingness and selection bias | 104 | workbook/p2/p2_4/source_eda/review_queues/missingness_bias_human_review_queue.csv | workbook/p2/p2_4/p4_2_model_readiness/qa/missingness_selection_audit.csv | 결측이 구조적 결측/관측 불가/표본 제한/대체 가능 중 무엇인지 정책 확정 |
| HR-007 | P1 | rate extremes with small denominators | 1264 | workbook/p2/p2_4/source_eda/review_queues/rate_extreme_small_denominator_review_queue.csv | workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet | 0/100% 비율이 작은 분모의 정상값인지 이상치/제외/가중치 대상인지 판정 |
| HR-008 | P1 | all-null/source unavailable fields | 22 | workbook/p2/p2_4/source_eda/review_queues/all_null_or_source_unavailable_review_queue.csv | workbook/p2/p2_4/source_eda/tables/target_like_column_inventory.csv | 재수집/재생성할지, placeholder로 유지할지, feature에서 제거할지 확정 |
| HR-009 | P2 | unseen category encoding policy | 6 | workbook/p2/p2_4/source_eda/review_queues/unseen_category_policy_review_queue.csv | workbook/p2/p2_4/p4_2_model_readiness/qa/unseen_category_audit.csv | 식별자는 피처에서 제외하고 실제 범주형은 unknown 처리할지 확정 |
| HR-010 | P2 | panel/softmax source missing | 2 | workbook/p2/p2_4/source_eda/review_queues/panel_source_missing_review_queue.csv | workbook/p2/p2_4/p4_2_model_readiness/qa/panel_softmax_readiness.csv | 2023-2025 패널을 새로 만들지, 해당 트랙을 계속 BLOCKED로 둘지 확정 |
| HR-011 | P2 | job-cert bridge design | 32 | workbook/p2/p2_4/source_eda/review_queues/job_cert_bridge_design_review_queue.csv | workbook/p2/p2_3/p4_handoff_candidate/shared/department_model_column_registry.csv | 직무분류 자료를 학과/계열에 연결할 브리지 키와 집계 수준을 설계 |
| HR-012 | P1 | normalized department duplicate names | 8 | workbook/p2/p2_4/source_eda/review_queues/normalized_department_duplicate_review_queue.csv | workbook/p2/p2_4/p4_1_data_contract/qa/d08_normalized_name_duplicate_rows.csv | 중점/가운뎃점 제거 후 같은 학과가 된 행을 병합할지 별도 유지할지 확정 |

## 현재 상태 요약

### 구조 매칭 상태

| match_status | rows |
| --- | --- |
| auto_high_confidence | 8561 |
| manual_pending | 1316 |
| unmatched | 365 |

검토가 필요한 구조 매칭 사유:

| unmatched_reason | rows |
| --- | --- |
| multiple_fuzzy_or_conflict | 672 |
| multiple_candidates | 644 |
| department_formatting_or_source_coverage_mismatch | 189 |
| no_candidate | 152 |
| campus_mismatch | 24 |

D08 row QA 상태:

| row_qa_status | rows |
| --- | --- |
| ok | 8561 |
| manual_match_pending | 1316 |
| review_unmatched | 365 |

### major_group_7 상태

| major7_mapping_method | rows |
| --- | --- |
| inherited_headcount | 8561 |
| keyword_rule | 859 |
| exact_dictionary | 679 |
| ambiguous | 85 |
| unknown | 58 |

### 레지스트리 제외/사용 사유

| registry_reason | columns |
| --- | --- |
| candidate_feature_or_context | 120 |
| job_cert_bridge_direct_join_prohibited | 32 |
| identifier_label_or_qa_metadata | 23 |
| ctx24_wage_reference_context | 13 |
| target_candidate_not_feature | 6 |
| all_null_source_unavailable | 4 |

### target leakage 실패 요약

| target | failed_feature_n |
| --- | --- |
| employment_rate_pct | 2 |
| graduate_school_progression_rate_pct | 6 |
| health_employment_rate_pct | 2 |
| progression_rate_pct | 6 |

### 비율형 타깃 극단값 요약

| column | non_null_n | zero_n | hundred_n | min | max |
| --- | --- | --- | --- | --- | --- |
| a_rate_pct | 10242 | 319 | 79 | 0.0 | 100.0 |
| cd_rate_pct | 10242 | 475 | 55 | 0.0 | 100.0 |
| f_rate_pct | 10242 | 1808 | 40 | 0.0 | 100.0 |
| employment_rate_pct | 7477 | 78 | 252 | 0.0 | 100.0 |
| health_employment_rate_pct | 7477 | 136 | 180 | 0.0 | 100.0 |
| progression_rate_pct | 7587 | 3098 | 8 | 0.0 | 100.0 |
| graduate_school_progression_rate_pct | 7587 | 3343 | 8 | 0.0 | 100.0 |

## 상세 검토 항목

### HR-001 Target Leakage Feature Exclusion

- 검토 큐: `workbook/p2/p2_4/source_eda/review_queues/target_leakage_feature_exclusion_review.csv`
- 원본 QA: `workbook/p2/p2_4/p4_2_model_readiness/qa/target_leakage_audit.csv`
- 수정 대상 후보: `workbook/p2/p2_3/p4_handoff_candidate/shared/department_model_column_registry.csv` 및 모델별 feature set/specification 생성 로직
- 건수: `16` target-feature 조합
- 사람이 확인할 것: 같은 타깃 패밀리 결과변수, 타깃 자기 자신, `has_*` 관측 플래그가 해당 타깃 모델에서 피처로 들어가면 안 되는지 확정한다.
- 수정 방향: 전역 `p4_use=False`만으로는 부족할 수 있다. `employment_rate_pct`는 employment 타깃에는 누수지만 grade 모델의 설명변수로는 별도 논의가 필요하므로 target-specific denylist를 두는 편이 안전하다.
- 사람이 채울 컬럼: `human_decision`, `target_specific_exclusion`, `registry_or_model_spec_change`, `reviewer_note`

실패 조합 미리보기:

| target | feature | reasons | abs_corr_train_validation | deterministic_equal_rate |
| --- | --- | --- | --- | --- |
| health_employment_rate_pct | employment_rate_pct | same_target_family_outcome\|employment_lineage_name | 0.8102478276975554 | 0.254493278960882 |
| health_employment_rate_pct | has_employment | employment_lineage_name |  | 0.0 |
| employment_rate_pct | employment_rate_pct | same_as_target\|corr_abs_gt_0.995\|deterministic_equality | 1.0 | 1.0 |
| employment_rate_pct | has_employment | employment_lineage_name |  | 0.0 |
| graduate_school_progression_rate_pct | progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.9947958618143944 | 0.9058543125279308 |
| graduate_school_progression_rate_pct | vocational_college_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.0230136402500334 | 0.4275286757038581 |
| graduate_school_progression_rate_pct | university_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.0240808251406509 | 0.422910770147475 |
| graduate_school_progression_rate_pct | domestic_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.9938044852313588 | 0.8912557723819455 |
| graduate_school_progression_rate_pct | overseas_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.1173446512741289 | 0.4361686280351556 |
| graduate_school_progression_rate_pct | has_progression | progression_lineage_name |  | 0.0001489646953671 |
| progression_rate_pct | progression_rate_pct | same_as_target\|corr_abs_gt_0.995\|deterministic_equality | 1.0 | 1.0 |
| progression_rate_pct | vocational_college_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.0475804611375327 | 0.4136749590347088 |
| progression_rate_pct | university_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.0975347058503601 | 0.4214211231938031 |
| progression_rate_pct | domestic_progression_rate_pct | same_target_family_outcome\|progression_lineage_name\|corr_abs_gt_0.995 | 0.9988130355127952 | 0.9754208252644124 |
| progression_rate_pct | overseas_progression_rate_pct | same_target_family_outcome\|progression_lineage_name | 0.1218384021958973 | 0.4057798301802472 |
| progression_rate_pct | has_progression | progression_lineage_name |  | 0.0001489646953671 |

### HR-002 Structure Match Manual/Unmatched Queue

- 검토 큐: `workbook/p2/p2_4/source_eda/review_queues/structure_match_human_review_queue.csv`
- 원본 브리지: `workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_outcome_headcount_v2.csv`
- 기준 D08: `workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet`
- 건수: `1681` rows (`manual_pending=1316`, `unmatched=365`)
- 사람이 확인할 것: `candidate_preview`, `candidate_headcount_row_ids`, `match_evidence`, 학교/캠퍼스/학과명을 보고 올바른 `headcount_row_id`를 승인할지, unmatched로 남길지 판단한다.
- 수정 방향: 승인된 행은 `bridge_outcome_headcount_v2.csv`에 반영하고 D03/D08을 재빌드한다. 애매한 행은 구조 컨텍스트가 필요한 샘플에서 제외한다.
- 사람이 채울 컬럼: `human_match_decision`, `approved_headcount_row_id`, `approved_match_method`, `campus_policy`, `alias_rule_to_add`, `reviewer_note`

### HR-003 D08 Duplicate Key/Campus Identity

- 검토 큐: `workbook/p2/p2_4/source_eda/review_queues/d08_key_duplicate_human_review_queue.csv`
- 원본 QA: `workbook/p2/p2_4/p4_2_model_readiness/qa/d08_key_duplicate_detail.csv`
- 관련 QA: `workbook/p2/p2_4/p4_1_data_contract/qa/d08_headcount_uid_duplicate_rows.csv`
- 건수: `36` rows, 18 carried headcount UID duplicate cases
- 사람이 확인할 것: 같은 `school_uid/campus_uid/dept_uid`에 outcome row가 둘 이상 붙은 경우가 실제 중복인지, 캠퍼스 구분 누락인지, 학부/학과 명칭 차이인지 확인한다.
- 대표 사례: 고려대 본교/세종 분교, 단국대 뉴뮤직학부/뉴뮤직과, 연세대/충남대/우석대/한남대의 중점 문자 제거 후 중복.
- 수정 방향: 캠퍼스 alias를 분리해야 하면 `bridge_campus_alias.csv`와 `campus_uid` 생성 로직을 고친다. 실제 중복이면 outcome spine에서 병합/제외 정책을 문서화한다.
- 사람이 채울 컬럼: `human_duplicate_decision`, `campus_uid_fix`, `dept_uid_fix`, `row_keep_drop_or_split`, `reviewer_note`

### HR-012 Normalized Department Duplicate Names

- 검토 큐: `workbook/p2/p2_4/source_eda/review_queues/normalized_department_duplicate_review_queue.csv`
- 원본 QA: `workbook/p2/p2_4/p4_1_data_contract/qa/d08_normalized_name_duplicate_rows.csv`
- 건수: `8` rows
- 사람이 확인할 것: `문화・미디어전공` vs `문화미디어전공`처럼 정규화 후 같아지는 학과명이 실제 같은 모집단위인지 별도 모집단위인지 판단한다.
- 수정 방향: 같은 단위면 canonical name/merge rule을 추가하고, 별도 단위면 normalized key에 disambiguator를 추가한다.

### HR-004 major_group_7 Human Labeling

- 검토 큐: `workbook/p2/p2_4/source_eda/review_queues/major7_human_label_review_queue.csv`
- 원본 브리지: `workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_department_major7_v2.csv`
- 샘플 검토 파일: `workbook/p2/p2_4/p4_1_data_contract/samples/major7_mapping_sample.csv`
- 건수: `143` rows (`ambiguous=85`, `unknown=58`)
- 사람이 확인할 것: 학과명을 보고 `HUM`, `SOC`, `EDU`, `ENG`, `NAT`, `MED`, `ART` 중 하나를 부여하거나 major-context 샘플에서 제외할지 확정한다.
- 수정 방향: 확정 라벨은 `bridge_department_major7_v2.csv` 또는 별도 human label overlay에 반영하고, 반복되는 패턴은 dictionary/keyword rule로 승격한다.
- 사람이 채울 컬럼: `human_major_group_7`, `major_label_decision`, `dictionary_rule_to_add`, `exclude_from_major_samples`, `reviewer_note`

### HR-005 Special-Term Major Rules

- 검토 큐: `workbook/p2/p2_4/source_eda/review_queues/major7_special_term_review_queue.csv`
- 원본 QA: `workbook/p2/p2_4/p4_1_data_contract/qa/major7_special_term_search.csv`
- 건수: `67` rows
- 사람이 확인할 것: 자유전공, 융합, 데이터사이언스, 바이오, 산업디자인, 교육공학, 의공학, 문화콘텐츠, 스포츠과학, AI, 반도체 등 이름만으로 계열이 흔들리는 항목의 라벨 규칙을 정한다.
- 수정 방향: 사람이 승인한 특수어 규칙만 dictionary/keyword rule에 추가한다. 자동 승격 금지.

### HR-006 Missingness And Selection Bias Policy

- 검토 큐: `workbook/p2/p2_4/source_eda/review_queues/missingness_bias_human_review_queue.csv`
- 원본 QA: `workbook/p2/p2_4/p4_2_model_readiness/qa/missingness_selection_audit.csv`
- 건수: `104` diagnostic rows
- 사람이 확인할 것: 결측이 구조적 결측인지, 원천 미제공인지, 관측 대상이 아닌지, 표본 선택 편향인지 구분한다. 0과 결측을 섞으면 안 된다.
- 특히 `has_selectivity`, `has_employment`, `has_progression`, `structural_match_eligible`, `major_context_eligible`는 관측 여부 자체가 학교유형/지역/계열/분모와 연동된다.
- 수정 방향: 무조건 대체하지 말고, target별 사용 가능 표본 제한, missing indicator, 가중치/층화, 또는 해당 분석 제외 중 하나를 선택한다.

상위 진단 미리보기:

| audit_type | flag | group_col | group_value | feature | observed_rate | smd | ks_statistic | cramers_v |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| numeric_observed_vs_unobserved | has_progression |  |  | has_employment |  | 12.352477187099083 | 0.9870643190801294 |  |
| numeric_observed_vs_unobserved | has_employment |  |  | has_progression |  | 7.382478093498334 | 0.9646191646191646 |  |
| numeric_observed_vs_unobserved | major_context_eligible |  |  | headcount_match_flag |  | 3.3619208502385325 | 0.8496696777672914 |  |
| numeric_observed_vs_unobserved | major_context_eligible |  |  | candidate_count |  | -0.9937302080410862 | 0.7907040293534159 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  | applicants_n |  | 0.7901784497911345 | 0.6806534781179718 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  | admits_n |  | 0.7632249674348867 | 0.6248541583626361 |  |
| numeric_observed_vs_unobserved | has_employment |  |  | domestic_progression_rate_pct |  | -0.7378748059272766 | 0.3456093072891235 |  |
| numeric_observed_vs_unobserved | has_employment |  |  | progression_rate_pct |  | -0.7359246015548706 | 0.3446992635726928 |  |
| numeric_observed_vs_unobserved | has_progression |  |  | graduates_n |  | 0.6296163907092743 | 0.9583886925234874 |  |
| numeric_observed_vs_unobserved | has_employment |  |  | graduates_n |  | 0.6151877664550554 | 0.9216573475682932 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  | admit_per_applicant_ratio |  | -0.5712520480155945 | 0.2360873222351074 |  |
| numeric_observed_vs_unobserved | structural_match_eligible |  |  | campus_conflict_flag |  | -0.5707894602774168 | 0.1401792991035045 |  |
| numeric_observed_vs_unobserved | structural_match_eligible |  |  | candidate_count |  | -0.553968217385755 | 0.534637326813366 |  |
| numeric_observed_vs_unobserved | major_context_eligible |  |  | campus_conflict_flag |  | -0.5230373667660475 | 0.1490145707737052 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  | admission_capacity_n |  | 0.1570098928984071 | 0.6887072177692 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  | recruitment_n |  | 0.1533250644802032 | 0.6547928847032093 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  | has_selectivity |  |  | 1.0 |  |
| numeric_observed_vs_unobserved | has_employment |  |  | has_employment |  |  | 1.0 |  |
| numeric_observed_vs_unobserved | has_progression |  |  | has_progression |  |  | 1.0 |  |
| numeric_observed_vs_unobserved | structural_match_eligible |  |  | headcount_match_flag |  |  | 1.0 |  |

### HR-007 Rate Extremes With Small Denominators

- 검토 큐: `workbook/p2/p2_4/source_eda/review_queues/rate_extreme_small_denominator_review_queue.csv`
- 원본 D08: `workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet`
- 건수: `1264` rows
- 필터 조건: 비율 컬럼 중 하나가 `0` 또는 `100`이고, `graduates_n <= 5` 또는 `enrolled_students_n <= 20`.
- 사람이 확인할 것: 0/100%가 원천 공식상 정상값인지, 분모가 너무 작아 모델에서 가중치/제외가 필요한지, 원천 계산 오류인지 판정한다.
- 수정 방향: 값 자체가 정상이라면 수정하지 말고 small-n flag/가중치 정책을 둔다. 오류라면 원천 D02/D08 재생성 단계에서 고친다.

### HR-008 All-Null Or Source-Unavailable Fields

- 검토 큐: `workbook/p2/p2_4/source_eda/review_queues/all_null_or_source_unavailable_review_queue.csv`
- 컬럼 인벤토리: `workbook/p2/p2_4/source_eda/tables/target_like_column_inventory.csv`
- 레지스트리: `workbook/p2/p2_3/p4_handoff_candidate/shared/department_model_column_registry.csv`
- 건수: `22` rows
- 사람이 확인할 것: `ctx24_industry_top3_pct`, `ctx24_industry_hhi`는 2024 D08/D04에서 all-null source unavailable이다. 2023 sample의 `selectivity_proxy_pct`, health/progression 세부율도 all-null이다.
- 수정 방향: 필요한 분석이면 원천을 새로 만들거나 재수집한다. 현재 데이터로 분석하지 않을 항목이면 명시적으로 제외하고 placeholder로만 유지한다.

### HR-009 Unseen Category Encoding Policy

- 검토 큐: `workbook/p2/p2_4/source_eda/review_queues/unseen_category_policy_review_queue.csv`
- 원본 QA: `workbook/p2/p2_4/p4_2_model_readiness/qa/unseen_category_audit.csv`
- 건수: `6` feature rows
- 사람이 확인할 것: `school_uid_x`, `school_uid_y`처럼 split상 당연히 unseen인 식별자는 모델 피처에서 제외해야 한다. 실제 범주형인 `campus_name_raw_x`의 `분교|ERICA` 같은 값은 unknown category 처리 정책을 정한다.
- 수정 방향: 식별자/UID는 feature registry에서 제외하고, 진짜 범주형은 OneHotEncoder unknown handling 또는 rare bucket 정책을 둔다.

### HR-010 Panel/Softmax Source Missing

- 검토 큐: `workbook/p2/p2_4/source_eda/review_queues/panel_source_missing_review_queue.csv`
- 원본 QA: `workbook/p2/p2_4/p4_2_model_readiness/qa/panel_softmax_readiness.csv`
- 누락 파일: `mart_department_panel_2023_2025.parquet`, `mart_A_rate_transition_2023_2025.parquet`
- 사람이 확인할 것: 2023-2025 패널을 실제로 만들 것인지, 이번 P4에서는 단면 2024 분석만 할 것인지 결정한다.
- 수정 방향: 패널을 원하면 2023/2025 outcome+headcount를 같은 spine으로 재구축해야 한다. 아니면 Adam-Softmax/패널 트랙은 계속 `BLOCKED_PANEL_DATA`로 둔다.

### HR-011 Job-Cert Bridge Design

- 검토 큐: `workbook/p2/p2_4/source_eda/review_queues/job_cert_bridge_design_review_queue.csv`
- 원본 D05/레지스트리: `workbook/p2/p2_3/p4_handoff_candidate/shared/department_model_column_registry.csv`
- 건수: `32` columns
- 사람이 확인할 것: 직무분류 기반 자격증 자료를 학과/전공/계열에 어떤 키로 연결할지 설계해야 한다.
- 수정 방향: 승인된 브리지 없이 D05를 D08 학과행에 직접 조인하지 않는다. 계열 수준 집계만 쓸지, 학과명 키워드 브리지를 만들지 먼저 결정한다.

## 권장 작업 순서

1. `HR-001` target leakage denylist를 확정한다.
2. `HR-002`, `HR-003`, `HR-012`로 D08 spine/구조 매칭을 먼저 안정화한다.
3. `HR-004`, `HR-005` 전공계열 라벨을 사람이 확정한다.
4. `HR-006`, `HR-007`, `HR-008`로 결측/극단값/원천 부재 정책을 문서화한다.
5. `HR-009` 인코딩 정책을 반영한 뒤, 모델 readiness를 재실행한다.
6. 패널 분석이 필요할 때만 `HR-010`을 진행한다.

## 산출 큐 파일 목록

| id | priority | review_area | rows_or_items | queue_path |
| --- | --- | --- | --- | --- |
| HR-001 | P0 | target leakage | 16 | workbook/p2/p2_4/source_eda/review_queues/target_leakage_feature_exclusion_review.csv |
| HR-002 | P0 | structure match manual/unmatched | 1681 | workbook/p2/p2_4/source_eda/review_queues/structure_match_human_review_queue.csv |
| HR-003 | P0 | D08 duplicate key/campus identity | 36 | workbook/p2/p2_4/source_eda/review_queues/d08_key_duplicate_human_review_queue.csv |
| HR-004 | P0 | major_group_7 human labeling | 143 | workbook/p2/p2_4/source_eda/review_queues/major7_human_label_review_queue.csv |
| HR-005 | P1 | special-term major rules | 67 | workbook/p2/p2_4/source_eda/review_queues/major7_special_term_review_queue.csv |
| HR-006 | P1 | missingness and selection bias | 104 | workbook/p2/p2_4/source_eda/review_queues/missingness_bias_human_review_queue.csv |
| HR-007 | P1 | rate extremes with small denominators | 1264 | workbook/p2/p2_4/source_eda/review_queues/rate_extreme_small_denominator_review_queue.csv |
| HR-008 | P1 | all-null/source unavailable fields | 22 | workbook/p2/p2_4/source_eda/review_queues/all_null_or_source_unavailable_review_queue.csv |
| HR-009 | P2 | unseen category encoding policy | 6 | workbook/p2/p2_4/source_eda/review_queues/unseen_category_policy_review_queue.csv |
| HR-010 | P2 | panel/softmax source missing | 2 | workbook/p2/p2_4/source_eda/review_queues/panel_source_missing_review_queue.csv |
| HR-011 | P2 | job-cert bridge design | 32 | workbook/p2/p2_4/source_eda/review_queues/job_cert_bridge_design_review_queue.csv |
| HR-012 | P1 | normalized department duplicate names | 8 | workbook/p2/p2_4/source_eda/review_queues/normalized_department_duplicate_review_queue.csv |
