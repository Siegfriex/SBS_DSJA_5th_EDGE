# HANDOFF TO CHATGPT - P2 Integrated Engineering Blueprint

FINAL_STATUS: PASS_WITH_WARNINGS
RUN_ID: 20260713T084211Z_5b1a3d5
OUTPUT_RUN_DIR: /home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_integrated_engineering_blueprint_v1/runs/20260713T084211Z_5b1a3d5
ACTIVE_D08: /home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet
ACTIVE_D08_SHAPE: 10242 x 151
ACTIVE_D08_SHA256: 598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962
REPRESENTATIVE_NOTEBOOKS: 17 selected, 0 clone hash mismatches
KEY_DUPLICATE: outcome_row_id duplicate rows = 0
PCT_RANGE_VIOLATION: 0
TARGET_NON_NULL: {"a_rate_pct": 10242, "health_employment_rate_pct": 7477, "graduate_school_progression_rate_pct": 7587}
P6_OVERALL_STATUS: READY_WITH_WARNINGS
P5_OVERALL_STATUS: READY_WITH_WARNINGS

GATE_MATRIX:
| stage | status | evidence |
| --- | --- | --- |
| V00_inventory | PASS | representative_notebook_clone_inventory.csv |
| V01_source_lineage | PASS | data_source_catalog.csv |
| V02_integrity | PASS | key_integrity_audit.csv |
| V03_samples | PASS | phase_sample_summary.csv |
| V04_existing_results | PASS | existing_result_numeric_readout.csv |
| V05_interpretation_limits | PASS | numeric_interpretation_scaffold.csv |
| Final_handoff | PASS | INTEGRATED_ENGINEERING_BLUEPRINT_REPORT.md |

ISSUES:
| issue_id | severity | evidence | impact | required_decision |
| --- | --- | --- | --- | --- |
| WARN_D08_SPLIT_EXTERNAL | WARN | D08_active has no split column; dim_school_split and membership registries carry split | Do not infer split from row order | Use school_uid merge to dim_school_split |
| PASS_PCT_RANGE | PASS | 0 pct range violations in active/clean/strict marts | Non-blocking | No decision |
| PASS_OUTCOME_ROW_ID | PASS | outcome_row_id duplicate rows = 0 | Stable row ID usable | No decision |
| WARN_DIRECT_URL_LIMIT | WARN | Some source direct download URLs not in manifest; portal URL + local hash retained | External provenance is portal-level for those files | Keep local hashes as provenance anchor |
| WARN_Q_BRANCH_BLOCKED | WARN | P6_Q_BRANCH_STATUS=BLOCKED_FEATURE_CONTRACT | Selectivity/Q branch is not launch-ready | Resolve feature contract before Q branch interpretation |
| WARN_PHASE_STATUS_MIXED | WARN | P5 v2 strict reports residual pending, P6 run-up reports residual handoff ready | Use newest phase-specific artifact when citing residual status | Freeze canonical phase status if publishing |

KEY_OUTPUTS:
- /home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_integrated_engineering_blueprint_v1/runs/20260713T084211Z_5b1a3d5/reports/INTEGRATED_ENGINEERING_BLUEPRINT_REPORT.md
- /home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_integrated_engineering_blueprint_v1/runs/20260713T084211Z_5b1a3d5/qa/representative_notebook_clone_inventory.csv
- /home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_integrated_engineering_blueprint_v1/runs/20260713T084211Z_5b1a3d5/qa/key_integrity_audit.csv
- /home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_integrated_engineering_blueprint_v1/runs/20260713T084211Z_5b1a3d5/qa/existing_result_numeric_readout.csv
- /home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_integrated_engineering_blueprint_v1/runs/20260713T084211Z_5b1a3d5/figures/integrated_blueprint_dashboard.png
