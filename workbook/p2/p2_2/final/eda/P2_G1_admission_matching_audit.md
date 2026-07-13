# P2_G1 입결 매칭 감사

작성 기준: `P2_G1_concat.csv`, `data/crawl_2024_admission`, `data/actual_admission_2024/recruitment_grade_department_crosswalk_2024.csv`.

## 결론

현재 `P2_G1_concat.csv`의 `입결_프록시`는 전체 대학-학과를 전수 커버한 값이 아니다. `raw_percentile_70cut`를 원천으로 사용했지만, crawl 원자료 자체가 전체 227개 대학을 덮지 않고, crawl된 대학 안에서도 모집단위-학과 매칭이 일부만 성립한다.

따라서 입결 결측률 87.56%는 단순 오류라기보다 아래 세 요인의 합이다.

1. 최종 CSV는 227개 대학인데, 입결 raw crawl은 51개 대학만 있다.
2. crawl된 대학 51개 중 최종 CSV에 같은 학교명으로 잡힌 대학은 46개다.
3. crawl된 대학 내부에서도 raw 모집단위가 성적분포 학과 라벨과 정확히 맞지 않아 crosswalk에서 탈락하거나 broad/loose/unmatched로 남는다.

## 전체 단계별 커버리지

| 단계 | 값 |
| --- | ---: |
| 최종 CSV 행 | 10242 |
| 최종 CSV 대학 수 | 227 |
| raw crawl 행 | 3096 |
| raw crawl 대학 수 | 51 |
| raw `raw_percentile_70cut` non-null | 2473 |
| raw `raw_percentile_70cut` 0~100 | 2300 |
| raw `raw_percentile_70cut` 100 초과 | 173 |
| raw score가 있는 대학 수 | 43 |
| crosswalk 행 | 2026 |
| crosswalk score non-null | 2018 |
| crosswalk `valid_for_primary_model=True` | 1406 |
| 실제 입결 모델 행 | 1216 |
| 실제 입결 모델 대학 수 | 35 |
| 최종 CSV 입결 non-null | 1274 |

## 최종 CSV 결측 분해

| 구분 | 행 | 대학 수 | 입결 non-null |
| --- | ---: | ---: | ---: |
| crawl 대상 밖 대학 | 6998 | 181 | 0 |
| crawl 대상 안 대학 | 3244 | 46 | 1274 |

즉 전체 결측 8968행 중 6998행은 애초에 crawl 대상 밖 대학에서 발생한다. 나머지 1970행은 crawl 대상 대학 안에서 학과 매칭이 안 되거나 raw score가 없는 경우다.

## crosswalk 상태

| mapping_type | 행 |
| --- | ---: |
| alias_1to1 | 1239 |
| unmatched | 226 |
| alias_not_present_in_university_grade_list | 177 |
| exact_1to1 | 167 |
| loose_candidate_review | 144 |
| broad_recruitment_unit | 73 |

현재 `P2_G1_concat.csv`에서는 품질 플래그를 최종 컬럼에서 제거하라는 지시에 따라 `mapping_type`, `valid_for_primary_model`, `score_comparability_tier`를 노출하지 않았다. 그러나 결측 원인 진단에는 이 내부 crosswalk 상태가 필요하다.

## 100 초과 raw 값

`raw_percentile_70cut`가 이미 정규화된 백분위라면 0~100 범위를 벗어나면 안 된다. 현재 raw에는 100 초과값이 173개 있다.

| 대학 | raw score non-null | 0~100 | 100 초과 | 최종 입결 non-null |
| --- | ---: | ---: | ---: | ---: |
| 경북대학교 | 105 | 0 | 105 | 0 |
| 동국대학교 | 52 | 0 | 52 | 0 |
| 삼육대학교 | 54 | 46 | 8 | 16 |
| 덕성여자대학교 | 7 | 0 | 7 | 0 |
| 강원대학교 | 62 | 61 | 1 | 47 |

이 값들은 최종 CSV에는 100 초과로 들어가지 않았다. 하지만 raw 단계에서는 백분위가 아닌 대학별 환산점수 또는 parser column shift 가능성을 의심해야 한다.

## 저장된 상세 감사표

- `tables/12_admission_raw_crosswalk_final_coverage_by_university.csv`

