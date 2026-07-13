# P4 Phase Data Contract

Phase-specific allowlists are stored in `artifacts/p4_phase_model_contract.csv`; forbidden candidate-pool variables do not block the whole contract unless they remain allowed in a phase model.

| phase_id | target | allowed_feature_n | total_feature_n |
| --- | --- | --- | --- |
| P1 | a_rate_pct | 2 | 151 |
| P2-Q | a_rate_pct | 22 | 151 |
| P2-S | a_rate_pct | 18 | 151 |
| P3-Q | a_rate_pct | 22 | 151 |
| P3-S | a_rate_pct | 18 | 151 |
| P4-E | health_employment_rate_pct | 23 | 151 |
| P4-P | graduate_school_progression_rate_pct | 23 | 151 |
| P5 | major7_year_context | 43 | 151 |
| P6 | octant_type_label | 22 | 151 |
| P7 | task_specific | 0 | 151 |
| P8 | t_plus_1_target | 22 | 151 |
