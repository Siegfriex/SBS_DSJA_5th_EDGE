# P4-2 Model Readiness Summary

최종 판정: `MODELING_BLOCKED_CONTRACT`

## 핵심 수치

- D08 source shape: `10242 x 151`
- analysis frame shape after membership: `10242 x 162`
- D08 SHA256: `598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962`
- key duplicate: `18`
- split leakage school count: `0`
- active feature count: `120`
- active all-null feature count: `0`
- target leakage FAIL: `16`
- sample registry mismatch: `0`
- sklearn available: `True`

## Target N

| target_group | target | split | non_null_n | school_n | major_n | mean | std | min | p01 | p05 | p25 | p50 | p75 | p95 | p99 | max | skewness | kurtosis | zero_ratio | hundred_ratio | unique_n | within_school_var | between_school_var | icc_approx |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| grade | a_rate_pct | train | 7529 | 140 | 7 | 41.94975662231445 | 17.30177116394043 | 0.0 | 0.0 | 13.083333396911636 | 32.57882308959961 | 39.97598648071289 | 50.14860534667969 | 73.70250244140621 | 92.94736480712893 | 100.0 | 0.37477296590805054 | 1.2885257005691528 | 0.03280648160446274 | 0.007570726524106787 | 6778 | 211.25244140625 | 127.98833465576172 | 0.37727874620934726 |
| grade | a_rate_pct | validation | 1514 | 30 | 7 | 41.106956481933594 | 15.499285697937012 | 0.0 | 0.0 | 20.0 | 32.4217004776001 | 39.06777381896973 | 49.062209129333496 | 69.05766830444335 | 87.98867141723626 | 100.0 | 0.4645269215106964 | 1.9102517366409302 | 0.023778071334214 | 0.0066050198150594455 | 1423 | 148.4541473388672 | 83.29933166503906 | 0.35943077110672 |
| employment | health_employment_rate_pct | train | 5494 | 131 | 7 | 52.46809768676758 | 19.091739654541016 | 0.0 | 0.0 | 20.541667079925567 | 41.379310607910156 | 52.44902038574219 | 63.6363639831543 | 85.71428680419922 | 100.0 | 100.0 | -0.03516039252281189 | 0.6047868728637695 | 0.019111758281761922 | 0.025482344375682562 | 1021 | 358.76519775390625 | 53.84953689575195 | 0.1305080317635151 |
| employment | health_employment_rate_pct | validation | 1127 | 30 | 7 | 52.85990905761719 | 19.230117797851562 | 0.0 | 0.0 | 20.0 | 40.0 | 53.846153259277344 | 63.7147331237793 | 85.71428680419922 | 100.0 | 100.0 | -0.07294780015945435 | 0.2744271755218506 | 0.01419698314108252 | 0.01774622892635315 | 441 | 415.53448486328125 | 60.67472839355469 | 0.12741191624285256 |
| employment | employment_rate_pct | train | 5494 | 131 | 7 | 61.1380500793457 | 17.49732780456543 | 0.0 | 0.0 | 33.33333206176758 | 50.0 | 61.53845977783203 | 71.42857360839844 | 91.42857360839844 | 100.0 | 100.0 | -0.31269240379333496 | 1.0658975839614868 | 0.011103021477975974 | 0.03421914816163087 | 974 | 291.7237243652344 | 48.79903030395508 | 0.14330622442944316 |
| employment | employment_rate_pct | validation | 1127 | 30 | 7 | 62.19026565551758 | 16.873165130615234 | 0.0 | 20.421621742248536 | 33.33333206176758 | 52.380950927734375 | 62.5 | 72.18706130981445 | 91.0457489013672 | 100.0 | 100.0 | -0.27652665972709656 | 0.9104023575782776 | 0.007985803016858917 | 0.025732031943212066 | 409 | 357.786865234375 | 45.714866638183594 | 0.11329534182178458 |
| progression | graduate_school_progression_rate_pct | train | 5566 | 138 | 7 | 7.979428768157959 | 12.84231948852539 | 0.0 | 0.0 | 0.0 | 0.0 | 2.3809523582458496 | 10.714285850524902 | 35.1804313659668 | 56.603995513916104 | 100.0 | 2.5402896404266357 | 8.424614906311035 | 0.43837585339561624 | 0.0008983111749910168 | 792 | 109.33934020996094 | 276.49932861328125 | 0.7166190196969326 |
| progression | graduate_school_progression_rate_pct | validation | 1147 | 30 | 7 | 9.240663528442383 | 14.563077926635742 | 0.0 | 0.0 | 0.0 | 0.0 | 2.941176414489746 | 12.799145221710205 | 39.355715560913104 | 66.66666412353516 | 100.0 | 2.5466392040252686 | 8.312554359436035 | 0.4115082824760244 | 0.0026155187445510027 | 337 | 192.947509765625 | 165.67636108398438 | 0.46197806267464425 |
| progression | progression_rate_pct | train | 5566 | 138 | 7 | 8.272462844848633 | 12.913000106811523 | 0.0 | 0.0 | 0.0 | 0.0 | 2.963125467300415 | 11.11111068725586 | 35.71428680419922 | 56.93181686401379 | 100.0 | 2.5065712928771973 | 8.229738235473633 | 0.4094502335609055 | 0.0008983111749910168 | 809 | 110.67138671875 | 275.6279602050781 | 0.7135087397893722 |
| progression | progression_rate_pct | validation | 1147 | 30 | 7 | 9.59257984161377 | 14.631012916564941 | 0.0 | 0.0 | 0.0 | 0.0 | 3.5714285373687744 | 13.043478012084961 | 39.355715560913104 | 66.66666412353516 | 100.0 | 2.512296199798584 | 8.089893341064453 | 0.3714036617262424 | 0.0026155187445510027 | 345 | 194.426513671875 | 171.30194091796875 | 0.4683855980253985 |

## Rank / VIF summary

| specification | n_rows | n_cols | rank | rank_deficiency | condition_number | min_singular_value | max_singular_value | complete_duplicate_columns_n | feature_before_encoding_n | meta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SPEC_FE | 7529 | 97 | 82 | 15 | inf | 3.1575599482262666e-16 | 48737.285005904814 | 3 | 30 | {"numeric_cols": ["has_major_group_7_high_medium", "admission_capacity_n", "recruitment_n", "applicants_n", "admits_n", "enrolled_students_n", "graduates_n", "fulltime_faculty_n", "nonfulltime_faculty_n", "competition_ratio", "admission_yield_ratio", "admit_per_applicant_ratio", "female_student_share_pct", "international_student_share_pct", "student_faculty_ratio", "fulltime_faculty_share_pct", "log_enrolled_students", "log_graduates", "has_selectivity", "selectivity_proxy_pct"], "categorical_cols": ["hc_major_group_7", "major_group_7", "campus_branch", "school_type", "region_sido", "field_middle_name"], "dropped_cols": ["degree_course_conflict_flag", "degree_course", "region_sigungu", "field_small_name"]} |
| SPEC_CTX24 | 7529 | 93 | 82 | 11 | inf | 1.0488014839660348e-17 | 4419320.442478857 | 2 | 40 | {"numeric_cols": ["admission_capacity_n", "recruitment_n", "applicants_n", "admits_n", "enrolled_students_n", "graduates_n", "fulltime_faculty_n", "nonfulltime_faculty_n", "competition_ratio", "admission_yield_ratio", "admit_per_applicant_ratio", "female_student_share_pct", "international_student_share_pct", "student_faculty_ratio", "fulltime_faculty_share_pct", "log_enrolled_students", "log_graduates", "has_selectivity", "selectivity_proxy_pct", "ctx24_reference_sample_n", "ctx24_mean_income_10kkrw", "ctx24_median_income_10kkrw", "ctx24_income_300plus_pct", "ctx24_income_400plus_pct", "ctx24_large_company_pct", "ctx24_mid_company_pct", "ctx24_small_company_pct", "ctx24_large_mid_company_pct", "ctx24_public_nonprofit_pct", "ctx24_cert_rate_pct", "ctx24_cert_per_person", "ctx24_log10_mean_income"], "categorical_cols": ["campus_branch", "school_type", "region_sido", "field_middle_name"], "dropped_cols": ["degree_course_conflict_flag", "degree_course", "region_sigungu", "field_small_name"]} |
| SPEC_GOMS | 7529 | 100 | 82 | 18 | inf | 4.0429875697927603e-16 | 52822.203084948145 | 2 | 53 | {"numeric_cols": ["admission_capacity_n", "recruitment_n", "applicants_n", "admits_n", "enrolled_students_n", "graduates_n", "fulltime_faculty_n", "nonfulltime_faculty_n", "competition_ratio", "admission_yield_ratio", "admit_per_applicant_ratio", "female_student_share_pct", "international_student_share_pct", "student_faculty_ratio", "fulltime_faculty_share_pct", "log_enrolled_students", "log_graduates", "has_selectivity", "selectivity_proxy_pct", "goms_recent_employment_rate_pct", "goms_recent_firm_300plus_pct", "goms_recent_public_nonprofit_pct", "goms_recent_permanent_pct", "goms_recent_unstable_pct", "goms_recent_self_employed_pct", "goms_recent_industry_hhi", "goms_recent_industry_top3_pct", "goms_recent_professional_highskill_pct", "goms_recent_mean_income_10kkrw", "goms_recent_weekly_work_hours", "goms_recent_hourly_income_proxy", "goms_income_trend_per_year", "goms_hours_trend_per_year", "goms_firm_300plus_trend_per_year", "goms_permanent_trend_per_year", "goms_latest_2019_mean_income_10kkrw", "goms_latest_2019_weekly_work_hours", "goms_latest_2019_firm_300plus_pct", "goms_latest_2019_permanent_pct"], "categorical_cols": ["campus_branch", "school_type", "region_sido", "field_middle_name"], "dropped_cols": ["degree_course_conflict_flag", "degree_course", "region_sigungu", "field_small_name", "goms_profile_start_year", "goms_profile_end_year", "goms_profile_years_n", "goms_aggregation_method", "goms_mapping_confidence", "goms_row_qa_status"]} |
| SPEC_INTERACTION | 7529 | 114 | 83 | 31 | inf | 9.858140192224485e-17 | 4419418.697304239 | 2 | 67 | {"numeric_cols": ["admission_capacity_n", "recruitment_n", "applicants_n", "admits_n", "enrolled_students_n", "graduates_n", "fulltime_faculty_n", "nonfulltime_faculty_n", "competition_ratio", "admission_yield_ratio", "admit_per_applicant_ratio", "female_student_share_pct", "international_student_share_pct", "student_faculty_ratio", "fulltime_faculty_share_pct", "log_enrolled_students", "log_graduates", "has_selectivity", "selectivity_proxy_pct", "a_rate_pct", "ctx24_reference_sample_n", "ctx24_mean_income_10kkrw", "ctx24_median_income_10kkrw", "ctx24_income_300plus_pct", "ctx24_income_400plus_pct", "ctx24_large_company_pct", "ctx24_mid_company_pct", "ctx24_small_company_pct", "ctx24_large_mid_company_pct", "ctx24_public_nonprofit_pct", "ctx24_cert_rate_pct", "ctx24_cert_per_person", "ctx24_log10_mean_income", "goms_recent_employment_rate_pct", "goms_recent_firm_300plus_pct", "goms_recent_public_nonprofit_pct", "goms_recent_permanent_pct", "goms_recent_unstable_pct", "goms_recent_self_employed_pct", "goms_recent_industry_hhi", "goms_recent_industry_top3_pct", "goms_recent_professional_highskill_pct", "goms_recent_mean_income_10kkrw", "goms_recent_weekly_work_hours", "goms_recent_hourly_income_proxy", "goms_income_trend_per_year", "goms_hours_trend_per_year", "goms_firm_300plus_trend_per_year", "goms_permanent_trend_per_year", "goms_latest_2019_mean_income_10kkrw", "goms_latest_2019_weekly_work_hours", "goms_latest_2019_firm_300plus_pct", "goms_latest_2019_permanent_pct"], "categorical_cols": ["campus_branch", "school_type", "region_sido", "field_middle_name"], "dropped_cols": ["degree_course_conflict_flag", "degree_course", "region_sigungu", "field_small_name", "goms_profile_start_year", "goms_profile_end_year", "goms_profile_years_n", "goms_aggregation_method", "goms_mapping_confidence", "goms_row_qa_status"]} |
| SPEC_MAJOR_PLUS_CTX24_GOMS_DIAGNOSTIC | 7529 | 50 | 15 | 35 | inf | 1.4944388245155103e-33 | 4419349.74971916 | 0 | 42 | {"numeric_cols": ["has_major_group_7_high_medium", "ctx24_reference_sample_n", "ctx24_mean_income_10kkrw", "ctx24_median_income_10kkrw", "ctx24_income_300plus_pct", "ctx24_income_400plus_pct", "ctx24_large_company_pct", "ctx24_mid_company_pct", "ctx24_small_company_pct", "ctx24_large_mid_company_pct", "ctx24_public_nonprofit_pct", "ctx24_cert_rate_pct", "ctx24_cert_per_person", "ctx24_log10_mean_income", "goms_recent_employment_rate_pct", "goms_recent_firm_300plus_pct", "goms_recent_public_nonprofit_pct", "goms_recent_permanent_pct", "goms_recent_unstable_pct", "goms_recent_self_employed_pct", "goms_recent_industry_hhi", "goms_recent_industry_top3_pct", "goms_recent_professional_highskill_pct", "goms_recent_mean_income_10kkrw", "goms_recent_weekly_work_hours", "goms_recent_hourly_income_proxy", "goms_income_trend_per_year", "goms_hours_trend_per_year", "goms_firm_300plus_trend_per_year", "goms_permanent_trend_per_year", "goms_latest_2019_mean_income_10kkrw", "goms_latest_2019_weekly_work_hours", "goms_latest_2019_firm_300plus_pct", "goms_latest_2019_permanent_pct"], "categorical_cols": ["hc_major_group_7", "major_group_7"], "dropped_cols": ["goms_profile_start_year", "goms_profile_end_year", "goms_profile_years_n", "goms_aggregation_method", "goms_mapping_confidence", "goms_row_qa_status"]} |

## Model feasibility

| model_family | readiness | n_rows_train | n_schools_train | n_features_before_encoding | n_features_after_encoding | rows_per_parameter | minimum_school_cluster_size | median_school_cluster_size | singleton_schools |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OLS_cluster | READY | 7529 | 140 | 69 | 130 | 57.91538461538462 | 1 | 48.5 | 7 |
| MixedLM | READY | 7529 | 140 | 69 | 130 | 57.91538461538462 | 1 | 48.5 | 7 |
| School_fixed_effects | READY | 7529 | 140 | 69 | 130 | 57.91538461538462 | 1 | 48.5 | 7 |
| GAM | OPTIONAL_PACKAGE_CHECK | 7529 | 140 | 69 | 130 | 57.91538461538462 | 1 | 48.5 | 7 |
| Ridge | READY | 7529 | 140 | 69 | 130 | 57.91538461538462 | 1 | 48.5 | 7 |
| Elastic_Net | READY | 7529 | 140 | 69 | 130 | 57.91538461538462 | 1 | 48.5 | 7 |
| Gradient_Boosting | READY | 7529 | 140 | 69 | 130 | 57.91538461538462 | 1 | 48.5 | 7 |
| Context_interaction | READY | 7529 | 140 | 69 | 130 | 57.91538461538462 | 1 | 48.5 | 7 |
| Softmax_panel | BLOCKED_PANEL_DATA | 7529 | 140 | 69 | 130 | 57.91538461538462 | 1 | 48.5 | 7 |

## Panel / Softmax

Panel과 Softmax는 별도 상태다. 2023~2025 panel/transition parquet가 없으면 `BLOCKED_PANEL_DATA`지만, 2024 단면 모델링 READY 여부와 분리한다.

## 이후 실행 순서

1. `p2_G4_2.ipynb - current readiness gate`
2. `p4_2_grade_formation.ipynb - only after P4_MODELING_READY`
3. `p4_3_grade_leniency_oof.ipynb`
4. `p4_4_employment_progression.ipynb`
5. `p4_5_context_interactions.ipynb`
6. `p4_6_ml_benchmark.ipynb`
7. `p4_7_panel_fixed_effects.ipynb - only if panel_ready`
8. `p4_8_adam_softmax.ipynb - only if transition panel ready`
9. `p4_9_integrated_findings.ipynb`
