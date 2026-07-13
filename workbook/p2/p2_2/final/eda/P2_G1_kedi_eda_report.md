# P2_G1_kedi — GOMS 추출 CSV 전수 EDA

## 데이터 계약

- 원본 위치: `workbook/p2/p2_2/data/goms_subject_crawl/raw_downloads/`
- 정규화 위치: `workbook/p2/p2_2/data/goms_subject_crawl/normalized/`
- EDA 산출 위치: `workbook/p2/p2_2/data/goms_subject_crawl/eda/`
- 검토 대상: 39개 주제, 정규화 행 29,160 + 2,230
- 원본 `.xls` 39개는 수정하지 않았고, HTML 표로 전수 재파싱 가능 여부만 확인했다.

## 전수 QA 요약

- 최종 매니페스트 성공 주제: 39/39
- 원본 HTML-XLS 재파싱 성공: 39/39
- 주제별 연도 커버리지: 29개 주제는 2007~2019년 13개 연도, 직업분류 개편 주제는 `~2016` 5개와 `2017~` 5개로 분리되어 모두 기대 범위 PASS
- 파싱 실패: 0
- 비중 합계 REVIEW: 0
- 중복 행: 범주형 0, 연속형 0
- 표준편차/분산: 사이트 UI/스크립트 버그로 공식 다운로드 경로에서 취득 불가, 최종 기준선에서는 평균만 사용

## 2019년 전공계열 기준선

- 월평균 근로소득은 의약 271.8만원이 가장 높고, 예체능 192.7만원이 가장 낮다.
- 가중 빈도 기반 취업률은 의약 81.2%가 가장 높고, 인문 58.3%가 가장 낮다.
- 상용근로자 비중은 의약 89.7%가 가장 높다.
- 이 값은 대학별 실적이 아니라 2007~2019년 GOMS 표본조사의 전공계열별 노동시장 구조 기준선이다.

## 핵심 산출 테이블

- `goms_topic_inventory.csv`: 39개 원본 파일/정규화/스키마 전수 인벤토리
- `goms_topic_year_coverage.csv`: 주제-연도별 정규화 행 커버리지
- `goms_major_year_baseline.csv`: 전공계열-연도별 기준선 전체
- `goms_major_2019_snapshot.csv`: 2019년 전공계열 기준선 스냅샷
- `goms_major_2007_2019_trend.csv`: 2007년 대비 2019년 변화
- `goms_major_top3_industry_2019.csv`: 2019년 전공계열별 상위 산업 3개
- `goms_major_top3_job_2019.csv`: 2019년 전공계열별 상위 직업군 3개
- `goms_metric_correlation_2019.csv`: 2019년 주요 수치형 기준선 상관행렬

## 그림

- `workbook/p2/p2_2/data/goms_subject_crawl/eda/figures/major_monthly_income_2019.png`
- `workbook/p2/p2_2/data/goms_subject_crawl/eda/figures/major_core_metrics_trend_2007_2019.png`
- `workbook/p2/p2_2/data/goms_subject_crawl/eda/figures/major_income_employment_hours_scatter_2019.png`
- `workbook/p2/p2_2/data/goms_subject_crawl/eda/figures/major_top3_industry_2019.png`
- `workbook/p2/p2_2/data/goms_subject_crawl/eda/figures/major_top3_job_2019.png`

## 해석 제한

인용 시 “한국고용정보원 GOMS 분석시스템의 가중 표본분석 결과”로 출처를 적고, 사이트 화면 자체가 공식 통계표 원자료는 아니라는 점을 함께 적는다. 동일 전공계열 값이 여러 대학에 반복 부여되므로 대학별 독립 설명변수처럼 p-value를 해석하면 안 된다.
