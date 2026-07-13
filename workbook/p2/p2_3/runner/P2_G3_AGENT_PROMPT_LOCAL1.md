# Local Agent 1 실행 프롬프트 — `p3_1.ipynb`

당신은 P2-G3의 **2024 대학·학과 canonical dataset 및 최종 P4 handoff 담당 데이터 엔지니어**다.

## 0. 작업 목적

다음 원천과 Local Agent 2의 GOMS handoff를 이용해 P4가 즉시 읽을 수 있는 최종 데이터셋을 만든다.

```text
D01 dept_headcount_master_2024.parquet
D02 dept_outcomes_2024.parquet
D03 dept_master_2024_core.parquet
D04 wage_reference_by_major.parquet
D05 job_cert_bridge.parquet
D08 mart_department_model_base_2024.parquet
```

모델 학습·스케일링·결측 대체·원-핫 인코딩은 수행하지 않는다.

## 1. 입력

노트북:

```text
workbook/p2/p2_3/p3_1.ipynb
```

원천:

```text
P2_G2_메인_입결_A_취업진학.CSV
P2_G2_정시입결.csv
P2_G2_임금분류_학부대학원.CSV
P2_G2_임금분류_학부대학원_사분위기준.CSV
P2_G2_임금분류_학부대학원_컬럼설명.CSV
P2_G2_직무별_자격증매핑.CSV
```

Local 2 handoff:

```text
shared_handoff/goms_major_profile_recent.parquet
shared_handoff/goms_column_registry.csv
shared_handoff/goms_run_manifest.json
```

## 2. 선행 사실

- `P2_G2_메인_입결_A_취업진학.CSV`는 15,727×120이며, 실제로는 target이 없는 인원·구조 master다. 내부 canonical 이름을 `dept_headcount_master_2024`로 사용한다.
- `P2_G2_정시입결.csv`는 10,242×17이며 A/CD/F, 취업률, 진학률, 입결 proxy를 가진 outcome spine이다.
- outcome spine의 A비율은 결측이 없고, 입결 약 63.5%, 취업 약 27%, 진학 약 25.9%가 결측이다.
- `학교명+학과명` 중복은 캠퍼스 차이에서 발생할 수 있으므로 캠퍼스를 합치지 않는다.
- 직무 자격증 파일의 `join_now`는 전부 False이므로 학과 mart에 조인하지 않는다.

## 3. 절대규칙

1. D02 10,242행을 canonical spine으로 사용한다.
2. D03과 D08의 행수는 정확히 10,242를 유지한다.
3. 모든 merge에 `validate`를 지정한다.
4. 캠퍼스 확정 전 count 합산 금지.
5. 후보 2개 이상 fuzzy match 자동확정 금지.
6. 비율 평균 금지. 분자·분모가 없으면 원값 보존.
7. `graduates_n`을 공식 취업률 분모라고 부르지 않는다.
8. 결측 대체·스케일링·one-hot·PCA·winsorization 금지.
9. 원본 파일 수정 금지.
10. 모든 판단과 변환의 근거를 로그로 제출한다.

## 4. 단계별 수행

### Gate 0 — 입력 동결

- 모든 입력의 path, shape, mtime, SHA256 기록
- Python/pandas/pyarrow 버전 기록
- 원천 파일명과 실제 semantic role의 불일치를 decision log에 기록

출력:

```text
logs/run_manifest_initial.json
logs/decision_log.jsonl
```

### Gate 1 — D01 구조 master

1. 원 120열 보존
2. `analysis_year == 2024` 확인
3. 학교·캠퍼스·학과·학위과정 grain 감사
4. raw/std 이름 생성
5. undergraduate candidate 플래그 생성
6. 핵심 count를 nullable integer로 강제
7. 구조 파생변수 생성
8. 0분모는 NA
9. 중복 원인을 캠퍼스·학위과정·주야 등으로 분류

출력:

```text
p3_1/dept_headcount_master_2024.parquet
qa/headcount_duplicate_audit.csv
```

### Gate 2 — D02 outcome spine

1. 10,242행 유지
2. 비율을 Float32, 0~100으로 검사
3. 입결·취업·진학 결측 플래그 생성
4. 원문 학교·학과명 보존
5. 괄호 캠퍼스 정보가 있으면 raw/std campus 컬럼 분리
6. target을 선택하지 않고 candidate role만 registry에 기록

출력:

```text
p3_1/dept_outcomes_2024.parquet
qa/outcome_range_audit.csv
```

### Gate 3 — 학교·학과 매칭

매칭 ladder:

```text
L0 공식 코드
L1 학교+캠퍼스+학과 원문 완전일치
L2 학교+캠퍼스+정규화 학과 완전일치
L3 동일 학교·캠퍼스 내 fuzzy unique + 계열 일치
L4 manual review
L5 unmatched
```

정규화는 비교키에만 사용하고 raw는 보존한다.

자동 fuzzy 조건:

- 후보 1개
- 학교 일치
- 캠퍼스 충돌 없음
- 계열 모순 없음
- 점수 threshold 충족
- 금지 토큰 충돌 없음: 학부/대학원, 본교/분교, 주간/야간 등

출력:

```text
shared/bridge_outcome_headcount.csv
qa/ambiguous_matches.csv
qa/unmatched_departments.csv
qa/dept_match_gap_report.csv
```

D03은 outcome spine left join으로 생성한다.

```python
assert len(D03) == 10242
```

### Gate 4 — `major_group_7` bridge

우선순위:

1. D01 고신뢰 매칭행의 `대계열` 상속
2. exact dictionary
3. `학과_계열`·`학과_전공` 키워드 규칙
4. manual approved
5. ambiguous/unknown

키워드 규칙은 순서가 있는 결정 트리로 작성하고 충돌 검사를 수행한다. 예:

```text
간호/의학/약학/치의/한의/보건 → MED
컴퓨터/기계/전자/건축공학/화공 → ENG
수학/물리/화학/생명과학 → NAT
교육/교직/초등교육/유아교육 → EDU
디자인/미술/음악/체육/무용 → ART
경영/경제/행정/사회복지/법 → SOC
국문/영문/철학/역사/언어 → HUM
```

융합·자유전공·복수 후보는 자동확정하지 않는다.

필수 로그:

```text
어떤 raw 문자열이 어떤 규칙에 걸렸는지
후보 계열 수
선택 근거
confidence
review 여부
```

출력:

```text
shared/bridge_department_major7.csv
qa/major7_ambiguous.csv
qa/major7_coverage.csv
```

### Gate 5 — D04/D05

D04:

- 원 컬럼설명 파일의 semantic_type/unit/null/zero policy를 우선
- 14행 유지
- 계열 접미사 제거로 `major_group_7` 생성
- 66열을 보존하고 model context 14열을 registry에서 표시

D05:

- 24행 유지
- `join_now=False`
- `is_model_row=False`
- 학과 mart 직접 조인 금지 이유 기록

### Gate 6 — D08 최종 조립

Local 2의 D07을 읽는다. 없으면 D01~D05까지만 생성하고 D08을 `BLOCKED` 처리한다. 임의 대체 파일을 만들지 않는다.

병합:

```text
D03
+ D04 undergrad 7행 on major_group_7 (many_to_one)
+ D07 7행 on major_group_7 (many_to_one)
→ D08
```

context prefix:

```text
ctx24_*
goms_*
```

D08 행수는 10,242다.

### Gate 7 — split/sample registry

학교 단위 70/15/15 split:

- seed 3085/3086
- 동일 학교 leakage 0
- 기존 split 파일이 있으면 재사용
- split별 행수, 학교 수, major 분포 보고

sample registry 최소:

```text
GRADE_ALL
GRADE_SELECTIVITY
EMPLOYMENT_HEALTH
PROGRESSION_GRADSCHOOL
JOINT_EMP_PROG
```

### Gate 8 — Restart & Run All

노트북 마지막에 `P3-1 Final Contract Build` 섹션을 추가한다.

- 기존 EDA 셀 삭제 금지
- 재실행 성공
- 출력 shape/hash 기록
- 실패한 QA는 숨기지 말고 failed_checks에 기록

## 5. 필수 산출물

```text
p3_1/dept_headcount_master_2024.parquet
p3_1/dept_outcomes_2024.parquet
p3_1/dept_master_2024_core.parquet
p3_1/wage_reference_by_major.parquet
p3_1/job_cert_bridge.parquet
shared/mart_department_model_base_2024.parquet
shared/bridge_outcome_headcount.csv
shared/bridge_department_major7.csv
shared/dim_school_split.csv
shared/model_sample_registry.csv
shared/department_model_column_registry.csv
qa/merge_audit.csv
qa/final_qa_summary.csv
qa/failed_checks.csv
logs/decision_log.jsonl
logs/transformation_log.jsonl
logs/run_manifest.json
logs/schema_deviation_report.csv
```

## 6. 완료 보고서 형식

최종 응답에 반드시 포함:

1. 산출물별 실제 shape·hash
2. match_method 분포
3. 구조 master 고신뢰 매칭률
4. major_group_7 방법별 매핑률
5. 입결/취업/진학 실제 N
6. split별 행·학교 수
7. FAIL/WARN 목록
8. 각 핵심 판단의 근거 파일 경로
9. D08을 P4에서 사용할 때의 금지사항
