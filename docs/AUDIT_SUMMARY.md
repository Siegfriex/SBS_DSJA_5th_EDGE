# Audit Summary

독립감사는 `audit/p2_g3_candidate_green_audit` 기준으로 재계산했다.

## Verdict

- final verdict: **GREEN**
- critical failure count: **0**
- Local 1 QA: `9/9 PASS`
- Local 2 QA: `8/8 PASS`
- manifest hash mismatch: `0`

## Core Checks

- D01 grain duplicate: `0`
- D08 row count: `10,242`
- structure high-confidence match rate: `83.59%`
- major mapping rate: `98.60%`
- split leakage: `0`
- D07 to D08 lineage mismatch: see `data/cross_agent_handoff_audit.csv`

## Evidence Files

- `data/local1_independent_qa.csv`
- `data/local2_independent_qa.csv`
- `data/manifest_hash_check.csv`
- `data/sample_registry_recalculation.csv`
- `data/audit_failures.csv`
