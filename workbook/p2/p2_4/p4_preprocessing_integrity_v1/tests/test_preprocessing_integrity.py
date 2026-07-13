from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = json.loads((ROOT / "manifest" / "integrity_summary.json").read_text(encoding="utf-8"))
CRIT = SUMMARY["critical"]

def test_required_inputs_exist():
    assert CRIT["required_input_fail_n"] == 0

def test_key_null_and_duplicates():
    assert CRIT["outcome_row_id_null_n"] == 0
    assert CRIT["outcome_row_id_duplicate_n"] == 0

def test_exact_duplicate_or_ledger():
    assert CRIT["exact_duplicate_n"] == 0

def test_unapproved_many_to_many_and_expansion():
    assert CRIT["unapproved_many_to_many_n"] == 0
    assert CRIT["row_expansion_unexplained_n"] == 0

def test_domain_and_rate_integrity():
    assert CRIT["domain_fail_anomaly_n"] == 0
    assert CRIT["rate_reconciliation_fail_n"] == 0

def test_registry_and_split():
    assert CRIT["sample_registry_mismatch_n"] == 0
    assert CRIT["school_split_leakage_n"] == 0

def test_feature_leakage_roles():
    assert CRIT["target_self_leakage_n"] == 0
    assert CRIT["active_id_metadata_feature_n"] == 0
    assert CRIT["unresolved_other_role_n"] == 0
    assert CRIT["active_all_null_feature_n"] == 0

def test_manifest_and_lineage():
    manifest = json.loads((ROOT / "PREPROCESSING_INTEGRITY_MANIFEST.json").read_text(encoding="utf-8"))
    assert len(manifest["files"]) > 0
    assert CRIT["row_lineage_missing_n"] == 0
    assert (ROOT / "data" / "row_lineage.parquet").exists()
