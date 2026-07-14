# DATAMINING 브랜치: 크롤러 산출물 제출 패키지

이 브랜치는 SBS DSJA 5기 EDGE 프로젝트의 데이터마이닝/크롤링 산출물을 제출용으로 정리한 전용 브랜치다. 핵심 목적은 웹 재수집에 의존하지 않고, 이미 저장된 HTML 캐시와 원자료를 기준으로 입시 데이터와 GOMS 주제별 통계를 재현 가능하게 검증하는 것이다.

## 제출 파일

- 전체 제출 ZIP: `datamining_submission/package/P2_2_CRAWL_ADMISSION_GOMS_SUBMISSION_20260714.zip`
- ZIP 해시: `datamining_submission/package/P2_2_CRAWL_ADMISSION_GOMS_SUBMISSION_20260714.zip.sha256`
- 미리보기 폴더: `datamining_submission/preview/`

ZIP에는 전체 HTML 캐시, CSV/Parquet 원자료, 정규화 산출물, 실행 완료 노트북, 보고서, 재현 코드, 파일 해시 매니페스트가 들어 있다. GitHub에서 바로 확인할 수 있도록 실행 노트북과 보고서, 매니페스트, 재현 코드는 `preview` 폴더에도 별도로 배치했다.

## 데이터 범위

| 구분 | 포함 내용 | 수량 |
|---|---:|---:|
| ADIGA 핵심 입시 HTML 캐시 | 51개 대학 정시 입시결과 원문 HTML | 51개 |
| ADIGA 확장 입시 HTML 캐시 | 병합·확장 대상 대학 HTML | 163개 |
| GOMS 주제별 페이지 HTML | 고용·소득·근로시간 주제별 스냅샷 | 57개 |
| 실행 완료 노트북 | 캐시 기반 검증·정제·시각화 노트북 | 6개 |
| 제출 패키지 파일 | 정제 후 ZIP 내부 파일 | 579개 |

## 실행 검증 결과

`datamining_submission/preview/run_logs/notebook_execution_summary.csv` 기준으로 아래 노트북은 모두 새로 실행했고, 에러 출력 없이 통과했다.

| 순서 | 노트북 | 역할 | 상태 |
|---:|---|---|---|
| 1 | `01_crawl_eda.executed.ipynb` | ADIGA 크롤 원자료 EDA와 Gate 1/Gate 2 준비도 점검 | 통과 |
| 2 | `02_gate2_admission_rules.executed.ipynb` | 모집요강 반영규칙 후보 표·텍스트 추출 | 통과 |
| 3 | `03_gate2_final_rule_confirmation.executed.ipynb` | 대학별 최종 규칙 확인 요약 | 통과 |
| 4 | `04_h1_h2_measurement_validation.executed.ipynb` | H1/H2 측정 검증과 수동검토 경계 확인 | 통과 |
| 5 | `05_P2_G1_admission_visual_eda.executed.ipynb` | 최종 입시 프록시 시각화 EDA | 통과 |
| 6 | `06_P2_G1_kedi_goms_subject.executed.ipynb` | GOMS 주제별 원자료 정규화와 QA | 통과 |

## 폴더 구성

```text
datamining_submission/
├── package/
│   ├── P2_2_CRAWL_ADMISSION_GOMS_SUBMISSION_20260714.zip
│   └── P2_2_CRAWL_ADMISSION_GOMS_SUBMISSION_20260714.zip.sha256
└── preview/
    ├── notebooks_executed/
    ├── reports/
    ├── manifests/
    ├── run_logs/
    └── code_repro/
```

## 정제 기준

제출 ZIP과 미리보기 폴더에서는 아래 항목을 제외했다.

- 파이썬 바이트코드와 `__pycache__`
- 주피터 체크포인트 폴더
- 중간 백업 파일과 임시 파일
- 원본 작업트리의 unrelated 파일

반대로 재현에 필요한 캐시, 원자료, 정규화 결과, 실행 완료 노트북, 보고서, 재현 스크립트, 해시 매니페스트는 보존했다.

## 핵심 해석

이 브랜치의 크롤러 산출물은 최종 통계모형의 결론이 아니라, 모델링 이전의 데이터 수집·측정·검증 기반이다. ADIGA 입시결과는 대학별 산식과 공개 범위가 다르기 때문에 원자료 그대로 대학 간 동일 척도라고 가정하면 안 된다. 따라서 이 패키지는 다음 판단을 가능하게 한다.

- 어떤 대학과 모집단위가 실제 HTML 캐시로 확인되는지
- 어느 행이 header-only, 중복 후보, 비교가능성 경고를 갖는지
- 모집요강 규칙 추출이 어디까지 자동화되었고 어디서 검토가 필요한지
- GOMS 주제별 통계가 어떤 원자료와 정규화 산출물로 이어지는지

최종 연구 결론은 `FINAL` 브랜치에서 통합 노트북과 최종 포트폴리오 형태로 정리한다.
