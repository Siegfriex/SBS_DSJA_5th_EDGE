# P2-G3 최종 청사진 — P4 모델링 이전 Canonical Data Handoff

- 버전: `v1.0`
- 기준일: `2026-07-12`
- 기준연도: 대학·학과 코어는 `2024`
- 목적: `p3_1.ipynb`와 `p3_2.ipynb`가 서로 다른 에이전트에 의해 관리되는 상황에서, P2-G4가 별도의 임의 병합·재해석 없이 학습/검증/테스트를 시작할 수 있도록 데이터 계약을 동결한다.
- 비목표: P3에서는 모델 학습, 결측 대체, 스케일링, 원-핫 인코딩, PCA, 타깃 선택을 수행하지 않는다.

---

## 1. 최종 결정 요약

### 1.1 Canonical 분석 grain

P4의 기본 행 단위는 다음으로 고정한다.

```text
한 행 = 2024년 × 학교 × 캠퍼스 × 학과
```

기본 spine은 `P2_G2_정시입결.csv`의 10,242행이다. 구조자료와의 매칭 실패 때문에 spine 행을 삭제하지 않는다. 매칭 결과는 품질 컬럼으로 남기고, 실제 모델 표본은 `model_sample_registry.csv`의 마스크로 결정한다.

### 1.2 최종 핵심 데이터 산출물

모델·분석 데이터셋은 총 8개다.

| ID | 파일명 | 담당 | Grain | 예상 행수 | 역할 |
|---|---|---|---|---:|---|
| D01 | `dept_headcount_master_2024.parquet` | Local 1 | 학교×캠퍼스×학위과정×학과 | 15,727 | 정원·지원·입학·재적·졸업·교원 구조 원장 |
| D02 | `dept_outcomes_2024.parquet` | Local 1 | 2024 학교×학과_전공 | 10,242 | A/CD/F, 취업, 진학, 입결 후보값 |
| D03 | `dept_master_2024_core.parquet` | Local 1 | 2024 학교×캠퍼스×학과 | 10,242 | D02 spine에 D01 구조값을 left join한 코어 |
| D04 | `wage_reference_by_major.parquet` | Local 1 | 계열7×학부/대학원 | 14 | 2024 계열 단위 임금·기업·산업 맥락 |
| D05 | `job_cert_bridge.parquet` | Local 1 | 직무분류 | 24 | 자격증-직무 참조. 학과 mart 직접 조인 금지 |
| D06 | `goms_major_year_labor_baseline.parquet` | Local 2 | 계열7×2007~2019 | 91 | 전공계열별 장기 노동시장 패널 |
| D07 | `goms_major_profile_recent.parquet` | Local 2 | 계열7 | 7 | 2017~2019 최근 노동시장 프로필 |
| D08 | `mart_department_model_base_2024.parquet` | Local 1 최종 조립 | 2024 학교×캠퍼스×학과 | 10,242 | P4가 직접 읽는 최종 feature/outcome base |

성별·학교유형 GOMS mart는 이번 P4 handoff의 필수 산출물에서 제외한다. 필요 시 후속 참조 산출물로 생성한다.

### 1.3 핵심 브리지

```text
학교·학과 코어:
정시입결 outcome spine
→ 학교/캠퍼스/학과 정규화
→ headcount master 매칭
→ major_group_7 상속·보완

노동시장 context:
GOMS major_group_7 × year
→ 2017~2019 recent profile
→ major_group_7로 학과 mart에 many-to-one 결합
```

---

## 2. 데이터 소스별 역할

### 2.1 Local 1 소스 패밀리

| 원천 | 실측 shape | 최종 의미 |
|---|---:|---|
| `P2_G2_메인_입결_A_취업진학.CSV` | 15,727×120 | 파일명과 달리 target 없음. 구조·인원·교원 count master |
| `P2_G2_정시입결.csv` | 10,242×17 | A비율·취업률·진학률·입결 proxy를 가진 outcome spine |
| `P2_G2_임금분류_학부대학원.CSV` | 14×66 | 계열7×학부/대학원 reference |
| `P2_G2_임금분류_학부대학원_사분위기준.CSV` | 23×10 | 임금지표 구간 검증 reference |
| `P2_G2_임금분류_학부대학원_컬럼설명.CSV` | 66×10 | dtype·role·unit·zero/null policy source of truth |
| `P2_G2_직무별_자격증매핑.CSV` | 24×26 | join_now=False 24/24. 별도 bridge |

### 2.2 Local 2 소스 패밀리

Local 2는 아래 검증 완료 long 파일만 사용한다.

```text
normalized/goms_distribution_long.csv   # 29,160행
normalized/goms_continuous_long.csv     # 2,230행
```

원본 `.xls` 재파싱은 금지한다. 기존 `p3_2.ipynb`의 wide EDA 출력은 육안 검증용이며 canonical mart의 입력으로 사용하지 않는다.

---

## 3. 확정된 주요 설계 결정

### 3.1 Canonical spine은 10,242행을 유지한다

구조 master와 매칭되지 않은 outcome 행을 삭제하지 않는다.

```text
잘못된 방식:
매칭 성공 행만 남겨 dept_master 생성

확정 방식:
outcome 10,242행을 left spine으로 유지
→ 구조값 결측과 match_quality를 보존
→ P4 표본은 sample registry로 선택
```

### 3.2 캠퍼스는 독립 식별축이다

`학교명+학과명` 중복의 주요 원인은 본교/분교 또는 캠퍼스 차이다. 캠퍼스가 확정되기 전에 count를 합산하지 않는다.

최소 식별요소:

```text
analysis_year
school_name_std
campus_name_std
dept_name_std
degree_course
```

공식 코드가 신뢰 가능하면 이름보다 우선한다.

### 3.3 `major_group_7` 매핑은 Local 1이 책임진다

별도의 세 번째 에이전트를 두지 않는다.

매핑 ladder:

1. 구조 master 고신뢰 매칭행에서 `대계열` 상속
2. `대계열`의 `계열` 접미사 제거 후 7종 enum 변환
3. 구조 master 미매칭행은 `학과_계열`·`학과_전공` 기반 결정적 키워드 규칙 적용
4. 복수 계열 후보·융합학과·자유전공은 자동 확정 금지
5. 수동 검토 또는 `unknown`

공통 enum:

| code | label |
|---|---|
| `HUM` | 인문 |
| `SOC` | 사회 |
| `EDU` | 교육 |
| `ENG` | 공학 |
| `NAT` | 자연 |
| `MED` | 의약 |
| `ART` | 예체능 |

모든 판단은 `bridge_department_major7.csv`에 근거와 함께 남긴다.

### 3.4 GOMS recent profile 정책

2024 학과 데이터에 붙이는 기본 GOMS context는 `2017~2019` 최근 3개년 프로필로 확정한다.

근거:

- 직업분류가 2017년 이후 동일 버전이다.
- 2019 단일값보다 일시적 변동에 덜 민감하다.
- 2007~2019 전체평균보다 2024 노동시장에 상대적으로 가깝다.

집계 규칙:

- 가능한 경우 적절한 분모로 연도 가중평균
  - 경제활동률: `graduate_total_n`
  - 취업자 조건부 분포: `employed_n`
- 분모가 없으면 단순평균을 사용하고 `aggregation_method="simple_mean"`을 기록
- 2019 최신값과 2007~2019 추세는 진단 컬럼으로만 보존
- 2024년 특정 학과 실적이라고 해석하지 않는다

### 3.5 자격증-직무 자료는 직접 결합하지 않는다

`job_cert_bridge.parquet`는 보존하지만 D08에 조인하지 않는다. 향후 `학과/계열↔직무` 확률 bridge가 검증된 경우에만 별도 버전에서 사용한다.

### 3.6 P3에서는 타깃을 고정하지 않는다

후보 outcome은 보존하되 P4에서 분석 질문별로 하나씩 선택한다.

기본 sample ID:

| sample_id | 필수 outcome/exposure |
|---|---|
| `GRADE_ALL` | `a_rate_pct` |
| `GRADE_SELECTIVITY` | `a_rate_pct`, `selectivity_proxy_pct` |
| `EMPLOYMENT_HEALTH` | `health_employment_rate_pct` |
| `PROGRESSION_GRADSCHOOL` | `graduate_school_progression_rate_pct` |
| `JOINT_EMP_PROG` | 건강보험취업률과 대학원진학률 모두 존재 |

---

## 4. 처리 단계

### Wave A — 병렬 canonical build

Local 1:

```text
6개 CSV 감사
→ D01/D02/D04/D05 생성
→ 학교·캠퍼스·학과 bridge
→ major_group_7 bridge
→ D03 생성
```

Local 2:

```text
검증 완료 long 2개 로드
→ topic axis registry
→ 전공계열×연도 재구성
→ D06 생성
→ 2017~2019 recent profile D07 생성
```

### Wave B — handoff 조립

Local 2가 D07과 관련 manifest를 전달한 뒤 Local 1이 다음을 수행한다.

```text
D03
+ 학부 7행 wage context(D04)
+ GOMS recent profile(D07)
→ D08
→ 학교 단위 split
→ model sample registry
```

---

## 5. 전처리 허용·금지 경계

### P3에서 허용

- Unicode·공백·구두점 정규화
- raw/std 이름 동시 보존
- 공식 코드 우선 병합
- deterministic crosswalk
- 분자·분모 기반 비율 재계산
- `log1p` 파생컬럼 추가
- nullable dtype 강제
- 품질 플래그 생성
- 학교 단위 split 동결
- provenance 및 hash 기록

### P3에서 금지

- 결측 대체
- scaler
- one-hot encoding
- target encoding
- PCA/UMAP
- winsorization
- 임의 이상치 제거
- target 선택
- 전체 데이터로 학습한 변환기
- 모호한 fuzzy match 자동 확정
- 계열 context를 학과 실적으로 이름 변경

---

## 6. P4 split 계약

분할 단위는 `school_uid`다. 동일 학교의 학과가 여러 split에 들어가면 실패다.

```python
# 1차: test 15%
GroupShuffleSplit(n_splits=1, test_size=0.15, random_state=3085)

# 2차: 남은 85%에서 validation 약 17.647%
GroupShuffleSplit(n_splits=1, test_size=0.1764705882, random_state=3086)
```

최종 비율은 약 70/15/15다.

`dim_school_split.csv`를 저장한 후 재실행 시 새로 만들지 않고 기존 파일을 우선 사용한다. 데이터 버전이 달라졌다면 split version을 올리고 변경 로그를 남긴다.

---

## 7. 필수 판단·변환 로그

각 에이전트는 결과뿐 아니라 “어떤 근거로 왜 그렇게 처리했는지”를 제출해야 한다.

### 7.1 `decision_log.jsonl`

한 줄에 하나의 판단:

```json
{
  "timestamp": "ISO-8601",
  "agent": "local1|local2",
  "decision_id": "D-MATCH-001",
  "stage": "department_matching",
  "question": "가천대학교 두 행을 합산할 것인가?",
  "observed_evidence": {
    "rows": 2,
    "campus_values": ["성남", "인천"],
    "dept_code_collision": true
  },
  "evidence_paths": ["qa/campus_collision.csv"],
  "alternatives_considered": ["sum", "keep_separate", "drop"],
  "chosen_action": "keep_separate",
  "rationale": "서로 다른 캠퍼스이며 동일 학과코드는 캠퍼스를 식별하지 못함",
  "confidence": "high",
  "affected_outputs": ["dept_headcount_master_2024.parquet"],
  "review_required": false
}
```

### 7.2 `transformation_log.jsonl`

필수 필드:

```text
timestamp
agent
step_id
function_or_cell
input_files
input_shape
input_hashes
grain_before
keys_before
operation
columns_read
columns_created
columns_dropped
row_count_before
row_count_after
duplicate_count_before
duplicate_count_after
null_delta
output_file
output_hash
qa_status
```

### 7.3 `merge_audit.csv`

```text
merge_id
left_file
right_file
left_shape
right_shape
join_type
keys
validate_mode
left_key_duplicates
right_key_duplicates
row_count_before
row_count_after
matched_n
left_only_n
right_only_n
match_rate
status
```

### 7.4 기타 필수 증거

```text
run_manifest.json
schema_deviation_report.csv
manual_review_queue.csv
column_registry.csv
qa_summary.csv
failed_checks.csv
```

---

## 8. Acceptance Gates

### Local 1

- D02 행수 10,242
- D03/D08 행수 10,242
- spine key 중복 0
- 병합 후 행 증가 0
- ambiguous 자동 확정 0
- 비율 0~100 범위 위반 0
- 음수 count 0
- `major_group_7` 고신뢰/중신뢰/미확정 비율 보고
- 구조 master 고신뢰 매칭률 70% 이상을 목표로 하되, 미달 시 실패로 숨기지 않고 원인표 제출
- 취업·진학·입결 결측을 대체하지 않음

### Local 2

- D06 행수 91
- D07 행수 7
- `major_group_7` 7종 완비
- year 2007~2019
- GOMS_003 경제활동률은 frequency에서 재계산
- 조건부 분포합 허용오차 내 PASS
- pre/post 직업분류 혼합 0
- 표준편차 위조·복제 0
- `population_scope` topic group 기준 분류
- inf/-inf 0

### Shared handoff

- 동일 학교 split 중복 0
- context-only 컬럼 registry 완성
- P4에 전달하는 파일과 hash 동결
- 모델 sample별 실제 N·학교 수·계열 분포 기록

---

## 9. P4가 직접 읽는 파일

```text
shared/mart_department_model_base_2024.parquet
shared/dim_school_split.csv
shared/model_sample_registry.csv
shared/department_model_column_registry.csv
```

P4는 이 네 파일 이외의 원천 CSV를 직접 다시 병합하지 않는다.

---

## 10. 완료 정의

P2-G3는 다음이 모두 충족될 때 완료다.

1. 8개 데이터 산출물 생성
2. D08 10,242행 동결
3. 모든 컬럼의 role·dtype·unit·null policy·source 기록
4. 학교 단위 train/validation/test 동결
5. 모델 sample registry 생성
6. decision/transformation/merge 로그 제출
7. 모든 FAIL 항목이 0이거나 명시적 waiver와 근거가 존재
8. 두 노트북을 Restart & Run All하여 결과가 재현됨
