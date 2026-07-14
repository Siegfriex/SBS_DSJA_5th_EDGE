# SBS DSJA 5기 EDGE 데이터사이언스 최종 포트폴리오

## 프로젝트 결론

이 프로젝트는 “같은 A학점은 정말 같은 의미인가?”라는 질문에서 출발했다. 2024년 대학-학과 단위 성적분포를 입시 선택성, 학교·학과 구조, 전공계열, 노동시장 맥락, 취업성과, 대학원 진학성과와 연결해 검증했다.

최종 결론은 다음과 같다.

> 대학·학과별 A비율은 단순한 학점 관대성 지표 하나로 해석하기 어렵다. 입학생 구성, 전공구조, 학교 맥락, 취업·진학 성과와 함께 읽어야 하는 조건부 신호다. 다만 이 분석은 개인 단위 인과효과가 아니라 대학-학과 단위 집단 자료에서 관찰된 조건부 연관성이다.

최종 제출 상태는 `PASS_WITH_WARNINGS`다. 이는 실패가 아니라, 데이터와 해석의 경계를 명시한 상태다. Q/selectivity branch는 launch-ready 결론으로 쓰지 않았고, registry coverage와 split merge 제한은 QA 파일과 최종 보고서에 남겼다.

## 최종 브랜치

| 브랜치 | 역할 | 핵심 위치 |
|---|---|---|
| [`DATAMINING`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/DATAMINING) | ADIGA/GOMS 크롤러와 캐시 기반 데이터마이닝 제출 패키지 | `datamining_submission/` |
| [`FINAL`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/FINAL) | 통합 엔지니어링 최종 결론 포트폴리오 | `final_portfolio/` |
| [`P2_2`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_2) | 입시 데이터 이해, H1-H7 EDA, 검증 노트북 | `workbook/p2/p2_2/` |
| [`P2_3`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_3) | GOMS bridge, 독립 감사, P4 handoff 후보 | `workbook/p2/p2_3/` |
| [`P2_4`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_4) | 엄격한 학점 형성 모델링과 residual/outcome chain | `workbook/p2/p2_4/` |
| [`P2_5`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_5) | 전공 7계열 이질성 모델링과 A2 시각화 | `workbook/p2/p2_5/` |
| [`P2_6`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_6) | 최종 strict-chain run-up과 confirmatory closure | `workbook/p2/P2_6/` |

`main` 브랜치는 전체 프로젝트를 안내하는 랜딩 README만 유지한다. 실제 산출물은 목적별 브랜치에 분리했다.

## 최종 검증 요약

| 항목 | 값 |
|---|---:|
| 최종 분석 mart 행 수 | 10,242 |
| 최종 분석 mart 컬럼 수 | 151 |
| 최종 원자료 파일 수 | 30 |
| 최종 파생 데이터 파일 수 | 136 |
| 최종 provenance 파일 수 | 11 |
| 최종 manifest 검증 행 수 | 207 |
| 최종 manifest 해시 불일치 | 0 |
| 최종 실행 노트북 에러 출력 | 0 |
| cell-by-cell 결론 노트북 에러 출력 | 0 |
| DATAMINING 실행 노트북 | 6개 모두 통과 |
| DATAMINING 제출 ZIP 해시 | 일치 |

## 데이터마이닝 산출물

`DATAMINING` 브랜치에는 제출용 크롤러 패키지를 정리했다.

- ADIGA 핵심 입시 HTML 캐시: 51개
- ADIGA 확장 입시 HTML 캐시: 163개
- GOMS 주제별 페이지 HTML 스냅샷: 57개
- 실행 완료 노트북: 6개
- 제출 ZIP: `datamining_submission/package/P2_2_CRAWL_ADMISSION_GOMS_SUBMISSION_20260714.zip`
- 실행 요약: `datamining_submission/preview/run_logs/notebook_execution_summary.csv`

이 브랜치는 최종 모델링 결론이 아니라, 모델링 이전의 수집·측정·검증 기반이다. ADIGA 입시결과는 대학별 산식과 공개 범위가 다르기 때문에, 원자료를 그대로 대학 간 동일 척도로 가정하지 않는다.

## 최종 포트폴리오 산출물

`FINAL` 브랜치에는 최종 결론과 제출 패키지를 정리했다.

- 최종 실행 노트북: `final_portfolio/p2_integrated_engineering_final_submission_v1/P2_FINAL_SUBMISSION.ipynb`
- 최종 결론 설계 노트북: `final_portfolio/p2_integrated_engineering_final_submission_v1/provenance/blueprints/P2_INTEGRATED_ENGINEERING_BLUEPRINT_CELL_BY_CELL.ipynb`
- 최종 보고서: `final_portfolio/p2_integrated_engineering_final_submission_v1/reports/FINAL_SUBMISSION_REPORT.md`
- 최종 검증 요약: `final_portfolio/FINAL_VALIDATION_SUMMARY.md`
- 최종 manifest: `final_portfolio/p2_integrated_engineering_final_submission_v1/FINAL_SUBMISSION_PACKAGE_MANIFEST.csv`

## 연구 흐름

1. 입시·성적분포·학교 구조 데이터의 측정 가능성을 검증했다.
2. ADIGA와 GOMS 크롤링/캐시를 정리해 재현 가능한 데이터마이닝 기반을 만들었다.
3. 학교-학과 단위 분석 mart를 구성하고 handoff manifest와 해시를 고정했다.
4. A비율, 입시 선택성, 전공계열, 취업·진학 결과를 strict-chain으로 연결했다.
5. 최종 결론에서는 통과한 근거만 사용하고, 경고가 남은 branch는 해석 범위에서 제한했다.

## 해석 원칙

- A비율 계수와 AME는 조건부 연관성이다.
- 개인 단위 GPA나 개인 취업성과에 대한 인과효과로 해석하지 않는다.
- Q/selectivity branch는 최종 근거로 확정하지 않는다.
- 최종 결론은 `FINAL` 브랜치의 실행 노트북, 최종 보고서, QA 파일이 동시에 지지하는 범위 안에서만 사용한다.
