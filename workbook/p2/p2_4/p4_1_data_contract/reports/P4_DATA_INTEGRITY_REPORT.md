# P4 Data Integrity Report

## Final Status
**P4_DATA_CONTRACT_READY**

## Core Hashes
- D01 v2: `2f187b5af44c828d4107af12368029caf6b83b6254af75b9653b6402b8f1b0ce` shape `[34969, 186]`
- D03 v2: `c6fd569052684502e5bab5758510d3cd945f68ddeaa47fdfb3e9bab803889dca` shape `[10242, 108]`
- D08 v2: `598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962` shape `[10242, 151]`

## Gate Summary
- Manifest hash mismatch: `0`
- Manifest shape mismatch: `0`
- Manifest missing files: `0`
- D01 canonical grain duplicate: `0`
- D01 unexplained raw count delta: `0`
- D08 P4 composite duplicate: `0`
- Outcome mismatch cells D03->D08: `0`
- Structure high-confidence rate: `83.59%`
- Major high/medium rate: `98.60%`
- D07->D08 GOMS mismatch: `0`
- Split leakage: `0`
- Registry missing count: `0`
- All-null active feature sets: `0`
- FAIL checks: `0`

## Evidence Paths
- Manifest audit: `qa/manifest_integrity_audit.csv`
- D01 explanation: `reports/D01_GRAIN_EXPLANATION.md`
- Spine comparison: `qa/d03_d08_spine_comparison.csv`
- Structure matching: `qa/structure_match_integrity.csv`
- Major mapping: `qa/major7_mapping_integrity.csv`
- Local2 lineage: `qa/local2_context_lineage_integrity.csv`
- Split/sample: `qa/split_sample_integrity.csv`
- Registry: `qa/registry_integrity.csv`
