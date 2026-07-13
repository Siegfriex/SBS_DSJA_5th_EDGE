# workbook/p2/p2_3 — P2-G3 Bridge, Audit, and Handoff

This folder contains the P2-G3 engineering bridge from cleaned grade-signal inputs to downstream modeling contracts.

## Representative Notebook

[`p3_1.ipynb`](p3_1.ipynb)

Start here to understand lineage, contract formation, audit gates, and how the package becomes consumable by P2-G4.

## Key Files

| Path | Description |
|---|---|
| `p3_1.ipynb` | Representative handoff/contract notebook |
| `p3_2.ipynb` | GOMS major-profile and labor-context notebook |
| `audit/P2_G3_INDEPENDENT_AUDIT_REPORT.md` | Independent audit report |
| `p4_handoff_candidate/` | Candidate handoff package for P4 |
| `shared_handoff/` | Shared handoff outputs and manifests |
| `logs/` | Run manifests and execution evidence |
| `qa/` | Bridge and matching QA tables |

## Interpretation Guardrails

- Treat the handoff lock and manifests as contract boundaries.
- Do not assume unresolved/ambiguous department mappings are harmless.
- Use the audit report before consuming the handoff as modeling-ready.
- Keep GOMS context as aggregate labor-market evidence, not individual-level outcome data.
