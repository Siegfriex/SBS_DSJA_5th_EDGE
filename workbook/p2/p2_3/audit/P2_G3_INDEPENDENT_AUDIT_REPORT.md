# P2-G3 Independent Audit Report

기준일: 2026-07-12  
감사 대상: `workbook/p2/p2_3/p3_1.ipynb`, `workbook/p2/p2_3/p3_2.ipynb` 및 P2-G3 최종 산출물

## 1. 최종 판정

| 영역 | 판정 | 근거 |
|---|---|---|
| Local 1 | AMBER | D01-D05/D08 hash·shape는 일치하고 bridge critical fail은 없지만, major mapping에서 모호 토큰 자동확정 246행, keyword contradiction proxy 541행, D04 빈 context 컬럼 활성 registry가 남아 있음 |
| Local 2 | AMBER | D06/D07 독립 재계산은 통과했지만 분포합 재분류 기준에서 WARN 74건, occupation crosswalk review 8건이 D06에 포함된 상태 |
| 통합 P4 readiness | AMBER | D07→D08 lineage, split leakage, sample registry는 통과. 단, major mapping·빈 feature registry·로그 namespace 추적성 문제가 남아 GREEN은 아님 |

RED critical fail은 발견하지 못했다. 다만 P4 진입 전 AMBER 항목은 수정 또는 명시적 waiver가 필요하다.

## 2. 파일 hash/shape 재계산

| ID | actual shape | hash 일치 |
|---|---:|---|
| D01 `dept_headcount_master_2024.parquet` | 15,727 x 175 | PASS |
| D02 `dept_outcomes_2024.parquet` | 10,242 x 32 | PASS |
| D03 `dept_master_2024_core.parquet` | 10,242 x 88 | PASS |
| D04 `wage_reference_by_major.parquet` | 14 x 87 | PASS |
| D05 `job_cert_bridge.parquet` | 24 x 32 | PASS |
| D06 `goms_major_year_labor_baseline.parquet` | 91 x 45 | PASS |
| D07 `goms_major_profile_recent.parquet` | 7 x 29 | PASS |
| D08 `mart_department_model_base_2024.parquet` | 10,242 x 131 | PASS |
| D07 handoff `shared_handoff/goms_major_profile_recent.parquet` | 7 x 29 | PASS |
| national benchmark | 13 x 45 | shape PASS |

`D07`와 handoff는 byte-identical이며 sha256은 `51473a3514f34e6695d175af005436f77cb700a76390d08a964772dbc3ccde30`이다.

## 3. D07 to D08 lineage

Local 1 생성 코드는 `shared_handoff/goms_major_profile_recent.parquet`를 직접 읽는다.

- `scripts/p3_1_final_contract_build.py:912`: handoff 경로 지정
- `scripts/p3_1_final_contract_build.py:924`: `pd.read_parquet(d07_path)`
- `scripts/p3_1_final_contract_build.py:926`: D07 한글 계열 라벨을 major code로 변환
- `scripts/p3_1_final_contract_build.py:941-943`: `goms_` prefix 후 D08에 `major_group_7` 기준 병합

검산 결과:

- D08 `major_group_7` non-null 행: 9,361
- D08 `goms_*` non-null 행: 9,361
- D08 `major_group_7` missing 행: 881
- D07 변환 후 D08 `goms_*` exact diff column: 0

lineage PASS.

## 4. Local 1 audit

### Bridge outcome to headcount

`bridge_outcome_headcount.csv` 재계산:

| match_method | rows |
|---|---:|
| unmatched | 5,204 |
| exact_normalized | 4,710 |
| manual_review | 327 |
| fuzzy_unique | 1 |

검산:

- 총 행수: 10,242 PASS
- `outcome_row_id` 중복: 0 PASS
- `candidate_count >= 2` 자동확정: 0 PASS
- 캠퍼스 scope mismatch 자동확정: 0 PASS
- exact_normalized 50행 표본: 학교·캠퍼스·학과 normalized 기준 모두 PASS
- fuzzy_unique 1행: 표본 파일에 전수 기록
- unmatched 5,204행: D03/D08에 모두 보존 PASS
- manual_review 327행: `review_needed=True`; 승인완료 상태 컬럼 없음. 검토대기 상태로 봐야 함

표본 파일:

- `audit/bridge_stratified_sample_seed3085.csv`
- `audit/bridge_full_joined_audit.csv`

### Major mapping

`bridge_department_major7.csv` 재계산:

| method | rows |
|---|---:|
| inherited_headcount | 4,711 |
| exact_dictionary | 3,481 |
| keyword_rule | 1,169 |
| ambiguous | 472 |
| unknown | 409 |

`ambiguous + unknown = 881 / 10,242 = 8.60%`.

자동확정 리스크:

- auto rows: 9,361
- 모호 토큰(`융합`, `자유전공`, `자율전공` 등) 포함 자동확정: 246행
- keyword contradiction proxy: 541행, 5.78%

주의: 541행은 공식 headcount 상속/사전과 단순 키워드 규칙 충돌을 잡은 프록시이며 전부 오분류로 단정하지 않는다. 하지만 246행은 청사진의 "융합학과·자유전공 자동확정 금지" 경계와 직접 충돌한다.

특수 검색어 감사 예:

- `자유전공`: 15행, 자동확정 10행, review 5행
- `융합`: 418행, 자동확정 224행, review 194행
- `데이터사이언스`: 34행, 자동확정 27행
- `바이오`: 133행, 자동확정 107행
- `심리`: 107행, 자동확정 101행, HUM/SOC/MED/ENG 혼재
- `의공학`: 13행, MED/ENG/NAT 혼재

표본 파일:

- `audit/major_mapping_stratified_sample_seed3085.csv`
- `audit/major_special_terms_audit.csv`
- `audit/major_full_joined_audit.csv`

### D04/D05 feature boundary

`ctx24_industry_top3_pct`, `ctx24_industry_hhi`:

- D04: 전부 NA
- D08: 전부 NA
- registry: `context_2024_reference`로 남아 있음

판정: MAJOR WARN. 빈 컬럼을 P4 기본 feature registry에서 제외하거나 role을 비활성 QA metadata로 낮춰야 한다.

D05:

- `join_now=True`: 0
- D08 `job_cert_*` 컬럼: 0

직무 자격증 직접 조인 금지 정책은 PASS. 단, D04 기반 `ctx24_cert_*` 계열 context는 D08에 존재한다.

## 5. Local 2 audit

### Canonical source

코드상 canonical 입력은 long 파일이다.

- `scripts/build_p2_g3_goms_local2.py:19`: `goms_distribution_long.csv`
- `scripts/build_p2_g3_goms_local2.py:20`: `goms_continuous_long.csv`
- `scripts/build_p2_g3_goms_local2.py:237-248`: manifest input hash/shape 기록

raw xls 또는 기존 wide EDA를 D06/D07 입력으로 쓰는 증거는 발견하지 못했다.

### D06 independent recompute

요청 12개 컬럼을 91행 전부 long 파일에서 재계산했다.

- mismatch rows > 1e-4: 전 컬럼 0
- 최대 차이는 float32 저장 오차 수준
- `GOMS_003` 경제활동률은 share가 아니라 frequency로 계산됨

검산 요약 파일:

- `audit/goms_d06_requested_recalc_summary.csv`
- `audit/goms_d06_requested_recalc_rowdiff.csv`

### Frequency identity

`graduate_total_n = employed_n + unemployed_n + inactive_n` 최대 차이:

- max abs gap: 2명
- nonzero rows: 84

이는 보고값과 일치한다. 발생 행은 `audit/goms_frequency_identity_nonzero_gaps.csv`에 전수 기록했다.

### Distribution sum reclassification

요청 기준으로 재분류:

| status | groups |
|---|---:|
| PASS | 498 |
| WARN | 74 |
| REVIEW | 0 |
| FAIL | 0 |

최대 오차는 1.7%p다. 따라서 기존 QA의 `WARN 0`은 요청 기준에서는 타당하지 않다. Local 2는 AMBER.

파일: `audit/goms_distribution_sum_reclassified.csv`

### Occupation crosswalk review

review_required 8건 전수 확인:

- D06 포함: True
- other 처리: 0
- arbitrary assignment flag: 0
- pre/post schema boundary violation: 0

임의배정 증거는 없지만, review_required=True인 중간확신 매핑이 D06 occupation metrics에 포함되어 있다. 이는 AMBER이며, P4 전에 crosswalk review 완료 또는 feature 사용 제한이 필요하다.

파일: `audit/goms_occupation_crosswalk_review_audit.csv`

### D07 recent profile

D06에서 2017-2019 recent profile을 전수 재계산했다.

- 7계열 x 모든 D07 컬럼 mismatch rows: 0
- 경제활동률: `graduate_total_n` 가중
- 취업자 조건부 분포·소득·시간: `employed_n` 가중
- trend 및 latest 2019 diagnostic: 재계산 일치

파일:

- `audit/goms_d07_recent_profile_recalc_summary.csv`
- `audit/goms_d07_recent_profile_recalc_rowdiff.csv`

## 6. Split and sample registry

split 재계산:

| split | rows | schools |
|---|---:|---:|
| train | 7,529 | 140 |
| val | 1,514 | 30 |
| test | 1,199 | 30 |

검산:

- 학교 총수: 200
- school split leakage: 0
- D08 split missing: 0

sample registry 재계산:

| sample_id | rows | schools |
|---|---:|---:|
| GRADE_ALL | 10,242 | 200 |
| GRADE_SELECTIVITY | 3,737 | 151 |
| EMPLOYMENT_HEALTH | 7,477 | 188 |
| PROGRESSION_GRADSCHOOL | 7,587 | 197 |
| JOINT_EMP_PROG | 7,477 | 188 |

파일: `audit/split_sample_summary.csv`

## 7. Log namespace audit

현재 로그는 출처별로 분리되어 있지 않다.

확인:

- `logs/run_manifest.json` = Local 1 manifest
- `logs/p3_1_run_manifest.json` = Local 1 manifest
- `shared_handoff/goms_run_manifest.json` = Local 2 manifest
- Local 2 manifest의 `logs` 항목은 generic `logs/decision_log.jsonl`, `logs/transformation_log.jsonl`, `logs/merge_audit.csv`, `logs/schema_deviation_report.csv`를 가리킴
- 현재 `logs/transformation_log.jsonl`은 D01-D05/D08 Local 1 레코드만 포함
- 현재 `logs/merge_audit.csv`는 Local 2 GOMS merge audit
- 현재 `logs/schema_deviation_report.csv`는 Local 1 D04/D08 schema warning
- agent 필드가 대부분 없음

판정: 추적성 WARN. 권고 경로는 `logs/local1/`, `logs/local2/`.

파일: `audit/logs_namespace_audit.csv`

## 8. RED criteria check

| 기준 | 결과 |
|---|---|
| D03/D08 10,242행 불일치 | PASS |
| D07 hash lineage 불일치 | PASS |
| school split leakage | PASS |
| 캠퍼스 충돌 자동매칭 | PASS |
| 후보 복수 fuzzy 자동확정 | PASS |
| GOMS_003 share 오용 | PASS |
| 직업 pre/post 무근거 결합 | PASS |
| 직무 자격증 직접 조인 | PASS |
| 평균을 표준편차로 복제 | PASS |

RED는 아니다. P4는 AMBER 조건부 readiness로 판정한다.
