# workbook/p2/p2_2 — Data Understanding, Admission Validation, and H1-H7 Briefing

This folder is the data-understanding and journalism-EDA foundation for the P2 grade-signal project.

## Representative Notebook

[`h1_h7_intelligence_briefing.ipynb`](h1_h7_intelligence_briefing.ipynb)

Use this first when reviewing the branch. It provides the integrated narrative layer across H1-H7, with tables and figures grounded in local artifacts.

## What This Folder Contributes

1. Validated admission and grade-distribution evidence.
2. Major-level integration for enterprise type, industry, certificate, starting salary, and job-category inputs.
3. Crawl-rule confirmation based on cached admission pages and parsed outputs.
4. Evidence tables and visual artifacts for article-style interpretation.
5. Explicit handling of missingness semantics before modeling.

## Key Files

| Path | Description |
|---|---|
| `h1_h7_intelligence_briefing.ipynb` | Representative integrated briefing notebook |
| `reports/h1_h7_intelligence_briefing.md` | Markdown report paired with the briefing notebook |
| `h1_h2_measurement_validation.ipynb` | Measurement validation notebook for admission variables |
| `gate2_final_rule_confirmation.ipynb` | Final rule confirmation notebook |
| `final/eda/P2_G0.ipynb` | Major-level integrated cleaning notebook |
| `final/eda/P2_G1_concat_eda.ipynb` | Concatenated EDA notebook |
| `val_outputs/38_final_validation_summary.csv` | Final validation summary |
| `figures/` | Static visualization outputs |

## Interpretation Guardrails

- Do not treat admission-observed rows as a random sample.
- Do not merge structural zero, source-coded unknown, and missing values.
- Do not re-crawl when reviewing this branch; cached artifacts are the reproducibility boundary.
- Treat all conclusions as aggregate school/department-level evidence, not individual student inference.
