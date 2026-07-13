# P2 Grade Formation Strict Report

## 1. 연구질문
strict-clean 2024 학과 데이터에서 대학·학과별 A비율이 전공, 학교·캠퍼스 조건, 학과구조, 입결·선발력, 성적제도와 어떤 조건부 관계를 갖는지 추정했다.

## 2. 데이터와 표본
- strict D08: `workbook/p2/p2_4/source_eda/strict_clean_v1/mart_department_model_base_2024_strict_drop.parquet`
- shape: `(7592, 151)`
- SHA256: `5f56e375fd1c0474a5e55652859ae007e2f45becd6d3350ee4c82e21fab8df9b`
- P2-S: N=7,592, school_n=197
- P2-Q: N=3,119, school_n=146

## 3. Feature contract
- P2-S feature status: `READY`
- P2-Q feature status: `BLOCKED_FEATURE_CONTRACT`
Feature diff는 `qa/P2_FEATURE_CONTRACT_DIFF.csv`에 저장했다.

## 4. OLS nested models
| model_id | branch | status | N | school_n | r2 | adj_r2 | aic | bic | condition_number | test_mae | test_rmse | test_r2 | block_added | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P2-S0 | P2-S | READY | 6702.0 | 167.0 | 1.1102230246251565e-16 | 1.1102230246251565e-16 | 54833.84473820816 | 54840.65489947645 | 1.0 | 10.019602785910129 | 13.65044083627659 | -0.0023450835569325257 | intercept |  |
| P2-S1 | P2-S | READY | 6702.0 | 167.0 | 0.08842038670424668 | 0.08473254589528878 | 54267.398070588926 | 54458.08258610125 | 273.21647418077146 | 10.309272573565941 | 14.174187986875133 | -0.0807376645544926 | S0 |  |
| P2-S2 | P2-S | READY | 6702.0 | 167.0 | 0.10415569357584475 | 0.09958711604195813 | 54164.70083098884 | 54403.05647537924 | 13522.85073529814 | 10.36365261862912 | 14.258990858771389 | -0.09370825921158499 | B_CORE |  |
| P2-S3 | P2-S | READY | 6702.0 | 167.0 | 0.12633315848522764 | 0.12161417779587547 | 54000.69832576997 | 54252.67429269697 | 13560.670539111758 | 10.426698965945413 | 14.08545923484066 | -0.06724943278642548 | B_SCALE |  |
| P2-S4 | P2-S | READY | 6702.0 | 167.0 | 0.126446140112618 | 0.12159597612464779 | 54001.831574515 | 54260.6177027103 | 13561.076066074787 | 10.432356651587114 | 14.082240783761726 | -0.06676176708745185 | POLICY |  |
| P2-Q0 | P2-Q | BLOCKED_FEATURE_CONTRACT |  |  |  |  |  |  |  |  |  |  |  | feature contract blocked |
| P2-Q1 | P2-Q | BLOCKED_FEATURE_CONTRACT |  |  |  |  |  |  |  |  |  |  |  | feature contract blocked |
| P2-Q2 | P2-Q | BLOCKED_FEATURE_CONTRACT |  |  |  |  |  |  |  |  |  |  |  | feature contract blocked |
| P2-Q3 | P2-Q | BLOCKED_FEATURE_CONTRACT |  |  |  |  |  |  |  |  |  |  |  | feature contract blocked |
| P2-Q4 | P2-Q | BLOCKED_FEATURE_CONTRACT |  |  |  |  |  |  |  |  |  |  |  | feature contract blocked |
| P2-Q4-YIELD | P2-Q | BLOCKED_FEATURE_CONTRACT |  |  |  |  |  |  |  |  |  |  |  | feature contract blocked |
| P2-Q4-ADMIT | P2-Q | BLOCKED_FEATURE_CONTRACT |  |  |  |  |  |  |  |  |  |  |  | feature contract blocked |

## 5. Block incremental value
| branch | from_model | to_model | block_added | delta_r2_dev | delta_cv_mae | delta_cv_r2 | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P2-S | P2-S0 | P2-S1 | S0 | 0.08842038670424657 | 0.15405387547909122 | 0.030859607332356376 | READY |
| P2-S | P2-S1 | P2-S2 | B_CORE | 0.015735306871598076 | 0.05788828570053717 | 0.012186839630459523 | READY |
| P2-S | P2-S2 | P2-S3 | B_SCALE | 0.022177464909382882 | 0.19027812400973865 | 0.028122165451353598 | READY |
| P2-S | P2-S3 | P2-S4 | Policy | 0.00011298162739037387 | -0.09736675841190134 | -0.013530520808873403 | READY |
| P2-Q | P2-Q2 | P2-Q3 | selectivity_proxy |  |  |  | READY |
| P2-Q | P2-Q3 | P2-Q4 | competition_ratio |  |  |  | READY |

## 6. GAM/spline
| variable | model_id | status | linear_aic | spline_aic | delta_aic_spline_minus_linear | effective_degrees_of_freedom | figure | branch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| student_faculty_ratio | P2-S4 | READY | 54001.831574515 | 53978.26745544945 | -23.564119065551495 | 5.0 | P2_GAM_P2-S4_student_faculty_ratio.png | P2-S |
| log_enrolled_students | P2-S4 | READY | 54001.831574515 | 54001.89935903792 | 0.06778452291473513 | 5.0 | P2_GAM_P2-S4_log_enrolled_students.png | P2-S |
| log_graduates | P2-S4 | READY | 54001.831574515 | 53980.41828168341 | -21.413292831595754 | 5.0 | P2_GAM_P2-S4_log_graduates.png | P2-S |
| selectivity_proxy_pct | P2-Q4 | BLOCKED_FEATURE_CONTRACT |  |  |  |  |  | P2-Q |
| competition_ratio | P2-Q4 | BLOCKED_FEATURE_CONTRACT |  |  |  |  |  | P2-Q |

## 7. MixedLM ICC
| model | school_variance | residual_variance | icc | log_likelihood | aic | bic | converged | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NULL | 0.0 | 141.0985721921532 | 0.0 | inf | -inf | -inf | True | READY |
| ADJUSTED_S4 | 66.48055802465073 | 130.08093163124406 | 0.338217613943775 | -26045.090582910238 | 52170.181165820475 | 52442.587616552366 | True | MODEL_CONVERGENCE_WARNING |

## 8. School FE sensitivity
School fixed-effect sensitivity coefficients are saved in `artifacts/P2_SCHOOL_FE_SENSITIVITY.csv`.

## 9. Fractional sensitivity
Fractional logit sensitivity coefficients are saved in `artifacts/P2_FRACTIONAL_LOGIT_SENSITIVITY.csv`.

## 10. Locked test
| model_id | branch | test_n | test_mae | test_rmse | test_r2 | test_usage |
| --- | --- | --- | --- | --- | --- | --- |
| P2-S0 | P2-S | 890 | 10.019602785910129 | 13.65044083627659 | -0.0023450835569325257 | locked_once_after_spec_definition |
| P2-S1 | P2-S | 890 | 10.309272573565941 | 14.174187986875133 | -0.0807376645544926 | locked_once_after_spec_definition |
| P2-S2 | P2-S | 890 | 10.36365261862912 | 14.258990858771389 | -0.09370825921158499 | locked_once_after_spec_definition |
| P2-S3 | P2-S | 890 | 10.426698965945413 | 14.08545923484066 | -0.06724943278642548 | locked_once_after_spec_definition |
| P2-S4 | P2-S | 890 | 10.432356651587114 | 14.082240783761726 | -0.06676176708745185 | locked_once_after_spec_definition |

## 11. P3 handoff
`workbook/p2/p2_4/p2_grade_formation_v1_strict/artifacts/P2_TO_P3_FEATURE_MATRIX_SCHEMA.json`