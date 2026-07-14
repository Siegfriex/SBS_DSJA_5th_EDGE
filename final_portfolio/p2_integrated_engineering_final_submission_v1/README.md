# P2 통합 엔지니어링 최종 제출 패키지

이 폴더는 SBS DSJA 5기 EDGE 프로젝트의 최종 제출용 패키지다. 최종 노트북은 이 폴더 안의 파일만 읽도록 구성되어 있으며, 원자료 복제본, 파생 데이터, provenance, QA 결과, 최종 보고서를 한 번에 검증한다.

## 핵심 파일

- `P2_FINAL_SUBMISSION.ipynb`: 최종 실행 노트북
- `provenance/blueprints/P2_INTEGRATED_ENGINEERING_BLUEPRINT_CELL_BY_CELL.ipynb`: 사용자가 최종 결론으로 지정한 cell-by-cell 통합 설계 노트북
- `data/raw/`: 원자료 복제본과 원자료 manifest
- `data/derived/`: D01-D08 handoff, integrity 산출물, 단계별 결과 readout
- `provenance/`: 데이터 출처 카탈로그, handoff lock, blueprint 노트북
- `qa/`: 최종 노트북 실행으로 생성된 무결성 점검표
- `figures/`: 최종 점검용 lineage·분포 시각화
- `reports/FINAL_SUBMISSION_REPORT.md`: 최종 실행 보고서
- `FINAL_SUBMISSION_PACKAGE_MANIFEST.csv`: 제출 폴더 전체 파일 manifest와 SHA-256 해시

## 최종 실행 상태

최종 노트북은 새로 실행했으며, 실행 결과는 다음과 같다.

- 최종 상태: `PASS_WITH_WARNINGS`
- 실행 ID: `20260714T062125Z`
- 활성 분석 mart: `data/derived/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet`
- 활성 분석 mart shape: `10242 x 151`
- 활성 분석 mart SHA-256: `598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962`
- 원자료 파일 수: `30`
- 파생/provenance 파일 수: `136 / 11`

`PASS_WITH_WARNINGS`는 제출 차단 실패가 아니라, 아래 해석 제한을 명시적으로 남긴 상태다.

- D08에는 직접 split 컬럼이 없어 `school_uid` 기준 외부 split merge를 사용한다.
- 일부 원자료 URL은 파일 직접 URL이 아니라 포털 수준 URL이다. 대신 로컬 파일 해시와 공식 포털 URL을 provenance anchor로 보존한다.
- P6 Q/selectivity branch는 launch-ready 결론으로 해석하지 않는다.
- registry와 D08 컬럼이 완전 대칭은 아니므로 누락/미등록 컬럼을 `qa/`에 기록한다.

## 최종 결론의 위치

이 패키지에서 최종 결론은 다음 순서로 읽으면 된다.

1. `provenance/blueprints/P2_INTEGRATED_ENGINEERING_BLUEPRINT_CELL_BY_CELL.ipynb`
2. `P2_FINAL_SUBMISSION.ipynb`
3. `reports/FINAL_SUBMISSION_REPORT.md`
4. `qa/final_status_matrix.csv`
5. `FINAL_SUBMISSION_PACKAGE_MANIFEST.csv`

## 재실행 방법

프로젝트 루트에서 아래 명령을 실행하면 최종 노트북을 다시 검증할 수 있다.

```bash
MPLCONFIGDIR=/tmp/mplconfig .venv/bin/jupyter nbconvert --to notebook --execute workbook/p2/p2_integrated_engineering_final_submission_v1/P2_FINAL_SUBMISSION.ipynb --inplace --ExecutePreprocessor.timeout=900
```

## 해석 원칙

이 프로젝트의 결론은 개인 단위 GPA 예측이 아니라, 대학-학과 단위 A비율 신호가 입학생 구성, 전공구조, 노동시장 맥락, 취업성과, 대학원 진학성과와 어떻게 연결되는지 검증한 집단 수준 분석이다. 계수와 AME는 조건부 연관성으로 읽어야 하며, 인과효과로 단정하지 않는다.
