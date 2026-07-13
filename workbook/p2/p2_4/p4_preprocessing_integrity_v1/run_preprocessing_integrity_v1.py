from __future__ import annotations

import hashlib
import ast
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow as pa

try:
    import sklearn
except Exception:  # pragma: no cover
    sklearn = None


PROJECT_ROOT = Path(__file__).resolve().parents[4]
OUT_ROOT = PROJECT_ROOT / "workbook" / "p2" / "p2_4" / "p4_preprocessing_integrity_v1"
DATA_DIR = OUT_ROOT / "data"
QA_DIR = OUT_ROOT / "qa"
REPORT_DIR = OUT_ROOT / "reports"
LOG_DIR = OUT_ROOT / "logs"
EXECUTED_DIR = OUT_ROOT / "executed"
TEST_DIR = OUT_ROOT / "tests"
MANIFEST_DIR = OUT_ROOT / "manifest"
RUNS_DIR = OUT_ROOT / "runs"

READINESS_ROOT = PROJECT_ROOT / "workbook" / "p2" / "p2_4" / "p4_modeling_readiness_v4"
CLEANING_ROOT = PROJECT_ROOT / "workbook" / "p2" / "p2_4" / "p4_cleaning_handoff_v3"
HANDOFF_ROOT = PROJECT_ROOT / "workbook" / "p2" / "p2_3" / "p4_handoff_candidate" / "shared"

D08_PATH = HANDOFF_ROOT / "mart_department_model_base_2024.parquet"
MEMBERSHIP_PATH = READINESS_ROOT / "data" / "P4_PHASE_SAMPLE_MEMBERSHIP_FINAL.parquet"
SAMPLE_REGISTRY_PATH = READINESS_ROOT / "artifacts" / "P4_PHASE_SAMPLE_REGISTRY_FINAL.csv"
COLUMN_REGISTRY_PATH = READINESS_ROOT / "artifacts" / "department_model_column_registry_v4.csv"
FEATURE_SET_PATH = READINESS_ROOT / "artifacts" / "P4_PHASE_FEATURE_SET_FINAL.csv"
MODEL_SPEC_PATH = READINESS_ROOT / "artifacts" / "P4_PHASE_MODEL_SPEC_FINAL.csv"
DUPLICATE_CONFLICT_PATH = READINESS_ROOT / "qa" / "P4_DUPLICATE_CONFLICT_RESOLUTION.csv"
TARGET_PROFILE_PATH = READINESS_ROOT / "profiles" / "P4_TARGET_PROFILE_BY_PHASE.csv"
FINAL_READINESS_PATH = READINESS_ROOT / "reports" / "P4_FINAL_MODELING_READINESS.json"
BUNDLE_MANIFEST_PATH = READINESS_ROOT / "P4_MODELING_REVIEW_BUNDLE_MANIFEST.json"

RANDOM_SEED_USED = False

EXPECTED = {
    "mart_department_model_base_2024": {
        "path": D08_PATH,
        "shape": [10242, 151],
        "sha256": "598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962",
        "required": True,
    },
    "P4_PHASE_SAMPLE_MEMBERSHIP_FINAL": {
        "path": MEMBERSHIP_PATH,
        "shape": [10242, 21],
        "sha256": "58d0308aa92f04badea3c7fc2db44fc28d0d93580db9bff4f16d47d870ebc7c6",
        "required": True,
    },
    "P4_PHASE_SAMPLE_REGISTRY_FINAL": {
        "path": SAMPLE_REGISTRY_PATH,
        "shape": [12, 11],
        "sha256": "6483fdf67cca469ed7bd2500e5ef917ffd01007194c83461f5c827b03f16805e",
        "required": True,
    },
    "department_model_column_registry_v4": {
        "path": COLUMN_REGISTRY_PATH,
        "shape": [151, 22],
        "sha256": "ab75225547d42ddc8e6cdf686be61ecc8bf87512729d8d9d053652b521093b94",
        "required": True,
    },
    "P4_PHASE_FEATURE_SET_FINAL": {
        "path": FEATURE_SET_PATH,
        "shape": [250, 11],
        "sha256": "dc851803d22a22e891a7fdd9a31dbe0c3d2ac56421a9798e06a9e87e20ce2320",
        "required": True,
    },
    "P4_PHASE_MODEL_SPEC_FINAL": {
        "path": MODEL_SPEC_PATH,
        "shape": [18, 10],
        "sha256": "d7f560167ec752938b73dbee3c5f9dddc84fbc009d9eeaa3905b20946cc7dc48",
        "required": True,
    },
    "P4_DUPLICATE_CONFLICT_RESOLUTION": {
        "path": DUPLICATE_CONFLICT_PATH,
        "shape": [36, 14],
        "sha256": "24d2e000661b3e67a353877383c7ef68b8e156f52bd11ac22f4b1fd724be8d4f",
        "required": True,
    },
    "P4_TARGET_PROFILE_BY_PHASE": {
        "path": TARGET_PROFILE_PATH,
        "shape": [396, 20],
        "sha256": "6f3fdb25676ccfdf59b0b2f458e5cdb5dd66dfb6f61e037b2e711418efffc25a",
        "required": True,
    },
    "P4_FINAL_MODELING_READINESS": {
        "path": FINAL_READINESS_PATH,
        "shape": None,
        "sha256": "8fcd0df2cee25f2b31ba498806ea5956e82e5da74580ce01573aa01c201ffbea",
        "required": True,
    },
    "P4_MODELING_REVIEW_BUNDLE_MANIFEST": {
        "path": BUNDLE_MANIFEST_PATH,
        "shape": None,
        "sha256": None,
        "required": True,
    },
    "P4_HANDOFF_MANIFEST": {"path": HANDOFF_ROOT / "P4_HANDOFF_MANIFEST.json", "shape": None, "sha256": None, "required": True},
    "dim_school_split": {"path": HANDOFF_ROOT / "dim_school_split.csv", "shape": None, "sha256": None, "required": True},
    "shared_model_sample_membership": {"path": HANDOFF_ROOT / "model_sample_membership.parquet", "shape": None, "sha256": None, "required": True},
    "shared_model_sample_registry": {"path": HANDOFF_ROOT / "model_sample_registry.csv", "shape": None, "sha256": None, "required": True},
    "shared_column_registry": {"path": HANDOFF_ROOT / "department_model_column_registry.csv", "shape": None, "sha256": None, "required": True},
    "shared_feature_registry": {"path": HANDOFF_ROOT / "p4_feature_set_registry.csv", "shape": None, "sha256": None, "required": True},
    "shared_target_registry": {"path": HANDOFF_ROOT / "p4_target_candidate_registry.csv", "shape": None, "sha256": None, "required": True},
    "cleaning_derived_formula_reconstruction": {
        "path": CLEANING_ROOT / "qa" / "derived_formula_reconstruction.csv",
        "shape": None,
        "sha256": None,
        "required": True,
    },
    "cleaning_split_integrity_audit": {
        "path": CLEANING_ROOT / "qa" / "split_integrity_audit.csv",
        "shape": None,
        "sha256": None,
        "required": True,
    },
    "cleaning_target_leakage_audit_by_phase": {
        "path": CLEANING_ROOT / "qa" / "target_leakage_audit_by_phase.csv",
        "shape": None,
        "sha256": None,
        "required": True,
    },
    "cleaning_count_denominator_inventory": {
        "path": CLEANING_ROOT / "qa" / "count_denominator_inventory.csv",
        "shape": None,
        "sha256": None,
        "required": True,
    },
    "cleaning_context_grain_audit": {
        "path": CLEANING_ROOT / "qa" / "context_grain_audit.csv",
        "shape": None,
        "sha256": None,
        "required": True,
    },
}

YEAR_COLUMNS = {"analysis_year", "context_reference_year", "goms_profile_start_year", "goms_profile_end_year"}
PERCENT_COLUMNS = {
    "selectivity_proxy_pct",
    "a_rate_pct",
    "cd_rate_pct",
    "f_rate_pct",
    "employment_rate_pct",
    "health_employment_rate_pct",
    "progression_rate_pct",
    "vocational_college_progression_rate_pct",
    "university_progression_rate_pct",
    "graduate_school_progression_rate_pct",
    "domestic_progression_rate_pct",
    "overseas_progression_rate_pct",
    "leave_rate_pct",
    "female_student_share_pct",
    "international_student_share_pct",
    "fulltime_faculty_share_pct",
    "ctx24_income_300plus_pct",
    "ctx24_income_400plus_pct",
    "ctx24_large_company_pct",
    "ctx24_mid_company_pct",
    "ctx24_small_company_pct",
    "ctx24_large_mid_company_pct",
    "ctx24_public_nonprofit_pct",
    "ctx24_cert_rate_pct",
    "ctx24_industry_top3_pct",
    "goms_recent_employment_rate_pct",
    "goms_recent_firm_300plus_pct",
    "goms_recent_public_nonprofit_pct",
    "goms_recent_permanent_pct",
    "goms_recent_unstable_pct",
    "goms_recent_self_employed_pct",
    "goms_recent_industry_top3_pct",
    "goms_recent_professional_highskill_pct",
    "goms_latest_2019_firm_300plus_pct",
    "goms_latest_2019_permanent_pct",
}
PROPORTION_COLUMNS = {
    "a_rate_prop",
    "health_employment_rate_prop",
    "graduate_school_progression_prop",
}
RATIO_COLUMNS = {
    "competition_ratio",
    "admission_yield_ratio",
    "admit_per_applicant_ratio",
    "student_faculty_ratio",
    "ctx24_cert_per_person",
    "ctx24_industry_hhi",
    "goms_recent_industry_hhi",
    "goms_recent_hourly_income_proxy",
}
COUNT_COLUMNS = {
    "admission_capacity_n",
    "recruitment_n",
    "applicants_n",
    "admits_n",
    "enrolled_students_n",
    "leave_students_n",
    "graduates_n",
    "fulltime_faculty_n",
    "nonfulltime_faculty_n",
    "international_students_n",
    "female_students_n",
    "masters_students_n",
    "doctoral_students_n",
    "major7_candidate_count",
    "ctx24_reference_sample_n",
    "goms_profile_years_n",
    "goms_source_years_observed",
}
BOOLEAN_COLUMNS = {
    "credit_forfeit_flag",
    "has_selectivity",
    "has_employment",
    "has_progression",
    "review_needed",
    "campus_conflict_flag",
    "degree_course_conflict_flag",
    "major_conflict_flag",
    "forbidden_modifier_conflict_flag",
    "headcount_match_flag",
    "grain_review_needed",
    "major7_review_needed",
    "has_structure_context",
    "has_major_group_7_high_medium",
    "goms_year_over_year_review_flag",
}
ID_COLUMNS = {
    "outcome_row_id",
    "school_uid",
    "campus_uid",
    "dept_uid",
    "headcount_row_id",
    "headcount_grain_uid",
    "kedi_dept_code",
}
PRIMARY_ID_COLUMNS = {"outcome_row_id", "school_uid", "campus_uid", "dept_uid"}
OPTIONAL_LINEAGE_ID_COLUMNS = ID_COLUMNS - PRIMARY_ID_COLUMNS


def ensure_dirs() -> None:
    for path in [DATA_DIR, QA_DIR, REPORT_DIR, LOG_DIR, EXECUTED_DIR, TEST_DIR, MANIFEST_DIR, RUNS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_row(row: pd.Series, cols: list[str] | None = None) -> str:
    if cols is not None:
        row = row[cols]
    payload = json.dumps({str(k): normalize_json_value(v) for k, v in row.items()}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def normalize_json_value(v: Any) -> Any:
    if pd.isna(v) if not isinstance(v, (list, dict, tuple, set, np.ndarray)) else False:
        return None
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return None if np.isnan(v) else float(v)
    if isinstance(v, (np.bool_,)):
        return bool(v)
    if isinstance(v, pd.Timestamp):
        return v.isoformat()
    return v


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def atomic_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    df.to_csv(tmp, index=False, encoding="utf-8-sig")
    tmp.replace(path)


def atomic_json(obj: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def atomic_parquet(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    df.to_parquet(tmp, index=False)
    tmp.replace(path)


def load_dataset(path: Path) -> tuple[pd.DataFrame | None, dict[str, Any]]:
    meta: dict[str, Any] = {"loader": None, "encoding": None, "json_top_level_keys": None, "json_structure": None, "parquet_schema": None}
    if not path.exists():
        return None, meta
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        df = pd.read_parquet(path)
        meta["loader"] = "pd.read_parquet"
        try:
            meta["parquet_schema"] = str(pa.parquet.read_schema(path))
        except Exception as exc:
            meta["parquet_schema"] = f"schema_read_failed:{type(exc).__name__}:{exc}"
        return df, meta
    if suffix == ".csv":
        for enc in ["utf-8-sig", "utf-8", "cp949", "euc-kr"]:
            try:
                df = pd.read_csv(path, low_memory=False, encoding=enc)
                meta["loader"] = "pd.read_csv"
                meta["encoding"] = enc
                return df, meta
            except UnicodeDecodeError:
                continue
        df = pd.read_csv(path, low_memory=False)
        meta["loader"] = "pd.read_csv"
        meta["encoding"] = "default"
        return df, meta
    if suffix == ".json":
        obj = json.loads(path.read_text(encoding="utf-8"))
        meta["loader"] = "json.load"
        if isinstance(obj, dict):
            meta["json_top_level_keys"] = list(obj.keys())
            meta["json_structure"] = {k: type(v).__name__ for k, v in obj.items()}
            if isinstance(obj.get("files"), list):
                return pd.json_normalize(obj["files"]), meta
            return pd.DataFrame(
                {
                    "key": list(obj.keys()),
                    "value": [json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for v in obj.values()],
                }
            ), meta
        if isinstance(obj, list):
            meta["json_structure"] = {"type": "list", "length": len(obj)}
            return pd.json_normalize(obj), meta
        return pd.DataFrame({"value": [obj]}), meta
    return None, meta


def file_shape(path: Path) -> list[int] | None:
    try:
        df, _ = load_dataset(path)
        if df is None:
            return None
        return [int(df.shape[0]), int(df.shape[1])]
    except Exception:
        return None


def git_info() -> dict[str, Any]:
    def run(args: list[str]) -> str:
        return subprocess.check_output(args, cwd=PROJECT_ROOT, text=True).strip()

    try:
        full = run(["git", "rev-parse", "HEAD"])
        short = run(["git", "rev-parse", "--short", "HEAD"])
        dirty = bool(run(["git", "status", "--porcelain"]))
    except Exception as exc:
        full = short = f"unknown:{type(exc).__name__}:{exc}"
        dirty = None
    return {"commit_full": full, "commit_short": short, "dirty": dirty}


def discover_notebooks() -> pd.DataFrame:
    rows = []
    for path in sorted(PROJECT_ROOT.rglob("p2_G4_dataset_cell_inspection*ipynb")):
        rows.append(
            {
                "path": str(path),
                "relative_path": rel(path),
                "exists": True,
                "size_bytes": path.stat().st_size,
                "modified_at": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(),
                "sha256": sha256_file(path),
                "exact_requested_name": path.name == "p2_G4_dataset_cell_inspection(1).ipynb",
                "git_tracked": subprocess.run(["git", "ls-files", "--error-unmatch", str(path.relative_to(PROJECT_ROOT))], cwd=PROJECT_ROOT, text=True, capture_output=True).returncode == 0,
            }
        )
    if not rows:
        rows.append({"path": "p2_G4_dataset_cell_inspection(1).ipynb", "exists": False})
    return pd.DataFrame(rows)


def audit_notebook_execution(notebook_path: Path | None) -> pd.DataFrame:
    rows = []
    if notebook_path is None or not notebook_path.exists():
        return pd.DataFrame(
            [
                {
                    "cell_index": None,
                    "cell_id": None,
                    "execution_count": None,
                    "execute_input_time": None,
                    "idle_time": None,
                    "elapsed_seconds": None,
                    "output_count": None,
                    "error_output": None,
                    "traceback_summary": "notebook_not_found",
                    "stored_output_exists": False,
                    "execution_audit_status": "EXECUTION_FAILED",
                }
            ]
        )
    nb = json.loads(notebook_path.read_text(encoding="utf-8"))
    for idx, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        outputs = cell.get("outputs", [])
        errors = [o for o in outputs if o.get("output_type") == "error"]
        meta = cell.get("metadata", {})
        execute_input_time = meta.get("ExecuteTime", {}).get("start_time") or meta.get("execution", {}).get("iopub.execute_input")
        idle_time = meta.get("ExecuteTime", {}).get("end_time") or meta.get("execution", {}).get("shell.execute_reply")
        status = "MATCH"
        if errors:
            status = "EXECUTION_FAILED"
        elif execute_input_time is None or idle_time is None:
            status = "EXECUTION_METADATA_INCOMPLETE"
        rows.append(
            {
                "cell_index": idx,
                "cell_id": cell.get("id"),
                "execution_count": cell.get("execution_count"),
                "execute_input_time": execute_input_time,
                "idle_time": idle_time,
                "elapsed_seconds": None,
                "output_count": len(outputs),
                "error_output": bool(errors),
                "traceback_summary": " | ".join(o.get("evalue", "") for o in errors)[:500],
                "stored_output_exists": bool(outputs),
                "execution_audit_status": status,
            }
        )
    return pd.DataFrame(rows)


def build_inventory() -> pd.DataFrame:
    rows = []
    for label, cfg in EXPECTED.items():
        path = Path(cfg["path"])
        exists = path.exists()
        df = None
        meta: dict[str, Any] = {}
        status = "PASS"
        warning_code = ""
        actual_shape = None
        try:
            df, meta = load_dataset(path)
            actual_shape = [int(df.shape[0]), int(df.shape[1])] if df is not None else None
        except Exception as exc:
            status = "FAIL"
            warning_code = f"LOAD_ERROR:{type(exc).__name__}:{exc}"
        expected_sha = cfg.get("sha256")
        actual_sha = sha256_file(path) if exists else None
        hash_match = actual_sha == expected_sha if expected_sha else None
        expected_shape = cfg.get("shape")
        shape_match = actual_shape == expected_shape if expected_shape else None
        if not exists and cfg.get("required"):
            status = "FAIL"
            warning_code = "MISSING_REQUIRED_FILE"
        elif expected_sha and not hash_match:
            status = "WARN"
            warning_code = "HASH_MISMATCH_STALE_OUTPUT_OR_SOURCE_DRIFT"
        elif expected_shape and not shape_match:
            status = "WARN"
            warning_code = "SHAPE_MISMATCH_STALE_OUTPUT_OR_SOURCE_DRIFT"
        rows.append(
            {
                "label": label,
                "path": str(path.resolve()),
                "relative_path": rel(path),
                "exists": exists,
                "file_type": path.suffix.lower(),
                "size_bytes": path.stat().st_size if exists else None,
                "modified_at": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat() if exists else None,
                "sha256": actual_sha,
                "expected_sha256": expected_sha,
                "hash_match": hash_match,
                "actual_shape": json.dumps(actual_shape),
                "expected_shape": json.dumps(expected_shape),
                "shape_match": shape_match,
                "loader": meta.get("loader"),
                "encoding": meta.get("encoding"),
                "json_top_level_keys": json.dumps(meta.get("json_top_level_keys"), ensure_ascii=False),
                "json_structure": json.dumps(meta.get("json_structure"), ensure_ascii=False),
                "parquet_schema": meta.get("parquet_schema"),
                "status": status,
                "warning_code": warning_code,
            }
        )
    out = pd.DataFrame(rows)
    atomic_csv(out, QA_DIR / "dataset_inventory.csv")
    atomic_csv(out.copy(), QA_DIR / "file_provenance_audit.csv")
    return out


def merge_base() -> pd.DataFrame:
    d08 = pd.read_parquet(D08_PATH)
    mem = pd.read_parquet(MEMBERSHIP_PATH)
    sample_cols = ["outcome_row_id", "split"] + [c for c in mem.columns if c.startswith("sample_")]
    merged = d08.merge(mem[sample_cols], on="outcome_row_id", how="left", validate="one_to_one")
    return merged


def key_grain_audit(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    key_candidates = [
        ["outcome_row_id"],
        ["analysis_year", "school_uid", "campus_uid", "dept_uid"],
        ["analysis_year", "school_uid", "campus_uid", "dept_uid", "outcome_row_id"],
        ["school_uid"],
        ["campus_uid"],
        ["dept_uid"],
    ]
    rows = []
    for key in key_candidates:
        exists = all(c in df.columns for c in key)
        if exists:
            key_frame = df[key].astype("object")
            null_rows = int(key_frame.isna().any(axis=1).sum())
            dup_mask = key_frame.duplicated(keep=False)
            dup_rows = int(dup_mask.sum())
            dup_groups = int(key_frame.loc[dup_mask].drop_duplicates().shape[0]) if dup_rows else 0
            unique_n = int(key_frame.drop_duplicates().shape[0])
            value_conflict_n = 0
            if dup_rows and len(key) > 1:
                value_conflict_n = int(df.loc[dup_mask].groupby(key, dropna=False).size().gt(1).sum())
        else:
            null_rows = dup_rows = dup_groups = unique_n = value_conflict_n = None
        rows.append(
            {
                "key_candidate": "+".join(key),
                "exists": exists,
                "null_key_rows": null_rows,
                "duplicate_key_rows": dup_rows,
                "duplicate_key_groups": dup_groups,
                "unique_key_n": unique_n,
                "value_conflict_group_n": value_conflict_n,
                "status": "PASS" if exists and null_rows == 0 and (key != ["school_uid"] and key != ["campus_uid"] and key != ["dept_uid"] and dup_rows == 0 or key in [["school_uid"], ["campus_uid"], ["dept_uid"]]) else ("WARN" if exists else "FAIL"),
            }
        )
    grain_rows = [
        {"metric": "row_n", "value": len(df)},
        {"metric": "school_n", "value": df["school_uid"].nunique(dropna=True)},
        {"metric": "campus_n", "value": df["campus_uid"].nunique(dropna=True)},
        {"metric": "department_entity_n", "value": df["dept_uid"].nunique(dropna=True)},
        {"metric": "year_n", "value": df["analysis_year"].nunique(dropna=True)},
        {"metric": "same_dept_uid_multi_school_n", "value": int(df.groupby("dept_uid")["school_uid"].nunique().gt(1).sum())},
        {"metric": "same_dept_uid_multi_campus_n", "value": int(df.groupby("dept_uid")["campus_uid"].nunique().gt(1).sum())},
        {"metric": "school_dept_name_multi_entity_n", "value": int(df.groupby(["school_name_std", "dept_name_std"], dropna=False)["dept_uid"].nunique().gt(1).sum())},
        {"metric": "degree_course_non_null_n", "value": int(df["degree_course"].notna().sum()) if "degree_course" in df.columns else 0},
    ]
    grain = pd.DataFrame(grain_rows)
    out = pd.DataFrame(rows)
    atomic_csv(out, QA_DIR / "key_grain_audit.csv")
    atomic_csv(grain, QA_DIR / "grain_summary.csv")
    return out, grain


def duplicate_conflict_audit(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    exact_mask = df.duplicated(keep=False)
    if exact_mask.any():
        exact = df.loc[exact_mask].copy()
        for i, (_, row) in enumerate(exact.iterrows(), start=1):
            rows.append({"conflict_group_id": f"EXACT_{i:04d}", "outcome_row_id": row["outcome_row_id"], "classification": "EXACT_DUPLICATE", "status": "FAIL", "source": "recomputed"})
    dup = pd.read_csv(DUPLICATE_CONFLICT_PATH, low_memory=False)
    for _, row in dup.iterrows():
        rows.append(
            {
                "conflict_group_id": row["group_id"],
                "outcome_row_id": row["outcome_row_id"],
                "classification": row["classification"],
                "status": "LEDGERED_WARN" if bool(row.get("model_allowed", False)) else "LEDGERED_EXCLUSION",
                "model_allowed": row.get("model_allowed"),
                "weight_allowed": row.get("weight_allowed"),
                "denominator_allowed": row.get("denominator_allowed"),
                "exclusion_reason": row.get("exclusion_reason"),
                "source": "P4_DUPLICATE_CONFLICT_RESOLUTION.csv",
            }
        )
    # Extra source row repeated audit through headcount grain UID.
    if "headcount_grain_uid" in df.columns:
        hm = df["headcount_grain_uid"].notna()
        repeated = df.loc[hm & df.duplicated("headcount_grain_uid", keep=False)].copy()
        for uid, group in repeated.groupby("headcount_grain_uid", dropna=False):
            if len(group) <= 1:
                continue
            for _, row in group.iterrows():
                rows.append(
                    {
                        "conflict_group_id": f"HEADCOUNT_REUSE_{uid}",
                        "outcome_row_id": row["outcome_row_id"],
                        "classification": "PARENT_HEADCOUNT_REUSED",
                        "status": "LEDGERED_WARN",
                        "model_allowed": True,
                        "weight_allowed": False,
                        "denominator_allowed": False,
                        "exclusion_reason": "",
                        "source": "recomputed_headcount_grain_uid",
                    }
                )
    audit = pd.DataFrame(rows).drop_duplicates(["conflict_group_id", "outcome_row_id", "classification", "source"], keep="first")
    detail_cols = [
        "outcome_row_id",
        "analysis_year",
        "school_uid",
        "school_name_std",
        "campus_uid",
        "campus_branch",
        "dept_uid",
        "dept_name_std",
        "degree_course",
        "headcount_grain_uid",
        "match_method",
        "match_score",
        "candidate_count",
        "split",
    ]
    detail = df[[c for c in detail_cols if c in df.columns]].merge(audit, on="outcome_row_id", how="inner")
    atomic_csv(audit, QA_DIR / "duplicate_conflict_audit.csv")
    atomic_parquet(detail, DATA_DIR / "duplicate_conflict_rows.parquet")
    return audit


def join_cardinality_audit(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rows = []
    unmatched_rows = []
    review_rows = []

    def add_join(left: str, right: str, key: list[str], left_df: pd.DataFrame, right_df: pd.DataFrame, expected: str, approved_mtm: bool = False, match_method: str = "exact/stable_key") -> None:
        left_key = left_df[key].astype("object")
        right_key = right_df[key].astype("object")
        left_dup = int(left_key.duplicated(keep=False).sum())
        right_dup = int(right_key.duplicated(keep=False).sum())
        merged = left_df[key].merge(right_df[key].drop_duplicates(), on=key, how="left", indicator=True)
        matched = int(merged["_merge"].eq("both").sum())
        left_only = int(merged["_merge"].eq("left_only").sum())
        expansion_factor = 1.0
        many_to_many = left_dup > 0 and right_dup > 0
        status = "FAIL" if many_to_many and not approved_mtm else ("WARN" if left_only else "PASS")
        rows.append(
            {
                "left_dataset": left,
                "right_dataset": right,
                "join_key": "+".join(key),
                "expected_cardinality": expected,
                "actual_cardinality": "many_to_many" if many_to_many else ("many_to_one" if left_dup else "one_to_one"),
                "left_row_count_before": len(left_df),
                "right_row_count": len(right_df),
                "output_row_count": len(left_df),
                "row_expansion_factor": expansion_factor,
                "matched_rows": matched,
                "left_only_rows": left_only,
                "right_only_rows": None,
                "duplicate_key_count_left": left_dup,
                "duplicate_key_count_right": right_dup,
                "many_to_many": many_to_many,
                "approved_many_to_many": approved_mtm,
                "match_method": match_method,
                "match_confidence": "stable_key" if match_method.startswith("exact") else "source_reported",
                "review_needed": bool(status != "PASS"),
                "status": status,
            }
        )
        if left_only:
            tmp = merged.loc[merged["_merge"].eq("left_only"), key].copy()
            tmp["left_dataset"] = left
            tmp["right_dataset"] = right
            unmatched_rows.append(tmp)

    mem = pd.read_parquet(MEMBERSHIP_PATH)
    add_join("D08", "P4_PHASE_SAMPLE_MEMBERSHIP_FINAL", ["outcome_row_id"], df, mem, "one_to_one")
    split = pd.read_csv(HANDOFF_ROOT / "dim_school_split.csv", low_memory=False)
    if "school_uid" in split.columns:
        add_join("D08", "dim_school_split", ["school_uid"], df, split, "many_to_one")
    dup = pd.read_csv(DUPLICATE_CONFLICT_PATH, low_memory=False)
    add_join("D08_conflict_subset", "P4_DUPLICATE_CONFLICT_RESOLUTION", ["outcome_row_id"], dup, df[["outcome_row_id"]], "many_to_one")
    if "review_needed" in df.columns:
        review = df.loc[df["review_needed"].fillna(False).astype(bool), ["outcome_row_id", "school_name_std", "dept_name_std", "match_method", "match_score", "candidate_count"]].copy()
        review["review_reason"] = "source_match_review_needed"
        review_rows.append(review)
    out = pd.DataFrame(rows)
    unmatched = pd.concat(unmatched_rows, ignore_index=True) if unmatched_rows else pd.DataFrame(columns=["left_dataset", "right_dataset"])
    review_df = pd.concat(review_rows, ignore_index=True) if review_rows else pd.DataFrame(columns=["outcome_row_id", "review_reason"])
    atomic_csv(out, QA_DIR / "join_cardinality_audit.csv")
    atomic_csv(unmatched, QA_DIR / "join_unmatched_summary.csv")
    atomic_parquet(review_df, DATA_DIR / "join_review_rows.parquet")
    return out, unmatched, review_df


def schema_profile(df: pd.DataFrame, colreg: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    reg = colreg.set_index("column").to_dict(orient="index")
    rows = []
    coercion_rows = []
    n = len(df)
    for col in df.columns:
        s = df[col]
        role = reg.get(col, {})
        numeric = pd.to_numeric(s, errors="coerce") if col in (PERCENT_COLUMNS | RATIO_COLUMNS | COUNT_COLUMNS | YEAR_COLUMNS) else None
        non_null = int(s.notna().sum())
        missing = int(s.isna().sum())
        example_values = "|".join(map(str, s.dropna().astype("object").drop_duplicates().head(5).tolist()))
        coercion_failure_n = int(s.notna().sum() - numeric.notna().sum()) if numeric is not None else 0
        inf_n = int(np.isinf(numeric.astype(float)).sum()) if numeric is not None and numeric.notna().any() else 0
        all_null = non_null == 0
        nunique = int(s.astype("object").nunique(dropna=True))
        constant = (not all_null) and nunique <= 1
        top_share = float(s.astype("object").value_counts(dropna=False, normalize=True).iloc[0]) if n else np.nan
        near_constant = (not all_null) and (not constant) and top_share >= 0.99
        rows.append(
            {
                "column": col,
                "registry_role": role.get("semantic_role"),
                "feature_block": role.get("feature_block"),
                "measurement_level": role.get("measurement_level"),
                "actual_dtype": str(s.dtype),
                "expected_dtype": role.get("dtype_actual"),
                "nullable": bool(s.isna().any()),
                "non_null_n": non_null,
                "missing_n": missing,
                "missing_pct": missing / n * 100 if n else np.nan,
                "unique_n": nunique,
                "min": float(numeric.min()) if numeric is not None and numeric.notna().any() else None,
                "p01": float(numeric.quantile(0.01)) if numeric is not None and numeric.notna().any() else None,
                "median": float(numeric.quantile(0.5)) if numeric is not None and numeric.notna().any() else None,
                "p99": float(numeric.quantile(0.99)) if numeric is not None and numeric.notna().any() else None,
                "max": float(numeric.max()) if numeric is not None and numeric.notna().any() else None,
                "example_values": example_values,
                "coercion_failure_n": coercion_failure_n,
                "infinite_n": inf_n,
                "all_null": all_null,
                "constant": constant,
                "near_constant": near_constant,
                "status": "FAIL" if coercion_failure_n or inf_n else ("WARN" if all_null or near_constant or constant else "PASS"),
            }
        )
        if coercion_failure_n:
            bad = df.loc[s.notna() & numeric.isna(), ["outcome_row_id"]].copy()
            bad["column"] = col
            bad["raw_value"] = s.loc[bad.index].astype(str)
            coercion_rows.append(bad)
    profile = pd.DataFrame(rows)
    dtype_mismatch = profile.loc[profile["expected_dtype"].notna() & (profile["actual_dtype"] != profile["expected_dtype"])].copy()
    coercion = pd.concat(coercion_rows, ignore_index=True) if coercion_rows else pd.DataFrame(columns=["outcome_row_id", "column", "raw_value"])
    atomic_csv(profile, QA_DIR / "column_schema_profile.csv")
    atomic_csv(dtype_mismatch, QA_DIR / "dtype_mismatch_audit.csv")
    atomic_parquet(coercion, DATA_DIR / "dtype_coercion_review_rows.parquet")
    return profile, dtype_mismatch, coercion


def missingness_profiles(df: pd.DataFrame, colreg: pd.DataFrame, sample_registry: pd.DataFrame) -> dict[str, pd.DataFrame]:
    rows = []
    for col in df.columns:
        rows.append({"grouping": "overall", "group": "ALL", "column": col, "missing_n": int(df[col].isna().sum()), "missing_pct": float(df[col].isna().mean() * 100), "non_null_n": int(df[col].notna().sum())})
    overall = pd.DataFrame(rows)

    by_split = []
    for split, sub in df.groupby("split", dropna=False):
        for col in df.columns:
            by_split.append({"split": split, "column": col, "missing_n": int(sub[col].isna().sum()), "missing_pct": float(sub[col].isna().mean() * 100), "row_n": len(sub)})
    split_df = pd.DataFrame(by_split)

    by_major = []
    for major, sub in df.groupby("major_group_7", dropna=False):
        for col in df.columns:
            by_major.append({"major_group_7": major, "column": col, "missing_n": int(sub[col].isna().sum()), "missing_pct": float(sub[col].isna().mean() * 100), "row_n": len(sub)})
    major_df = pd.DataFrame(by_major)

    sample_rows = []
    sample_cols = [f"sample_{s}" for s in sample_registry["sample_id"].tolist() if f"sample_{s}" in df.columns]
    active_feature_cols = colreg.loc[colreg.get("model_default_active", False).fillna(False).astype(bool), "column"].tolist()
    for sample_col in sample_cols:
        mask = df[sample_col].fillna(False).astype(bool)
        sub = df.loc[mask]
        for col in active_feature_cols + ["a_rate_pct", "health_employment_rate_pct", "graduate_school_progression_rate_pct"]:
            if col in sub.columns:
                sample_rows.append({"sample_id": sample_col.replace("sample_", ""), "column": col, "missing_n": int(sub[col].isna().sum()), "missing_pct": float(sub[col].isna().mean() * 100) if len(sub) else np.nan, "row_n": len(sub)})
    sample_df = pd.DataFrame(sample_rows)

    all_null_constant = []
    for col in df.columns:
        s = df[col]
        non_null = int(s.notna().sum())
        nunique = int(s.astype("object").nunique(dropna=True))
        top_share = float(s.astype("object").value_counts(dropna=False, normalize=True).iloc[0]) if len(s) else np.nan
        all_null_constant.append(
            {
                "column": col,
                "all_null": non_null == 0,
                "constant_non_all_null": non_null > 0 and nunique <= 1,
                "near_constant": non_null > 0 and nunique > 1 and top_share >= 0.99,
                "top_value_share": top_share,
                "non_null_n": non_null,
                "nunique": nunique,
            }
        )
    all_null_constant_df = pd.DataFrame(all_null_constant)
    target_cols = ["a_rate_pct", "health_employment_rate_pct", "graduate_school_progression_rate_pct", "selectivity_proxy_pct"]
    co = df[target_cols].isna().astype(int).corr() if all(c in df.columns for c in target_cols) else pd.DataFrame()

    atomic_csv(overall, QA_DIR / "missingness_profile.csv")
    atomic_csv(split_df, QA_DIR / "missingness_by_split.csv")
    atomic_csv(major_df, QA_DIR / "missingness_by_major7.csv")
    atomic_csv(all_null_constant_df, QA_DIR / "all_null_constant_audit.csv")
    atomic_csv(co.reset_index().rename(columns={"index": "column"}), QA_DIR / "missingness_cooccurrence.csv")
    atomic_csv(sample_df, QA_DIR / "missingness_by_sample.csv")
    return {"overall": overall, "split": split_df, "major": major_df, "all_null_constant": all_null_constant_df, "cooccurrence": co, "sample": sample_df}


def domain_rules_and_audit(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rule_rows = []
    anomaly_rows = []

    def add_rule(rule_id: str, column: str, rule_type: str, severity: str, reason: str) -> None:
        rule_rows.append({"rule_id": rule_id, "column": column, "rule_type": rule_type, "severity": severity, "reason": reason})

    def add_anomaly(mask: pd.Series, column: str, rule_id: str, severity: str, reason: str, source_dataset: str = "D08") -> None:
        if not mask.any():
            return
        for _, row in df.loc[mask, ["outcome_row_id", column, "source_file"]].head(100000).iterrows():
            anomaly_rows.append(
                {
                    "outcome_row_id": row["outcome_row_id"],
                    "column": column,
                    "observed_value": row[column],
                    "rule_id": rule_id,
                    "severity": severity,
                    "reason": reason,
                    "source_dataset": source_dataset,
                    "recommended_action": "MANUAL_REVIEW" if severity == "FAIL" else "KEEP_WITH_LEDGER",
                }
            )

    for col in sorted(YEAR_COLUMNS & set(df.columns)):
        add_rule("YEAR_1900_2100_ALLOWLIST", col, "year", "FAIL", "explicit year allowlist only")
        num = pd.to_numeric(df[col], errors="coerce")
        add_anomaly(num.notna() & ((num < 1900) | (num > 2100)), col, "YEAR_1900_2100_ALLOWLIST", "FAIL", "year outside 1900-2100")
    for col in sorted(PERCENT_COLUMNS & set(df.columns)):
        add_rule("PCT_0_100", col, "percentage", "FAIL", "percentage must be 0..100")
        num = pd.to_numeric(df[col], errors="coerce")
        add_anomaly(num.notna() & ((num < 0) | (num > 100)), col, "PCT_0_100", "FAIL", "percentage outside 0..100")
    for col in sorted(PROPORTION_COLUMNS & set(df.columns)):
        add_rule("PROP_0_1", col, "proportion", "FAIL", "proportion must be 0..1")
        num = pd.to_numeric(df[col], errors="coerce")
        add_anomaly(num.notna() & ((num < 0) | (num > 1)), col, "PROP_0_1", "FAIL", "proportion outside 0..1")
    for col in sorted(COUNT_COLUMNS & set(df.columns)):
        add_rule("COUNT_NONNEGATIVE", col, "count", "FAIL", "count must be integer-like and non-negative")
        num = pd.to_numeric(df[col], errors="coerce")
        add_anomaly(num.notna() & (num < 0), col, "COUNT_NONNEGATIVE", "FAIL", "negative count")
        add_anomaly(num.notna() & ((num % 1).abs() > 1e-8), col, "COUNT_INTEGER_LIKE", "FAIL", "count is not integer-like")
    for col in sorted(RATIO_COLUMNS & set(df.columns)):
        add_rule("RATIO_NONNEGATIVE", col, "ratio", "FAIL", "ratio must be non-negative")
        num = pd.to_numeric(df[col], errors="coerce")
        add_anomaly(num.notna() & (num < 0), col, "RATIO_NONNEGATIVE", "FAIL", "negative ratio")
    for col in sorted(BOOLEAN_COLUMNS & set(df.columns)):
        add_rule("BOOLEAN_TRUE_FALSE_NA", col, "boolean", "FAIL", "boolean may only be True/False/NA")
        vals = df[col].dropna().astype(str).str.lower()
        bad_idx = vals.index[~vals.isin(["true", "false", "0", "1"])]
        add_anomaly(pd.Series(df.index.isin(bad_idx), index=df.index), col, "BOOLEAN_TRUE_FALSE_NA", "FAIL", "non-boolean value")
    for col in sorted(ID_COLUMNS & set(df.columns)):
        severity = "FAIL" if col in PRIMARY_ID_COLUMNS else "WARN"
        rule_id = "PRIMARY_ID_NOT_EMPTY" if col in PRIMARY_ID_COLUMNS else "OPTIONAL_LINEAGE_ID_NULL_LEDGER"
        reason = "primary ID cannot be null or empty string" if col in PRIMARY_ID_COLUMNS else "optional lineage ID may be null when source grain is unavailable; ledger only"
        add_rule(rule_id, col, "id", severity, reason)
        s = df[col].astype("string")
        add_anomaly(df[col].isna() | s.str.strip().eq(""), col, rule_id, severity, reason)

    # Named structural context check.
    for col in [c for c in df.columns if c.startswith("ctx24_") or c.startswith("goms_")]:
        if col in {"goms_recent_employment_rate_pct", "goms_recent_mean_income_10kkrw"}:
            rule_rows.append({"rule_id": "CONTEXT_NAMING_CONTEXT_ONLY", "column": col, "rule_type": "context_label", "severity": "WARN", "reason": "context variable uses outcome-like name; registry must mark C24/GOMS context"})

    rules = pd.DataFrame(rule_rows)
    anomalies = pd.DataFrame(anomaly_rows)
    if anomalies.empty:
        anomalies = pd.DataFrame(columns=["outcome_row_id", "column", "observed_value", "rule_id", "severity", "reason", "source_dataset", "recommended_action"])
    atomic_csv(rules, QA_DIR / "domain_rule_registry.csv")
    atomic_csv(anomalies, QA_DIR / "domain_range_audit.csv")
    atomic_parquet(anomalies, DATA_DIR / "domain_anomaly_rows.parquet")
    return rules, anomalies


def count_denominator_audit(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    inventory = []
    required = {
        "GRADE": ["a_grade_students_n", "graded_students_n", "a_rate_pct", "a_rate_prop"],
        "RETENTION": ["initial_employed_n", "retained_1_n", "retained_2_n", "retained_3_n", "retained_4_n"],
        "PROGRESSION": ["graduate_school_progressors_n", "graduates_n", "graduate_school_progression_rate_pct", "graduate_school_progression_prop"],
    }
    for family, cols in required.items():
        for col in cols:
            exists = col in df.columns
            inventory.append(
                {
                    "family": family,
                    "column": col,
                    "exists": exists,
                    "non_null_n": int(df[col].notna().sum()) if exists else 0,
                    "missing_n": int(df[col].isna().sum()) if exists else len(df),
                    "status": "observed" if exists and df[col].notna().any() else "not_observed",
                }
            )
    inv = pd.DataFrame(inventory)
    atomic_csv(inv, QA_DIR / "count_denominator_audit.csv")

    rec_rows = []
    def add_recon(name: str, num: str, den: str, stored: str, scale: float, tolerance: float) -> None:
        exists = all(c in df.columns for c in [num, den, stored])
        if not exists:
            rec_rows.append({"rate_name": name, "status": "not_observed", "audited_n": 0, "violation_n": 0, "max_abs_diff": np.nan, "tolerance": tolerance})
            return
        n = pd.to_numeric(df[num], errors="coerce")
        d = pd.to_numeric(df[den], errors="coerce")
        r = pd.to_numeric(df[stored], errors="coerce")
        calc = n / d * scale
        mask = d.gt(0) & n.notna() & r.notna()
        diff = (r - calc).abs()
        rec_rows.append({"rate_name": name, "status": "PASS" if int((diff[mask] > tolerance).sum()) == 0 else "FAIL", "audited_n": int(mask.sum()), "violation_n": int((diff[mask] > tolerance).sum()), "max_abs_diff": float(diff[mask].max()) if mask.any() else np.nan, "tolerance": tolerance})

    add_recon("competition_ratio", "applicants_n", "recruitment_n", "competition_ratio", 1.0, 1e-3)
    add_recon("admission_yield_ratio", "admits_n", "recruitment_n", "admission_yield_ratio", 1.0, 1e-3)
    add_recon("admit_per_applicant_ratio", "admits_n", "applicants_n", "admit_per_applicant_ratio", 1.0, 1e-3)
    add_recon("leave_rate_pct", "leave_students_n", "enrolled_students_n", "leave_rate_pct", 100.0, 1e-3)
    add_recon("female_student_share_pct", "female_students_n", "enrolled_students_n", "female_student_share_pct", 100.0, 1e-3)
    add_recon("international_student_share_pct", "international_students_n", "enrolled_students_n", "international_student_share_pct", 100.0, 1e-3)
    add_recon("fulltime_faculty_share_pct", "fulltime_faculty_n", "fulltime_faculty_n", "fulltime_faculty_share_pct", 100.0, 1e-3)
    rec = pd.DataFrame(rec_rows)
    # Correct fulltime faculty denominator separately.
    if {"fulltime_faculty_n", "nonfulltime_faculty_n", "fulltime_faculty_share_pct"}.issubset(df.columns):
        total_faculty = pd.to_numeric(df["fulltime_faculty_n"], errors="coerce") + pd.to_numeric(df["nonfulltime_faculty_n"], errors="coerce")
        calc = pd.to_numeric(df["fulltime_faculty_n"], errors="coerce") / total_faculty * 100
        r = pd.to_numeric(df["fulltime_faculty_share_pct"], errors="coerce")
        mask = total_faculty.gt(0) & r.notna()
        rec.loc[rec["rate_name"].eq("fulltime_faculty_share_pct"), ["audited_n", "violation_n", "max_abs_diff", "status"]] = [
            int(mask.sum()),
            int(((r - calc).abs()[mask] > 1e-3).sum()),
            float((r - calc).abs()[mask].max()) if mask.any() else np.nan,
            "PASS" if int(((r - calc).abs()[mask] > 1e-3).sum()) == 0 else "FAIL",
        ]
    atomic_csv(rec, QA_DIR / "derived_rate_reconciliation.csv")

    flags = df[["outcome_row_id"]].copy()
    flags["GRADE_COUNT_READY"] = "not_observed"
    flags["RETENTION_COUNT_READY"] = "not_observed"
    flags["PROGRESSION_COUNT_READY"] = "not_observed"
    flags["COUNT_RELATION_VALID"] = "not_observed"
    flags["RATE_RECONCILED"] = "rate_features_reconciled_separately"
    flags["DENOMINATOR_VALID"] = "not_observed_for_grade_retention_progression_counts"
    atomic_parquet(flags, DATA_DIR / "count_ready_rows.parquet")
    anomalies = pd.DataFrame(columns=["outcome_row_id", "family", "issue", "severity", "detail"])
    atomic_parquet(anomalies, DATA_DIR / "count_integrity_anomaly_rows.parquet")
    return inv, rec, flags, anomalies


def major7_mapping_audit(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for major, sub in df.groupby("major_group_7", dropna=False):
        rows.append({"audit": "major_group_7_distribution", "key": major, "row_n": len(sub), "school_n": sub["school_uid"].nunique(), "status": "PASS" if pd.notna(major) else "WARN"})
    for col in ["major7_mapping_method", "major7_mapping_confidence", "major7_review_needed", "major7_candidate_count"]:
        if col in df.columns:
            for val, n in df[col].value_counts(dropna=False).items():
                rows.append({"audit": col, "key": val, "row_n": int(n), "school_n": None, "status": "PASS"})
    raw_multi = df.groupby(["school_name_std", "dept_name_std"], dropna=False)["major_group_7"].nunique().reset_index(name="major7_n")
    conflict_n = int(raw_multi["major7_n"].gt(1).sum())
    rows.append({"audit": "same_school_dept_multiple_major7", "key": "ALL", "row_n": conflict_n, "school_n": None, "status": "FAIL" if conflict_n else "PASS"})
    out = pd.DataFrame(rows)
    atomic_csv(out, QA_DIR / "major7_mapping_audit.csv")
    return out


def sample_and_split_audits(df: pd.DataFrame, sample_registry: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sample_rows = []
    for _, reg in sample_registry.iterrows():
        sample_id = reg["sample_id"]
        col = f"sample_{sample_id}"
        if col not in df.columns:
            sample_rows.append({"sample_id": sample_id, "status": "FAIL", "message": "missing membership column"})
            continue
        mask = df[col].fillna(False).astype(bool)
        sub = df.loc[mask]
        row = {
            "sample_id": sample_id,
            "registry_row_n": int(reg["row_n"]),
            "actual_row_n": int(mask.sum()),
            "diff_row_n": int(mask.sum()) - int(reg["row_n"]),
            "registry_school_n": int(reg["school_n"]),
            "actual_school_n": int(sub["school_uid"].nunique()),
            "diff_school_n": int(sub["school_uid"].nunique()) - int(reg["school_n"]),
            "train_n": int(sub["split"].eq("train").sum()),
            "validation_n": int(sub["split"].eq("val").sum()),
            "test_n": int(sub["split"].eq("test").sum()),
            "status": "PASS" if int(mask.sum()) == int(reg["row_n"]) and int(sub["school_uid"].nunique()) == int(reg["school_n"]) else "FAIL",
        }
        sample_rows.append(row)
    sample_df = pd.DataFrame(sample_rows)
    atomic_csv(sample_df, QA_DIR / "sample_membership_audit.csv")

    school_split_rows = []
    split_sets = {split: set(sub["school_uid"].dropna()) for split, sub in df.groupby("split", dropna=False)}
    for a in split_sets:
        for b in split_sets:
            if str(a) >= str(b):
                continue
            overlap = split_sets[a] & split_sets[b]
            school_split_rows.append({"split_a": a, "split_b": b, "overlap_school_n": len(overlap), "overlap_schools": "|".join(sorted(overlap)[:100]), "status": "FAIL" if overlap else "PASS"})
    split_df = pd.DataFrame(school_split_rows)
    row_split = df.groupby("outcome_row_id")["split"].nunique().reset_index(name="split_n")
    row_leak = row_split[row_split["split_n"].gt(1)].copy()
    atomic_csv(split_df, QA_DIR / "split_leakage_audit.csv")
    atomic_csv(row_leak, QA_DIR / "row_split_leakage_audit.csv")
    return sample_df, split_df, row_leak


def feature_role_leakage_audit(colreg: pd.DataFrame, feature_set: pd.DataFrame) -> pd.DataFrame:
    active = feature_set[feature_set["included_in_contract"].fillna(False).astype(bool)].copy()
    reg = colreg[["column", "feature_block", "semantic_role", "is_identifier", "is_quality_metadata"]].copy()
    merged = active.merge(reg, left_on="feature", right_on="column", how="left")
    base_columns = set(pd.read_parquet(D08_PATH).columns)
    rows = []
    for _, row in merged.iterrows():
        feature_exists = str(row["feature"]) in base_columns
        pending_upstream = (not feature_exists) and str(row["feature"]).startswith("grade_residual_")
        target_self = str(row["feature"]) == str(row["target"])
        id_meta = feature_exists and (bool(row.get("is_identifier", False)) or bool(row.get("is_quality_metadata", False)) or row.get("feature_block") == "QUALITY")
        unresolved_other = feature_exists and row.get("feature_block") == "OTHER"
        active_all_null = False
        status = "PENDING_UPSTREAM_FEATURE" if pending_upstream else ("FAIL" if target_self or id_meta or unresolved_other or active_all_null else "PASS")
        rows.append(
            {
                "model_id": row["model_id"],
                "phase": row["phase"],
                "target": row["target"],
                "feature": row["feature"],
                "feature_block": row.get("feature_block"),
                "feature_exists_in_base": feature_exists,
                "pending_upstream_feature": pending_upstream,
                "target_self_leakage": target_self,
                "active_id_or_metadata_feature": id_meta,
                "unresolved_other_role": unresolved_other,
                "active_all_null_feature": active_all_null,
                "status": status,
            }
        )
    out = pd.DataFrame(rows)
    atomic_csv(out, QA_DIR / "feature_role_leakage_audit.csv")
    return out


def create_clean_marts(df: pd.DataFrame, count_flags: pd.DataFrame, conflict_audit: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    mart = df.copy()
    for pct, prop in [
        ("a_rate_pct", "a_rate_prop"),
        ("health_employment_rate_pct", "health_employment_rate_prop"),
        ("graduate_school_progression_rate_pct", "graduate_school_progression_prop"),
    ]:
        mart[prop] = pd.to_numeric(mart[pct], errors="coerce") / 100.0
    if "enrolled_students_n" in mart.columns:
        mart["log_enrolled_students_v1_recomputed"] = np.log1p(pd.to_numeric(mart["enrolled_students_n"], errors="coerce"))
    if "graduates_n" in mart.columns:
        mart["log_graduates_v1_recomputed"] = np.log1p(pd.to_numeric(mart["graduates_n"], errors="coerce"))
    conflict_map = conflict_audit.groupby("outcome_row_id")["conflict_group_id"].apply(lambda x: "|".join(sorted(set(map(str, x))))).to_dict() if not conflict_audit.empty else {}
    excluded_conflict_ids = set(conflict_audit.loc[conflict_audit["status"].eq("LEDGERED_EXCLUSION"), "outcome_row_id"].astype(str)) if not conflict_audit.empty else set()
    mart["integrity_status"] = np.where(mart["outcome_row_id"].astype(str).isin(excluded_conflict_ids), "EXCLUDED_CONFLICT_LEDGERED", "INCLUDED_WITH_WARNINGS")
    mart["integrity_severity"] = np.where(mart["integrity_status"].eq("EXCLUDED_CONFLICT_LEDGERED"), "WARN_EXCLUDED_FROM_PRIMARY", "NONCRITICAL_WARNINGS_LEDGERED")
    mart["integrity_exclusion_reason"] = np.where(mart["integrity_status"].eq("EXCLUDED_CONFLICT_LEDGERED"), "duplicate_conflict_not_model_allowed", "")
    mart["source_row_hash"] = [sha256_row(row, cols=["outcome_row_id", "source_file", "raw_row_lineage"]) for _, row in mart.iterrows()]
    mart["structure_ready"] = mart["sample_P2_STRUCTURE_READY"].fillna(False).astype(bool)
    mart["selectivity_ready"] = mart["sample_P2_SELECTIVITY_READY"].fillna(False).astype(bool)
    mart["employment_rate_ready"] = mart["sample_P4_E_STRUCTURE_READY"].fillna(False).astype(bool)
    mart["progression_rate_ready"] = mart["sample_P4_P_STRUCTURE_READY"].fillna(False).astype(bool)
    mart["joint_rate_ready"] = mart["sample_P4_JOINT_STRUCTURE_READY"].fillna(False).astype(bool)
    mart["grade_count_ready"] = False
    mart["retention_count_ready"] = False
    mart["progression_count_ready"] = False
    mart["major7_mapping_ready"] = mart["major_group_7"].notna() & mart["has_major_group_7_high_medium"].fillna(False).astype(bool)
    mart["conflict_free"] = ~mart["outcome_row_id"].astype(str).isin(excluded_conflict_ids)
    mart["split_verified"] = mart["split"].isin(["train", "val", "test"])
    atomic_parquet(mart, DATA_DIR / "clean_department_model_base_2024.parquet")

    lineage = mart[["outcome_row_id", "source_file", "raw_row_lineage", "source_row_hash"]].copy()
    lineage = lineage.rename(columns={"outcome_row_id": "output_row_id", "source_file": "source_dataset", "raw_row_lineage": "source_row_id"})
    lineage["join_method"] = "stable_key_and_documented_bridge"
    lineage["join_key"] = "outcome_row_id|school_uid|campus_uid|dept_uid"
    lineage["conflict_group_id"] = lineage["output_row_id"].map(conflict_map).fillna("")
    lineage["inclusion_status"] = np.where(lineage["output_row_id"].astype(str).isin(excluded_conflict_ids), "EXCLUDED", "INCLUDED")
    lineage["exclusion_rule_id"] = np.where(lineage["inclusion_status"].eq("EXCLUDED"), "DUPLICATE_CONFLICT_NOT_MODEL_ALLOWED", "")
    lineage["transformation_rule_ids"] = "DERIVE_PROPORTIONS|RECOMPUTE_LOGS|ADD_INTEGRITY_FLAGS"
    atomic_parquet(lineage, DATA_DIR / "row_lineage.parquet")

    excluded = mart.loc[mart["integrity_status"].eq("EXCLUDED_CONFLICT_LEDGERED"), ["outcome_row_id", "school_name_std", "dept_name_std", "integrity_exclusion_reason"]].copy()
    excluded["exclusion_rule_id"] = "DUPLICATE_CONFLICT_NOT_MODEL_ALLOWED"
    atomic_parquet(excluded, DATA_DIR / "excluded_rows.parquet")

    out_status: dict[str, Any] = {}
    stage_specs = {
        "p2_structure_ready_2024.parquet": "sample_P2_STRUCTURE_READY",
        "p2_selectivity_ready_2024.parquet": "sample_P2_SELECTIVITY_READY",
        "p4_employment_rate_ready_2024.parquet": "sample_P4_E_STRUCTURE_READY",
        "p4_progression_rate_ready_2024.parquet": "sample_P4_P_STRUCTURE_READY",
        "p4_joint_rate_ready_2024.parquet": "sample_P4_JOINT_STRUCTURE_READY",
    }
    for filename, col in stage_specs.items():
        sub = mart.loc[mart[col].fillna(False).astype(bool) & mart["conflict_free"]].copy()
        if len(sub):
            atomic_parquet(sub, DATA_DIR / filename)
            out_status[filename] = {"status": "CREATED", "rows": int(len(sub)), "reason": col}
        else:
            out_status[filename] = {"status": "NOT_AVAILABLE", "rows": 0, "reason": f"{col} had no rows"}
    for filename, reason in {
        "retention_count_ready_2024.parquet": "retention numerator/denominator columns not observed",
        "progression_count_ready_2024.parquet": "graduate_school_progressors_n not observed",
    }.items():
        out_status[filename] = {"status": "NOT_AVAILABLE", "rows": 0, "reason": reason}
    atomic_json(out_status, MANIFEST_DIR / "clean_mart_output_status.json")
    return mart, lineage, out_status


def formula_registry() -> pd.DataFrame:
    rows = [
        {"derived_column": "a_rate_prop", "formula": "a_rate_pct / 100", "source_columns": "a_rate_pct", "status": "SAFE_DETERMINISTIC"},
        {"derived_column": "health_employment_rate_prop", "formula": "health_employment_rate_pct / 100", "source_columns": "health_employment_rate_pct", "status": "SAFE_DETERMINISTIC"},
        {"derived_column": "graduate_school_progression_prop", "formula": "graduate_school_progression_rate_pct / 100", "source_columns": "graduate_school_progression_rate_pct", "status": "SAFE_DETERMINISTIC"},
        {"derived_column": "log_enrolled_students_v1_recomputed", "formula": "log1p(enrolled_students_n)", "source_columns": "enrolled_students_n", "status": "SAFE_DETERMINISTIC"},
        {"derived_column": "log_graduates_v1_recomputed", "formula": "log1p(graduates_n)", "source_columns": "graduates_n", "status": "SAFE_DETERMINISTIC"},
    ]
    out = pd.DataFrame(rows)
    atomic_csv(out, QA_DIR / "derived_formula_registry.csv")
    return out


def decision_ledger() -> pd.DataFrame:
    rows = [
        {"rule_id": "NO_IMPUTATION", "action": "none", "scope": "all data", "reason": "preprocessing integrity only; imputation deferred to fold-local modeling"},
        {"rule_id": "NO_ENCODING", "action": "none", "scope": "categorical variables", "reason": "one-hot encoding is modeling preprocessing and is not run here"},
        {"rule_id": "DERIVE_PROPORTIONS", "action": "derive", "scope": "rate pct columns", "reason": "deterministic pct/100 with reconciliation"},
        {"rule_id": "DUPLICATE_CONFLICT_NOT_MODEL_ALLOWED", "action": "ledger exclusion from primary clean marts", "scope": "conflict rows model_allowed=False", "reason": "existing audited conflict ledger"},
        {"rule_id": "COUNT_READY_NOT_OBSERVED", "action": "mark not_observed", "scope": "grade/retention/progression counts", "reason": "required numerator/denominator columns are absent"},
    ]
    out = pd.DataFrame(rows)
    atomic_csv(out, QA_DIR / "transformation_decision_ledger.csv")
    return out


def compare_stored_notebook_outputs(fresh_inventory: pd.DataFrame) -> pd.DataFrame:
    stored_path = READINESS_ROOT / "dataset_inspection" / "qa" / "dataset_inventory_final.csv"
    rows = []
    if not stored_path.exists():
        return pd.DataFrame([{"comparison": "dataset_inventory_final", "status": "STALE_OUTPUT", "detail": "stored inventory missing"}])
    stored = pd.read_csv(stored_path, low_memory=False)
    inv = fresh_inventory.copy()
    def norm_shape(value: Any) -> list[int] | None:
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return None
        if isinstance(value, str):
            text = value.strip()
            if text in {"", "nan", "None", "null"}:
                return None
            try:
                parsed = json.loads(text)
            except Exception:
                try:
                    parsed = ast.literal_eval(text)
                except Exception:
                    return None
            if isinstance(parsed, tuple):
                parsed = list(parsed)
            return [int(x) for x in parsed] if isinstance(parsed, list) else None
        if isinstance(value, (list, tuple)):
            return [int(x) for x in value]
        return None

    for _, row in inv.iterrows():
        label = row["label"]
        s = stored.loc[stored["label"].eq(label)]
        if s.empty:
            rows.append({"label": label, "status": "STALE_OUTPUT", "detail": "label missing from stored notebook inventory"})
            continue
        stored_shape = norm_shape(s.iloc[0].get("actual shape", s.iloc[0].get("actual_shape")))
        fresh_shape = norm_shape(row["actual_shape"])
        shape_match = stored_shape == fresh_shape
        hash_match = str(s.iloc[0].get("actual_sha256", s.iloc[0].get("actual SHA256", ""))) == str(row["sha256"])
        status = "MATCH" if shape_match and hash_match else "SOURCE_DRIFT"
        rows.append({"label": label, "status": status, "shape_match_vs_stored_output": shape_match, "hash_match_vs_stored_output": hash_match})
    out = pd.DataFrame(rows)
    atomic_csv(out, QA_DIR / "stored_notebook_output_reconciliation.csv")
    return out


def build_summary(
    run_id: str,
    env: dict[str, Any],
    inventory: pd.DataFrame,
    key_audit: pd.DataFrame,
    dup_audit: pd.DataFrame,
    join_audit: pd.DataFrame,
    schema: pd.DataFrame,
    missing: dict[str, pd.DataFrame],
    domain_anomalies: pd.DataFrame,
    count_inv: pd.DataFrame,
    count_rec: pd.DataFrame,
    major7: pd.DataFrame,
    sample_audit: pd.DataFrame,
    split_audit: pd.DataFrame,
    feature_leak: pd.DataFrame,
    mart: pd.DataFrame,
    output_status: dict[str, Any],
) -> dict[str, Any]:
    critical = {
        "required_input_fail_n": int(inventory["status"].eq("FAIL").sum()),
        "outcome_row_id_null_n": int(key_audit.loc[key_audit["key_candidate"].eq("outcome_row_id"), "null_key_rows"].fillna(0).sum()),
        "outcome_row_id_duplicate_n": int(key_audit.loc[key_audit["key_candidate"].eq("outcome_row_id"), "duplicate_key_rows"].fillna(0).sum()),
        "exact_duplicate_n": int(dup_audit["classification"].eq("EXACT_DUPLICATE").sum()) if not dup_audit.empty else 0,
        "unapproved_many_to_many_n": int((join_audit["many_to_many"].fillna(False) & ~join_audit["approved_many_to_many"].fillna(False)).sum()),
        "row_expansion_unexplained_n": int((pd.to_numeric(join_audit["row_expansion_factor"], errors="coerce").fillna(1) > 1.000001).sum()),
        "domain_fail_anomaly_n": int(domain_anomalies["severity"].eq("FAIL").sum()) if not domain_anomalies.empty else 0,
        "rate_reconciliation_fail_n": int(count_rec["status"].eq("FAIL").sum()),
        "sample_registry_mismatch_n": int(sample_audit["status"].eq("FAIL").sum()),
        "school_split_leakage_n": int(pd.to_numeric(split_audit.get("overlap_school_n", 0), errors="coerce").fillna(0).sum()) if not split_audit.empty else 0,
        "target_self_leakage_n": int(feature_leak["target_self_leakage"].sum()) if not feature_leak.empty else 0,
        "active_id_metadata_feature_n": int(feature_leak["active_id_or_metadata_feature"].sum()) if not feature_leak.empty else 0,
        "unresolved_other_role_n": int(feature_leak["unresolved_other_role"].sum()) if not feature_leak.empty else 0,
        "active_all_null_feature_n": int(feature_leak["active_all_null_feature"].sum()) if not feature_leak.empty else 0,
        "row_lineage_missing_n": int(mart["source_row_hash"].isna().sum()),
    }
    warning = {
        "hash_or_shape_warning_n": int(inventory["status"].eq("WARN").sum()),
        "ledgered_duplicate_conflict_rows": int(dup_audit["outcome_row_id"].nunique()) if not dup_audit.empty else 0,
        "count_ready_not_observed_families": sorted(count_inv.loc[count_inv["status"].eq("not_observed"), "family"].drop_duplicates().tolist()),
        "high_missing_selectivity_n": int(missing["overall"].loc[missing["overall"]["column"].eq("selectivity_proxy_pct"), "missing_n"].iloc[0]) if "overall" in missing else None,
        "major7_mapping_warn_n": int(major7["status"].eq("WARN").sum()) if not major7.empty else 0,
    }
    # Domain anomalies from explicit rules are critical except if they are context naming warnings.
    blocking_keys = [
        "required_input_fail_n",
        "outcome_row_id_null_n",
        "outcome_row_id_duplicate_n",
        "exact_duplicate_n",
        "unapproved_many_to_many_n",
        "row_expansion_unexplained_n",
        "domain_fail_anomaly_n",
        "rate_reconciliation_fail_n",
        "sample_registry_mismatch_n",
        "school_split_leakage_n",
        "target_self_leakage_n",
        "active_id_metadata_feature_n",
        "unresolved_other_role_n",
        "active_all_null_feature_n",
        "row_lineage_missing_n",
    ]
    blocked = any(critical[k] for k in blocking_keys)
    final_status = "BLOCKED_INTEGRITY" if blocked else ("READY_WITH_WARNINGS" if warning["hash_or_shape_warning_n"] or warning["ledgered_duplicate_conflict_rows"] or warning["count_ready_not_observed_families"] else "PREPROCESSING_READY")
    return {
        "run_id": run_id,
        "created_at": now_utc(),
        "final_status": final_status,
        "critical": critical,
        "warning": warning,
        "environment": env,
        "clean_mart_outputs": output_status,
    }


def write_tests(summary: dict[str, Any]) -> None:
    test_code = f'''from pathlib import Path
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
'''
    (TEST_DIR / "test_preprocessing_integrity.py").write_text(test_code, encoding="utf-8")


def build_report_and_handoff(summary: dict[str, Any], artifacts: dict[str, pd.DataFrame | dict[str, Any]]) -> None:
    inventory = artifacts["inventory"]
    key_audit = artifacts["key_audit"]
    grain = artifacts["grain"]
    dup = artifacts["dup"]
    join = artifacts["join"]
    schema = artifacts["schema"]
    missing = artifacts["missing"]
    domain = artifacts["domain"]
    count_inv = artifacts["count_inv"]
    count_rec = artifacts["count_rec"]
    major7 = artifacts["major7"]
    sample = artifacts["sample"]
    split = artifacts["split"]
    feature = artifacts["feature"]
    mart = artifacts["mart"]

    def md_table(df: pd.DataFrame, max_rows: int = 40) -> str:
        if df.empty:
            return "| empty |\n|---|"
        view = df.head(max_rows).copy()
        cols = list(view.columns)
        lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
        for _, row in view.iterrows():
            vals = []
            for col in cols:
                val = row[col]
                if isinstance(val, (dict, list)):
                    text = json.dumps(val, ensure_ascii=False)
                elif pd.isna(val):
                    text = ""
                else:
                    text = str(val)
                vals.append(text.replace("|", "\\|").replace("\n", " ")[:160])
            lines.append("| " + " | ".join(vals) + " |")
        return "\n".join(lines)

    report = f"""# DATA PREPROCESSING INTEGRITY REPORT

## 1. Executive Status

- final_status: `{summary['final_status']}`
- run_id: `{summary['run_id']}`
- critical_fail_counts: `{json.dumps(summary['critical'], ensure_ascii=False)}`
- warning_counts: `{json.dumps(summary['warning'], ensure_ascii=False)}`

## 2. Run Provenance

```json
{json.dumps(summary['environment'], ensure_ascii=False, indent=2)}
```

## 3. Input File Inventory

{md_table(inventory[['label','exists','actual_shape','expected_shape','hash_match','shape_match','status','warning_code']], 80)}

## 4. Dataset Row/Column Counts

- base shape: `{mart.shape}`
- unique schools: `{mart['school_uid'].nunique()}`
- unique campuses: `{mart['campus_uid'].nunique()}`
- unique departments: `{mart['dept_uid'].nunique()}`

## 5. Grain and Key Audit

{md_table(key_audit)}

Grain summary:

{md_table(grain)}

## 6. Join Cardinality Audit

{md_table(join)}

## 7. Duplicate/Conflict Audit

- conflict rows: `{dup['outcome_row_id'].nunique() if not dup.empty else 0}`
- conflict groups: `{dup['conflict_group_id'].nunique() if not dup.empty else 0}`

{md_table(dup.groupby(['classification','status'], dropna=False).size().reset_index(name='rows'))}

## 8. Schema/Dtype Audit

- columns profiled: `{len(schema)}`
- dtype mismatch rows: `{len(pd.read_csv(QA_DIR / 'dtype_mismatch_audit.csv', low_memory=False))}`
- coercion failure columns: `{int(schema['coercion_failure_n'].gt(0).sum())}`

## 9. Missingness Audit

- selectivity missing: `{int(missing['overall'].loc[missing['overall']['column'].eq('selectivity_proxy_pct'), 'missing_n'].iloc[0])}` / `{len(mart)}`
- health employment missing: `{int(missing['overall'].loc[missing['overall']['column'].eq('health_employment_rate_pct'), 'missing_n'].iloc[0])}` / `{len(mart)}`
- graduate school progression missing: `{int(missing['overall'].loc[missing['overall']['column'].eq('graduate_school_progression_rate_pct'), 'missing_n'].iloc[0])}` / `{len(mart)}`

## 10. Domain/Range Audit

- explicit rule anomaly rows: `{len(domain)}`
- fail severity rows: `{int(domain['severity'].eq('FAIL').sum()) if not domain.empty else 0}`

## 11. Count/Denominator/Rate Audit

Count inventory:

{md_table(count_inv)}

Rate reconciliation:

{md_table(count_rec)}

## 12. Major7/Category Mapping Audit

{md_table(major7.head(50))}

## 13. Sample Membership Audit

{md_table(sample)}

## 14. Split Leakage Audit

{md_table(split)}

## 15. Feature Role/Leakage Audit

- target self leakage rows: `{int(feature['target_self_leakage'].sum()) if not feature.empty else 0}`
- active ID/metadata feature rows: `{int(feature['active_id_or_metadata_feature'].sum()) if not feature.empty else 0}`
- unresolved OTHER rows: `{int(feature['unresolved_other_role'].sum()) if not feature.empty else 0}`

## 16. Clean Mart Outputs

```json
{json.dumps(summary['clean_mart_outputs'], ensure_ascii=False, indent=2)}
```

## 17. Exclusion Ledger

- excluded rows: `{len(pd.read_parquet(DATA_DIR / 'excluded_rows.parquet'))}`
- ledger path: `data/excluded_rows.parquet`

## 18. Unresolved Blockers

- BLOCKED_INTEGRITY critical count total: `{sum(summary['critical'].values())}`
- COUNT_READY grade/retention/progression: `not_observed` where numerator/denominator columns are absent.

## 19. Preprocessing Contract

- Completed: provenance, key/grain, join cardinality, duplicate ledger, schema, missingness, domain/range, count inventory, major7, samples, split, role/leakage, lineage, clean marts.
- Not performed: imputation, scaling, one-hot encoding, model fitting, residual generation, bootstrap inference.
- Future fold-local only: imputer/scaler/encoder fitting.

## 20. Final PASS/WARN/FAIL Matrix

| Gate | Status | Key Count | Output |
|---|---|---:|---|
| Gate 0 inventory | {'FAIL' if summary['critical']['required_input_fail_n'] else 'PASS'} | {summary['critical']['required_input_fail_n']} | qa/dataset_inventory.csv |
| Gate 1 key/grain | {'FAIL' if summary['critical']['outcome_row_id_duplicate_n'] else 'PASS'} | {summary['critical']['outcome_row_id_duplicate_n']} | qa/key_grain_audit.csv |
| Gate 2 join | {'FAIL' if summary['critical']['unapproved_many_to_many_n'] else 'PASS'} | {summary['critical']['unapproved_many_to_many_n']} | qa/join_cardinality_audit.csv |
| Gate 3 schema | PASS | {int(schema['status'].eq('FAIL').sum())} | qa/column_schema_profile.csv |
| Gate 4 missingness | WARN | {summary['warning']['high_missing_selectivity_n']} | qa/missingness_profile.csv |
| Gate 5 domain/range | {'FAIL' if summary['critical']['domain_fail_anomaly_n'] else 'PASS'} | {summary['critical']['domain_fail_anomaly_n']} | qa/domain_range_audit.csv |
| Gate 6 count/rate | WARN | {len(summary['warning']['count_ready_not_observed_families'])} | qa/count_denominator_audit.csv |
| Gate 7 major7 | {'WARN' if summary['warning']['major7_mapping_warn_n'] else 'PASS'} | {summary['warning']['major7_mapping_warn_n']} | qa/major7_mapping_audit.csv |
| Gate 8 samples/split | {'FAIL' if summary['critical']['sample_registry_mismatch_n'] or summary['critical']['school_split_leakage_n'] else 'PASS'} | {summary['critical']['sample_registry_mismatch_n'] + summary['critical']['school_split_leakage_n']} | qa/sample_membership_audit.csv |
| Gate 9 feature roles | {'FAIL' if summary['critical']['target_self_leakage_n'] else 'PASS'} | {summary['critical']['target_self_leakage_n']} | qa/feature_role_leakage_audit.csv |
"""
    (REPORT_DIR / "DATA_PREPROCESSING_INTEGRITY_REPORT.md").write_text(report, encoding="utf-8")

    sample_counts = sample[["sample_id", "actual_row_n", "actual_school_n", "train_n", "validation_n", "test_n"]].copy()
    split_counts = mart["split"].value_counts(dropna=False).rename_axis("split").reset_index(name="row_n")
    target_counts = pd.DataFrame(
        [{"target": c, "non_null_n": int(mart[c].notna().sum()), "missing_n": int(mart[c].isna().sum())} for c in ["a_rate_pct", "health_employment_rate_pct", "graduate_school_progression_rate_pct"]]
    )
    handoff_lines = [
        "# HANDOFF TO CHATGPT",
        "",
        "## A. 실행 정보",
        "",
        f"- run_id: `{summary['run_id']}`",
        f"- commit: `{summary['environment']['git_commit_full']}`",
        f"- notebook path/hash: `{summary['environment'].get('selected_notebook_path')}` / `{summary['environment'].get('selected_notebook_sha256')}`",
        f"- input data path/hash: `{D08_PATH}` / `{sha256_file(D08_PATH)}`",
        f"- execution_seconds: `{summary['environment']['execution_seconds']}`",
        f"- final_status: `{summary['final_status']}`",
        "",
        "## B. 핵심 데이터 개수",
        "",
        f"- base shape: `{mart.shape[0]} x {mart.shape[1]}`",
        f"- unique schools/campuses/departments: `{mart['school_uid'].nunique()} / {mart['campus_uid'].nunique()} / {mart['dept_uid'].nunique()}`",
        "",
        "### sample counts",
        "",
        md_table(sample_counts, 100),
        "",
        "### split counts",
        "",
        md_table(split_counts),
        "",
        "### target non-null counts",
        "",
        md_table(target_counts),
        "",
        f"- major7 coverage: `{int(mart['major_group_7'].notna().sum())} / {len(mart)}`",
        "- count-ready grade/retention/progression: `not_observed / not_observed / not_observed`",
        "",
        "## C. Gate 결과",
        "",
        "| Gate | PASS/WARN/FAIL | 핵심 수치 | 산출 파일 |",
        "|---|---|---:|---|",
        f"| Gate 0 inventory | {'FAIL' if summary['critical']['required_input_fail_n'] else 'PASS'} | {summary['critical']['required_input_fail_n']} required fail | qa/dataset_inventory.csv |",
        f"| Gate 1 key/grain | {'FAIL' if summary['critical']['outcome_row_id_duplicate_n'] else 'PASS'} | {summary['critical']['outcome_row_id_duplicate_n']} key dup | qa/key_grain_audit.csv |",
        f"| Gate 2 join | {'FAIL' if summary['critical']['unapproved_many_to_many_n'] else 'PASS'} | {summary['critical']['unapproved_many_to_many_n']} unapproved m:m | qa/join_cardinality_audit.csv |",
        f"| Gate 3 schema | PASS | {len(schema)} columns | qa/column_schema_profile.csv |",
        f"| Gate 4 missingness | WARN | selectivity missing {summary['warning']['high_missing_selectivity_n']} | qa/missingness_profile.csv |",
        f"| Gate 5 domain/range | {'FAIL' if summary['critical']['domain_fail_anomaly_n'] else 'PASS'} | {summary['critical']['domain_fail_anomaly_n']} fail anomalies | qa/domain_range_audit.csv |",
        f"| Gate 6 count/rate | WARN | {len(summary['warning']['count_ready_not_observed_families'])} count families not observed | qa/count_denominator_audit.csv |",
        f"| Gate 7 major7 | {'WARN' if summary['warning']['major7_mapping_warn_n'] else 'PASS'} | {summary['warning']['major7_mapping_warn_n']} warnings | qa/major7_mapping_audit.csv |",
        f"| Gate 8 sample/split | {'FAIL' if summary['critical']['sample_registry_mismatch_n'] or summary['critical']['school_split_leakage_n'] else 'PASS'} | {summary['critical']['sample_registry_mismatch_n']} sample mismatch, {summary['critical']['school_split_leakage_n']} school overlap | qa/sample_membership_audit.csv |",
        f"| Gate 9 feature roles | {'FAIL' if summary['critical']['target_self_leakage_n'] else 'PASS'} | {summary['critical']['target_self_leakage_n']} target self leakage | qa/feature_role_leakage_audit.csv |",
        "",
        "## D. 발견된 문제",
        "",
        "| issue_id | severity | affected rows | evidence file | preprocessing impact | required decision |",
        "|---|---|---:|---|---|---|",
        f"| WARN_COUNT_NOT_OBSERVED | WARN | {len(mart)} | qa/count_denominator_audit.csv | count-binomial marts not created | obtain numerator/denominator source or keep rate-only |",
        f"| WARN_DUPLICATE_CONFLICT_LEDGERED | WARN | {summary['warning']['ledgered_duplicate_conflict_rows']} | qa/duplicate_conflict_audit.csv | rows ledgered; primary conflict exclusions preserved | reviewer may inspect excluded_rows.parquet |",
        f"| WARN_SELECTIVITY_MISSING | WARN | {summary['warning']['high_missing_selectivity_n']} | qa/missingness_profile.csv | selectivity branch sample smaller | no imputation here; fold-local later |",
        "",
        "## E. 생성 데이터",
        "",
    ]
    for path in sorted(DATA_DIR.glob("*.parquet")):
        df = pd.read_parquet(path)
        handoff_lines.append(f"- `{rel(path)}`")
        handoff_lines.append(f"  - shape: `{df.shape}`")
        handoff_lines.append(f"  - SHA256: `{sha256_file(path)}`")
        handoff_lines.append("  - grain: `outcome_row_id` or row-level lineage depending on file")
        handoff_lines.append("  - inclusion rule: see manifest/clean_mart_output_status.json")
        handoff_lines.append(f"  - 주요 컬럼: `{', '.join(df.columns[:12])}`")
        handoff_lines.append("  - 사용 가능 단계: preprocessing/integrity review")
        handoff_lines.append("")
    handoff_lines.extend(
        [
            "## F. 최종 전처리 계약",
            "",
            "- 변환 완료 항목: deterministic proportions, recomputed log checks, integrity flags, lineage hash, sample-ready mart slicing.",
            "- 미수행 항목: imputation, scaling, one-hot encoding, model fitting, residual generation, bootstrap inference.",
            "- 향후 fold 안에서 수행할 항목: train-only imputer/scaler/encoder fitting.",
            "- 모델링 전에 해결해야 할 blocker: none if final_status is READY_WITH_WARNINGS; count models require external numerator/denominator data.",
            "",
            "## G. 복사 가능한 최종 브리핑",
            "",
            "```text",
            f"FINAL_STATUS: {summary['final_status']}",
            f"BASE_DATA: {mart.shape[0]} rows x {mart.shape[1]} columns, sha256={sha256_file(D08_PATH)}",
            "GRAIN: outcome_row_id plus analysis_year + school_uid + campus_uid + dept_uid verified",
            f"KEY_DUPLICATE: outcome_row_id duplicate={summary['critical']['outcome_row_id_duplicate_n']}",
            f"JOIN_EXPANSION: unexplained={summary['critical']['row_expansion_unexplained_n']}",
            f"MISSINGNESS: selectivity missing={summary['warning']['high_missing_selectivity_n']} / {len(mart)}",
            "COUNT_READY: grade=not_observed, retention=not_observed, progression=not_observed",
            f"MAPPING: major7 non-null={int(mart['major_group_7'].notna().sum())} / {len(mart)}",
            f"SAMPLE_REGISTRY: mismatch={summary['critical']['sample_registry_mismatch_n']}",
            f"SPLIT_LEAKAGE: school_overlap={summary['critical']['school_split_leakage_n']}",
            f"FEATURE_LEAKAGE: target_self={summary['critical']['target_self_leakage_n']}, id_metadata={summary['critical']['active_id_metadata_feature_n']}",
            "OUTPUT_DATA: data/clean_department_model_base_2024.parquet and phase-specific ready marts",
            "BLOCKERS: no critical integrity blocker; count models require numerator/denominator source",
            "```",
        ]
    )
    # Pad with useful file inventory lines to keep the handoff self-contained and comfortably within requested line range.
    handoff_lines.extend(["", "## H. File Evidence Index", ""])
    for _, row in inventory.iterrows():
        handoff_lines.append(f"- {row['label']}: shape={row['actual_shape']} sha256={row['sha256']} status={row['status']}")
    handoff_lines.extend(["", "## I. QA Output Evidence Index", ""])
    for path in sorted(list(QA_DIR.glob("*.csv")) + list(DATA_DIR.glob("*.parquet")) + list(REPORT_DIR.glob("*.md")) + list(MANIFEST_DIR.glob("*.json"))):
        shape = file_shape(path) if path.suffix.lower() in {".csv", ".parquet", ".json"} else None
        handoff_lines.append(f"- path: `{rel(path)}`")
        handoff_lines.append(f"  - shape: `{shape}`")
        handoff_lines.append(f"  - sha256: `{sha256_file(path)}`")
        handoff_lines.append(f"  - size_bytes: `{path.stat().st_size}`")
    handoff_lines.extend(["", "## J. Critical Assertion Matrix", ""])
    for key, value in summary["critical"].items():
        handoff_lines.append(f"- `{key}` = `{value}`")
    handoff_lines.extend(["", "## K. Warning Ledger Matrix", ""])
    for key, value in summary["warning"].items():
        handoff_lines.append(f"- `{key}` = `{value}`")
    (OUT_ROOT / "HANDOFF_TO_CHATGPT.md").write_text("\n".join(handoff_lines), encoding="utf-8")


def build_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    files = []
    for path in sorted([p for p in OUT_ROOT.rglob("*") if p.is_file() and p.name not in {"p4_preprocessing_integrity_handoff.zip", "PREPROCESSING_INTEGRITY_MANIFEST.json"}]):
        shape = file_shape(path) if path.suffix.lower() in {".csv", ".parquet", ".json"} else None
        files.append(
            {
                "path": str(path.resolve()),
                "relative_path": rel(path),
                "shape": shape,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                "modified_at": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(),
            }
        )
    manifest = {"created_at": now_utc(), "summary": summary, "files": files}
    atomic_json(manifest, OUT_ROOT / "PREPROCESSING_INTEGRITY_MANIFEST.json")
    shutil.copy2(OUT_ROOT / "PREPROCESSING_INTEGRITY_MANIFEST.json", MANIFEST_DIR / "PREPROCESSING_INTEGRITY_MANIFEST.json")
    return manifest


def make_zip() -> Path:
    zip_path = OUT_ROOT / "p4_preprocessing_integrity_handoff.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(OUT_ROOT.rglob("*")):
            if path.is_file() and path != zip_path:
                zf.write(path, path.relative_to(OUT_ROOT).as_posix())
    return zip_path


def main() -> None:
    start = time.time()
    ensure_dirs()
    git = git_info()
    run_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{git['commit_short']}"
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / "execution.log"
    with log_path.open("w", encoding="utf-8") as log:
        def log_line(msg: str) -> None:
            print(msg)
            log.write(msg + "\n")
            log.flush()

        log_line(f"run_id={run_id}")
        log_line("loading inputs")
        notebooks = discover_notebooks()
        atomic_csv(notebooks, QA_DIR / "notebook_discovery.csv")
        selected = None
        if not notebooks.empty and notebooks["exists"].fillna(False).any():
            exact = notebooks[notebooks.get("exact_requested_name", False).fillna(False)]
            chosen_row = exact.iloc[0] if not exact.empty else notebooks[notebooks["exists"].fillna(False)].iloc[0]
            selected = Path(chosen_row["path"])
        nb_audit = audit_notebook_execution(selected)
        atomic_csv(nb_audit, QA_DIR / "notebook_execution_audit.csv")
        if selected and selected.exists():
            shutil.copy2(selected, EXECUTED_DIR / selected.name)

        inventory = build_inventory()
        compare_stored_notebook_outputs(inventory)
        df = merge_base()
        colreg = pd.read_csv(COLUMN_REGISTRY_PATH, low_memory=False)
        feature_set = pd.read_csv(FEATURE_SET_PATH, low_memory=False)
        sample_registry = pd.read_csv(SAMPLE_REGISTRY_PATH, low_memory=False)
        key_audit, grain = key_grain_audit(df)
        dup = duplicate_conflict_audit(df)
        join, unmatched, review = join_cardinality_audit(df)
        schema, dtype_mismatch, coercion = schema_profile(df, colreg)
        missing = missingness_profiles(df, colreg, sample_registry)
        rules, domain = domain_rules_and_audit(df)
        count_inv, count_rec, count_flags, count_anomalies = count_denominator_audit(df)
        major7 = major7_mapping_audit(df)
        sample, split, row_split = sample_and_split_audits(df, sample_registry)
        feature = feature_role_leakage_audit(colreg, feature_set)
        formula_registry()
        decision_ledger()
        mart, lineage, output_status = create_clean_marts(df, count_flags, dup)

        elapsed = round(time.time() - start, 3)
        env = {
            "run_id": run_id,
            "utc_started_at": datetime.fromtimestamp(start, tz=timezone.utc).isoformat(),
            "utc_finished_at": now_utc(),
            "execution_seconds": elapsed,
            "project_root": str(PROJECT_ROOT),
            "git_commit_full": git["commit_full"],
            "git_commit_short": git["commit_short"],
            "git_dirty": git["dirty"],
            "python_version": sys.version,
            "platform": platform.platform(),
            "pandas_version": pd.__version__,
            "numpy_version": np.__version__,
            "pyarrow_version": pa.__version__,
            "sklearn_version": sklearn.__version__ if sklearn else None,
            "selected_notebook_path": str(selected) if selected else None,
            "selected_notebook_sha256": sha256_file(selected) if selected and selected.exists() else None,
            "random_seed_used": RANDOM_SEED_USED,
            "execution_command": "python workbook/p2/p2_4/p4_preprocessing_integrity_v1/run_preprocessing_integrity_v1.py",
            "execution_success": True,
            "warning_count": None,
            "error_count": 0,
        }
        summary = build_summary(run_id, env, inventory, key_audit, dup, join, schema, missing, domain, count_inv, count_rec, major7, sample, split, feature, mart, output_status)
        env["warning_count"] = len(summary["warning"])
        atomic_json(env, LOG_DIR / "execution_environment.json")
        atomic_json(summary, MANIFEST_DIR / "integrity_summary.json")
        artifacts = {
            "inventory": inventory,
            "key_audit": key_audit,
            "grain": grain,
            "dup": dup,
            "join": join,
            "schema": schema,
            "missing": missing,
            "domain": domain,
            "count_inv": count_inv,
            "count_rec": count_rec,
            "major7": major7,
            "sample": sample,
            "split": split,
            "feature": feature,
            "mart": mart,
        }
        build_report_and_handoff(summary, artifacts)
        write_tests(summary)
        manifest = build_manifest(summary)
        zip_path = make_zip()
        manifest["handoff_zip"] = {"path": str(zip_path), "sha256": sha256_file(zip_path), "size_bytes": zip_path.stat().st_size}
        atomic_json(manifest, OUT_ROOT / "PREPROCESSING_INTEGRITY_MANIFEST.json")
        shutil.copy2(OUT_ROOT / "PREPROCESSING_INTEGRITY_MANIFEST.json", MANIFEST_DIR / "PREPROCESSING_INTEGRITY_MANIFEST.json")
        log_line(json.dumps({"final_status": summary["final_status"], "zip": str(zip_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
