# P2-G6_1 Visualization Specification

대상 노트북: `workbook/p2/P2_6/P2_G6_1.ipynb`

이 시각화 개발은 P3/P4 strict 산출물을 새로 학습하지 않는다. 목적은 P6 진입 전 모델 구조, 표본 구조, 결과 해석, 경고 문구를 학생과 후속 에이전트가 검증 가능한 형태로 읽게 만드는 것이다.

## 셀별 개발 방침

| 원 셀 | 기존 역할 | 추가 시각화/담론 | 모델 질문 |
|---:|---|---|---|
| 1 | 노트북 목적 선언 | 본 spec에서 P3/P4/P6 구조를 명시 | 이 노트북은 학습인가, strict 결과 읽기인가? |
| 2 | 환경/경로 함수 | V00 helper, `OUT_ROOT=P2_6` 경로 수정 | 그림과 산출물이 올바른 폴더로 저장되는가? |
| 3 | 산출물 존재 확인 | 기존 existence table 유지 | 필요한 P3/P4 strict 파일이 있는가? |
| 4 | 상태/hash lineage | V01 readiness matrix + hash chain | READY/WARNING/BLOCKED를 분리해서 읽는가? |
| 5 | P3 residual 성능 | V02 observed-vs-expected, residual histogram, fold stability | residual은 무엇을 남기는가? |
| 6 | P4 표본/진단 | V03 sample split + outcome availability | P4 비교가 같은 universe에서 이루어지는가? |
| 7 | P4 primary slope | V04 AME forest plot | grade signal이 outcome별로 얼마나 큰가? |
| 8 | 취업-진학 차이 D | V05 D bootstrap CI | 진학 slope가 취업 slope보다 큰가? |
| 9 | locked test | V06 metric improvement bars | test에서도 base보다 좋아졌는가? |
| 10 | RAW/residual 동등성 | V07 equivalence delta + scatter | residual을 독립 신호처럼 말해도 되는가? |
| 11 | P6 status | V08 decision dashboard | 무엇은 ready이고 무엇은 blocked인가? |
| 12 | 기존 AME summary | 기존 요약 그림 유지 | 핵심 AME 방향성 quick view |
| 13 | artifact 저장 | V09 visual manifest + reading guide | 후속 에이전트가 그림과 claim을 추적할 수 있는가? |
| 14 | 최종 상태 출력 | 기존 status print 유지 | run-all 후 사람이 확인할 final status는 무엇인가? |

## V00. 시각화 실행 헬퍼

- 시각화 목적: P3/P4 strict 결과를 다시 학습하지 않고, 모델 구조와 결과 해석을 읽는 그림만 저장한다.
- 사용할 데이터: 이후 셀에서 로드되는 P3/P4 CSV·parquet 산출물.
- 필요한 전처리: 공통 figure 저장 함수와 관찰/원인/제한/결론 템플릿.
- 코드 셀 설계: 모든 추가 그림은 `workbook/p2/P2_6/figures` 아래 저장하고 manifest에 누적한다.
- 그래프 해석 포인트: figure 자체보다 figure가 답하는 모델 질문을 우선한다.
- 학생이 자주 하는 오해: 새 그림이 새 모델 적합을 의미한다고 착각하는 것.
- 체크포인트 질문: 이 노트북은 모델을 다시 학습하는가, 아니면 strict 산출물을 읽는가?

## V01. Status / Lineage Map

- 시각화 목적: P3/P4 strict chain이 같은 입력 hash와 READY/WARNING/BLOCKED 상태를 공유하는지 확인한다.
- 사용할 데이터: `P3_P4_CONFIRMATORY_STATUS.json`, P3/P4 status JSON.
- 필요한 전처리: status 문자열을 ready score로 변환하고 hash를 짧은 anchor로 요약한다.
- 코드 셀 설계: readiness matrix와 lineage hash chain.
- 그래프 해석 포인트: P6는 READY지만 Q branch와 warning은 독립적으로 유지된다.
- 학생이 자주 하는 오해: hash가 같으면 통계 해석까지 자동으로 안전하다고 생각하는 것.
- 체크포인트 질문: `READY_WITH_WARNINGS`는 `READY`와 어떻게 다른가?

## V02. P3 Residual Model Diagnostic

- 시각화 목적: OOF residual이 무엇을 남기는지 observed/expected/residual/fold metric으로 분해한다.
- 사용할 데이터: `P3_STRUCTURE_GRADE_RESIDUAL_FULL.parquet`, `P3_OOF_PERFORMANCE.csv`, `P3_FULL_FOLD_METRICS.csv`.
- 필요한 전처리: residual parquet 샘플링, OOF/test R2 long-form 변환.
- 코드 셀 설계: observed-vs-expected scatter, residual histogram, OOF/test R2 bar, fold stability line.
- 그래프 해석 포인트: residual은 raw A와 강하게 상관된 구조 통제 후 잔여 grade signal이다.
- 학생이 자주 하는 오해: residual을 곧바로 인과적 shock 또는 독립 신호로 읽는 것.
- 체크포인트 질문: locked-test R2가 낮은데 residual을 어떻게 제한적으로 써야 하는가?

## V03. P4 Sample / Outcome Structure

- 시각화 목적: outcome model이 어떤 표본 분할과 결측 universe 위에서 비교되는지 확인한다.
- 사용할 데이터: `P4_SAMPLE_AUDIT.csv`, `P4_STRUCTURE_JOINT_FRAME.parquet`.
- 필요한 전처리: train/validation/test count와 outcome availability 집계.
- 코드 셀 설계: split stacked bar와 outcome/signal availability stacked bar.
- 그래프 해석 포인트: slope 비교는 표본 universe와 outcome coverage를 함께 읽어야 한다.
- 학생이 자주 하는 오해: 같은 학과 수로 모든 outcome이 동시에 추정됐다고 보는 것.
- 체크포인트 질문: 취업률과 진학률 비교에서 결측 구조는 어떤 제한을 주는가?

## V04. P4 AME Forest Plot

- 시각화 목적: RAW_A와 OOF residual의 outcome별 평균한계효과를 CI와 함께 비교한다.
- 사용할 데이터: `P4_COEFFICIENT_RESULTS.csv`, `P4_BOOTSTRAP_CI.csv`.
- 필요한 전처리: AME를 percentage point로 변환하고 bootstrap CI를 merge한다.
- 코드 셀 설계: outcome/signal별 horizontal forest plot.
- 그래프 해석 포인트: 대학원 진학률 slope가 취업률 slope보다 크고, RAW_A/OOF residual은 거의 겹친다.
- 학생이 자주 하는 오해: p-value만 보고 effect size와 외부예측 개선을 생략하는 것.
- 체크포인트 질문: 같은 AME라도 outcome baseline과 표본 차이에 따라 해석이 어떻게 달라지는가?

## V05. Employment vs Progression Difference D

- 시각화 목적: grade signal이 취업률보다 대학원 진학률에 더 크게 정렬되는지 직접 차이로 본다.
- 사용할 데이터: `P4_EMPLOYMENT_PROGRESSION_DIFFERENCE.csv`, `P4_BOOTSTRAP_CI.csv`.
- 필요한 전처리: D와 bootstrap CI를 percentage point 단위로 변환한다.
- 코드 셀 설계: signal별 D point + CI plot.
- 그래프 해석 포인트: D가 양수면 progression slope가 employment slope보다 크다.
- 학생이 자주 하는 오해: D를 두 독립 모형의 단순 눈대중 차이로 처리하는 것.
- 체크포인트 질문: D 결과가 P6의 결과론적 담론을 어떻게 바꾸는가?

## V06. Locked-Test Improvement

- 시각화 목적: signal 추가가 base 대비 test 성능을 실제로 개선했는지 metric별로 분리한다.
- 사용할 데이터: `P4_LOCKED_TEST_METRICS.csv`.
- 필요한 전처리: base metric - signal metric을 improvement로 계산한다.
- 코드 셀 설계: deviance, Brier, MAE improvement bar.
- 그래프 해석 포인트: slope 유의성과 locked-test 개선은 같은 질문이 아니다.
- 학생이 자주 하는 오해: coefficient가 유의하면 test metric도 반드시 좋아진다고 믿는 것.
- 체크포인트 질문: test 결과를 보고 사양을 다시 고르면 어떤 문제가 생기는가?

## V07. RAW_A / OOF Residual Equivalence Audit

- 시각화 목적: 현재 P4 선형 설계에서 RAW_A와 OOF residual이 거의 같은 추가정보 축인지 확인한다.
- 사용할 데이터: `P4_WITHIN_RAW_EQUIVALENCE_AUDIT.csv`, P3 residual parquet.
- 필요한 전처리: max delta log scale 변환과 raw/residual scatter 샘플링.
- 코드 셀 설계: metric delta bar와 raw A vs residual scatter.
- 그래프 해석 포인트: residual만의 별도 효과라고 과장하지 않는다.
- 학생이 자주 하는 오해: residual이라는 이름 때문에 raw A와 독립적인 신호라고 믿는 것.
- 체크포인트 질문: 같은 controls를 넣으면 왜 raw A와 residual이 같은 축을 공유하는가?

## V08. P6 Decision Dashboard

- 시각화 목적: P6로 넘길 준비 상태, 결과론적 claim, 유지할 경고를 한 장으로 고정한다.
- 사용할 데이터: P3/P4 summary objects와 `p6_status`.
- 필요한 전처리: question/finding/evidence/risk/next_action matrix 구성.
- 코드 셀 설계: decision matrix CSV 저장과 horizontal dashboard.
- 그래프 해석 포인트: READY와 BLOCKED가 같은 프로젝트 안에 공존할 수 있다.
- 학생이 자주 하는 오해: 전체 status 하나로 모든 branch가 승인됐다고 보는 것.
- 체크포인트 질문: P6가 열렸다는 말과 Q branch가 차단됐다는 말은 어떻게 동시에 참인가?

## V09. Visual Artifact Manifest / Reading Guide

- 시각화 목적: 추가된 그림과 해석 가이드를 후속 로컬 에이전트가 그대로 사용할 수 있게 고정한다.
- 사용할 데이터: `VISUAL_FIGURE_RECORDS`, decision matrix.
- 필요한 전처리: figure record를 표로 저장하고 모델 읽기 가이드를 markdown으로 작성한다.
- 코드 셀 설계: `P2_G6_1_VISUAL_ARTIFACTS.csv`, `P2_G6_1_VISUAL_MODEL_READING_GUIDE.md` 저장.
- 그래프 해석 포인트: 시각화는 최종 claim이 아니라 claim 안전장치다.
- 학생이 자주 하는 오해: 예쁜 그림이 많을수록 분석이 강해진다고 생각하는 것.
- 체크포인트 질문: 각 그림은 어떤 모델 질문에 답하는가?