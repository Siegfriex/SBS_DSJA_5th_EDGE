# P4 Confirmatory Closure Report

## 한 줄 판정
P4 closure는 RAW_A primary와 OOF residual sensitivity를 분리해 재검산했으며, P5 residual refresh까지 생성했다. P2-Q/P3-Q 차단과 RAW_A-residual 등가성 경고는 유지한다.

## Input hashes
- strict D08: `5f56e375fd1c0474a5e55652859ae007e2f45becd6d3350ee4c82e21fab8df9b`
- P2→P3 handoff: `2bbc7d64784b7b530d57bb6a2096d14cb11c5879f41a5208f9ff3b02f4bdddcb`
- P3 FULL residual: `d8decd39dca42ccd0dc194fa3813ba0036541098eea08ddfb64627f6fc6cb8cc`

## Bootstrap CI
                          signal        estimand   median     mean      std    ci_2_5  ci_97_5  successful_n  attempted_n  positive_probability
               OOF_RESIDUAL_FULL  AME employment 0.005640 0.005549 0.002687  0.000024 0.010903           500          500                 0.974
               OOF_RESIDUAL_FULL AME progression 0.016340 0.016206 0.003308  0.009166 0.022448           500          500                 1.000
               OOF_RESIDUAL_FULL           D AME 0.010578 0.010657 0.003875  0.003430 0.018486           500          500                 0.996
               OOF_RESIDUAL_FULL   IV employment 0.000222 0.000275 0.000232  0.000003 0.000853           500          500                 1.000
               OOF_RESIDUAL_FULL  IV progression 0.005975 0.005996 0.002343  0.001758 0.010974           500          500                 1.000
               OOF_RESIDUAL_FULL            D IV 0.005709 0.005721 0.002299  0.001581 0.010609           500          500                 1.000
OOF_RESIDUAL_FULL_ALPHA_RESELECT  AME employment 0.005717 0.005564 0.003021 -0.001074 0.011889           100          100                 0.960
OOF_RESIDUAL_FULL_ALPHA_RESELECT AME progression 0.015904 0.015722 0.003329  0.009435 0.021757           100          100                 1.000
OOF_RESIDUAL_FULL_ALPHA_RESELECT           D AME 0.009954 0.010157 0.003487  0.003099 0.016565           100          100                 1.000
OOF_RESIDUAL_FULL_ALPHA_RESELECT   IV employment 0.000242 0.000292 0.000260  0.000001 0.000990           100          100                 1.000
OOF_RESIDUAL_FULL_ALPHA_RESELECT  IV progression 0.005764 0.005652 0.002321  0.001758 0.010246           100          100                 1.000
OOF_RESIDUAL_FULL_ALPHA_RESELECT            D IV 0.005365 0.005361 0.002236  0.001587 0.009979           100          100                 1.000
                           RAW_A  AME employment 0.005841 0.005900 0.003010  0.000518 0.011589           500          500                 0.988
                           RAW_A AME progression 0.017510 0.017397 0.003683  0.010217 0.024669           500          500                 1.000
                           RAW_A           D AME 0.011794 0.011497 0.004237  0.003216 0.019641           500          500                 0.994
                           RAW_A   IV employment 0.000190 0.000250 0.000219  0.000003 0.000773           500          500                 1.000
                           RAW_A  IV progression 0.005329 0.005433 0.002178  0.001789 0.010186           500          500                 1.000
                           RAW_A            D IV 0.005084 0.005183 0.002132  0.001638 0.009981           500          500                 0.998

## Two-part combined AME
     grade_signal                          signal_column  combined_AME    N  school_n
            RAW_A                            a_rate_10pp      0.015659 5013       165
OOF_RESIDUAL_FULL grade_residual_structure_full_oof_10pp      0.015052 5013       165

## Hypothesis decisions
  hypothesis primary_signal                           estimand   effect               95% CI       Holm p    CV IV   test IV         bootstrap CI            decision                                                                     limitation
         H_E          RAW_A                           AME 10pp 0.006163 [0.000518, 0.011589] 3.331334e-02 0.000225 -0.001818 [0.000518, 0.011589] PARTIALLY_SUPPORTED                        RAW_A provides added information for health employment.
         H_P          RAW_A                           AME 10pp 0.017260 [0.010217, 0.024669] 1.216459e-11 0.005394  0.004102 [0.010217, 0.024669]           SUPPORTED              RAW_A provides added information for graduate-school progression.
         H_D          RAW_A D AME progression minus employment 0.011794 [0.003216, 0.019641]          NaN      NaN       NaN [0.003216, 0.019641]           SUPPORTED                          D is judged by school bootstrap CI, not by a p-value.
H_P_TWO_PART          RAW_A              Two-part combined AME 0.015659 [0.009023, 0.019981]          NaN      NaN       NaN [0.009023, 0.019981]           SUPPORTED Two-part model is sensitivity for zero process in graduate-school progression.

## P5 residual comparison
major_group_7                 outcome   raw_AME  residual_AME    difference  sign_agreement  CI_overlap  relative_attenuation
          ART GRAD_SCHOOL_PROGRESSION  0.005543      0.005623  7.985441e-05            True        True             -0.014406
          ART       HEALTH_EMPLOYMENT -0.001511     -0.001807 -2.963994e-04            True        True             -0.196192
          EDU GRAD_SCHOOL_PROGRESSION  0.004945      0.004823 -1.218612e-04            True        True              0.024642
          EDU       HEALTH_EMPLOYMENT  0.013206      0.014660  1.454017e-03            True        True             -0.110099
          ENG GRAD_SCHOOL_PROGRESSION  0.034633      0.034293 -3.393359e-04            True        True              0.009798
          ENG       HEALTH_EMPLOYMENT  0.016151      0.015929 -2.223772e-04            True        True              0.013769
          HUM GRAD_SCHOOL_PROGRESSION  0.010608      0.010263 -3.455115e-04            True        True              0.032570
          HUM       HEALTH_EMPLOYMENT  0.018289      0.017490 -7.990433e-04            True        True              0.043690
          MED GRAD_SCHOOL_PROGRESSION  0.000677      0.001422  7.449389e-04            True        True             -1.100745
          MED       HEALTH_EMPLOYMENT -0.004508     -0.004509 -6.186256e-07            True        True             -0.000137
          NAT GRAD_SCHOOL_PROGRESSION  0.036500      0.035839 -6.603269e-04            True        True              0.018091
          NAT       HEALTH_EMPLOYMENT -0.001430     -0.000024  1.406063e-03            True        True              0.983030
          SOC GRAD_SCHOOL_PROGRESSION  0.010518      0.010162 -3.559932e-04            True        True              0.033846
          SOC       HEALTH_EMPLOYMENT  0.004843      0.005246  4.031064e-04            True        True             -0.083239

## Status
                                                                                                                      0
python                                                                                                           3.12.3
platform                                                  Linux-6.18.33.2-microsoft-standard-WSL2-x86_64-with-glibc2.39
pandas                                                                                                            3.0.3
numpy                                                                                                             2.5.0
statsmodels                                                                                                      0.14.6
working_directory                                                               /home/sieg/projects-wsl/SBS_dataScience
git_commit                                                                     5b1a3d54266d881a839ad9a3cec750da66e94bc7
execution_timestamp_utc                                                                2026-07-13T08:31:16.939981+00:00
notebook_path                    /home/sieg/projects-wsl/SBS_dataScience/workbook/p2/P2_6/p4_confirmatory_closure.ipynb
output_root                                                    /home/sieg/projects-wsl/SBS_dataScience/workbook/p2/P2_6
P4_INPUT_STATUS                                                                                                   READY
P4_CV_ALGORITHM_STATUS                                                                              READY_WITH_WARNINGS
P4_SIGNAL_CONTRACT_STATUS                                                                                         READY
P4_RAW_A_BOOTSTRAP_STATUS                                                                                         READY
P4_RESIDUAL_BOOTSTRAP_STATUS                                                                                      READY
P4_ALPHA_RESELECT_STATUS                                                                                          READY
P4_TWO_PART_STATUS                                                                                                READY
P4_LOCKED_TEST_STABILITY_STATUS                                                                     READY_WITH_WARNINGS
P4_HYPOTHESIS_STATUS                                                                                              READY
P5_RESIDUAL_REFRESH_STATUS                                                                                        READY
P4_CLOSURE_OVERALL_STATUS                                                                           READY_WITH_WARNINGS
raw_bootstrap_successful_n                                                                                          500
residual_bootstrap_successful_n                                                                                     500
alpha_reselect_successful_n                                                                                         100
two_part_bootstrap_successful_n                                                                                     250
strict_d08_sha256                                      5f56e375fd1c0474a5e55652859ae007e2f45becd6d3350ee4c82e21fab8df9b
p2_handoff_sha256                                      2bbc7d64784b7b530d57bb6a2096d14cb11c5879f41a5208f9ff3b02f4bdddcb
p3_full_residual_sha256                                d8decd39dca42ccd0dc194fa3813ba0036541098eea08ddfb64627f6fc6cb8cc