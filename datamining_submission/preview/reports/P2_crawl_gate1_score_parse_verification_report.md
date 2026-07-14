# crawl.ipynb Gate0/Gate1 성적 파싱 검증

## 결론

`crawl.ipynb` 기준 실제 입력 엑셀은 54개가 아니라 52행이다. 그중 크롤 대상은 51개이고, 1개는 같은 ADIGA 코드 중복이라 제외됐다. Gate1 산출물 자체에는 대상 51개 모두 들어갔다.

단, `crawl.ipynb`의 v1 의미 컬럼(`raw_score_70cut`, `raw_percentile_70cut`)만 보면 모든 대학의 성적이 완전하게 들어간 것은 아니다. 다중 헤더 대학 일부는 v1 의미 컬럼이 비었지만, `raw_cells_json`에는 원문 성적표가 보존되어 있고 v2 추출에서 복구됐다.

## Gate0/Gate1 무결성

| 항목 | 값 |
|---|---:|
| 순위 엑셀 row | 52 |
| target institution row | 51 |
| target excluded row | 1 |
| source registry row | 51 |
| source registry success | 51 |
| raw HTML existing | 51 |
| raw rows > 0인 target | 51 |
| raw CSV/parquet row | 3096 |

별도 무결성 확인 결과:

- `02_admission_result_raw_2024.csv`: 3,096행 x 18열
- `02_admission_result_raw_2024.parquet`: 3,096행 x 18열
- CSV/parquet 컬럼 동일: True
- CSV/parquet `raw_row_id` set 동일: True
- registry `content_sha256`와 raw HTML 파일 SHA 일치: 51/51
- registry 51개 source 모두 raw row 보유

## 성적 파싱 상태

| 기준 | 값 |
|---|---:|
| v1 의미 컬럼에 score 또는 percentile이 있는 target | 48 / 51 |
| v1 `raw_percentile_70cut` 0~100 보유 target | 43 / 51 |
| v2 metric 보유 target | 51 / 51 |
| v1 score/percentile field가 있는 raw row | 2830 / 3096 |
| v1 percentile 0~100 raw row | 2293 |
| v1 percentile 100 초과 raw row | 173 |
| v2 metric raw row | 2794 / 3096 |

## v1 의미 컬럼 누락이나 v2에서 복구된 대학

| crawl_priority | univ_name_raw | univ_name_std | raw_rows | v1_any_score_field_nonnull | v2_metric_nonnull | v2_percentile_rows | v2_score_ratio_rows |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 16 | 숙명여대 | 숙명여자대학교 | 42 | 0 | 40 | 40 | 0 |
| 26 | 광운대 | 광운대학교 | 65 | 0 | 57 | 57 | 0 |
| 36 | 동덕여대 | 동덕여자대학교 | 86 | 0 | 76 | 76 | 0 |

## 제외 seed

| crawl_priority | univ_name_raw | univ_name_std | univ_id | target_institution_flag | seed_note |
| --- | --- | --- | --- | --- | --- |
| 38 | 한국외대(글캠) | 한국외국어대학교 | U0000192 | False | adiga에 별도 캠퍼스 코드 없음 — U0000192와 동일 페이지, 중복크롤링 방지 위해 크롤링 대상에서 제외 |

## 해석

- `크롤 자체가 들어갔냐`: 들어갔다. target 51개 모두 registry, raw HTML, raw row가 있다.
- `crawl.ipynb v1 의미 컬럼만으로 모든 대학 성적이 파싱됐냐`: 아니다. 48/51 target만 v1 score 또는 percentile 의미 컬럼이 채워졌다.
- `기존 raw HTML/raw_cells_json에서 못 잡냐`: 잡을 수 있다. 숙명여대, 광운대, 동덕여대는 v1 컬럼은 비었지만 v2에서 `raw_cells_json`을 재해석해 백분위 row를 복구했다.
- `그래도 최종 결측이 남는 이유`: 51개 크롤 대학 내부에서도 최종 학점 데이터의 세부 학과 라벨과 ADIGA 모집단위가 1:1로 대응하지 않는 경우가 많고, 전체 227개 대학 중 181개 대학은 raw HTML 자체가 없다.
