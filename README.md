# P2_4 Branch — Grade Formation, Strict Modeling Readiness, and Confirmatory Chain

This branch publishes the `workbook/p2/p2_4` modeling package for the university grade-signal project.

## Representative Notebook

- [`workbook/p2/p2_4/p2_grade_formation_v1_strict/p2_grade_formation_strict.ipynb`](workbook/p2/p2_4/p2_grade_formation_v1_strict/p2_grade_formation_strict.ipynb)  
  Strict-clean P2 grade-formation notebook: nested OLS, GAM checks, MixedLM diagnostics, locked-test reporting, and handoff artifacts.

## Supporting Notebooks

| Notebook | Role |
|---|---|
| [`p2_G4_VISUAL.ipynb`](workbook/p2/p2_4/p2_G4_VISUAL.ipynb) | Visual lecture/reporting notebook for G4 source and modeling interpretation |
| [`p2_G4_source_parquet_csv_eda.ipynb`](workbook/p2/p2_4/p2_G4_source_parquet_csv_eda.ipynb) | Source parquet/CSV EDA and schema inspection |
| [`p2_G4_1.ipynb`](workbook/p2/p2_4/p2_G4_1.ipynb) | P4-1 data contract notebook |
| [`p2_G4_2.ipynb`](workbook/p2/p2_4/p2_G4_2.ipynb) | P4-2 modeling readiness notebook |
| [`p3_grade_residual_v1_strict/p3_grade_residual_strict.ipynb`](workbook/p2/p2_4/p3_grade_residual_v1_strict/p3_grade_residual_strict.ipynb) | Strict grade residual branch |
| [`p4_grade_signal_outcomes_v1_strict/p4_grade_signal_outcomes_strict.ipynb`](workbook/p2/p2_4/p4_grade_signal_outcomes_v1_strict/p4_grade_signal_outcomes_strict.ipynb) | Strict outcome modeling branch |

## Engineering Research Value

- Converts P2-G3 handoff artifacts into a strict modeling matrix.
- Separates P2-S structure-ready modeling from P2-Q selectivity-blocked modeling.
- Tracks model contract, feature approval, leakage, missingness, and multicollinearity gates.
- Produces interpretable model diagnostics: nested OLS, GroupKFold, GAM, MixedLM, school FE, and locked-test results.
- Provides downstream residual and outcome branches for P5/P6 research.

## Important Reports

| Artifact | Purpose |
|---|---|
| [`p2_grade_formation_v1_strict/reports/P2_GRADE_FORMATION_REPORT.md`](workbook/p2/p2_4/p2_grade_formation_v1_strict/reports/P2_GRADE_FORMATION_REPORT.md) | P2 strict grade-formation report |
| [`p2_grade_formation_v1_strict/reports/P2_GRADE_FORMATION_STATUS.json`](workbook/p2/p2_4/p2_grade_formation_v1_strict/reports/P2_GRADE_FORMATION_STATUS.json) | P2 status contract |
| [`p4_2_model_readiness/reports/P4_MODEL_READINESS_SUMMARY.md`](workbook/p2/p2_4/p4_2_model_readiness/reports/P4_MODEL_READINESS_SUMMARY.md) | P4 model-readiness summary |
| [`p4_preprocessing_integrity_v1/reports/DATA_PREPROCESSING_INTEGRITY_REPORT.md`](workbook/p2/p2_4/p4_preprocessing_integrity_v1/reports/DATA_PREPROCESSING_INTEGRITY_REPORT.md) | Preprocessing integrity report |
| [`p4_grade_signal_outcomes_v1_strict/reports/P4_GRADE_SIGNAL_OUTCOME_REPORT.md`](workbook/p2/p2_4/p4_grade_signal_outcomes_v1_strict/reports/P4_GRADE_SIGNAL_OUTCOME_REPORT.md) | Outcome modeling report |

## Branch Scope

```text
workbook/p2/p2_4/
```

Runtime caches such as `__pycache__` and `.pyc` files are intentionally excluded.

## Portfolio Navigation

- [`main`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/main): portfolio landing README
- [`P2_2`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_2): data understanding and H1-H7 EDA
- [`P2_3`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_3): GOMS bridge, independent audit, and P4 handoff
- [`P2_5`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_5): major7 heterogeneity modeling
- [`P2_6`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_6): confirmatory chain run-up and closure
