# Local Agent 2 실행 프롬프트 — `p3_2.ipynb`

당신은 P2-G3의 **GOMS 전공계열 노동시장 baseline 및 recent profile 담당 데이터 엔지니어**다.

## 0. 목적

검증 완료된 GOMS long 파일에서 다음을 만든다.

```text
D06 goms_major_year_labor_baseline.parquet
D07 goms_major_profile_recent.parquet
```

D07은 Local Agent 1이 2024 학과 mart에 결합한다.

## 1. 입력

노트북:

```text
workbook/p2/p2_3/p3_2.ipynb
```

반드시 사용할 입력:

```text
normalized/goms_distribution_long.csv
normalized/goms_continuous_long.csv
```

금지:

```text
raw_downloads/*.xls 재파싱
기존 wide EDA 표를 canonical 입력으로 사용
표준편차를 평균 복제로 생성
```

## 2. 선행 사실

- distribution long: 29,160행
- continuous long: 2,230행
- 파싱 실패 0, 중복 0, 연도 커버리지 QA 완료
- 전공계열은 전체+7종이며 raw 문자열이 일관됨
- GOMS_003과 GOMS_006은 축 방향이 다름
- 직업분류 pre/post 기간은 겹치지 않음
- 표준편차는 사이트 버그로 취득 불가

## 3. 절대규칙

1. 모든 topic의 `group_axis`, `outcome_axis`, `population_scope`를 metadata registry로 명시한다.
2. topic_name 텍스트만으로 population scope를 판단하지 않는다.
3. topic_group 2는 전체졸업자, 3·4·5는 취업자 조건부로 지정한다.
4. GOMS_003 share를 전공별 취업률로 쓰지 않는다.
5. 경제활동률은 frequency에서 재계산한다.
6. 산업·직업·사업체 분포 long끼리 직접 merge하지 않는다.
7. 직업 pre/post raw 분류를 그대로 이어붙이지 않는다.
8. 전체 행을 삭제하지 말고 national benchmark로 분리한다.
9. P3에서 scaling/imputation/PCA/modeling 금지.
10. 모든 판단·변환 근거를 로그로 제출한다.

## 4. 단계별 수행

### Gate 0 — 입력 동결

- input shape·컬럼·SHA256
- long schema 확인
- year/topic coverage
- Python/pandas/pyarrow 버전

출력:

```text
logs/run_manifest_initial.json
```

### Gate 1 — Topic Axis Registry

39개 topic 전부에 다음 metadata를 작성한다.

```text
topic_id
topic_group_code
topic_name
population_scope
group_axis
outcome_axis
metric_family
statistic
unit
classification_version
share_direction
frequency_reconstruction_rule
include_in_major_mart
decision_rationale
```

예:

```text
GOMS_003:
group_axis=major_group
outcome_axis=economic_status
share_direction=P(major|status)
employment rate는 frequency 재계산

GOMS_006:
group_axis=major_group
outcome_axis=industry
share_direction=P(industry|major)
share 직접 사용 가능
```

각 판단 근거를 decision log에 기록한다.

### Gate 2 — Canonical major-year blocks

#### 경제활동

GOMS_003 frequency에서:

```text
graduate_total_n
employed_n
unemployed_n
inactive_n
employment_rate_pct
unemployment_rate_pct
inactivity_rate_pct
```

항등식 검증:

```text
graduate_total_n ≈ employed_n + unemployed_n + inactive_n
```

원표의 세부 상태가 추가로 존재하면 정의를 registry에 명시하고 항등식을 조정한다.

#### 산업

GOMS_006의 `P(industry|major)`를 사용한다.

- 주요 업종 5개
- top1/top3
- HHI
- entropy

#### 직업

GOMS_011 pre-2017, GOMS_012 post-2017.

- raw는 분리 보존
- broad occupation crosswalk 작성
- 동일 broad 그룹 10개로 요약
- 해당 연도의 schema version 기록
- crosswalk 불명확 범주는 `other` 또는 review. 임의 분배 금지

#### 사업체 규모/유형/종사상지위

원 범주 inventory를 먼저 출력하고 mapping table을 작성한다.

법적 대기업과 300인 이상 사업체를 동일시하지 않는다. 컬럼명은 `firm_300plus_pct`로 사용한다.

#### 연속형

GOMS_024, GOMS_033에서 mean만 사용한다.

```text
mean_monthly_income_10kkrw
weekly_work_hours
hourly_income_proxy
```

단위는 원표·사이트 metadata에서 검증한다.

### Gate 3 — D06

정확히 91행, 45열 계약을 맞춘다.

병합은 각 block을 먼저 `year×major_group_7` one-row로 만든 후 수행한다.

```python
merge(..., on=["year", "major_group_7"], validate="one_to_one")
```

### Gate 4 — D07 recent profile

기본기간:

```text
2017~2019
```

집계:

- 경제활동률: graduate_total_n 가중
- 취업자 조건부 share: employed_n 가중
- 소득·시간: 적절한 분모가 있으면 가중, 없으면 simple mean
- 사용한 집계법을 `aggregation_method`와 decision log에 기록

보존:

- recent profile
- 2019 latest diagnostic
- 2007~2019 linear trend
- 전년 대비 급변 review flag

D07은 정확히 7행, 29열이다.

### Gate 5 — National benchmark

`전체`는 모델행에서 제외하되 별도 파일에 보존한다.

```text
goms_national_year_benchmark.parquet
```

### Gate 6 — QA

- D06 91행
- D07 7행
- 7개 major 모두 존재
- year 2007~2019
- 비율 0~100
- HHI 0~1
- entropy >= 0
- 분포합 허용오차
- 키 중복 0
- inf/-inf 0
- pre/post raw category 혼합 0
- standard deviation 컬럼 0
- population scope 미확정 0 또는 REVIEW 명시

### Gate 7 — Restart & Run All

기존 wide EDA 셀은 삭제하지 않는다. 마지막에 `P3-2 Final Contract Build`를 추가한다.

Canonical build는 long 파일에서 시작해야 한다.

## 5. 필수 산출물

```text
p3_2/goms_major_year_labor_baseline.parquet
p3_2/goms_major_profile_recent.parquet
p3_2/goms_national_year_benchmark.parquet
shared_handoff/goms_major_profile_recent.parquet
shared_handoff/goms_column_registry.csv
shared_handoff/goms_topic_axis_registry.csv
shared_handoff/goms_run_manifest.json
qa/goms_distribution_sum_check.csv
qa/goms_key_duplicate_check.csv
qa/goms_occupation_crosswalk_review.csv
qa/goms_final_qa_summary.csv
qa/goms_failed_checks.csv
logs/decision_log.jsonl
logs/transformation_log.jsonl
logs/merge_audit.csv
logs/run_manifest.json
logs/schema_deviation_report.csv
```

## 6. 판단 로그 의무

특히 아래 판단은 각기 별도 decision event로 기록한다.

1. GOMS_003 share 미사용 결정
2. topic_group 기반 population scope 결정
3. 직업 pre/post crosswalk
4. 사업체 규모 재분류
5. 공공·비영리 합산 정의
6. unstable employment 정의
7. 2017~2019 recent 기간 선택
8. 가중평균 또는 단순평균 선택
9. 소득 단위 확인
10. 급변값 review threshold

각 event에는:

```text
관찰 근거
원표·QA 경로
대안
선택
근거
confidence
영향받는 컬럼
review 필요 여부
```

를 기록한다.

## 7. 완료 보고서 형식

최종 응답에 반드시 포함:

1. D06/D07 actual shape·hash
2. 45/29 컬럼 목록과 dtype
3. 7개 계열·13개 연도 완비 여부
4. topic별 population scope
5. frequency 재구성 결과
6. 분포합 QA
7. 직업 crosswalk review 건수
8. recent profile 집계 방법
9. WARN/FAIL 목록
10. Local 1 handoff 경로
