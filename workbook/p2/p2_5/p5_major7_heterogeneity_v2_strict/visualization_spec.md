# P5 v2 Strict Modeling Visualization Spec

## V00. Strict Input / Sample Contract

- 시각화 목적: strict-clean/manual-approved 입력이 실제 모델 표본을 어떻게 제한했는지 보여준다.
- 사용할 데이터: `qa/P5_STRICT_INPUT_CONTRACT.csv`, `qa/P5_STRICT_SAMPLE_AUDIT.csv`
- 필요한 전처리: sample_id를 짧은 라벨로 바꾸고 row_n과 school_n을 같은 패널에 표시한다.
- 코드 셀 설계: strict diagnostic dashboard의 sample audit 패널.
- 그래프 해석 포인트: structure와 selectivity 표본 크기 차이가 이후 slope 안정성 차이를 설명하는지 본다.
- 학생이 자주 하는 오해: 표본이 작아졌다고 결과가 틀렸다는 뜻은 아니다. strict 계약에 맞춘 재현 가능한 분석 단위다.
- 체크포인트 질문: 어떤 입력 계약과 sample gate가 현재 모델 결과의 모집단을 정의하는가?

## V01. RAW_A / Outcome AME Heatmap

- 시각화 목적: RAW_A +10%p에 대한 취업률과 대학원 진학률 AME를 전공계열별로 비교한다.
- 사용할 데이터: `artifacts/P5_MAJOR7_SLOPE_ESTIMATES.csv`
- 필요한 전처리: STRUCTURE/B_CORE/fractional_logit/primary_model/RAW_A만 필터링하고 AME를 percentage point로 변환한다.
- 코드 셀 설계: `P5_STRICT_INSIGHT_AME_HEATMAP_RAW_A.png`
- 그래프 해석 포인트: 같은 계열에서 취업과 진학 방향이 같은지, 어느 outcome 쪽 AME가 큰지 본다.
- 학생이 자주 하는 오해: heatmap 색이 진하다고 인과효과가 크다는 뜻은 아니다. 조건부 기울기 크기다.
- 체크포인트 질문: RAW_A 신호가 진학과 취업에 같은 방향으로 연결되는 계열은 어디인가?

## V02. Progression Minus Employment Contrast

- 시각화 목적: 계열별로 grade signal이 취업보다 진학에 더 연결되는지 확인한다.
- 사용할 데이터: `artifacts/P5_EMPLOYMENT_PROGRESSION_AME_DIFFERENCE.csv`
- 필요한 전처리: `(progression_ame - employment_ame) * 100`으로 변환한다.
- 코드 셀 설계: `P5_STRICT_INSIGHT_PROGRESSION_MINUS_EMPLOYMENT_RAW_A.png`
- 그래프 해석 포인트: 양수는 진학 쪽 연결이 더 큼, 음수는 취업 쪽 연결이 더 큼.
- 학생이 자주 하는 오해: 두 outcome의 차이가 통계적으로 확정됐다는 뜻은 아니다. 탐색적 contrast다.
- 체크포인트 질문: NAT, ENG, EDU의 contrast 방향은 어떻게 다른가?

## V03. Strict vs v1 Sensitivity

- 시각화 목적: strict-clean 재실행 후 v1 결론이 바뀌었는지 확인한다.
- 사용할 데이터: `artifacts/P5_V1_VS_STRICT_SENSITIVITY.csv`
- 필요한 전처리: primary STRUCTURE/B_CORE/fractional_logit만 필터링하고 strict-v1 AME 차이를 pp 단위로 계산한다.
- 코드 셀 설계: `P5_STRICT_INSIGHT_V1_SENSITIVITY_RAW_A.png`
- 그래프 해석 포인트: 부호 변화, CI overlap, 최대 변화량을 본다.
- 학생이 자주 하는 오해: strict와 v1 수치가 같다고 strict 검증이 불필요했다는 뜻은 아니다. strict는 입력 계약을 재확인한 것이다.
- 체크포인트 질문: strict-clean 이후 부호가 바뀐 모델 cell이 있는가?

## V04. Structure vs Selectivity Stability

- 시각화 목적: selectivity control이 들어간 표본에서도 구조분기 slope 방향이 유지되는지 확인한다.
- 사용할 데이터: `qa/P5_STRUCTURE_SELECTIVITY_STABILITY.csv`
- 필요한 전처리: AME를 pp 단위로 변환하고 y=x 기준선과 함께 산점도로 표시한다.
- 코드 셀 설계: `P5_STRICT_INSIGHT_STRUCTURE_SELECTIVITY_STABILITY_RAW_A.png`
- 그래프 해석 포인트: 기준선 근처는 안정적, 사분면이 바뀌면 부호 안정성이 약하다.
- 학생이 자주 하는 오해: selectivity branch는 더 좋은 모델이 아니라 다른 조건을 둔 민감도 분석이다.
- 체크포인트 질문: structure와 selectivity에서 부호가 다른 계열/outcome은 어디인가?

## V05. Context Rho / Diagnostic Board

- 시각화 목적: context와 slope 관계, 모델 상태, sample 규모를 함께 확인한다.
- 사용할 데이터: `artifacts/P5_SLOPE_CONTEXT_DESCRIPTIVE.csv`, `qa/P5_MODEL_DIAGNOSTICS.csv`, `qa/P5_STRICT_SAMPLE_AUDIT.csv`
- 필요한 전처리: context rho는 N=7 major-level 기술값으로만 표시한다.
- 코드 셀 설계: `P5_STRICT_INSIGHT_CONTEXT_RHO_HEATMAP_RAW_A.png`, `P5_STRICT_INSIGHT_MODEL_DIAGNOSTIC_DASHBOARD.png`
- 그래프 해석 포인트: context rho는 가설 생성용이며, diagnostic board는 결과 신뢰 범위를 정한다.
- 학생이 자주 하는 오해: N=7 rho를 context 효과 검정처럼 읽으면 안 된다.
- 체크포인트 질문: 어떤 결론은 모델 결과이고, 어떤 결론은 기술 통계인가?
