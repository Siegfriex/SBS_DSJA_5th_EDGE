# P2 입결 70% cut v2 오토런 최종 보고

## 결론

현재 로컬 `crawl_2024_admission` 원본 폴더 기준으로 자동 추출·정규화·매칭을 끝냈다.  
다만 이 산출물은 **현재 수집된 51개 대학 HTML 안에서 가능한 최종본**이다. 최종 분석 CSV의 227개 대학 전체에 대해 완성 변수를 만들려면, 아직 크롤되지 않은 대학의 ADIGA 결과 HTML을 추가 수집해야 한다.

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
| 원본 row | 3,096 |
| 원본 ADIGA `univ_id` 수 | 51 |
| 원본 표준 대학명 수 | 47 |
| v2 입결 metric 추출 row | 2,794 |
| v2 입결 metric 추출 대학 수 | 47 |
| 최종 매칭 source row | 1,985 |
| 대학-학과 입결 집계 row | 1,651 |
| 업데이트된 최종 CSV row | 10,242 |
| 최종 CSV 입결 non-null row | 1,651 |
| 최종 CSV 입결 non-null 대학 수 | 44 |

## metric source 분포

| source | rows |
| --- | --- |
| header_percentile | 2580 |
| missing_or_unusable | 272 |
| score_to_max_ratio | 214 |
| header_row_excluded | 30 |

## metric family 분포

| family | rows |
| --- | --- |
| percentile | 2580 |
| missing_or_unusable | 272 |
| score_ratio_normalized | 214 |
| header_row | 30 |

## 매칭/탈락 사유

| reason | rows |
| --- | --- |
| final_matched | 1985 |
| department_label_not_in_university_grade | 661 |
| metric_missing_or_unusable | 248 |
| special_selection_excluded | 89 |
| university_not_in_final_grade_universe | 61 |
| empty_recruitment_unit | 30 |
| broad_recruitment_unit_excluded | 22 |

## 입결 커버리지 0인 대학 상위

| 학교명 | final_grade_department_labels | raw_rows | raw_metric_nonnull | final_admission_department_labels |
| --- | --- | --- | --- | --- |
| 신라대학교 | 144 | 0 | 0 | 0 |
| 동의대학교 | 138 | 0 | 0 | 0 |
| 경상국립대학교 | 137 | 0 | 0 | 0 |
| 국립공주대학교 | 128 | 0 | 0 | 0 |
| 대구가톨릭대학교 | 127 | 0 | 0 | 0 |
| 국립부경대학교 | 120 | 0 | 0 | 0 |
| 대구한의대학교 | 113 | 0 | 0 | 0 |
| 동아대학교 | 109 | 0 | 0 | 0 |
| 전주대학교 | 104 | 0 | 0 | 0 |
| 영남대학교 | 100 | 0 | 0 | 0 |
| 상지대학교 | 99 | 0 | 0 | 0 |
| 목원대학교 | 98 | 0 | 0 | 0 |
| 한신대학교 | 98 | 0 | 0 | 0 |
| 제주대학교 | 94 | 0 | 0 | 0 |
| 계명대학교 | 93 | 0 | 0 | 0 |

## 산출 파일

- row 단위 추출 결과: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/admission/P2_admission_row_metric_v2.csv`
- row 단위 매칭 감사: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/admission/P2_admission_match_v2.csv`
- 최종 CSV에 붙인 대학-학과 입결표: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/admission/P2_admission_proxy_v2_by_department.csv`
- 미매칭/검토 큐: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/admission/P2_admission_unmatched_review_v2.csv`
- 대학별 커버리지: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/admission/P2_admission_coverage_by_university_v2.csv`
- 업데이트된 최종 CSV: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/data/P2_G1_concat.csv`

## 남은 한계

현재 원본 폴더 자체가 51개 대학만 포함하므로, 227개 대학 전체의 완성 변수는 아니다.  
네트워크 크롤을 추가로 허용해 ADIGA 결과 HTML을 181개 미수집 대학까지 확장하면 같은 v2 파서와 매칭 규칙으로 다시 실행하면 된다.
