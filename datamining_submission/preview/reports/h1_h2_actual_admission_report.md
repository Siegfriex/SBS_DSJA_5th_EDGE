# H1/H2/H3 실제 입결 기반 확장 분석 보고

## 1. 분석 계약

- 입결 기준연도: 2024
- 학점 기준연도: 2024
- 주 입결 원천 컬럼: `raw_percentile_70cut`
- 주 분석 피처: 0~100 범위로 정제한 `selectivity_pct_2024`
- 기존 대학순위 프록시 분석은 `H1-Baseline`으로 보존했고, 이 섹션은 실제 입결 기반 확장 분석이다.

## 2. 표본

| sample | rows | universities | departments |
| --- | --- | --- | --- |
| department_model_all_matched | 1216 | 35 | 544 |
| primary_sample_tier_a_only | 80 | 2 | 71 |
| analysis_sample_tier_a_b | 1186 | 35 | 528 |

## 3. H1-Main

- Spearman rho=0.163, p=0.000, 대학군집 bootstrap 95% CI=[-0.139, 0.412].
- 전공계열 통제 + 대학 군집표준오차 회귀의 selectivity 계수=0.220, p=0.159.

## 4. H1-Within University

- 대학 고정효과 모형의 selectivity 계수=0.007, p=0.854.
- between/within 분해의 within 계수=-0.018, p=0.725.

## 5. H2

- 대학 단위 실제 입결 통제 OLS에서 학점포기제 계수=-4.329, p=0.154.
- 학과 단위 보조모형에서 학점포기제 계수=-2.004, p=0.513.

## 6. H3

| model | term | outcome | coef | p | n | universities | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H3 actual-selectivity residual university outcome Spearman | actual_a_residual_mean_pctp | official_employment_rate_pct | 0.2568627450980392 | 0.13634168359523455 | 35 | 35 | 대학별 실제 입결 기대 A비율 잔차와 성과지표의 탐색 상관. |
| H3 actual-selectivity residual university outcome Spearman | actual_a_residual_mean_pctp | health_employment_rate_pct | 0.33613445378151263 | 0.04835385268616848 | 35 | 35 | 대학별 실제 입결 기대 A비율 잔차와 성과지표의 탐색 상관. |
| H3 actual-selectivity residual university outcome Spearman | actual_a_residual_mean_pctp | overall_advancement_rate_pct | 0.39355742296918766 | 0.019333417631588894 | 35 | 35 | 대학별 실제 입결 기대 A비율 잔차와 성과지표의 탐색 상관. |
| H3 actual-selectivity residual university outcome Spearman | actual_a_residual_mean_pctp | graduate_school_rate_pct | 0.392436974789916 | 0.019711849169670947 | 35 | 35 | 대학별 실제 입결 기대 A비율 잔차와 성과지표의 탐색 상관. |

## 7. 산출물

- `data/actual_admission_2024/department_h1_h2_actual_admission_2024.csv`
- `data/actual_admission_2024/actual_admission_h1_h2_h3_result_summary_2024.csv`
- `evidence/claim_evidence_matrix_actual_admission_2024.csv`
- `figures/actual_admission_2024/`

## 8. 해석 한계

- `raw_percentile_70cut`는 주 컬럼으로 사용했지만, 100 초과 값은 대학별 환산점수로 의심되어 제외했다.
- loose key만 일치하는 모집단위는 자동 확정하지 않았다.
- 학점포기제는 O/X만 있으므로 기준연도·허용학점·재수강상한 같은 정책 강도는 아직 통제하지 못했다.
- 모든 문장은 인과가 아니라 연관성으로 써야 한다.