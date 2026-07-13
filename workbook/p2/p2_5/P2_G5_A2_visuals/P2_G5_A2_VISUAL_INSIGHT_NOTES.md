# P2-G5 A2 Visual Insight Notes

## 핵심 인사이트
- P2-S4 개발 R2는 12.6%이지만 locked-test MAE와 test R2를 별도로 확인해야 한다.
- P2-Q는 `BLOCKED_FEATURE_CONTRACT` 상태라 현재 결론에서 제외한다.
- 입결 관측 표본 평균 A비율과 미관측 표본 차이는 -1.53%p다.
- 조정 MixedLM ICC는 33.8%로 학교 단위 분산이 남지만 warning을 동반한다.
- P5 residual branch는 `PENDING_UPSTREAM_RESIDUAL`라 RAW_A strict heterogeneity와 분리한다.

## 생성된 그림
| figure | size_kb |
| --- | --- |
| workbook/p2/p2_5/P2_G5_A2_visuals/figures/A2_00_environment_flow.png | 45.3 |
| workbook/p2/p2_5/P2_G5_A2_visuals/figures/A2_01_status_board.png | 161.0 |
| workbook/p2/p2_5/P2_G5_A2_visuals/figures/A2_02_lineage_artifact_sizes.png | 57.2 |
| workbook/p2/p2_5/P2_G5_A2_visuals/figures/A2_03_sample_feature_contract.png | 96.5 |
| workbook/p2/p2_5/P2_G5_A2_visuals/figures/A2_04_p2_nested_ols_performance.png | 143.6 |
| workbook/p2/p2_5/P2_G5_A2_visuals/figures/A2_05_p2_coefficients_forest.png | 125.1 |
| workbook/p2/p2_5/P2_G5_A2_visuals/figures/A2_06_p2_nonlinearity_variance_tests.png | 104.0 |
| workbook/p2/p2_5/P2_G5_A2_visuals/figures/A2_07_selectivity_bias_audit.png | 86.4 |
| workbook/p2/p2_5/P2_G5_A2_visuals/figures/A2_08_p5_strict_heterogeneity.png | 122.6 |
| workbook/p2/p2_5/P2_G5_A2_visuals/figures/A2_09_p5_context_profile.png | 96.7 |
| workbook/p2/p2_5/P2_G5_A2_visuals/figures/A2_10_final_judgement_board.png | 96.8 |

## 최종 판정
| item | status | bucket | note |
| --- | --- | --- | --- |
| P2 strict D08 | READY | READY/OK | 5f56e375fd1c0474a5e55652859ae007e2f45becd6d3350ee4c82e21fab8df9b |
| P2-S OLS | READY | READY/OK | P2-S4 R2=0.126 |
| P2-Q OLS | BLOCKED_FEATURE_CONTRACT | BLOCKED | selectivity_proxy_pct not manual-approved as feature |
| P2 GAM | READY_WITH_WARNINGS | WARN/PENDING | S4 spline checks available for structure variables |
| P2 MixedLM | MODEL_CONVERGENCE_WARNING | WARN/PENDING | adjusted ICC=33.8% with warning |
| P5 strict RAW_A | READY | READY/OK | major7 heterogeneity artifacts connected |
| P5 residual | PENDING_UPSTREAM_RESIDUAL | WARN/PENDING | P3 residual pending |

## 해석 가드레일
- P2/P5 계수와 AME는 조건부 association이며 인과효과가 아니다.
- P2-S와 P2-Q는 표본 관측 메커니즘이 다르므로 결론을 합치지 않는다.
- P5 context는 major7의 기술통계 보조판이며 confirmatory meta-regression이 아니다.