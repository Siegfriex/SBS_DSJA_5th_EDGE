# P2-G4 Data Collection Lineage and Method Audit

- 생성시각: `2026-07-13T15:42:32`
- 작업 루트: `/home/sieg/projects-wsl/SBS_dataScience`
- 기존 catalog 참조: `workbook/p2/p2_4/p4_preprocessing_integrity_v1/reports/DATA_SOURCE_CATALOG.md`
- live web 재수집은 수행하지 않았다. 본 감사는 현행 로컬 코드·로그·raw cache·manifest를 기준으로 한다.

## Executive Summary

현재 프로젝트의 데이터 계보는 `공식 원천 -> 로컬 원자료/cache -> 정규화·파생 산출물 -> D08 -> strict-clean/manual-approved 모델링 입력`으로 정리된다. KEDI/대학알리미 계열은 주로 로컬 다운로드 파일의 shape/hash로 고정되어 있고, ADIGA와 GOMS는 코드상 크롤/다운로드 절차와 raw snapshot/manifest가 남아 있다.

최종 모델링 기준은 원본 D08가 아니라 strict-clean D08다. 원본 D08는 `10,242 x 151`, strict-clean D08는 `7,592 x 151`이며, manual-approved feature registry에서 사용 승인된 feature는 `131`개다.

## 1. 공식 원천 -> 로컬 -> 파생 -> 최종 D08 계보

| source_id | official_institution | portal_name | local_raw | local_shape | normalized_or_derived | derived_shape | final_touchpoint | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-KEDI-HIGHER | KEDI | KESS/EDSS/local download | workbook/p2/p2_2/final/data/2024년 고등 학교별X학과별 입학정원 지원 입학 학생 외국인학생 졸업 교원_240912H.xlsx | 학교별 학과별 주요 현황:35444x129; 용어 정의:16x3; 요약정보:25x13 | workbook/p2/p2_3/p4_handoff_candidate/local1/dept_headcount_master_2024.parquet | 34969 x 186 | D01 -> D03 -> D08/strict-clean | A for local hash/shape; direct download URL not preserved |
| SRC-ACADEMY-GRADE | 대학알리미/KEDI 고등통계 | 대학알리미 | workbook/p2/p2_2/P2__전체대학학점비율.csv | 31743 x 53 | workbook/p2/p2_3/p4_handoff_candidate/local1/dept_outcomes_2024.parquet | 10242 x 37 | D02 -> D08/strict-clean | A for local data; direct download URL not preserved |
| SRC-KEDI-EMP | 대학알리미/KEDI 취업통계 | 대학알리미 | workbook/p2/p2_2/p2_취업률_데이터.csv | 9951 x 95 | workbook/p2/p2_3/p4_handoff_candidate/local1/dept_outcomes_2024.parquet | 10242 x 37 | D02 -> D08/strict-clean | A for local data; direct download URL not preserved |
| SRC-KEDI-PROGRESSION | 대학알리미/KEDI 취업통계 | 대학알리미 | workbook/p2/p2_2/p2_상위대학_진학률.csv | 9951 x 62 | workbook/p2/p2_3/p4_handoff_candidate/local1/dept_outcomes_2024.parquet | 10242 x 37 | D02 -> D08/strict-clean | A for local data; direct download URL not preserved |
| SRC-KCUE-ADIGA | 한국대학교육협의회 | 대입정보포털 어디가 | workbook/p2/p2_2/data/crawl_2024_admission_full/02_admission_result_raw_2024_merged.csv | 6316 x 18 | workbook/p2/p2_2/final/admission/P2_admission_proxy_v3_by_department.csv | 3737 x 8 | admission proxy -> D02 -> D08/strict-clean | A/B: official portal HTML + local registry/hash; 모집단위-학과 collapse는 내부 파생 |
| SRC-KEIS-GOMS | 한국고용정보원 | 고용조사분석시스템 GOMS 주제별 통계 | workbook/p2/p2_2/data/goms_subject_crawl/02_download_manifest.csv | 39 x 10 | workbook/p2/p2_3/shared_handoff/goms_major_profile_recent.parquet | 7 x 29 | D07_HANDOFF -> D08/strict-clean | A/B: official system export; 주제별 분석 결과는 가중 표본분석 결과로 해석 제한 |
| SRC-MAJOR-WAGE-CONTEXT | 미확정 | local project source workbook | workbook/p2/p2_3/P2_G2_임금분류_학부대학원.CSV | 14 x 66 | workbook/p2/p2_3/p4_handoff_candidate/local1/wage_reference_by_major.parquet | 14 x 87 | D04 -> D08/strict-clean | B/C: local hash exists; 발행기관/direct URL 미확정 |
| SRC-JOB-CERT-BRIDGE | 미확정 | local curated bridge | workbook/p2/p2_3/P2_G2_직무별_자격증매핑.CSV | 24 x 26 | workbook/p2/p2_3/p4_handoff_candidate/local1/job_cert_bridge.parquet | 24 x 32 | D05 reference only; manual-approved scope drops direct join | C for external provenance; valid as internal reference only |
| SRC-CREDIT-POLICY | 대학별 학칙/학사안내로 추정 | local policy workbook | workbook/p2/p2_2/학점포기제도현황.xlsx | 종합:54x3 | workbook/p2/p2_3/p4_handoff_candidate/local1/dept_outcomes_2024.parquet | 10242 x 37 | D02 -> D08/strict-clean | C: 대학별 URL/조항 번호 manifest 미완성 |

## 2. 코드베이스에서 확인한 크롤·수집 증거

| collection | evidence_file | rows | status_summary | method_signal |
| --- | --- | --- | --- | --- |
| ADIGA | workbook/p2/p2_2/data/crawl_2024_admission_full/01_crawl_source_registry_merged.csv | 214 | {'success': 179, 'partial': 35} | source_url, retrieved_at, http_status, content_sha256, raw_file_path, parser_version 보존 |
| ADIGA | workbook/p2/p2_2/data/crawl_2024_admission_full/02_admission_result_raw_2024_merged.csv | 6316 | {'columns': 18, 'raw_html_files': 163} | raw_header_json/raw_cells_json와 semantic field를 동시 보존 |
| GOMS | workbook/p2/p2_2/data/goms_subject_crawl/02_download_manifest.csv | 39 | {'success': 39} | topic_id, kind, measure, file_path, sha256, year range 보존 |
| GOMS | workbook/p2/p2_2/data/goms_subject_crawl/qa/final_qa_summary.csv | 1 | {'total_topics': 39, 'categorical_topics': 21, 'continuous_topics': 18, 'parse_failures': 0, 'proportion_review_count': 0, 'year_coverage_review_count': 0, 'duplicate_rows_categorical': 0, 'duplicate_rows_continuous': 0, 'cross_file_hash_duplicates': 'PASS', 'stddev_available': False, 'stddev_reason': 'site JS bug (callbackGOMSSubject unconditionally resets viewType2 to index 0 on every render) makes 분산/표준편차 unreachable via official UI/CSV flow'} | parse failure, proportion sum, year coverage, duplicate, stddev 제한 QA |
| GOMS normalized distribution | workbook/p2/p2_2/data/goms_subject_crawl/normalized/goms_distribution_long.csv | 29160 | {'columns': 9} | normalized downstream table |
| GOMS normalized continuous | workbook/p2/p2_2/data/goms_subject_crawl/normalized/goms_continuous_long.csv | 2230 | {'columns': 8} | normalized downstream table |
| ADIGA department proxy | workbook/p2/p2_2/final/admission/P2_admission_proxy_v3_by_department.csv | 3737 | {'columns': 8} | normalized downstream table |

## 3. 데이터사이언스 6프로세스별 기술적 방법론

| process | project_application | technical_method | audit_artifact |
| --- | --- | --- | --- |
| 1. 문제정의 | 학과 단위 성적/입결/취업/진학 차이를 설명할 수 있는 D08 모델링 mart 구축 | 타깃 후보와 관측 grain을 먼저 고정하고, source별 grain mismatch를 명시 | p4_target_candidate_registry, source catalog, strict target sample counts |
| 2. 데이터 수집 | KEDI/대학알리미 local download, ADIGA HTML crawl, GOMS Playwright export 수집 | 공식 포털 원천 URL + 로컬 raw hash + registry/log 보존. ADIGA/GOMS는 raw HTML/XLS snapshot 보존 | ADIGA registry, GOMS download_manifest, P4_HANDOFF_MANIFEST |
| 3. 저장·계보화 | 원천 raw, normalized long/proxy, D01~D08, strict-clean을 분리 저장 | sha256, shape, parser_version, source_url, retrieved_at, row lineage를 남김 | source_eda tables, P4_HANDOFF_MANIFEST, strict_clean_manifest |
| 4. 전처리·통합 | 학교/캠퍼스/학과명 정규화, 모집단위-학과 proxy, major7/GOMS context 결합 | stable key join, alias bridge, campus-aware match, row-order join 금지, cardinality QA | bridge_* csv, p4_1_data_contract QA, p4_cleaning_handoff_v3 QA |
| 5. EDA·품질감사 | 결측, 중복, target leakage, rate extreme, source unavailable, sample bias 확인 | column registry, missing profile, duplicate audit, target-specific denylist, small denominator deletion | p4_2_model_readiness QA, source_eda review_queues, strict_row_policy_audit |
| 6. 모델링 인계 | strict-clean D08와 manual-approved feature/target/scope policy를 최종 입력으로 확정 | manual_approved_p4_use=True feature만 사용, target별 strict_target_keep만 사용 | manual_approved_feature_registry, manual_approved_target_and_scope_policy |

## 4. 크롤링·데이터수집 방법 상세

### 4.1 ADIGA 어디가 입결 수집

- 코드 증거: `scripts/crawl_adiga_full_seed.py`, `scripts/crawl_adiga_full_fetch.py`, `scripts/adiga_crawl_lib.py`, `scripts/reparse_adiga_raw_full.py`.
- 대상 URL: `https://www.adiga.kr/`의 대학 상세/검색 flow.
- 수집 방식: `curl_cffi.requests.Session(impersonate='safari')`로 세션 생성, 상세 선택 페이지에서 CSRF token 획득, `univAjax.do`에 대학명 검색 POST, 확정된 ADIGA code로 상세 HTML GET.
- 캐시 정책: `raw_html/*.html`에 상세 페이지 HTML을 저장하고, registry에 `source_url`, `retrieved_at`, `http_status`, `content_sha256`, `raw_file_path`, `parser_version`을 남긴다.
- 파싱 방식: BeautifulSoup으로 `.tabCon.univInfoCon` 중 수능위주전형 탭의 표를 찾고, `모집단위`, `경쟁률`, `충원`, `cut/백분위` signature로 결과표를 식별한다. multi-row header와 rowspan은 `flatten_header()`와 선두 컬럼 carry-forward로 복원한다.
- 계보 보존: semantic field 매핑이 실패해도 `raw_header_json`, `raw_cells_json`을 보존한다. `reparse_adiga_raw_full.py`는 네트워크 재요청 없이 cached HTML만 재파싱하도록 설계되어 재현성이 좋다.
- 최종 사용: raw `6,316 x 18`에서 학과 proxy `3,737 x 8`로 정규화되어 D02/D08의 `selectivity_proxy_pct` 계열로 들어간다.

### 4.2 GOMS 주제별 통계 수집

- 코드 증거: `workbook/p2/p2_2/goms_subject_crawl_portfolio/scripts/crawl_goms_subjects.py`, `normalize_and_qa.py`, `scripts/build_p2_g3_goms_local2.py`.
- 대상 URL: `https://analysis.keis.or.kr/gomsSubject.do?goIndex=3-1`.
- 수집 범위: 경제활동 상태 3개, 현재 일자리 18개, 근로소득 9개, 근로시간 9개 총 39개 topic.
- 렌더링 방식: Playwright headless Chromium으로 실제 UI를 조작한다. 범주형은 `빈도+비중`, 연속형은 `평균` export를 저장한다.
- 저장 방식: `raw_downloads/frequency_share/*.xls`, `raw_downloads/mean/*.xls`, `page_snapshots/html/*.html`, screenshot, `02_download_manifest.csv`, request/response log를 남긴다.
- 사이트 이슈 대응: CSV 다운로드가 popup에서 발생하는 문제, 초기 기본 주제 응답이 후속 주제를 덮는 race condition, 연속형 표준편차 선택이 평균으로 리셋되는 JS 문제를 코드에서 명시적으로 처리한다. 표준편차는 구조적으로 수집하지 않고 `stddev_available=False`로 기록한다.
- 정규화 방식: 저장된 XLS-like HTML table을 `pd.read_html`로 읽고, 범주형은 `topic/year/subgroup/dimension/measure_type/value`, 연속형은 `topic/year/dimension/value` long-format으로 변환한다.
- 최종 사용: normalized long에서 D06/D07 계열 맥락을 만들고, 최근 2017~2019 major profile `7 x 29`가 D08의 GOMS context 28개 컬럼으로 들어간다.

### 4.3 KEDI/대학알리미/EDSS 계열 local download

- 코드상 자동 크롤보다 로컬 다운로드 파일을 source of truth로 사용한다.
- KEDI raw Excel은 sheet shape와 sha256이 manifest에 남아 있고, D01 headcount master `34,969 x 186`으로 복원된다.
- 대학알리미 성적/취업/진학 CSV는 D02 outcome spine으로 통합된다. direct download URL은 저장되어 있지 않으므로 공식 포털 URL과 로컬 hash를 함께 citation anchor로 둬야 한다.

### 4.4 내부 계약·수기 계보

- 임금/기업/자격 context와 학점포기제는 외부 공식 URL 계보가 약하다.
- D04 임금 context는 local contract와 hash는 있으나 발행기관/direct URL이 미확정이므로 KEDI 공식 원자료라고 단정하지 않는다.
- D05 job_cert는 직무분류 grain이므로 학과행 직접 조인이 금지되며, manual review에서 `drop_D05_scope`로 확정됐다.

## 5. 최종 D08 및 strict-clean 인계 상태

```json
{
  "legacy_d08": {
    "path": "workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet",
    "exists": true,
    "shape": "10242 x 151",
    "sha256": "598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962"
  },
  "strict_clean_d08": {
    "path": "workbook/p2/p2_4/source_eda/strict_clean_v1/mart_department_model_base_2024_strict_drop.parquet",
    "exists": true,
    "shape": "7592 x 151",
    "sha256": "5f56e375fd1c0474a5e55652859ae007e2f45becd6d3350ee4c82e21fab8df9b"
  },
  "strict_target_sample_membership": {
    "path": "workbook/p2/p2_4/source_eda/strict_clean_v1/strict_target_sample_membership.csv",
    "exists": true,
    "shape": "61452 x 7",
    "sha256": "29bf19120774e7d0a86e1c6b6892d012832f3fd6fd5dbed5e6a752e8f2e0e61c"
  },
  "manual_feature_registry": {
    "path": "workbook/p2/p2_4/source_eda/human_handoff_packet/03_MODEL_INPUT/manual_approved_feature_registry.csv",
    "exists": true,
    "shape": "198 x 11",
    "sha256": "2cdb7797c4619c625fc6a171710970b7691446f4d62cae9accd2ab5c68f15051"
  },
  "manual_scope_policy": {
    "path": "workbook/p2/p2_4/source_eda/human_handoff_packet/03_MODEL_INPUT/manual_approved_scope_policy.json",
    "exists": true,
    "shape": "json_keys=5",
    "sha256": "a54746950e43af33ad666b405c401f4f1a2f6fef9e35045016cf3f3d27e242ad"
  },
  "manual_target_policy": {
    "path": "workbook/p2/p2_4/source_eda/human_handoff_packet/03_MODEL_INPUT/manual_approved_target_and_scope_policy.csv",
    "exists": true,
    "shape": "32 x 7",
    "sha256": "c3f56647cc63135dd74609ed4b0436d0058655fc0e82354691b276a067d5b389"
  },
  "manual_policy": {
    "all_null_context_features": {
      "columns": [
        "ctx24_industry_hhi",
        "ctx24_industry_top3_pct"
      ],
      "decision": "exclude_from_features"
    },
    "panel_track": {
      "decision": "drop_panel_track",
      "artifacts": [
        "mart_department_panel_2023_2025",
        "mart_A_rate_transition_2023_2025"
      ]
    },
    "d05_job_cert": {
      "decision": "drop_D05_scope",
      "columns": 35
    },
    "historical_2023_targets": {
      "decision": "exclude_2023_target",
      "columns": [
        "domestic_progression_rate_pct",
        "graduate_school_progression_rate_pct",
        "health_employment_rate_pct",
        "overseas_progression_rate_pct",
        "progression_rate_pct",
        "selectivity_proxy_pct",
        "university_progression_rate_pct",
        "vocational_college_progression_rate_pct"
      ]
    },
    "target_leakage": {
      "decision": "keep_blocked",
      "pairs": 16
    },
    "deleted_rows": {
      "decision": "no_deleted_rows_recovered",
      "rows": 2650
    }
  },
  "manual_approved_feature_counts": {
    "true": 131,
    "false": 67
  },
  "manual_scope_decision_counts": {
    "inherit_strict_global_policy": 159,
    "drop_D05_scope_manual_review": 35,
    "exclude_from_features_manual_all_null": 4
  }
}
```

## 6. 알려진 제한과 보완 작업

| risk | where | handling |
| --- | --- | --- |
| direct download URL 누락 | KEDI/대학알리미 일부 raw | 공식 포털 URL + 로컬 raw sha256으로 provenance anchor를 둔다. |
| ADIGA 모집단위-학과 collapse | selectivity_proxy_pct | raw row와 proxy를 분리하고, proxy는 A/B 등급 파생 변수로 표기한다. |
| GOMS 주제별 표의 해석 | GOMS context | 공식 원자료가 아니라 주제별 분석시스템의 가중 표본분석 결과임을 표기한다. |
| GOMS 표준편차 수집 불가 | continuous topics | 사이트 JS 버그로 mean만 수집하고 final_qa_summary에 stddev_available=False 기록. |
| 계열별 임금 원 발행기관 미확정 | D04 wage context | KEDI 공식 원본으로 단정하지 않고 local contract B/C로 분류한다. |
| D05 job_cert 직접 조인 금지 | D05 | manual review에서 drop_D05_scope로 확정, bridge 설계 전까지 feature 제외. |
| strict-clean 이후 삭제 행 복구 없음 | D08 strict-clean | 2,650행 삭제 유지. 복구할 개별 원천 증빙 없음. |

## 7. 후속 작업 권고

1. 모델링/EDA는 원본 D08가 아니라 `source_eda/strict_clean_v1/mart_department_model_base_2024_strict_drop.parquet`를 사용한다.
2. feature 선택은 `manual_approved_feature_registry.csv`의 `manual_approved_p4_use == True`만 사용한다.
3. target별 표본은 `strict_target_sample_membership.csv`의 `strict_target_keep == True`로 제한한다.
4. ADIGA/GOMS는 raw cache와 registry가 있으므로 재크롤보다 cache 재파싱을 우선한다.
5. 공시 인용 수준을 높이려면 KEDI/대학알리미/임금 context/학점포기제 direct download URL과 기준일 manifest를 추가해야 한다.
