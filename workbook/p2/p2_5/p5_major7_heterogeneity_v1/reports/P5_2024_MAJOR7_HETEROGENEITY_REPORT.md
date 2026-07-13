# P5 2024 Major7 Grade-Signal Heterogeneity Report

## 1. 연구질문
같은 전공계열 안에서 학과별 A비율 또는 조건부 A비율 편차가 건강보험 취업률 및 대학원 진학률과 어떤 관계를 가지며, 그 관계의 기울기가 7개 전공계열 사이에서 어떻게 다른지 탐색했다.

## 2. 데이터와 표본
- D08: `workbook/p2/p2_4/source_eda/strict_clean_v1/mart_department_model_base_2024_strict_drop.parquet`
- D08 SHA256: `5f56e375fd1c0474a5e55652859ae007e2f45becd6d3350ee4c82e21fab8df9b`
- Structure sample: N=5,600, school_n=185
- Selectivity sample: N=2,355, school_n=130

## 3. Grade Signal 정의
- RAW_A: `a_rate_pct / 10`
- WITHIN_MAJOR_A: 같은 `major_group_7 × analysis_year` 평균에서 벗어난 A비율 편차 / 10
- OOF_RESIDUAL: P3 manifest가 제공될 때만 실행한다.

## 4. 계열별 cell eligibility
| branch | outcome | grade_signal | estimable_major_count |
| --- | --- | --- | --- |
| SELECTIVITY | GRAD_SCHOOL_PROGRESSION | RAW_A | 7 |
| SELECTIVITY | GRAD_SCHOOL_PROGRESSION | WITHIN_MAJOR_A | 7 |
| SELECTIVITY | HEALTH_EMPLOYMENT | RAW_A | 7 |
| SELECTIVITY | HEALTH_EMPLOYMENT | WITHIN_MAJOR_A | 7 |
| STRUCTURE | GRAD_SCHOOL_PROGRESSION | RAW_A | 7 |
| STRUCTURE | GRAD_SCHOOL_PROGRESSION | WITHIN_MAJOR_A | 7 |
| STRUCTURE | HEALTH_EMPLOYMENT | RAW_A | 7 |
| STRUCTURE | HEALTH_EMPLOYMENT | WITHIN_MAJOR_A | 7 |

## 5. 건강보험 취업 기울기
| grade_signal | cells | positive | negative | median_ame |
| --- | --- | --- | --- | --- |
| RAW_A | 7 | 4 | 3 | 0.007144458729515359 |
| WITHIN_MAJOR_A | 7 | 4 | 3 | 0.00714445872951518 |

## 6. 대학원 진학 기울기
| grade_signal | cells | positive | negative | median_ame |
| --- | --- | --- | --- | --- |
| RAW_A | 7 | 7 | 0 | 0.011690291773049801 |
| WITHIN_MAJOR_A | 7 | 7 | 0 | 0.01169029177304857 |

## 7. 취업·진학 차이
계열별 `AME_progression - AME_employment`는 `artifacts/P5_EMPLOYMENT_PROGRESSION_AME_DIFFERENCE.csv`에 저장했다. 이 차이는 탐색적 비교이며 확증적 검정 결론으로 사용하지 않는다.

## 8. 구조분기·입결분기 안정성
| outcome | grade_signal | compared_cells | sign_agreement_cells | ci_overlap_cells |
| --- | --- | --- | --- | --- |
| GRAD_SCHOOL_PROGRESSION | RAW_A | 7 | 5 | 6 |
| GRAD_SCHOOL_PROGRESSION | WITHIN_MAJOR_A | 7 | 5 | 7 |
| HEALTH_EMPLOYMENT | RAW_A | 7 | 6 | 7 |
| HEALTH_EMPLOYMENT | WITHIN_MAJOR_A | 7 | 6 | 7 |

## 9. 노동시장 context 기술 비교
Context는 `major_group_7` grain에서만 slope table과 결합했다. N=7 점 산점도와 Spearman rho는 기술적 참고값이며 context 효과를 주장하지 않는다.

## 10. 한계와 금지해석
- Fractional logit은 fractional response quasi-likelihood로 사용했다.
- 학과 단위 관측을 개인 Bernoulli 시행으로 해석하지 않는다.
- 특정 계열 context가 Grade Signal 효과를 높였다고 해석하지 않는다.
- 특정 학과 졸업생의 대기업 취업률이 높다는 식의 개인/학과 단정으로 확장하지 않는다.

## 11. P3 residual 대기 여부
`P5_RESIDUAL_BRANCH_STATUS = PENDING_UPSTREAM_RESIDUAL`

## 12. 미래 major7×year 확장 상태
`P5_MAJOR7_YEAR_STATUS = NOT_AVAILABLE`
