# P2-G6_1 Visual Model Reading Guide

## 목적

이 가이드는 P2-G6_1 노트북에 추가한 시각화가 어떤 모델 질문을 답하는지 고정한다.
노트북은 P3/P4를 다시 적합하지 않고, strict-clean 산출물을 읽어 P6 진입 전 판단을 구조화한다.

## 핵심 결론

1. P3 residual handoff는 준비됐지만, locked-test R2가 낮으므로 residual을 강한 예측모형의 순수 잔차처럼 해석하지 않는다.
2. P4에서 grade signal은 건강보험 취업률보다 대학원 진학률과 더 크게 정렬된다.
3. RAW_A와 OOF residual은 현재 P4 선형 설계에서 거의 같은 added-information 축을 제공한다.
4. P2-Q/P3-Q branch는 feature contract 승인 전까지 confirmatory chain에 넣지 않는다.

## 그림 목록

```csv
block_id,figure_path,question,data_used
V01_STATUS_LINEAGE,workbook/p2/P2_6/figures/P2_G6_1_V01_STATUS_LINEAGE.png,P3/P4 strict 상태와 hash가 같은 실행 사슬을 가리키는가?,"P3_P4_CONFIRMATORY_STATUS.json, P3/P4 status json"
V02_P3_RESIDUAL_DIAGNOSTIC,workbook/p2/P2_6/figures/P2_G6_1_V02_P3_RESIDUAL_DIAGNOSTIC.png,"P3 residual은 강한 예측모형의 잔차인가, 구조 통제 후 남은 grade signal인가?","P3_STRUCTURE_GRADE_RESIDUAL_FULL.parquet, P3_OOF_PERFORMANCE.csv, P3_FULL_FOLD_METRICS.csv"
V03_P4_SAMPLE_STRUCTURE,workbook/p2/P2_6/figures/P2_G6_1_V03_P4_SAMPLE_STRUCTURE.png,P4 모형의 비교가 같은 표본 구조와 outcome availability 위에서 이루어졌는가?,"P4_SAMPLE_AUDIT.csv, P4_STRUCTURE_JOINT_FRAME.parquet"
V04_P4_AME_FOREST,workbook/p2/P2_6/figures/P2_G6_1_V04_P4_AME_FOREST.png,RAW_A와 OOF residual은 취업률/대학원 진학률에 어느 정도의 추가 신호를 주는가?,"P4_COEFFICIENT_RESULTS.csv, P4_BOOTSTRAP_CI.csv"
V05_D_BOOTSTRAP,workbook/p2/P2_6/figures/P2_G6_1_V05_D_BOOTSTRAP.png,grade signal의 추가 효과가 취업률보다 대학원 진학률에서 더 큰가?,"P4_EMPLOYMENT_PROGRESSION_DIFFERENCE.csv, P4_BOOTSTRAP_CI.csv"
V06_LOCKED_TEST_IMPROVEMENT,workbook/p2/P2_6/figures/P2_G6_1_V06_LOCKED_TEST_IMPROVEMENT.png,P4 signal 추가가 locked test에서 base 대비 외부 예측을 개선했는가?,P4_LOCKED_TEST_METRICS.csv
V07_RAW_RESID_EQUIVALENCE,workbook/p2/P2_6/figures/P2_G6_1_V07_RAW_RESID_EQUIVALENCE.png,현재 P4 설계에서 RAW_A와 OOF residual을 독립적인 두 신호처럼 해석해도 되는가?,"P4_WITHIN_RAW_EQUIVALENCE_AUDIT.csv, P3_STRUCTURE_GRADE_RESIDUAL_FULL.parquet"
V08_P6_DECISION_DASHBOARD,workbook/p2/P2_6/figures/P2_G6_1_V08_P6_DECISION_DASHBOARD.png,P6로 넘길 결과론적 판단과 경고를 한 장으로 고정할 수 있는가?,"P3/P4 summary objects, P6 status dictionary"
```

## 구조화 담론

| 항목 | 관찰 | 원인 | 제한 | 결론 |
|---|---|---|---|---|
| P3 residual | coverage는 충분하지만 raw A와 residual 상관이 높다 | residual이 raw A에서 구조 기대값을 뺀 값이기 때문 | causal shock 아님 | topology signal로만 사용 |
| P4 employment | locked-test gain이 약하다 | 취업 outcome은 구조 통제 후 grade signal 추가정보가 제한적 | slope와 예측개선이 다름 | 강한 취업성과 claim 금지 |
| P4 progression | D가 양수 방향이다 | grade signal이 대학원 진학과 더 정렬 | selection/aspiration 혼재 | progression alignment로 표현 |
| RAW_A/residual | end-to-end delta가 극소다 | 같은 controls 안에서 같은 1차원 정보를 span | 현재 P4 선형 설계 한정 | residual 고유효과 과장 금지 |
