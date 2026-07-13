# workbook/p2/p2_4 — Strict Grade-Formation Modeling

This folder is the strict modeling core of the project. It turns validated P2/P3 handoff data into grade-formation, residual, and outcome-modeling artifacts.

## Representative Notebook

[`p2_grade_formation_v1_strict/p2_grade_formation_strict.ipynb`](p2_grade_formation_v1_strict/p2_grade_formation_strict.ipynb)

Start here for the final strict-clean grade-formation result.

## Key Components

| Path | Description |
|---|---|
| `p2_grade_formation_v1_strict/` | Strict P2 A-rate formation model |
| `p3_grade_residual_v1_strict/` | Residual branch for downstream signal modeling |
| `p4_grade_signal_outcomes_v1_strict/` | Outcome branch for employment/progression targets |
| `p4_1_data_contract/` | Data-contract and integrity gate |
| `p4_2_model_readiness/` | Modeling-readiness audits |
| `p4_preprocessing_integrity_v1/` | Preprocessing integrity checks |
| `source_eda/` | Source EDA, human handoff, and strict-clean source artifacts |
| `p2_G4_VISUAL.ipynb` | Visual interpretation notebook |

## Interpretation Guardrails

- P2-S and P2-Q are different branches; do not merge their conclusions.
- Locked-test metrics are not development R2.
- MixedLM and GAM diagnostics are model checks, not causal proof.
- Feature-contract blockers should remain blockers until explicitly approved.
