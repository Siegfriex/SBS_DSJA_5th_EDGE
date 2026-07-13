# P4 D08 Data Card

## Status
- final_status: **P4_DATA_CONTRACT_READY**
- D08 shape: `[10242, 151]`
- D08 hash: `598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962`

## Grain And Keys
- Grain: 2024년 × outcome 학교 × outcome 캠퍼스 × outcome 학과
- Frozen P4 key: `analysis_year`, `p4_school_uid`, `p4_campus_uid`, `p4_dept_uid`, with `outcome_row_id` as stable row identity.
- P4 composite duplicate rows: `0`
- Carried headcount UID composite duplicate rows: `18`. This is tracked as WARN because `dept_uid` is a matched D01 identifier, not the outcome spine key.

## Coverage
- structure high-confidence: `8561/10242 = 83.59%`
- major high/medium: `10099/10242 = 98.60%`
- Local2 D07 hash: `f44c6f9e7a7539361dce301686144780e0ce588deb929b625ebe811674bb621f`
- D07 to D08 GOMS mismatch cells: `0`

## P4 Restrictions
- Do not treat `manual_pending` or `unmatched` rows as having observed structure context.
- Do not use ambiguous/unknown `major_group_7` rows in major/context/GOMS samples.
- Do not activate all-null D04 industry features (`ctx24_industry_hhi`, `ctx24_industry_top3_pct`).
- Do not impute, scale, one-hot encode, train models, or recalculate ratios in this contract notebook.
