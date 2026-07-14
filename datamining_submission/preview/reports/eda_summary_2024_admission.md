# 2024학년도 정시 입시결과 크롤 데이터 EDA 보고서

## 1. 분석 목적

adiga.kr 대입정보포털에서 수집한 2024학년도 정시 입시결과 크롤 산출물이 H1/H2 분석의 입력으로 사용할 수 있는지 CRISP-DM 관점에서 점검했다. 이번 노트북은 웹 재수집과 통계모형 적합을 수행하지 않는다.

## 2. 입력 데이터

- seed: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/data/crawl_2024_admission/00_crawl_seed_university_2024.csv`
- source registry: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/data/crawl_2024_admission/01_crawl_source_registry.csv`
- raw admission result: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/data/crawl_2024_admission/02_admission_result_raw_2024.parquet`
- raw HTML cache: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/data/crawl_2024_admission/raw_html`
- 실행 시각: 2026-07-14T14:21:02 ~ 2026-07-14T14:21:11
- 실행 시간: 8.7초

## 3. 수집 커버리지

- 시드 행 수: 52
- 고유 크롤 대상 수: 51
- raw row 수: 3,096
- HTML 캐시 수: 51
- 한국외대 글로벌캠퍼스는 중복 adiga 코드로 설명되는 제외 시드로 분류했다.

## 4. 스키마와 관측 단위

관측 단위는 기본적으로 대학·정시군·전형명·모집단위·원본 테이블/행 조합이다. 동일 모집단위라도 정시군이나 전형명이 다르면 자동 삭제하지 않았다.

## 5. 결측 및 중복

- 모집단위 결측률: 0.0000%
- 헤더-only 파서 후보 행 수: 30
- 완전 중복 행 수: 0
- 파서 중복 후보 행 수: 693
- 설명형 표 오탐 후보 행 수: 0

## 6. 수치형 변수 품질

수치 파생변수는 원본 컬럼을 보존한 채 생성했다. 결측 입결은 0으로 채우지 않았다. 대학별 환산점수는 대학 간 동일척도로 해석하지 않는다.

## 7. 대학별 데이터 가용성

대학별 row 수, 고유 모집단위 수, 핵심 필드 가용률은 `eda_07_university_coverage.csv`와 `eda_16_university_quality_dashboard.csv`에 저장했다.

## 8. 입결 비교가능성

- Tier A: 104
- Tier B: 2,383
- Tier C: 35
- Tier D: 574

## 9. 모집단위 매핑 난이도

모집단위명은 department_like, major_like, division_like, college_like, broad_track, free_major, special_program, unknown으로 사전 분류했다. 이는 실제 crosswalk가 아니라 수동검토 작업량 추정용이다.

## 10. HTML 표본검증

10개 대학을 표본으로 HTML 캐시 존재, sha256 일치, 표본 모집단위 텍스트 포함 여부를 점검했다.

## 11. 주요 데이터 리스크

- 데이터 구조 리스크: 대학별 결과표 구조와 전형명 표기가 다르다.
- 수집 편향 리스크: adiga 캐시에 의존하므로 입학처 원문과 표본 이상 교차검증이 필요하다.
- 비교가능성 리스크: 대학 환산점수는 산식 차이가 있어 직접 비교하면 안 된다.
- 모집단위 매핑 리스크: 광역·자유전공·학부 단위가 학점학과와 1:1 대응되지 않을 수 있다.
- 통계분석 리스크: H1/H2 결론은 학점 타깃 병합과 모집요강 반영규칙 확인 후에만 가능하다.

## 12. Gate 1 판정

Gate 1: **CONDITIONAL PASS**

## 13. Gate 2 진행 조건

Gate 2 readiness: **READY_WITH_WARNINGS**

우선순위는 모집요강 반영규칙 수집, 입학처 결과 교차검증, 모집단위-학점학과 crosswalk, 학점 타깃 병합, H1/H2 모델 데이터 생성 순서다.

## 14. 최종 결론

기존 크롤 산출물만 사용해 EDA-ready 데이터를 생성했고, 51개 대학 수집 커버리지와 3,096개 raw row 구조를 재검증했다. H1/H2 통계 결론은 이번 노트북의 범위가 아니며, Gate 2에서 반영규칙과 crosswalk를 보완해야 한다.