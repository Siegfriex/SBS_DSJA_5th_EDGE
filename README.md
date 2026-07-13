# P2_2 Branch — Grade Signal Data Understanding & Journalism EDA

This branch publishes the `workbook/p2/p2_2` research package for the university grade-signal project.

## Representative Notebook

- [`workbook/p2/p2_2/h1_h7_intelligence_briefing.ipynb`](workbook/p2/p2_2/h1_h7_intelligence_briefing.ipynb)  
  End-to-end H1-H7 briefing notebook connecting grade distribution, admission selectivity, policy signals, employment, and progression questions.

## Supporting Notebooks

| Notebook | Role |
|---|---|
| [`h1_h2.ipynb`](workbook/p2/p2_2/h1_h2.ipynb) | Core grade-distribution and admission-selectivity EDA |
| [`h1_h2_measurement_validation.ipynb`](workbook/p2/p2_2/h1_h2_measurement_validation.ipynb) | Validation-gated measurement audit for admission variables |
| [`gate2_final_rule_confirmation.ipynb`](workbook/p2/p2_2/gate2_final_rule_confirmation.ipynb) | Final crawl-rule confirmation from cached admission evidence |
| [`final/eda/P2_G0.ipynb`](workbook/p2/p2_2/final/eda/P2_G0.ipynb) | Major-level integrated sample and cleaning decisions |
| [`final/eda/P2_G1_concat_eda.ipynb`](workbook/p2/p2_2/final/eda/P2_G1_concat_eda.ipynb) | Concatenated EDA frame and quality checks |

## Engineering Research Value

- Freezes a reproducible data-understanding layer before downstream modeling.
- Separates observed zero, structural null, source-coded unknown, and true missingness.
- Documents which admission metrics are validated, unresolved, or excluded.
- Keeps crawl validation on cached CSV/Parquet/HTML artifacts instead of re-crawling.
- Packages figures, evidence tables, and reports so later branches can reference the same audit trail.

## Important Reports

| Artifact | Purpose |
|---|---|
| [`reports/h1_h7_intelligence_briefing.md`](workbook/p2/p2_2/reports/h1_h7_intelligence_briefing.md) | Article-style integrated briefing |
| [`reports/grade_signal_grounded_report.md`](workbook/p2/p2_2/reports/grade_signal_grounded_report.md) | Grounded grade-signal evidence summary |
| [`reports/h1_h2_technical_statistics_report.md`](workbook/p2/p2_2/reports/h1_h2_technical_statistics_report.md) | Technical H1/H2 statistics notes |
| [`final/admission/P2_admission_v3_final_report.md`](workbook/p2/p2_2/final/admission/P2_admission_v3_final_report.md) | Admission data integration and validation report |
| [`val_outputs/38_final_validation_summary.csv`](workbook/p2/p2_2/val_outputs/38_final_validation_summary.csv) | Final validation gate summary table |

## Branch Scope

```text
workbook/p2/p2_2/
```

Runtime caches such as `__pycache__` and `.pyc` files are intentionally excluded from this portfolio branch.

## Portfolio Navigation

- [`main`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/main): portfolio landing README
- [`P2_3`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_3): GOMS bridge, independent audit, and P4 handoff
- [`P2_4`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_4): grade formation and strict modeling readiness
- [`P2_5`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_5): major7 heterogeneity modeling
- [`P2_6`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_6): confirmatory chain run-up and closure
