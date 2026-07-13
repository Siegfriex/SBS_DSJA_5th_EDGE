# P2-G3 통일 데이터 명세

- 버전: `v1.0`
- 스키마 원칙: 원 단위 보존, nullable dtype, raw/std 식별자 병행, context와 outcome 분리
- 비율 단위: 전부 `0~100 percentage points`
- 모델링 전 P3 산출물: imputation/encoding/scaling 미적용

---

## 1. 공통 컬럼 규칙

| 접미사/접두사 | 의미 |
|---|---|
| `*_uid` | 내부 안정 식별자 |
| `*_code` | 공식 또는 canonical 코드 |
| `*_name_raw` | 원문 |
| `*_name_std` | 정규화 문자열 |
| `*_n` | 인원·건수 |
| `*_pct` | 0~100 비율 |
| `*_ratio` | 단위 없는 배수 |
| `*_flag` | nullable boolean |
| `ctx24_*` | 2024 계열 참조값 |
| `goms_*` | GOMS 역사적 계열 맥락 |
| `*_proxy` | 직접 측정값이 아닌 근사치 |

### 공통 dtype

| 의미 | pandas dtype |
|---|---|
| 연도 | `Int16` |
| count | `Int32` 또는 원범위 초과 시 `Int64` |
| rate/continuous | `Float32` |
| 모델 계산 시 | P4 내부 `Float64` |
| flag | `boolean` |
| 고정 범주 | `category` |
| 이름·코드·ID | `string` |

---

## 2. D01 `dept_headcount_master_2024.parquet`

### Grain

```text
한 행 = 학교 × 캠퍼스 × 학위과정 × 학과
```

### 예상 shape

```text
15,727행 × (원본 120열 + canonical/QA 열)
```

원본 120열은 삭제하지 않고 canonical alias registry를 함께 제공한다.

### 필수 canonical 컬럼

#### 식별자

```text
analysis_year: Int16
headcount_row_id: string
school_uid: string
campus_uid: string
dept_uid: string
school_name_raw: string
school_name_std: string
campus_name_raw: string
campus_name_std: category
dept_name_raw: string
dept_name_std: string
kedi_dept_code: string
```

#### 계층·분류

```text
school_type: category
degree_course: category
campus_status: category
establishment_type: category
region_sido: category
region_sigungu: category
major_group_raw: string
major_group_7: category
field_middle_name: category
field_small_name: category
is_undergraduate_candidate: boolean
```

#### 모델용 핵심 count

```text
admission_capacity_n: Int32
recruitment_n: Int32
applicants_n: Int32
admits_n: Int32
enrolled_students_n: Int32
leave_students_n: Int32
graduates_n: Int32
fulltime_faculty_n: Int32
nonfulltime_faculty_n: Int32
international_students_n: Int32
female_students_n: Int32
masters_students_n: Int32
doctoral_students_n: Int32
```

#### 파생 구조변수

```text
competition_ratio: Float32
admission_yield_ratio: Float32
admit_per_applicant_ratio: Float32
leave_rate_pct: Float32
female_student_share_pct: Float32
international_student_share_pct: Float32
student_faculty_ratio: Float32
fulltime_faculty_share_pct: Float32
graduate_intensity_pct: Float32
log_enrolled_students: Float32
log_graduates: Float32
has_masters_program: boolean
has_doctoral_program: boolean
```

분모가 0이면 `NA`다.

#### 품질

```text
source_file: string
source_sha256: string
grain_duplicate_flag: boolean
row_qa_status: category
```

---

## 3. D02 `dept_outcomes_2024.parquet`

### Grain

```text
한 행 = 2024년 학교 × 학과_전공
```

### Shape

```text
10,242행 × canonical columns
```

### 컬럼

#### 식별

```text
analysis_year: Int16
outcome_row_id: string
school_name_raw: string
school_name_std: string
campus_name_raw: string
campus_name_std: category
dept_name_raw: string
dept_name_std: string
dept_field_raw: string
credit_forfeit_flag: boolean
```

#### 핵심 노출·후보 outcome

```text
selectivity_proxy_pct: Float32
a_rate_pct: Float32
cd_rate_pct: Float32
f_rate_pct: Float32

employment_rate_pct: Float32
health_employment_rate_pct: Float32

progression_rate_pct: Float32
vocational_college_progression_rate_pct: Float32
university_progression_rate_pct: Float32
graduate_school_progression_rate_pct: Float32
domestic_progression_rate_pct: Float32
overseas_progression_rate_pct: Float32
```

#### 결측 플래그

```text
has_selectivity: boolean
has_employment: boolean
has_progression: boolean
```

#### 품질

```text
rate_range_qa: category
source_file: string
source_sha256: string
```

### 실측 결측 기준

```text
selectivity_proxy_pct: 약 63.5%
employment 계열: 약 27.0%
progression 계열: 약 25.9%
a_rate_pct: 0%
```

P3에서 대체하지 않는다.

---

## 4. D03 `dept_master_2024_core.parquet`

### Grain/shape

```text
한 행 = 2024 학교×캠퍼스×학과
10,242행 고정
```

### 구성

D02 전체 + D01에서 선택한 식별·구조·count + 아래 매칭·계열 bridge 컬럼.

```text
school_uid: string
campus_uid: string
dept_uid: string
headcount_row_id: string

match_method: category
# exact_code
# exact_raw
# exact_normalized
# fuzzy_unique
# manual_approved
# manual_review
# unmatched

match_score: Float32
candidate_count: Int16
review_needed: boolean
headcount_match_flag: boolean

major_group_7: category
major7_mapping_method: category
# inherited_headcount
# exact_dictionary
# keyword_rule
# manual_approved
# ambiguous
# unknown

major7_mapping_confidence: category
# high / medium / low / unknown

major7_evidence: string
missing_feature_count: Int16
row_qa_status: category
```

### 자동 매칭 허용조건

- 공식 코드가 일치하고 캠퍼스 충돌 없음
- 원문 완전일치
- 정규화 이름 완전일치 + 동일 학교/캠퍼스
- fuzzy는 동일 학교·캠퍼스 내 후보 1개, 계열 일치, threshold 충족

후보 2개 이상은 자동확정하지 않는다.

---

## 5. D04 `wage_reference_by_major.parquet`

### Grain/shape

```text
한 행 = major_group_7 × degree_level
14행 × 66 원계약 컬럼
```

### 필수 식별

```text
analysis_year: Int16
major_group_7: category
degree_level: category  # undergrad / graduate
reference_sample_n: Int32
```

### P4용 context 선택컬럼

```text
mean_income_10kkrw: Float32
median_income_10kkrw: Float32
log10_mean_income: Float32
income_300plus_pct: Float32
income_400plus_pct: Float32
large_company_pct: Float32
mid_company_pct: Float32
small_company_pct: Float32
large_mid_company_pct: Float32
public_nonprofit_pct: Float32
cert_rate_pct: Float32
cert_per_person: Float32
industry_top3_pct: Float32
industry_hhi: Float32
```

전체 66열의 role·unit·null/zero policy는 원 `컬럼설명.CSV`를 canonical registry로 변환해 보존한다.

학과 mart에는 `degree_level == "undergrad"` 7행만 결합한다.

---

## 6. D05 `job_cert_bridge.parquet`

### Grain/shape

```text
한 행 = 직무분류
24행 × 26열
```

원본 컬럼과 dtype을 보존하고 아래 관리 컬럼을 강제한다.

```text
job_group_raw: string
mapping_type: category
confidence: category
primary_industry_candidate: string
review_needed: boolean
join_now: boolean
mapping_missing_flag: boolean
is_total_row: boolean
is_model_row: boolean
decision_reason: string
```

확정 정책:

```text
join_now=False인 상태로 D08에 조인하지 않는다.
```

---

## 7. D06 `goms_major_year_labor_baseline.parquet`

### Grain/shape

```text
한 행 = major_group_7 × year
7 × 13 = 91행
정확히 45열
```

### 정확한 컬럼 계약

#### Key — 2

```text
year: Int16
major_group_7: category
```

#### 경제활동 — 7

```text
graduate_total_n: Float64
employed_n: Float64
unemployed_n: Float64
inactive_n: Float64
employment_rate_pct: Float32
unemployment_rate_pct: Float32
inactivity_rate_pct: Float32
```

`GOMS_003` frequency에서 재계산한다.

#### 산업 — 9

```text
manufacturing_pct: Float32
information_communication_pct: Float32
professional_science_pct: Float32
education_service_pct: Float32
health_social_pct: Float32
industry_top1_pct: Float32
industry_top3_pct: Float32
industry_hhi: Float32
industry_entropy: Float32
```

#### 직업 — 7

```text
professional_highskill_pct: Float32
business_office_finance_pct: Float32
service_sales_pct: Float32
production_transport_pct: Float32
occupation_top3_pct: Float32
occupation_hhi: Float32
occupation_schema_version: category
```

`pre_2017`과 `post_2017` 원분류는 별도 crosswalk로 broad 10종에 매핑한다. raw category는 canonical long fact에 보존한다.

#### 사업체 규모 — 5

```text
firm_1_9_pct: Float32
firm_10_49_pct: Float32
firm_50_299_pct: Float32
firm_300plus_pct: Float32
firm_size_hhi: Float32
```

#### 사업체 유형 — 6

```text
private_domestic_pct: Float32
foreign_private_pct: Float32
public_enterprise_pct: Float32
government_pct: Float32
nonprofit_pct: Float32
public_nonprofit_pct: Float32
```

#### 종사상 지위 — 3

```text
permanent_pct: Float32
unstable_pct: Float32
self_employed_pct: Float32
```

`unstable_pct = temporary + day_labor`

#### 소득·시간 — 3

```text
mean_monthly_income_10kkrw: Float32
weekly_work_hours: Float32
hourly_income_proxy: Float32
```

#### QA — 3

```text
source_topic_count: Int16
missing_feature_count: Int16
row_qa_status: category
```

### Population scope

```text
topic_group 2 → all_graduates
topic_group 3 → employed_graduates
topic_group 4 → employed_graduates
topic_group 5 → employed_graduates
```

---

## 8. D07 `goms_major_profile_recent.parquet`

### Grain/shape

```text
한 행 = major_group_7
7행 × 29열
```

### 컬럼

```text
major_group_7: category
profile_start_year: Int16       # 2017
profile_end_year: Int16         # 2019
profile_years_n: Int16          # 3
aggregation_method: category
```

#### Recent profile

```text
recent_employment_rate_pct: Float32
recent_unemployment_rate_pct: Float32
recent_inactivity_rate_pct: Float32
recent_firm_300plus_pct: Float32
recent_public_nonprofit_pct: Float32
recent_permanent_pct: Float32
recent_unstable_pct: Float32
recent_self_employed_pct: Float32
recent_industry_hhi: Float32
recent_industry_top3_pct: Float32
recent_professional_highskill_pct: Float32
recent_mean_income_10kkrw: Float32
recent_weekly_work_hours: Float32
recent_hourly_income_proxy: Float32
```

#### 2007~2019 trends

```text
income_trend_per_year: Float32
hours_trend_per_year: Float32
firm_300plus_trend_per_year: Float32
permanent_trend_per_year: Float32
```

#### 2019 diagnostics

```text
latest_2019_mean_income_10kkrw: Float32
latest_2019_weekly_work_hours: Float32
latest_2019_firm_300plus_pct: Float32
latest_2019_permanent_pct: Float32
```

#### QA

```text
source_years_observed: Int16
year_over_year_review_flag: boolean
mapping_confidence: category
row_qa_status: category
```

---

## 9. D08 `mart_department_model_base_2024.parquet`

### Grain/shape

```text
한 행 = 2024 학교×캠퍼스×학과
10,242행
```

### 컬럼 블록

D03 전체를 보존하되 P4 기본 입력 registry는 다음 역할로 제한한다.

#### Keys — 모델 X 제외

```text
analysis_year
school_uid
campus_uid
dept_uid
school_name_raw
school_name_std
campus_name_raw
campus_name_std
dept_name_raw
dept_name_std
kedi_dept_code
outcome_row_id
headcount_row_id
```

#### Group/strata

```text
school_type
degree_course
establishment_type
region_sido
region_sigungu
major_group_7
field_middle_name
credit_forfeit_flag
```

#### Candidate exposures/outcomes

```text
selectivity_proxy_pct
a_rate_pct
cd_rate_pct
f_rate_pct
employment_rate_pct
health_employment_rate_pct
progression_rate_pct
vocational_college_progression_rate_pct
university_progression_rate_pct
graduate_school_progression_rate_pct
domestic_progression_rate_pct
overseas_progression_rate_pct
```

#### Scale controls

```text
recruitment_n
applicants_n
admits_n
enrolled_students_n
leave_students_n
graduates_n
fulltime_faculty_n
nonfulltime_faculty_n
competition_ratio
admission_yield_ratio
leave_rate_pct
female_student_share_pct
international_student_share_pct
student_faculty_ratio
fulltime_faculty_share_pct
graduate_intensity_pct
log_enrolled_students
log_graduates
```

#### 2024 field context

```text
ctx24_mean_income_10kkrw
ctx24_median_income_10kkrw
ctx24_income_300plus_pct
ctx24_income_400plus_pct
ctx24_large_mid_company_pct
ctx24_public_nonprofit_pct
ctx24_cert_rate_pct
ctx24_cert_per_person
ctx24_industry_hhi
ctx24_industry_top3_pct
```

#### GOMS historical context

```text
goms_recent_employment_rate_pct
goms_recent_firm_300plus_pct
goms_recent_public_nonprofit_pct
goms_recent_permanent_pct
goms_recent_unstable_pct
goms_recent_industry_hhi
goms_recent_industry_top3_pct
goms_recent_professional_highskill_pct
goms_recent_mean_income_10kkrw
goms_recent_weekly_work_hours
goms_recent_hourly_income_proxy
```

#### Quality/split

```text
match_method
match_score
candidate_count
review_needed
headcount_match_flag
major7_mapping_method
major7_mapping_confidence
has_selectivity
has_employment
has_progression
missing_feature_count
row_qa_status
split
model_eligible_core
model_eligible_selectivity
```

### Context 해석 규칙

`ctx24_*`와 `goms_*`는 동일 계열의 모든 학과에 반복되는 context다.

금지 표현:

```text
이 학과의 평균소득
이 학과의 대기업 취업률
```

허용 표현:

```text
이 학과가 속한 계열의 전국 노동시장 맥락
```

---

## 10. Control/Evidence schema

### `bridge_department_major7.csv`

```text
outcome_row_id
headcount_row_id
dept_name_raw
dept_field_raw
headcount_major_raw
major_group_7
mapping_method
matched_keyword_or_code
candidate_major_count
confidence
evidence
review_needed
review_status
```

### `model_sample_registry.csv`

```text
dataset_version
sample_id
required_non_null_columns
exclusion_rules
n_rows
n_schools
n_major_groups
train_n
validation_n
test_n
created_at
qa_status
```

### `department_model_column_registry.csv`

```text
column_name
source_dataset
source_column
role
semantic_type
dtype
unit
grain
population_scope
null_policy
zero_policy
allowed_range
context_only
target_leakage_group
description
```
