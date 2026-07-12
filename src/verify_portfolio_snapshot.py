from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    metrics = json.loads((ROOT / "data/portfolio_metrics.json").read_text(encoding="utf-8"))
    failures = pd.read_csv(ROOT / "data/audit_failures.csv", encoding="utf-8-sig")
    local1 = pd.read_csv(ROOT / "data/local1_independent_qa.csv", encoding="utf-8-sig")
    local2 = pd.read_csv(ROOT / "data/local2_independent_qa.csv", encoding="utf-8-sig")
    manifest = pd.read_csv(ROOT / "data/manifest_hash_check.csv", encoding="utf-8-sig")
    sample = pd.read_csv(ROOT / "data/sample_registry_recalculation.csv", encoding="utf-8-sig")

    checks = {
        "final_verdict_green": metrics["final_verdict"] == "GREEN",
        "critical_failure_zero": len(failures) == 0,
        "local1_all_pass": (local1["status"] == "PASS").all(),
        "local2_all_pass": (local2["status"] == "PASS").all(),
        "manifest_all_pass": (manifest["status"] == "PASS").all(),
        "sample_all_pass": (sample["status"] == "PASS").all(),
        "d08_rows_10242": metrics["d08_shape"][0] == 10242,
    }
    for name, ok in checks.items():
        print(f"{name}: {'PASS' if ok else 'FAIL'}")
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
