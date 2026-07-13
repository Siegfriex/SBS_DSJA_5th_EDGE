# P2_G1 입결 완성 변수 의사결정 메모

작성 기준: `workbook/p2/p2_2/data/crawl_2024_admission` 원본 폴더, `data/actual_admission_2024`, `final/data/P2_G1_concat.csv`.

## 1. 결론

현재 크롤 원본폴더만으로는 `모든 대학-학과에 대해 70% cut을 정확 추출·정확 매칭한 완성 변수`를 만들 수 없다.

이유는 세 가지다.

1. 현재 크롤 범위가 최종 분석모집단 전체가 아니다.  
   최종 CSV는 227개 대학, 10,242개 대학-학과 라벨인데, `crawl_2024_admission`은 51개 대학만 수집되어 있다.

2. parser가 일부 대학의 다단 헤더 결과표를 놓쳤다.  
   `광운대학교`, `동덕여자대학교`, `숙명여자대학교`, `서울시립대학교` 등은 `raw_cells_json` 안에 0~100 백분위로 보이는 값이 있으나 `raw_percentile_70cut`으로 추출되지 않았다.

3. `raw_percentile_70cut` 안에도 백분위가 아닌 값이 섞여 있다.  
   경북대, 동국대, 덕성여대 등은 `raw_percentile_70cut`이 100을 초과한다. 이는 0~100 백분위가 아니라 대학별 환산점수, 과목 백분위 합, parser column shift 중 하나로 봐야 한다.

## 2. 현재 폴더에서 확인한 수치

| 항목 | 값 |
| --- | ---: |
| 최종 CSV 행 | 10,242 |
| 최종 CSV 대학 수 | 227 |
| 현재 crawl seed | 52 |
| 실제 raw HTML | 51 |
| raw 입결 row | 3,096 |
| raw `raw_percentile_70cut` non-null | 2,473 |
| raw `raw_percentile_70cut` 0~100 | 2,300 |
| raw `raw_percentile_70cut` 100 초과 | 173 |
| crosswalk row | 2,026 |
| crosswalk `valid_for_primary_model=True` | 1,406 |
| 최종 CSV 입결 non-null | 1,274 |
| 최종 CSV 입결 결측 | 8,968 |

결측 분해:

| 구분 | 행 | 대학 수 | 입결 non-null |
| --- | ---: | ---: | ---: |
| crawl 대상 밖 대학 | 6,998 | 181 | 0 |
| crawl 대상 안 대학 | 3,244 | 46 | 1,274 |

## 3. raw parser 문제 유형

### A. 다단 헤더 때문에 값이 있는데도 놓친 케이스

예시:

- 광운대학교: row cell 마지막에 `81.7`, `79.5`, `79.8` 등이 있으나 `raw_percentile_70cut`은 결측.
- 동덕여자대학교: row cell 마지막에 `74.67`, `76.33` 등이 있으나 `raw_percentile_70cut`은 결측.
- 숙명여자대학교: row cell 마지막에 `85.50`, `86.38`, `87.13` 등이 있으나 `raw_percentile_70cut`은 결측.
- 서울시립대학교: `국어`, `수학`, `탐구`, `평균`, `영어` 다단 헤더 구조라 평균 column을 별도로 잡아야 한다.

저장된 후보표:

- `tables/14_parser_rescue_candidate_rows.csv`

### B. `raw_percentile_70cut`이 100 초과라 백분위가 아닌 케이스

| 대학 | raw score non-null | 0~100 | 100 초과 | 판단 |
| --- | ---: | ---: | ---: | --- |
| 경북대학교 | 105 | 0 | 105 | 백분위가 아니라 과목합 또는 별도 척도 가능성 |
| 동국대학교 | 52 | 0 | 52 | 1000점 환산점수 계열 가능성 |
| 덕성여자대학교 | 7 | 0 | 7 | 1000점 환산점수 계열 가능성 |
| 삼육대학교 | 54 | 46 | 8 | 일부 행만 유효 백분위 |
| 강원대학교 | 62 | 61 | 1 | 단일 이상행 점검 필요 |

이 유형은 `raw_percentile_70cut`라는 컬럼명만 믿고 쓰면 안 된다. 완성 변수에서는 0~100 range gate를 통과한 값만 백분위로 인정한다.

### C. 모집단위-학과 매칭 문제

현재 crosswalk 상태:

| mapping_type | 행 |
| --- | ---: |
| alias_1to1 | 1,239 |
| exact_1to1 | 167 |
| unmatched | 226 |
| alias_not_present_in_university_grade_list | 177 |
| loose_candidate_review | 144 |
| broad_recruitment_unit | 73 |

`broad_recruitment_unit`는 `인문계열`, `자연계열`, `과학기술대학`처럼 하나의 모집단위가 여러 학과를 포괄할 수 있다. 정확한 대학-학과 입결 변수로 만들려면 임의 배분하면 안 된다.

## 4. 완성 변수로 승격하기 위한 결정사항

### 결정 1. 타깃 모집단

`P2_G1_concat.csv`의 227개 대학-학과 전체를 타깃으로 둔다.  
다만 ADIGA 정시 입결이 공개되지 않는 대학/학과는 `입결 완성 변수`가 아니라 `입결 미공개/미수집`으로 남긴다.

완성 변수의 의미는 다음으로 제한한다.

> 2024학년도 정시 수능위주/일반전형 계열에서 공식 결과표에 0~100 백분위로 제시된 최종등록자 70% cut 평균 백분위.

### 결정 2. parser 수리 우선순위

현재 raw HTML 51개에 대해 먼저 parser를 고친다.

필수 수정:

1. 다단 헤더 flattening  
   상단 헤더와 하단 헤더를 합쳐 `최종등록자 70% cut 평균 백분위` column을 찾아야 한다.

2. row-level range gate  
   `0 < value <= 100`만 백분위로 인정한다. 100 초과값은 별도 `converted_or_nonpercentile` 후보로 분리한다.

3. 평균 column 우선  
   서울시립대처럼 `국어/수학/탐구/평균/영어` 구조인 경우 `평균` column만 사용한다. 과목별 백분위 평균을 임의 계산하지 않는다.

4. header-only row 제거  
   raw row 안에 헤더 행이 들어온 경우 분석 row에서 제외한다.

### 결정 3. 크롤 범위 확장

완성 변수를 원하면 51개 대학으로는 부족하다. 다음 파일을 기준으로 미수집 대학 181개를 seed 확장 대상으로 만든다.

- `tables/13_admission_target_universities_not_crawled.csv`

필요 작업:

1. 최종 CSV의 227개 `학교명`을 ADIGA 대학코드로 매핑.
2. `adiga_univ_code` 없는 대학은 `adiga_code_missing`으로 별도 목록화.
3. `searchSyr=2025`, `source_result_year=2024` 조건으로 동일한 source registry schema로 재수집.
4. 새 HTML은 기존 `raw_html`과 같은 방식으로 sha256, source_url, retrieved_at 보존.

### 결정 4. 대학-학과 매칭 규칙

정확 매칭 순서:

1. 같은 대학 안 exact normalized match.
2. `P2_학과별_A비율_대학아님.csv` 기반 alias match.
3. 학부/전공 접미사 제거 후 1:1 match.
4. crosswalk manual review queue.

금지:

- `인문계열`, `자연계열`, `과학기술대학` 같은 광역 모집단위를 하위 학과에 임의 복제하지 않는다.
- 동일 대학 안 후보가 2개 이상이면 자동 확정하지 않는다.

### 결정 5. 대학-학과 단일 입결값 산출

최종 한 컬럼 `입결_프록시`는 다음 방식으로 만든다.

1. row 후보: 2024학년도 정시, 일반/수능위주 성격, 0~100 백분위 값.
2. 같은 대학-학과에 여러 모집군/전형이 있으면 `모집 인원` 가중평균.
3. 모집 인원이 없으면 단순평균.
4. 특수전형, 실기전형, 농어촌/고른기회 등은 일반전형 값이 없을 때도 자동 대체하지 않는다. 별도 후보로만 보관한다.

현재 `P2_G1_concat.csv`는 단순평균으로 붙인 상태라, 완성 변수 단계에서는 가중평균으로 다시 만들어야 한다.

## 5. 실행 순서

1. current crawl parser repair  
   51개 HTML에서 다단헤더/평균 column을 재추출해 raw table v2 생성.

2. range and metric validation  
   0~100 백분위만 `admission_percentile_70cut`로 승인. 100 초과는 분리.

3. seed expansion  
   최종 target 대학 227개 중 미수집 181개 ADIGA 코드 매핑 및 추가 crawl.

4. full raw rebuild  
   기존 51개 + 신규 대학 HTML을 같은 parser로 재파싱.

5. crosswalk rebuild  
   대학-모집단위-학과 alias 사전으로 exact/alias/manual queue 재생성.

6. manual queue 처리  
   unmatched, loose, broad는 사람이 확인해야 한다. broad는 하위 학과 배분 근거 없으면 확정 금지.

7. final master rebuild  
   `P2_G1_concat.csv`를 재생성하되 `입결_프록시`는 검증된 가중평균 70% cut 백분위만 사용.

## 6. 현재 의사결정

현재 산출된 `입결_프록시`는 그대로 본분석 완성 변수로 쓰지 않는다.  
다음 단계는 `parser repair + seed expansion + crosswalk manual review`다.

단기적으로는 현재 51개 대학 안에서 parser repair를 먼저 수행한다. 이 작업만으로 광운대, 동덕여대, 숙명여대, 서울시립대 등 일부 결측은 복구 가능하다. 그러나 전체 227개 대학 전수 완성 변수는 seed expansion 없이는 불가능하다.

