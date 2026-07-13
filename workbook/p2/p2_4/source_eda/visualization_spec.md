# P2-G4 Source Visual EDA Specification

## Scope

- Target notebook: `workbook/p2/p2_4/p2_G4_VISUAL.ipynb`
- Source notebook: `workbook/p2/p2_4/p2_G4_source_parquet_csv_eda.ipynb`
- Dataset visual blocks: 96
- Default stack: `numpy`, `pandas`, `matplotlib`
- External downloads: none

## Visual Block Contract

### V00. 전체 소스 지도

- 시각화 목적: 전체 P4 후보 소스의 크기, 폭, dtype, 반복 컬럼 구조를 조망한다.
- 사용할 데이터: `source_eda/tables/source_dataset_inventory.csv`, `source_column_inventory.csv`, `source_column_reuse_summary.csv`
- 필요한 전처리: 원본 source EDA 산출 테이블을 그대로 읽는다.
- 코드 셀 설계: `plot_global_source_map()`
- 그래프 해석 포인트: 가장 큰 테이블, 가장 넓은 테이블, 반복 등장 컬럼, target-like 후보 컬럼을 분리해서 본다.
- 학생이 자주 하는 오해: 파일 크기와 모델 입력 적합성은 같은 개념이 아니다.
- 체크포인트 질문: 최종 분석 frame의 중심 테이블과 QA/registry 테이블을 구분할 수 있는가?

### V01. 후보 handoff 계약/레지스트리 지도

- 시각화 목적: P4 후보 handoff lock과 shared registry의 계약 역할을 확인한다.
- 사용할 데이터: `p4_handoff_candidate/P4_CANDIDATE_HANDOFF_LOCK.json`, `shared/*registry.csv`
- 필요한 전처리: registry CSV를 읽고 낮은 cardinality 컬럼을 카운트한다.
- 코드 셀 설계: `plot_registry_contract_summary()`
- 그래프 해석 포인트: `p4_use`, feature/target/sample 계열 컬럼의 분포와 registry 행 수를 본다.
- 학생이 자주 하는 오해: registry에 있는 모든 컬럼이 모델 feature는 아니다.
- 체크포인트 질문: active contract source와 feature-selection registry를 특정할 수 있는가?

### V02. 원본 노트북 셀 대응표

- 시각화 목적: 원본 96개 `eda_one(...)` 데이터셋 셀을 빠짐없이 시각화했는지 확인한다.
- 사용할 데이터: 원본 notebook JSON의 code cell AST.
- 필요한 전처리: `eda_one(path, source_kind)` 호출만 추출한다.
- 코드 셀 설계: `source_cell_map` 표와 source_kind bar chart.
- 그래프 해석 포인트: native CSV와 converted Parquet source의 비중을 본다.
- 학생이 자주 하는 오해: 전체 notebook cell 수와 EDA dataset 단위는 다르다.
- 체크포인트 질문: Dataset 001부터 Dataset 096까지 모두 대응되는가?

### V03. 데이터셋별 Visual EDA

- 시각화 목적: 각 파일의 dtype, 결측, 수치 분포, 범주/상태 쏠림을 한 화면에서 진단한다.
- 사용할 데이터: 원본 dataset call의 `path`와 `source_kind`.
- 필요한 전처리: full profile은 전체 행 기준, 그래프는 최대 50,000행 샘플 기준.
- 코드 셀 설계: `visual_eda_one(path, source_kind, dataset_no)`
- 그래프 해석 포인트: dtype mix, top missing columns, normalized numeric IQR/median, top categorical/status values.
- 학생이 자주 하는 오해: 단일 파일 분포가 깨끗해도 조인 후 duplicate key나 target leakage는 남을 수 있다.
- 체크포인트 질문: 이 파일이 모델 입력 후보인지, registry인지, QA 근거인지 구분할 수 있는가?
