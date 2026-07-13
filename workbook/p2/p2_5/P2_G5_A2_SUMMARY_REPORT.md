# P2-G5 A2 Strict Visual Summary

## Final judgement
| item | status | bucket | note |
| --- | --- | --- | --- |
| P2 strict D08 | READY | READY/OK | 5f56e375fd1c0474a5e55652859ae007e2f45becd6d3350ee4c82e21fab8df9b |
| P2-S OLS | READY | READY/OK | P2-S4 R2=0.126 |
| P2-Q OLS | BLOCKED_FEATURE_CONTRACT | BLOCKED | selectivity_proxy_pct not manual-approved as feature |
| P2 GAM | READY_WITH_WARNINGS | WARN/PENDING | S4 spline checks available for structure variables |
| P2 MixedLM | MODEL_CONVERGENCE_WARNING | WARN/PENDING | adjusted ICC=33.8% with warning |
| P5 strict RAW_A | READY | READY/OK | major7 heterogeneity artifacts connected |
| P5 residual | PENDING_UPSTREAM_RESIDUAL | WARN/PENDING | P3 residual pending |

## P2-S nested R2
| model_id | status | N | school_n | r2 | adj_r2 | test_mae | test_r2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P2-S0 | READY | 6702.0 | 167.0 | 1.1102230246251563e-16 | 1.1102230246251563e-16 | 10.019602785910129 | -0.0023450835569325 |
| P2-S1 | READY | 6702.0 | 167.0 | 0.0884203867042466 | 0.0847325458952887 | 10.30927257356594 | -0.0807376645544926 |
| P2-S2 | READY | 6702.0 | 167.0 | 0.1041556935758447 | 0.0995871160419581 | 10.36365261862912 | -0.0937082592115849 |
| P2-S3 | READY | 6702.0 | 167.0 | 0.1263331584852276 | 0.1216141777958754 | 10.426698965945413 | -0.0672494327864254 |
| P2-S4 | READY | 6702.0 | 167.0 | 0.126446140112618 | 0.1215959761246477 | 10.432356651587114 | -0.0667617670874518 |

## P2-S key coefficients
| label | coefficient | ci_low | ci_high | p_value | standardized_beta |
| --- | --- | --- | --- | --- | --- |
| 학점포기 제도 확인 | -0.5853193802147121 | -7.575386969614556 | 6.404748209185131 | 0.8696372393207334 | -0.0131472319250134 |
| 여학생 비중 | 0.0519531282343868 | -0.0022276010036086 | 0.1061338574723822 | 0.0601924204410782 | 0.0916125980287961 |
| 외국인 학생 비중 | 0.0028294947054429 | -0.0441819261518568 | 0.0498409155627426 | 0.9060952982022684 | 0.0023653110552936 |
| 중도탈락률 | 0.034752177932874 | -0.0257640643706212 | 0.0952684202363693 | 0.2603633157728394 | 0.0310267523830402 |
| 학생-교원비 | -0.0115901311749794 | -0.0337981818203449 | 0.0106179194703861 | 0.3063631211439731 | -0.0301624720101424 |
| 전임교원 비중 | -0.04879039381842 | -0.0728799958036126 | -0.0247007918332274 | 7.197670098057669e-05 | -0.0791170595545834 |
| 재학생 규모 log1p | -2.105105289373935 | -2.954066284741766 | -1.2561442940061045 | 1.1739964306785302e-06 | -0.1412558980716431 |
| 졸업생 규모 log1p | 1.634814611042362 | 1.2451440555374094 | 2.024485166547315 | 1.98828703465472e-16 | 0.1853898692401597 |

## P5 primary RAW_A AME
| major_group_7 | outcome | ame_pp_10pp | ci_low_pp_10pp | ci_high_pp_10pp |
| --- | --- | --- | --- | --- |
| ART | HEALTH_EMPLOYMENT | -0.42991134541361 | -1.4681595857461 | 0.73250050651784 |
| ART | GRAD_SCHOOL_PROGRESSION | 0.61742609083145 | 0.051497940665559995 | 1.6800437111055 |
| EDU | HEALTH_EMPLOYMENT | 1.56334932300441 | 0.025616321996390003 | 3.1025696339146402 |
| EDU | GRAD_SCHOOL_PROGRESSION | 0.5315531275911 | 0.16401970154029 | 1.2117358349005398 |
| ENG | HEALTH_EMPLOYMENT | 1.9293907647504702 | 0.82775062394367 | 2.87546222389914 |
| ENG | GRAD_SCHOOL_PROGRESSION | 4.5698291458772005 | 1.62284551217071 | 9.12135459790856 |
| HUM | HEALTH_EMPLOYMENT | 2.04564795931556 | 0.91402996860193 | 3.12120178022448 |
| HUM | GRAD_SCHOOL_PROGRESSION | 1.37323879019224 | 0.40904085648781 | 3.16457185901555 |
| MED | HEALTH_EMPLOYMENT | -0.56566468881035 | -3.1390369077737996 | 1.17552240774641 |
| MED | GRAD_SCHOOL_PROGRESSION | 0.38010818605338 | -0.05926394501188 | 7.30711929884181 |
| NAT | HEALTH_EMPLOYMENT | -0.47800716279940997 | -1.83576822877814 | 0.89526981441712 |
| NAT | GRAD_SCHOOL_PROGRESSION | 3.67302540297154 | 1.16894463053065 | 6.98756275232869 |
| SOC | HEALTH_EMPLOYMENT | 0.71444587295153 | -0.2409130184446 | 1.62080186209075 |
| SOC | GRAD_SCHOOL_PROGRESSION | 1.16902917730498 | 0.51742957375792 | 2.329864679287 |

## Figures
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

## Guardrails
- P2/P5 coefficients are conditional associations, not causal effects.
- P2-Q remains blocked under the current manual-approved feature contract.
- P5 context analysis is descriptive only with seven major groups.