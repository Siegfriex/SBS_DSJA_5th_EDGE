# P2_3 Branch — GOMS Bridge, Independent Audit, and P4 Handoff

This branch publishes the `workbook/p2/p2_3` package for the bridge between grade-distribution data, GOMS labor-market context, independent audit evidence, and downstream P4 modeling readiness.

## Representative Notebook

- [`workbook/p2/p2_3/p3_1.ipynb`](workbook/p2/p2_3/p3_1.ipynb)  
  Primary notebook for the P2-G3 handoff contract, lineage checks, bridge construction, and downstream readiness evidence.

## Supporting Notebooks

| Notebook | Role |
|---|---|
| [`p3_2.ipynb`](workbook/p2/p2_3/p3_2.ipynb) | GOMS labor-market context profiling and recent-major aggregation |
| [`P2_G1_kedi.ipynb`](workbook/p2/p2_3/P2_G1_kedi.ipynb) | KEDI/GOMS source-side exploratory notebook |

## Engineering Research Value

- Builds the cross-agent handoff layer from P2-G3 into P2-G4.
- Keeps lineage, hashes, local1/local2 manifests, and independent audit outputs in one branch.
- Provides a candidate P4 handoff package with explicit lock files and manifests.
- Separates bridge diagnostics from final modeling so downstream notebooks can consume stable contracts.

## Important Artifacts

| Artifact | Purpose |
|---|---|
| [`audit/P2_G3_INDEPENDENT_AUDIT_REPORT.md`](workbook/p2/p2_3/audit/P2_G3_INDEPENDENT_AUDIT_REPORT.md) | Independent audit evidence |
| [`p4_handoff_candidate/P4_CANDIDATE_HANDOFF_LOCK.json`](workbook/p2/p2_3/p4_handoff_candidate/P4_CANDIDATE_HANDOFF_LOCK.json) | Handoff readiness lock |
| [`shared_handoff/LOCAL2_HANDOFF_MANIFEST.json`](workbook/p2/p2_3/shared_handoff/LOCAL2_HANDOFF_MANIFEST.json) | Shared handoff manifest |
| [`logs/p2_g3_combined_run_manifest.json`](workbook/p2/p2_3/logs/p2_g3_combined_run_manifest.json) | Combined execution manifest |
| [`p3_2/goms_major_profile_recent.parquet`](workbook/p2/p2_3/p3_2/goms_major_profile_recent.parquet) | Recent major-group labor-market profile |

## Branch Scope

```text
workbook/p2/p2_3/
```

Runtime caches such as `__pycache__` and `.pyc` files are intentionally excluded.

## Portfolio Navigation

- [`main`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/main): portfolio landing README
- [`P2_2`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_2): data understanding and H1-H7 EDA
- [`P2_4`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_4): grade formation and strict modeling readiness
- [`P2_5`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_5): major7 heterogeneity modeling
- [`P2_6`](https://github.com/Siegfriex/SBS_DSJA_5th_EDGE/tree/P2_6): confirmatory chain run-up and closure
