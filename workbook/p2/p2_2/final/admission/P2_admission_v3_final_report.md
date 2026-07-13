# ADIGA 2024 정시 입결 v3 자동확정 대학 확장 보고: 최종 157개 대학 커버 (대상 227개 중)

## 결론

v2(51개 대학, 실제 매칭 성공 44개)에서 미수집이었던 대학을 추가로 크롤링해 `crawl_2024_admission_full`
(병합본, 기존 51개 + 신규 확정 168개)로 자동 추출·정규화·매칭을 다시 수행했다. 이번 산출물은
**ADIGA 코드가 자동확정(혹은 사람이 직접 확정)된 대학까지의 결과**이며, 최종 CSV에서 실제로
입결_프록시가 채워진 대학은 227개 중 **157개**다. 나머지는 ①ADIGA 코드/후보 확정이
안 된 대학(수동검토 대기), ②페이지는 수집했으나 결과표 파싱/학과 매칭이 안 된 대학,
③ADIGA 자체에 정시·수능위주 데이터가 없는 대학(과학기술원류·방송통신대 등)으로 나뉜다 —
아래 "0커버 대학" 섹션에서 원인별로 구분해서 확인할 수 있다.

## 적용한 의사결정

1. 같은 row에 `최종등록자 70% cut 평균 백분위` 또는 다중 헤더의 `평균/백분위` 열이 있으면 그 값을 1순위로 사용했다.
2. `raw_percentile_70cut`이 0~100이면 백분위로 인정했다.
3. `raw_percentile_70cut`이 100 초과이거나 백분위가 없고, 같은 row에 `대학별 환산점수`와 `총점/최고점`이 있으면 `점수 / 총점 * 100`으로 보조 정규화했다.
4. 농어촌, 기회균등, 고른기회, 저소득, 실기/체육 등 특별 전형은 최종 매칭에서 제외했다.
5. `인문계열`, `자유전공`, `광역`, 단독 `OO대학`처럼 세부 학과로 보기 어려운 광역 모집단위는 최종 매칭에서 제외했다.
6. 같은 대학-학과에 여러 row가 있으면 모집인원 가중평균을 사용했고, 모집인원이 없으면 단순평균으로 대체했다.
7. 최종 CSV에는 사용자가 요구한 컬럼만 유지했고, 추출/매칭 근거는 별도 감사 파일에만 남겼다.

## 주요 수치

| 항목 | 값 |
|---|---:|
| 원본 row | 6,316 |
| 원본 ADIGA `univ_id` 수 | 179 |
| 원본 표준 대학명 수 | 179 |
| v3 입결 metric 추출 row | 5,543 |
| v3 입결 metric 추출 대학 수 | 172 |
| 최종 매칭 source row | 4,341 |
| 대학-학과 입결 집계 row | 3,737 |
| 업데이트된 최종 CSV row | 10,242 |
| 최종 CSV 입결 non-null row | 3,737 |
| 최종 CSV 입결 non-null 대학 수 | 157 |

## metric source 분포

| source | rows |
| --- | --- |
| header_percentile | 4826 |
| missing_or_unusable | 770 |
| score_to_max_ratio | 701 |
| structural_last_percentile | 7 |
| raw_percentile_70cut_0_100 | 7 |
| header_row_excluded | 3 |
| structural_average_percentile | 2 |

## metric family 분포

| family | rows |
| --- | --- |
| percentile | 4842 |
| missing_or_unusable | 770 |
| score_ratio_normalized | 701 |
| header_row | 3 |

## 매칭/탈락 사유

| reason | rows |
| --- | --- |
| final_matched | 4341 |
| department_label_not_in_university_grade | 1140 |
| metric_missing_or_unusable | 600 |
| special_selection_excluded | 160 |
| broad_recruitment_unit_excluded | 39 |
| empty_recruitment_unit | 36 |

## 입결 커버리지 0인 대학 — 대분류

| zero_coverage_major_reason | 대학수 |
| --- | --- |
| crawled_but_zero_coverage | 57 |
| not_crawled_or_scope_excluded | 13 |

## 입결 커버리지 0인 대학 — 세부 원인

| zero_coverage_detail_reason | 대학수 |
| --- | --- |
| fetched_but_result_tables_0 | 35 |
| metric_exists_but_department_unmatched | 15 |
| not_crawled_or_scope_excluded | 13 |
| raw_fetched_but_no_usable_metric | 7 |

- `not_crawled_or_scope_excluded`: registry에 fetch 기록 자체가 없음 — **13개 전체가
  `00_scope_exclusion_2024_full.csv` 한 파일에 감사 추적 가능**: `manual_review_pending` 9개
  + `closed_institution`(폐교) 3개 + `code_duplicate_no_separate_source`(ADIGA가 별도 캠퍼스
  코드를 안 줘서 제외 — 경인교육대학교_제2캠퍼스) 1개 = 13개
- `fetched_but_result_tables_0`: **크롤은 했지만** Ⅳ탭에서 결과표를 못 찾음(`parse_status=partial`,
  `result_tables=0`) — `01_crawl_source_registry_merged.csv`에서 정확히 식별 가능. 표 구조가 기존
  51개와 달라 헤더 판별 로직이 못 잡는 경우가 다수로 추정된다(파서 한계, 아래 참고)
- `raw_fetched_but_no_usable_metric`: 결과표는 찾았으나 usable 백분위/점수 셀이 없음
- `metric_exists_but_department_unmatched`: 입결 수치는 뽑았으나 그 대학의 기존 학과_계열 목록과 매칭 실패(학과명 표기 차이)

## 입결 커버리지 0인 대학 상위 (원인 포함)

| 학교명 | final_grade_department_labels | raw_rows | raw_metric_nonnull | final_admission_department_labels | zero_coverage_major_reason | zero_coverage_detail_reason |
| --- | --- | --- | --- | --- | --- | --- |
| 부산외국어대학교 | 77 | 6 | 0 | 0 | crawled_but_zero_coverage | raw_fetched_but_no_usable_metric |
| 덕성여자대학교 | 76 | 7 | 7 | 0 | crawled_but_zero_coverage | metric_exists_but_department_unmatched |
| 한경국립대학교 | 75 | 26 | 25 | 0 | crawled_but_zero_coverage | metric_exists_but_department_unmatched |
| 건국대학교(글로컬)_분교 | 73 | 31 | 0 | 0 | crawled_but_zero_coverage | raw_fetched_but_no_usable_metric |
| 국립순천대학교 | 67 | 0 | 0 | 0 | crawled_but_zero_coverage | fetched_but_result_tables_0 |
| 국립목포대학교 | 65 | 33 | 0 | 0 | crawled_but_zero_coverage | raw_fetched_but_no_usable_metric |
| 세명대학교 | 65 | 34 | 0 | 0 | crawled_but_zero_coverage | raw_fetched_but_no_usable_metric |
| 호남대학교 | 64 | 0 | 0 | 0 | crawled_but_zero_coverage | fetched_but_result_tables_0 |
| 서원대학교 | 52 | 36 | 35 | 0 | crawled_but_zero_coverage | metric_exists_but_department_unmatched |
| 국립강릉원주대학교(폐교) | 51 | 0 | 0 | 0 | not_crawled_or_scope_excluded | not_crawled_or_scope_excluded |
| 상명대학교_제2캠퍼스 | 49 | 27 | 27 | 0 | crawled_but_zero_coverage | metric_exists_but_department_unmatched |
| 명지대학교_제2캠퍼스 | 44 | 0 | 0 | 0 | crawled_but_zero_coverage | fetched_but_result_tables_0 |
| 신경주대학교 | 43 | 19 | 1 | 0 | crawled_but_zero_coverage | metric_exists_but_department_unmatched |
| 우송대학교 | 41 | 0 | 0 | 0 | crawled_but_zero_coverage | fetched_but_result_tables_0 |
| 경남과학기술대학교(폐교) | 40 | 0 | 0 | 0 | not_crawled_or_scope_excluded | not_crawled_or_scope_excluded |

## 산출 파일

- row 단위 추출 결과: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/admission/P2_admission_row_metric_v3.csv`
- row 단위 매칭 감사: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/admission/P2_admission_match_v3.csv`
- 최종 CSV에 붙인 대학-학과 입결표: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/admission/P2_admission_proxy_v3_by_department.csv`
- 미매칭/검토 큐: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/admission/P2_admission_unmatched_review_v3.csv`
- 대학별 커버리지: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/admission/P2_admission_coverage_by_university_v3.csv`
- 업데이트된 최종 CSV: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/data/P2_G1_concat.csv`

## 남은 한계

- `00_scope_exclusion_2024_full.csv`에 남은 13개(`manual_review_pending` 9개 + `closed_institution`
  폐교 3개 + `code_duplicate_no_separate_source` 1개)가 감사 추적 가능하게 정리돼 있다.
  `manual_review_pending` 9개(과학기술원류 4개, 한국방송통신대학교, 한국예술종합학교,
  한국전통문화대학교, 한국에너지공과대학교, 순복음총회신학교)는 ADIGA 표준 검색 UI로 여러 별칭을
  시도해도 결과가 없어 현재로선 정시 CSAT 트랙 데이터 자체가 ADIGA에 없는 것으로 판단된다
  (과학기술원류는 자체 특별전형, 방송통신대는 원격대학, 예술종합학교는 실기 위주 전형이라 추정).
- alias 충돌 164건 중 실제 admission raw 데이터에 등장하는 것부터 keep/drop/canonical_override를
  결정한 감사 파일은 `P2_admission_alias_collision_decisions_v3.csv`에 있다(아래 참고).
- `department_label_not_in_university_grade`/`empty_recruitment_unit` 사유로 매칭되지 못한 대학이
  일부 남아 있다. 그 중 일부(중부대학교·신경주대학교 등)는 크로스워크가 아니라 **파서가 2행 헤더
  테이블의 두 번째 헤더 행을 데이터 행으로 오인하는 구조적 한계**이며, 51개 검증셋에 대한 회귀
  위험 때문에 이번 배치에서는 파서 자체를 고치지 않았다 — 별도 검증 배치로 분리해야 한다.
