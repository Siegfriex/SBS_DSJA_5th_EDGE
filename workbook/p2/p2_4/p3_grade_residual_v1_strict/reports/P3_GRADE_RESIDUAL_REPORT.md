# P3 Strict Grade Residual Report

P3-S-FULL and P3-S-NOPOLICY residuals were generated with school GroupKFold OOF on development rows and development-fit predictions on locked test rows.

## Performance
model_label  dev_row_n  test_row_n  oof_n   oof_mae  oof_rmse   oof_r2  oof_calibration_intercept  oof_calibration_slope  test_n  test_mae  test_rmse   test_r2  test_calibration_intercept  test_calibration_slope  devfit_rank  devfit_encoded_n
       FULL       6702         890   6702 10.473046 14.053527 0.056153                  12.081454               0.711055     890 10.432357  14.082241 -0.066762                   25.082007                0.377768           38                38
   NOPOLICY       6702         890   6702 10.375679 13.952432 0.069684                   9.840046               0.764013     890 10.426699  14.085459 -0.067249                   25.143242                0.376313           37                37

## Diagnostics
model_label  coverage_n  coverage_rate  raw_residual_corr  residual_variance  raw_variance  residual_to_raw_variance_ratio  expected_mean  residual_mean
       FULL        7592            1.0           0.926507         197.530286    209.282974                        0.943843      41.788217      -0.123777
   NOPOLICY        7592            1.0           0.926750         194.699208    209.282974                        0.930316      41.825725      -0.161285

P3-Q status: BLOCKED_FEATURE_CONTRACT