# FINAL 브랜치: P2 데이터사이언스 최종 결론 포트폴리오

이 브랜치는 SBS DSJA 5기 EDGE 프로젝트의 최종 결론 제출본이다. 프로젝트의 핵심 질문은 “대학·학과별 A학점 비율 차이가 단순한 학점 관대성인지, 아니면 입학생 구성·전공구조·노동시장 맥락·진학성과와 연결되는 신호인지”를 검증하는 것이다.

## 최종 결론

분석 결과, A비율은 단일한 의미의 성적 인플레이션 지표로만 읽기 어렵다. 입시 선택성, 학교·학과 구조, 전공계열, 취업성과, 대학원 진학성과가 얽힌 조건부 신호로 다뤄야 한다. 다만 이 프로젝트의 결론은 개인 단위 GPA의 인과효과가 아니라, 대학-학과 단위 집단 자료에서 관찰된 조건부 연관성이다.

최종 제출 상태는 `PASS_WITH_WARNINGS`다. 이는 실패가 아니라, 해석 제한을 명시적으로 남긴 제출 가능 상태다. 핵심 경고는 다음 네 가지다.

- D08 분석 mart에는 직접 split 컬럼이 없어 `school_uid` 기준 외부 split merge로 검증했다.
- 일부 원자료 URL은 파일 직접 URL이 아니라 공식 포털 수준 URL이므로, 로컬 파일 해시와 포털 URL을 provenance anchor로 보존했다.
- P6 Q/selectivity branch는 launch-ready 결론으로 해석하지 않는다.
- registry와 D08 컬럼은 완전 대칭이 아니므로 누락/미등록 컬럼을 `qa/`에 남겼다.

## 최종 파일 위치

- 최종 제출 폴더: `final_portfolio/p2_integrated_engineering_final_submission_v1/`
- 최종 실행 노트북: `final_portfolio/p2_integrated_engineering_final_submission_v1/P2_FINAL_SUBMISSION.ipynb`
- 사용자가 최종 결론으로 지정한 cell-by-cell 노트북: `final_portfolio/p2_integrated_engineering_final_submission_v1/provenance/blueprints/P2_INTEGRATED_ENGINEERING_BLUEPRINT_CELL_BY_CELL.ipynb`
- 최종 보고서: `final_portfolio/p2_integrated_engineering_final_submission_v1/reports/FINAL_SUBMISSION_REPORT.md`
- 패키지 파일 manifest: `final_portfolio/p2_integrated_engineering_final_submission_v1/FINAL_SUBMISSION_PACKAGE_MANIFEST.csv`
- 검증 요약: `final_portfolio/FINAL_VALIDATION_SUMMARY.md`

## 최종 검증 숫자

| 항목 | 값 |
|---|---:|
| 활성 분석 mart 행 수 | 10,242 |
| 활성 분석 mart 컬럼 수 | 151 |
| 원자료 파일 수 | 30 |
| 파생 데이터 파일 수 | 136 |
| provenance 파일 수 | 11 |
| 최종 manifest 검증 행 수 | 207 |
| manifest 해시 불일치 | 0 |
| 최종 실행 노트북 코드 셀 | 15 |
| 최종 실행 노트북 실행 셀 | 15 |
| 최종 실행 노트북 에러 출력 | 0 |
| cell-by-cell 결론 노트북 코드 셀 | 16 |
| cell-by-cell 결론 노트북 실행 셀 | 16 |
| cell-by-cell 결론 노트북 에러 출력 | 0 |

## 포트폴리오 읽는 순서

1. `README.md`: 프로젝트 최종 결론과 해석 제한
2. `final_portfolio/FINAL_VALIDATION_SUMMARY.md`: 제출 무결성 점검 요약
3. `final_portfolio/p2_integrated_engineering_final_submission_v1/provenance/blueprints/P2_INTEGRATED_ENGINEERING_BLUEPRINT_CELL_BY_CELL.ipynb`: 최종 결론 설계 흐름
4. `final_portfolio/p2_integrated_engineering_final_submission_v1/P2_FINAL_SUBMISSION.ipynb`: 최종 제출 패키지 실행 검증
5. `final_portfolio/p2_integrated_engineering_final_submission_v1/reports/FINAL_SUBMISSION_REPORT.md`: Gate별 PASS/WARN 근거
6. `final_portfolio/p2_integrated_engineering_final_submission_v1/qa/`: 원자료·파생자료·분석 mart·sample split·target coverage 점검표

## 최종 해석 원칙

- A비율 계수와 AME는 조건부 연관성으로 해석한다.
- 개인 단위 성적이나 학생 성과를 직접 예측하는 모델로 해석하지 않는다.
- 경고로 남긴 Q/selectivity branch는 최종 결론의 핵심 근거로 사용하지 않는다.
- 최종 주장은 `P2_FINAL_SUBMISSION.ipynb`, `FINAL_SUBMISSION_REPORT.md`, `qa/final_status_matrix.csv`가 동시에 지지하는 범위 안에서만 사용한다.

## 브랜치 관계

- `DATAMINING`: ADIGA/GOMS 크롤러와 캐시 기반 데이터마이닝 제출 패키지
- `FINAL`: 통합 엔지니어링 최종 결론 포트폴리오
- `main`: 전체 프로젝트의 최종 한글 랜딩 README
