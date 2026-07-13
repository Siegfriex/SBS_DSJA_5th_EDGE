# P2-G4 최종 다층 연구·모형 설계 v3.0

## 0. 연구의 최종 질문

본 연구는 다음을 검증한다.

> 대학·학과별 A비율이 입결·전공·학과구조·성적제도와 어떤 조건부 관계를 갖는지 분석하고, 이들 관측조건으로 예측되지 않는 A비율 편차가 유지취업성과와 대학원 진학성과 중 어느 쪽에 더 큰 추가정보를 제공하는지 검증한다. 또한 이 관계가 전공계열별 노동시장 환경과 외부연도에서도 어떻게 달라지는지 탐색한다.

연구의 핵심 연쇄는 다음이다.

```text
P1  A비율과 취업·진학의 기술적 정렬
P2  A비율의 구조적 설명
P3  Cross-fitted 조건부 A비율 편차
P4  조건부 A비율 편차의 유지취업·진학 검증
P5  major7×year 노동시장 환경에 따른 이질성
P6  학점·취업·진학 잔차공간의 유형화
P7  Ridge–XGBoost 비선형 benchmark
P8  2023~2025 패널·시차·외부연도 검증
```

핵심 confirmatory chain은 다음이다.

```text
P2 → P3 → P4
```

P1은 기술적·시각적 정렬, P5와 P6은 탐색적 확장, P7은 예측 보조검증, P8은 시간적 재현 검증이다.

---

# 1. 세 가지 측정수준

## Level 1 — 학과-연도

관측단위:

```text
school_uid × department_entity_id × year
```

실제 학과 수준 관측값:

```text
a_rate_pct
graded_students_n                  # 존재하는 경우

graduates_n
initial_employed_n
retained_1_n
retained_2_n
retained_3_n
retained_4_n
graduate_school_progressors_n

health_employment_rate_pct
graduate_school_progression_rate_pct

selectivity_proxy_pct
competition_ratio
student_faculty_ratio
fulltime_faculty_share_pct
enrolled_students_n
graduates_n
leave_rate_pct
```

이 수준에서만 특정 대학·학과의 A비율, 유지취업률, 진학률을 말할 수 있다.

---

## Level 2 — 전공계열-연도

관측단위:

```text
major_group_7 × year
```

변수:

```text
major_ctx_income_300plus_pct
major_ctx_income_400plus_pct
major_ctx_firm_300plus_pct
major_ctx_public_nonprofit_pct
major_ctx_permanent_pct
major_ctx_professional_highskill_pct
```

정확한 의미:

> 해당 학과가 속한 전공계열의 해당 연도 노동시장 환경.

의미하지 않는 것:

> 해당 대학·학과 졸업생의 실제 임금·기업규모·직업구조.

동일한 `major_group_7 × year`에 속하는 모든 학과에는 동일한 context 값이 반복된다.

---

## Level 3 — 전공계열 장기 노동시장 경로

관측단위:

```text
major_group_7 × year, 2007~2019
```

원시 형태는 최대:

```text
7개 계열 × 13개 연도 = 91행
```

모델용 요약형:

```text
major_group_7
goms_hist_income_mean
goms_hist_income_trend
goms_hist_income_volatility
goms_hist_firm300_mean
goms_hist_firm300_trend
goms_hist_permanent_mean
goms_hist_permanent_trend
goms_hist_industry_hhi_mean
goms_hist_industry_hhi_volatility
```

GOMS는 학과 outcome이 아니라 해당 전공계열의 장기 노동시장 프로파일이다.

---

# 2. 최종 데이터마트 계약

## 2.1 현재 2024년 분석마트

```text
mart_department_model_base_2024.parquet
```

한 행:

```text
학교 × 캠퍼스 × 학과 × 2024년
```

현재 확정 표본:

| 표본                       | 전체 usable | 고신뢰 구조표본 |
| ------------------------ | --------: | -------: |
| `GRADE_ALL`              |    10,099 |    8,561 |
| `GRADE_SELECTIVITY`      |     3,707 |    3,198 |
| `EMPLOYMENT_HEALTH`      |     7,389 |    6,270 |
| `PROGRESSION_GRADSCHOOL` |     7,498 |    6,366 |
| `JOINT_EMP_PROG`         |     7,389 |    6,270 |

---

## 2.2 학과 패널

```text
mart_department_panel_2023_2025.parquet
```

Grain:

```text
school_uid × department_entity_id × year
```

필수 key:

```text
school_uid
campus_uid
department_entity_id
year
major_group_7
```

필수 outcome:

```text
a_rate_pct
graduates_n
initial_employed_n
retained_1_n
retained_2_n
retained_3_n
retained_4_n
graduate_school_progressors_n
```

필수 학과조건:

```text
selectivity_proxy_pct
competition_ratio
enrolled_students_n
fulltime_faculty_n
student_faculty_ratio
fulltime_faculty_share_pct
leave_rate_pct
credit_forfeit_flag
```

---

## 2.3 계열-연도 노동시장 context

```text
mart_major7_context_2023_2025.parquet
```

Grain:

```text
major_group_7 × year
```

예시:

```text
major_group_7
year
major_ctx_income_300plus_pct
major_ctx_income_400plus_pct
major_ctx_firm_300plus_pct
major_ctx_public_nonprofit_pct
major_ctx_permanent_pct
major_ctx_professional_highskill_pct
```

---

## 2.4 GOMS 장기 context

원시형:

```text
mart_major7_goms_history_long.parquet
```

Grain:

```text
major_group_7 × year, 2007~2019
```

요약형:

```text
mart_major7_goms_history_summary.parquet
```

Grain:

```text
major_group_7
```

---

## 2.5 최종 조인

```text
mart_department_panel_2023_2025
LEFT JOIN mart_major7_context_2023_2025
    ON major_group_7, year

LEFT JOIN mart_major7_goms_history_summary
    ON major_group_7
```

최종 산출:

```text
mart_department_panel_context_2023_2025.parquet
```

조인 후 보존할 metadata:

```text
context_grain = "major7_year"
context_is_department_observed = False
context_source
context_reference_year
context_repeat_count
goms_history_window = "2007_2019"
goms_is_department_observed = False
```

금지 컬럼명:

```text
dept_income_400plus_pct
dept_firm_300plus_pct
```

허용 컬럼명:

```text
major_ctx_income_400plus_pct
major_ctx_firm_300plus_pct
goms_hist_income_trend
```

---

# 3. 비율·분자·분모 계약

## 3.1 유지취업

각 유지차수 (k)에 대해:

[
RetentionRate^{(k)}_{ist}
=========================

\frac{Retained^{(k)}*{ist}}
{InitialEmployed*{ist}}
]

파생 컬럼:

```text
retention_1_prop
retention_2_prop
retention_3_prop
retention_4_prop
```

Primary retention outcome:

```text
retained_4_n / initial_employed_n
```

이유:

> 최초 취업 여부보다 중장기 고용유지에 더 가까운 결과이기 때문.

Secondary:

```text
retention_1_prop
retention_2_prop
retention_3_prop
```

---

## 3.2 대학원 진학

[
ProgressionRate_{ist}
=====================

\frac{GraduateSchoolProgressors_{ist}}
{Graduates_{ist}}
]

파생:

```text
graduate_school_progression_prop
```

---

## 3.3 모델링 내부 단위

보고용:

```text
*_pct = 0~100
```

모델용:

```text
*_prop = 0~1
```

Count:

```text
Int64, 0 이상
```

유효성 검사:

```text
0 <= retained_k_n <= initial_employed_n
0 <= graduate_school_progressors_n <= graduates_n
denominator > 0
```

---

## 3.4 Count-ready gate

```text
RETENTION_COUNT_READY
PROGRESSION_COUNT_READY
GRADE_COUNT_READY
```

분자·분모가 모두 존재하면 aggregated binomial을 primary로 사용한다.

분자·분모가 없고 비율만 있으면:

```text
Fractional logit
+ denominator proxy weight
```

를 사용한다.

OLS는 percentage-point 해석용 민감도 모형으로 남긴다.

---

# 4. 핵심 Grade Signal

## 4.1 실제 A비율

```text
a_rate_pct
a_rate_prop
```

질문:

> A비율 자체가 유지취업·진학과 연결되는가?

---

## 4.2 Within-major-year A비율

[
A^{within}_{ist}
================

A_{ist}-\overline A_{gt}
]

파생:

```text
a_rate_major_year_mean
a_rate_within_major_year
```

질문:

> 같은 연도·같은 전공계열의 다른 학과보다 A비율이 높은 학과가 성과도 다른가?

---

## 4.3 Cross-fitted 조건부 잔차

[
GradeResidual_{ist}^{OOF}
=========================

A_{ist}-\widehat A_{ist}^{OOF}
]

질문:

> 입결·전공·학과규모·교원여건·성적제도가 비슷한 학과에 비해 예상보다 높은 A비율이 성과와 연결되는가?

연구의 primary grade signal:

```text
grade_residual_oof
```

Secondary grade signals:

```text
a_rate_pct
a_rate_within_major_year
```

---

# P1. A비율과 두 시장의 기술적 정렬

## 데이터프레임

```text
p1_signal_alignment_2024.parquet
```

Source:

```text
JOINT_EMP_PROG_STRUCTURE
N = 6,270
```

## 타깃

```text
y = a_rate_pct
```

## 피처

Base:

```text
S0
B
Policy
```

시장성과:

```text
health_employment_rate_pct
graduate_school_progression_rate_pct
```

## 주모형

[
A_i
===

\beta_0
+f_E(Employment_i)
+f_P(Progression_i)
+\gamma^\top X_i
+\epsilon_i
]

```text
GAM
```

## 민감도

```text
OLS + school-clustered SE
School fixed-effects OLS
```

## 역할

P1은 관계의 모양과 방향을 제시한다.

허용:

> 두 방향의 조건부 회귀에서 일관된 시장정렬이 관찰됐다.

금지:

> 취업률 또는 진학률이 A비율을 결정했다.

---

# P2. A비율 형성모형

## P2-S — 구조분기

데이터프레임:

```text
p2_grade_formation_structure.parquet
```

표본:

```text
GRADE_STRUCTURE
N = 8,561
```

타깃:

```text
a_rate_pct
```

동일표본 중첩모형:

```text
P2-S0 = intercept
P2-S1 = S0
P2-S2 = S0 + B
P2-S3 = S0 + B + Policy
```

주모형:

```text
OLS + school-clustered SE
GAM
MixedLM
School FE
```

---

## P2-Q — 입결분기

데이터프레임:

```text
p2_grade_formation_selectivity.parquet
```

표본:

```text
GRADE_SELECTIVITY_STRUCTURE
N = 3,198
```

동일표본 중첩모형:

```text
P2-Q0 = intercept
P2-Q1 = S0
P2-Q2 = S0 + B
P2-Q3 = S0 + B + Q
P2-Q4 = S0 + B + Q + Policy
```

입결 블록의 추가 설명력:

[
\Delta R_Q^2
============

R^2(P2\text{-}Q3)-R^2(P2\text{-}Q2)
]

구조분기와 입결분기의 R²를 직접 차감하지 않는다.

---

# P3. Nested cross-fitted Grade Residual

## P3-S

```text
source = p2_grade_formation_structure.parquet
N = 8,561
X = S0 + B + Policy
y = a_rate_pct
```

산출:

```text
grade_residual_structure_oof
```

## P3-Q

```text
source = p2_grade_formation_selectivity.parquet
N = 3,198
X = S0 + B + Q + Policy
y = a_rate_pct
```

산출:

```text
grade_residual_selectivity_oof
```

## 모형

```text
Ridge
```

## Nested GroupKFold

```text
Outer GroupKFold:
학교 단위 OOF prediction

Inner GroupKFold:
Ridge alpha 선택
```

각 outer fold 안에서 다시 fit:

```text
median imputer
missing indicator
OneHotEncoder
StandardScaler
Ridge alpha
```

금지 피처:

```text
employment outcome
retention outcome
progression outcome
major-year income/firm context
```

---

# P4. Grade Signal의 유지취업·진학 결과 검증

P4가 핵심 confirmatory 단계다.

## P4-S — 구조분기

데이터프레임:

```text
p4_outcome_validation_structure.parquet
```

표본:

```text
JOINT_EMP_PROG_STRUCTURE
+ P3-S residual
최대 N = 6,270
```

Base:

```text
S0 + B + Policy
```

Grade signal 대안:

```text
a_rate_prop
a_rate_within_major_year
grade_residual_structure_oof
```

---

## P4-Q — 입결분기

데이터프레임:

```text
p4_outcome_validation_selectivity.parquet
```

표본:

```text
JOINT_EMP_PROG_SELECTIVITY
+ P3-Q residual
```

Base:

```text
S0 + B + Q + Policy
```

Grade signal 대안:

```text
a_rate_prop
a_rate_within_major_year
grade_residual_selectivity_oof
```

---

## P4-E — 유지취업 모형

Primary, count-ready일 때:

[
Retained^{(4)}*{ist}
\sim
Binomial
\left(
InitialEmployed*{ist},
p^{(4)}_{ist}
\right)
]

[
logit(p^{(4)}_{ist})
====================

\alpha_s+\mu_g
+\beta GradeSignal_{ist}
+\gamma^\top X_{ist}
]

* (\alpha_s): 학교효과
* (\mu_g): major7 효과
* (X): 구조·입결·정책 통제

Secondary:

```text
retained_1_n
retained_2_n
retained_3_n
```

Count가 없을 때:

```text
Fractional logit on health_employment_rate_prop
OLS percentage-point sensitivity
```

---

## P4-P — 대학원 진학 모형

[
Progressors_{ist}
\sim
Binomial
\left(
Graduates_{ist},
q_{ist}
\right)
]

[
logit(q_{ist})
==============

\alpha_s+\mu_g
+\beta GradeSignal_{ist}
+\gamma^\top X_{ist}
]

Count가 없을 때:

```text
Fractional logit on graduate_school_progression_prop
```

---

## P4 핵심 비교

모형에 Grade Signal을 추가하기 전후를 비교한다.

```text
Base
Base + raw A
Base + within-major-year A
Base + grade residual
```

평가:

```text
Likelihood ratio
Pseudo R²
CV log loss
CV Brier score
CV MAE on rates
school bootstrap CI
```

취업과 진학의 차이:

[
D
=

## IncrementalValue_{Progression}

IncrementalValue_{Retention}
]

## Generated regressor 보정

학교 bootstrap마다 전체 파이프라인을 다시 수행한다.

```text
학교 bootstrap
→ P3 cross-fitting
→ grade residual 재생성
→ P4 유지취업모형
→ P4 진학모형
→ 효과·성능차 저장
```

---

# P5. Major7-year context에 따른 이질성

## 위치

```text
Exploratory heterogeneity analysis
```

2024 단면만 있을 때:

```text
7개 major cell
→ 기술적 비교만 가능
```

2023~2025 패널이 있을 때:

```text
7개 major × 3개 year
→ 최대 21개 major-year cell
```

---

## P5 1단계 — Cell별 Grade Signal slope

데이터프레임:

```text
p5_department_major_year_cells.parquet
```

각 `major_group_7 × year` cell 안에서 별도 모형을 적합한다.

유지취업:

[
logit(p_{ist}^{(4)})
====================

\alpha_{gt}
+\beta^{E}*{gt}GradeSignal*{ist}
+\gamma^\top X_{ist}
]

진학:

[
logit(q_{ist})
==============

\alpha_{gt}
+\beta^{P}*{gt}GradeSignal*{ist}
+\gamma^\top X_{ist}
]

산출:

```text
major_group_7
year
beta_grade_retention
se_grade_retention
beta_grade_progression
se_grade_progression
n_departments
total_initial_employed_n
total_graduates_n
```

---

## P5 2단계 — Slope와 context 비교

데이터프레임:

```text
p5_major_year_slope_context.parquet
```

Grain:

```text
major_group_7 × year
```

조인:

```text
P5 1단계 slope
+ mart_major7_context_2023_2025
```

별도 모형:

[
\widehat\beta_{gt}
==================

\theta_0
+\theta_1Context_{gt}
+u_{gt}
]

사전 지정 context는 각각 별도 모형으로 검토한다.

```text
major_ctx_firm_300plus_pct
major_ctx_income_400plus_pct
major_ctx_permanent_pct
```

한 모형에 3개를 모두 넣지 않는다.

가중치:

[
w_{gt}
======

\frac{1}
{SE(\widehat\beta_{gt})^2+\tau^2}
]

분석:

```text
weighted meta-regression
scatter plot
effect-size CI
leave-one-major-out sensitivity
```

21개 cell뿐이므로 유의성보다 방향과 효과크기를 중심으로 해석한다.

허용:

> 대기업 비중이 높은 major-year cell에서 grade-signal slope가 더 큰 패턴이 관찰됐다.

금지:

> 대기업 비중이 grade-signal 효과를 증가시켰다.

---

## GOMS의 P5 사용

GOMS 요약은 계열별 7개 값이므로 통계적 회귀의 독립표본으로 사용하지 않는다.

사용:

```text
계열 프로파일 카드
계열별 slope 해석
major7 ablation
민감도 시각화
```

비교모형:

```text
Model A:
major_group_7 fixed effect
GOMS 제외

Model B:
GOMS historical profile
major_group_7 fixed effect 제외
```

---

# P6. Grade–Retention–Progression Residual Topology

## 데이터프레임

```text
p6_department_residual_space.parquet
```

필수 residual:

```text
grade_residual_oof
retention_residual_oof
progression_residual_oof
```

## Outcome residual 생성

유지취업 expected model:

```text
S0 + B + Q + Policy
Grade Signal 제외
```

진학 expected model:

```text
S0 + B + Q + Policy
Grade Signal 제외
```

동일 조건:

```text
같은 TYPE_READY 표본
같은 school fold
같은 preprocessing
OOF prediction
```

Binomial outcome에서는 raw pp residual보다 다음을 사용한다.

```text
OOF deviance residual
또는
standardized Pearson residual
```

최종 공간:

```text
z_grade
z_retention
z_progression
```

---

## Primary typology — 8개 octant

```text
G+ R+ P+
G+ R+ P-
G+ R- P+
G+ R- P-
G- R+ P+
G- R+ P-
G- R- P+
G- R- P-
```

각 학과는 정확히 한 유형에 속한다.

Neutral zone 민감도:

```text
negative / neutral / positive
```

적용 시 27개 cell이 생기므로 희소 cell 병합규칙을 사전 지정한다.

---

## GMM 검증

```text
k = 1,...,8
```

선택:

```text
BIC
bootstrap stability
minimum cluster size
theoretical octant agreement
```

이론 유형과 실제 GMM 군집이 일치하지 않는 것도 유효한 결과다.

---

## 유형 설명모형

타깃:

```text
octant_label
```

피처:

```text
S0 + B + Q + Policy
```

금지:

```text
세 residual
원래 A비율
원래 retention/progression outcome
type 생성에 직접 사용된 값
```

모형:

```text
얕은 Decision Tree
Random Forest sensitivity
```

---

# P7. Ridge–XGBoost 비선형 benchmark

## Task A — A비율 형성

```text
source = p2_grade_formation_structure/selectivity
y = a_rate_prop
X = S0 + B + Q + Policy
```

## Task B — 유지취업

Count-ready:

```text
y = retention_4_prop
sample_weight = initial_employed_n
```

## Task C — 대학원 진학

```text
y = graduate_school_progression_prop
sample_weight = graduates_n
```

## 모델

```text
Mean/prevalence baseline
Ridge
XGBoost
```

XGBoost outcome objective:

```text
A비율: squared error 또는 logistic-bounded regression
Retention/Progression: reg:logistic + denominator weights
```

검증:

```text
GroupKFold by school
locked school test
paired school bootstrap
```

평가:

```text
MAE
RMSE
R²
Spearman
Log loss
Brier score
Calibration
```

XGBoost는 Ridge보다 일관된 외부성능 개선이 있을 때만 채택한다.

---

# P8. 2023~2025 시간 확장

## P8-0 — Entity linkage gate

모델 실행 전 다음을 해결한다.

```text
학과명 변경
학과 통폐합
학과 분리
캠퍼스 변경
학과코드 재사용
모집단위 변경
outcome grain 변경
```

필수 파일:

```text
dim_department_entity_history.parquet
```

P8의 신뢰도는 모델보다 entity bridge에 더 크게 좌우된다.

---

## P8-A — 동시점 학과 패널모형

질문:

> 같은 학과에서 A비율이 평소보다 높았던 해에 유지취업·진학도 함께 변했는가?

유지취업:

[
Retained^{(4)}*{it}
\sim Binomial(InitialEmployed*{it},p_{it})
]

[
logit(p_{it})
=============

\alpha_i+\lambda_t
+\beta GradeSignal_{it}
+\gamma^\top X_{it}
]

진학:

[
Progressors_{it}
\sim Binomial(Graduates_{it},q_{it})
]

[
logit(q_{it})
=============

\alpha_i+\lambda_t
+\beta GradeSignal_{it}
+\gamma^\top X_{it}
]

* (\alpha_i): 학과 fixed effect
* (\lambda_t): year fixed effect

GOMS·major context의 시간불변 부분은 학과 FE에 흡수되므로 이 모형에서는 제외한다.

해석:

> 동일 학과 내부의 동시점 조건부 연관.

---

## P8-B — 시차 결과모형

질문:

> 이전 연도 grading climate가 다음 연도 유지취업·진학성과에 선행적으로 연결되는가?

전이 데이터:

```text
mart_department_transition_2023_2025.parquet
```

한 행:

```text
department_entity_id × t→t+1
```

전이:

```text
2023→2024
2024→2025
```

타깃:

```text
retained_4_n_t1 / initial_employed_n_t1
graduate_school_progressors_n_t1 / graduates_n_t1
```

피처:

```text
a_rate_pct_t
a_rate_within_major_year_t
grade_residual_oof_t

selectivity_proxy_pct_t
competition_ratio_t
student_faculty_ratio_t
fulltime_faculty_share_pct_t
log_enrolled_students_t
log_graduates_t
credit_forfeit_flag_t
```

Model A:

```text
major_group_7 fixed effects
major context 제외
```

Model B:

```text
major-year context_t
major_group_7 fixed effects 제외 또는 축소
```

모형:

```text
Aggregated binomial GLM
school fixed effect
transition-year fixed effect
school-clustered SE
```

해석:

> 이전 연도 A비율 또는 A잔차가 다음 연도 성과와 선행적으로 연결됐다.

인과 주장은 아니다.

---

## P8-C — 다음 해 A비율 변화 예측

회귀 타깃:

[
\Delta A_{i,t+1}
================

A_{i,t+1}-A_{i,t}
]

분류 타깃:

```text
0 = 감소
1 = 유지
2 = 증가
```

피처:

```text
a_rate_pct_t
health_employment_rate_t
retention_4_prop_t
graduate_school_progression_prop_t
selectivity_proxy_pct_t
structure_t
policy_t
major context_t
```

금지:

```text
t+1 feature
delta_A 계산에 사용된 미래정보
미래 outcome
```

모델:

```text
Ridge
Multinomial Logistic
XGBoost
```

시간 검증:

```text
Train/validation:
2023 → 2024

Final out-of-time test:
2024 → 2025
```

---

# 5. Within-major-year 분석 규칙

다음 파생변수를 패널 전체에 생성한다.

```text
a_rate_major_year_mean
a_rate_within_major_year

retention_major_year_mean
retention_within_major_year

progression_major_year_mean
progression_within_major_year
```

하지만 count outcome의 주모형에서는 단순 centered rate만 쓰기보다:

```text
raw Grade Signal
+ major_group_7×year fixed effect
```

를 우선한다.

두 접근은 민감도로 비교한다.

---

# 6. Estimand와 가중치

## 비가중 분석

각 학과를 동일한 단위로 본다.

> 평균적인 학과에서의 관계.

## Count-binomial 분석

분모가 큰 학과가 더 많은 정보를 제공한다.

> 평균적인 취업자·졸업생 사건 확률과 연결된 관계.

Primary:

```text
유지취업·진학:
count-binomial
```

Sensitivity:

```text
학과 비가중 fractional logit
```

A비율:

```text
Primary:
학과 비가중 OLS/GAM

Sensitivity:
graded_students_n 가중
분자·분모 존재 시 binomial/beta-binomial
```

---

# 7. 코호트 불일치 제한

현재 연도별 A비율은 해당 연도의 학과 평가환경이다.

그러나 해당 연도 졸업자의 실제 학점 노출은 재학기간 전체에 걸쳐 형성된다.

따라서:

```text
A_rate_2024
≠
2024 졸업자 코호트의 4년 누적 grading exposure
```

현재 A비율의 해석:

> 해당 학과의 당시 grading climate.

현재 연구가 검정하는 것:

> 학과의 단기 평가환경과 졸업 후 성과의 조건부 연관.

인과에 가까운 분석을 위해서는 향후:

```text
졸업 코호트별 3~4년 평균 A비율
```

이 필요하다.

2023~2025의 2~3년 평균은 `recent_grading_climate` 민감도로만 사용하고, 코호트 노출로 부르지 않는다.

---

# 8. 최종 주장 판정 규칙

“진학시장과 더 강하게 정렬된다”는 문장은 다음 조건을 만족할 때만 사용한다.

1. P1에서 진학 정렬이 취업보다 큼
2. P4에서 grade signal의 진학 추가정보가 유지취업보다 큼
3. 전체 P3→P4 school bootstrap CI가 0을 넘음
4. raw A, within-major-year A, OOF residual의 방향이 대체로 일치
5. 구조분기와 입결분기에서 방향이 크게 뒤집히지 않음
6. P8의 외부연도 또는 시차 모형에서 최소한 부호가 재현

P5는 이 판정조건에 필수로 넣지 않는다. P5는 탐색적 이질성 분석이다.

---

# 9. 실행 순서

```text
1. 데이터 count·denominator audit
2. P2-S / P2-Q
3. P3-S / P3-Q nested cross-fitting
4. P4-S / P4-Q count-binomial outcome validation
5. P1 descriptive GAM alignment
6. P7 Ridge–XGBoost benchmark
7. 2023~2025 entity bridge 및 panel 구축
8. P8 동시점·시차·외부연도 검증
9. P6 residual topology
10. P5 major7-year slope heterogeneity
```

P5는 패널과 `major7×year` context가 모두 확보된 뒤 실행한다.

---

# 10. 최종 모형 포트폴리오

| 질문                 | 데이터 수준           | 주모형                          |
| ------------------ | ---------------- | ---------------------------- |
| A비율과 시장성과의 관계 모양   | 학과 2024          | GAM                          |
| A비율 형성             | 학과 2024          | Cluster OLS·GAM              |
| 조건부 A비율 편차         | 학과 2024          | Nested OOF Ridge             |
| 유지취업과 Grade Signal | 학과 또는 학과-연도      | Aggregated binomial          |
| 진학과 Grade Signal   | 학과 또는 학과-연도      | Aggregated binomial          |
| 계열 환경에 따른 이질성      | major7×year      | Cell slope + meta-regression |
| 학과 유형              | 표준화 OOF residual | Octant·GMM·shallow DT        |
| 비선형 추가효용           | 학과               | Ridge vs XGBoost             |
| 동일 학과 내부 변화        | 학과 패널            | Department FE                |
| 다음 연도 결과           | 학과 전이            | Lagged binomial              |
| 다음 연도 A변화          | 학과 전이            | Ridge·Logistic·XGBoost       |

---

# 11. 최종 압축 명제

> 학교·학과 수준에서는 A비율, 유지취업자 수, 진학자 수를 실제 관측성과로 사용한다. 소득구간·기업규모·고용형태는 학과 성과가 아니라 `major_group_7 × year` 노동시장 context로 사용한다. 따라서 분석의 중심은 특정 학과의 소득이나 대기업 취업비중을 추정하는 것이 아니라, 서로 다른 노동시장 환경 안에서 학과별 A비율 편차가 유지취업·대학원 진학과 어떻게 연결되는지 검정하는 것이다.
