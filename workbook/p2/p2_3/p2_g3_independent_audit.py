from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
P2_3 = ROOT / "workbook" / "p2" / "p2_3"


EXPECTED = {
    "D01": ("p3_1/dept_headcount_master_2024.parquet", (15727, 175), "9ad156f25ad71e17835e1d2c73a15515e63b49c87e161458579b6733e3d60a4f"),
    "D02": ("p3_1/dept_outcomes_2024.parquet", (10242, 32), "871cfacbfc1020717c0ccbea64f4fad3e6adf5dd9b091b72bd22f50a139d16c5"),
    "D03": ("p3_1/dept_master_2024_core.parquet", (10242, 88), "06892a716d5fef2b87e4b0806c6f4b398e8c0ddfa6c4f80d063c6643d54fffce"),
    "D04": ("p3_1/wage_reference_by_major.parquet", (14, 87), "489caf15edbefa1ed0c30fdfa98dbe31096b36c219f6610dae69a2d5e49c47e5"),
    "D05": ("p3_1/job_cert_bridge.parquet", (24, 32), "02dd640c73448f901b08c195091f6a6f3893cdf69af23d79139ebdac8f1cc33f"),
    "D06": ("p3_2/goms_major_year_labor_baseline.parquet", (91, 45), "75d8bc34a0bf092c3e2c4332fd213d4a01f5a86252b6f6b4ac6f29709b3202c3"),
    "D07": ("p3_2/goms_major_profile_recent.parquet", (7, 29), "51473a3514f34e6695d175af005436f77cb700a76390d08a964772dbc3ccde30"),
    "D08": ("shared/mart_department_model_base_2024.parquet", (10242, 131), "66ad0c147f40aaaf551c11c71d8bf15e15eb0c423eba3d06326c1c6eca32bc02"),
    "D07_HANDOFF": ("shared_handoff/goms_major_profile_recent.parquet", (7, 29), "51473a3514f34e6695d175af005436f77cb700a76390d08a964772dbc3ccde30"),
    "NATIONAL": ("p3_2/goms_national_year_benchmark.parquet", (13, 45), None),
}


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def shape_hash_report() -> pd.DataFrame:
    rows = []
    for dataset, (rel, expected_shape, expected_sha) in EXPECTED.items():
        path = P2_3 / rel
        exists = path.exists()
        shape = None
        sha = None
        if exists:
            if path.suffix == ".parquet":
                shape = tuple(pd.read_parquet(path).shape)
            else:
                shape = tuple(pd.read_csv(path).shape)
            sha = sha256_path(path)
        rows.append(
            {
                "dataset": dataset,
                "path": rel,
                "exists": exists,
                "shape": shape,
                "expected_shape": expected_shape,
                "shape_ok": shape == expected_shape,
                "sha256": sha,
                "expected_sha256": expected_sha,
                "hash_ok": None if expected_sha is None else sha == expected_sha,
            }
        )
    return pd.DataFrame(rows)


def read_csv_any(path: Path) -> pd.DataFrame:
    for enc in ["utf-8-sig", "utf-8", "cp949"]:
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path)


def bridge_audit() -> dict:
    bridge = read_csv_any(P2_3 / "shared" / "bridge_outcome_headcount.csv")
    d03 = pd.read_parquet(P2_3 / "p3_1" / "dept_master_2024_core.parquet")
    d08 = pd.read_parquet(P2_3 / "shared" / "mart_department_model_base_2024.parquet")
    out = {
        "bridge_shape": list(bridge.shape),
        "columns": list(bridge.columns),
        "match_method_counts": bridge["match_method"].value_counts(dropna=False).to_dict() if "match_method" in bridge.columns else {},
        "outcome_row_id_duplicates": int(bridge["outcome_row_id"].duplicated().sum()) if "outcome_row_id" in bridge.columns else None,
        "candidate_ge2_autoconfirm": None,
        "campus_conflict_autoconfirm": None,
        "manual_review_counts": {},
        "unmatched_retained_d03": None,
        "unmatched_retained_d08": None,
    }
    if {"candidate_count", "headcount_match_flag"}.issubset(bridge.columns):
        out["candidate_ge2_autoconfirm"] = int(((pd.to_numeric(bridge["candidate_count"], errors="coerce") >= 2) & bridge["headcount_match_flag"].astype(bool)).sum())
    if "campus_conflict_flag" in bridge.columns and "headcount_match_flag" in bridge.columns:
        out["campus_conflict_autoconfirm"] = int((bridge["campus_conflict_flag"].astype(bool) & bridge["headcount_match_flag"].astype(bool)).sum())
    conflict_cols = [c for c in bridge.columns if "campus" in c.lower() and "conflict" in c.lower()]
    out["campus_conflict_columns"] = conflict_cols
    for col in ["review_status", "manual_review_status", "review_needed", "match_method"]:
        if col in bridge.columns:
            out["manual_review_counts"][col] = bridge.loc[bridge.get("match_method", pd.Series(index=bridge.index, dtype=object)).eq("manual_review"), col].value_counts(dropna=False).to_dict()
    if "outcome_row_id" in bridge.columns:
        unmatched_ids = set(bridge.loc[bridge["match_method"].eq("unmatched"), "outcome_row_id"])
        for name, df in [("d03", d03), ("d08", d08)]:
            if "outcome_row_id" in df.columns:
                out[f"unmatched_retained_{name}"] = int(df["outcome_row_id"].isin(unmatched_ids).sum())
    return out


def major_audit() -> dict:
    bridge = read_csv_any(P2_3 / "shared" / "bridge_department_major7.csv")
    terms = ["자유전공", "융합", "데이터사이언스", "바이오", "산업디자인", "교육공학", "의공학", "문화콘텐츠", "스포츠과학", "심리", "식품영양", "건축학", "건축공학"]
    text_cols = [c for c in bridge.columns if bridge[c].dtype == object or str(bridge[c].dtype).startswith("string")]
    term_hits = {}
    full_text = bridge[text_cols].fillna("").astype(str).agg(" ".join, axis=1) if text_cols else pd.Series("", index=bridge.index)
    for term in terms:
        term_hits[term] = int(full_text.str.contains(term, regex=False).sum())
    return {
        "shape": list(bridge.shape),
        "columns": list(bridge.columns),
        "method_counts": bridge["major7_mapping_method"].value_counts(dropna=False).to_dict() if "major7_mapping_method" in bridge.columns else {},
        "major_counts": bridge["major_group_7"].value_counts(dropna=False).to_dict() if "major_group_7" in bridge.columns else {},
        "term_hits": term_hits,
    }


def context_registry_audit() -> dict:
    d04 = pd.read_parquet(P2_3 / "p3_1" / "wage_reference_by_major.parquet")
    d05 = pd.read_parquet(P2_3 / "p3_1" / "job_cert_bridge.parquet")
    d08 = pd.read_parquet(P2_3 / "shared" / "mart_department_model_base_2024.parquet")
    registry = read_csv_any(P2_3 / "shared" / "department_model_column_registry.csv")
    cols = ["ctx24_industry_top3_pct", "ctx24_industry_hhi"]
    d04_na = {c: bool(d04[c].isna().all()) if c in d04.columns else None for c in cols}
    d08_na = {c: bool(d08[c].isna().all()) if c in d08.columns else None for c in cols}
    registry_hits = {}
    if "column_name" in registry.columns:
        for c in cols:
            registry_hits[c] = registry.loc[registry["column_name"].eq(c)].to_dict("records")
    job_cert_cols = [c for c in d08.columns if c.startswith("job_cert_")]
    d05_join_true = None
    if "join_now" in d05.columns:
        d05_join_true = int(d05["join_now"].astype(bool).sum())
    return {
        "d04_all_na": d04_na,
        "d08_all_na": d08_na,
        "registry_hits": registry_hits,
        "d08_job_cert_cols": job_cert_cols,
        "d05_join_now_true": d05_join_true,
    }


def d07_d08_lineage_audit() -> dict:
    d07 = pd.read_parquet(P2_3 / "shared_handoff" / "goms_major_profile_recent.parquet")
    d08 = pd.read_parquet(P2_3 / "shared" / "mart_department_model_base_2024.parquet")
    label_to_code = {"인문": "HUM", "사회": "SOC", "교육": "EDU", "공학": "ENG", "자연": "NAT", "의약": "MED", "예체능": "ART"}
    d07_compare = d07.copy()
    d07_compare["major_group_7"] = d07_compare["major_group_7"].astype(str).map(label_to_code).fillna(d07_compare["major_group_7"].astype(str))
    d07_compare = d07_compare.rename(columns={c: f"goms_{c}" for c in d07_compare.columns if c != "major_group_7" and not c.startswith("goms_")})
    goms_cols = [c for c in d07_compare.columns if c.startswith("goms_")]
    key = "major_group_7"
    merged = d08[[key, *[c for c in goms_cols if c in d08.columns]]].merge(d07_compare[[key, *goms_cols]], on=key, how="left", suffixes=("_d08", "_d07"), validate="many_to_one")
    diffs = {}
    for c in goms_cols:
        c08 = f"{c}_d08"
        c07 = f"{c}_d07"
        if c08 not in merged.columns or c07 not in merged.columns:
            diffs[c] = "missing_in_d08"
            continue
        s1 = merged[c08]
        s2 = merged[c07]
        if pd.api.types.is_bool_dtype(s1) or pd.api.types.is_bool_dtype(s2):
            neq = ~(s1.astype("boolean").astype("string").fillna("<NA>") == s2.astype("boolean").astype("string").fillna("<NA>"))
        elif pd.api.types.is_numeric_dtype(s1) or pd.api.types.is_numeric_dtype(s2):
            n1 = pd.to_numeric(s1, errors="coerce").astype("float64").to_numpy()
            n2 = pd.to_numeric(s2, errors="coerce").astype("float64").to_numpy()
            neq = ~np.isclose(n1, n2, equal_nan=True)
        else:
            neq = ~(s1.astype("string").fillna("<NA>") == s2.astype("string").fillna("<NA>"))
        n = int(neq.sum())
        if n:
            diffs[c] = n
    return {
        "handoff_sha256": sha256_path(P2_3 / "shared_handoff" / "goms_major_profile_recent.parquet"),
        "d07_output_sha256": sha256_path(P2_3 / "p3_2" / "goms_major_profile_recent.parquet"),
        "d07_vs_handoff_same_bytes": (P2_3 / "shared_handoff" / "goms_major_profile_recent.parquet").read_bytes() == (P2_3 / "p3_2" / "goms_major_profile_recent.parquet").read_bytes(),
        "d07_major_values": d07[key].astype(str).tolist(),
        "d07_major_codes_for_merge": d07_compare[key].astype(str).tolist(),
        "d08_major_missing": int(d08[key].isna().sum()) if key in d08.columns else None,
        "d08_goms_rows_with_any": int(d08[[c for c in goms_cols if c in d08.columns]].notna().any(axis=1).sum()),
        "goms_col_diff_counts": diffs,
    }


def split_sample_audit() -> dict:
    d08 = pd.read_parquet(P2_3 / "shared" / "mart_department_model_base_2024.parquet")
    split = read_csv_any(P2_3 / "shared" / "dim_school_split.csv")
    registry = read_csv_any(P2_3 / "shared" / "model_sample_registry.csv")
    split_col = "split"
    if split_col not in d08.columns and "school_uid" in d08.columns:
        d08 = d08.merge(split[["school_uid", split_col]], on="school_uid", how="left", suffixes=("", "_dim"))
    leakage = None
    if {"school_uid", split_col}.issubset(d08.columns):
        leakage = int((d08.groupby("school_uid")[split_col].nunique(dropna=True) > 1).sum())
    split_summary = {}
    if split_col in d08.columns:
        split_summary = d08.groupby(split_col).agg(
            rows=("school_uid", "size"),
            schools=("school_uid", "nunique"),
            outcome_a_observed=("a_rate_pct", lambda s: int(s.notna().sum()) if "a_rate_pct" in d08.columns else np.nan),
            headcount_match_rate=("headcount_match_flag", lambda s: float(pd.Series(s).astype("boolean").mean()) if "headcount_match_flag" in d08.columns else np.nan),
        ).reset_index().to_dict("records")
    major_split = None
    if {split_col, "major_group_7"}.issubset(d08.columns):
        major_split = d08.groupby([split_col, "major_group_7"], dropna=False).size().unstack(fill_value=0).to_dict()

    sample_rows = []
    mask_expr_col = "filter_expression" if "filter_expression" in registry.columns else None
    for sid in ["GRADE_ALL", "GRADE_SELECTIVITY", "EMPLOYMENT_HEALTH", "PROGRESSION_GRADSCHOOL", "JOINT_EMP_PROG"]:
        reg = registry[registry.get("sample_id", pd.Series(dtype=str)).eq(sid)] if "sample_id" in registry.columns else pd.DataFrame()
        if sid == "GRADE_ALL":
            mask = d08["a_rate_pct"].notna()
        elif sid == "GRADE_SELECTIVITY":
            mask = d08["a_rate_pct"].notna() & d08["selectivity_proxy_pct"].notna()
        elif sid == "EMPLOYMENT_HEALTH":
            mask = d08["health_employment_rate_pct"].notna()
        elif sid == "PROGRESSION_GRADSCHOOL":
            mask = d08["graduate_school_progression_rate_pct"].notna()
        elif sid == "JOINT_EMP_PROG":
            mask = d08["health_employment_rate_pct"].notna() & d08["graduate_school_progression_rate_pct"].notna()
        part = d08[mask]
        sample_rows.append(
            {
                "sample_id": sid,
                "actual_rows": int(len(part)),
                "actual_schools": int(part["school_uid"].nunique()) if "school_uid" in part.columns else None,
                "actual_splits": part[split_col].value_counts(dropna=False).to_dict() if split_col in part.columns else {},
                "actual_major_counts": part["major_group_7"].value_counts(dropna=False).to_dict() if "major_group_7" in part.columns else {},
                "registry_record": reg.to_dict("records"),
                "registry_filter_expression": reg[mask_expr_col].iloc[0] if mask_expr_col and not reg.empty else None,
            }
        )
    return {
        "split_file_shape": list(split.shape),
        "split_counts_file": split[split_col].value_counts(dropna=False).to_dict() if split_col in split.columns else {},
        "schools_file": int(split["school_uid"].nunique()) if "school_uid" in split.columns else None,
        "school_split_leakage": leakage,
        "d08_split_missing": int(d08[split_col].isna().sum()) if split_col in d08.columns else None,
        "d08_split_summary": split_summary,
        "d08_major_split": major_split,
        "sample_rows": sample_rows,
    }


def log_audit() -> dict:
    log_dir = P2_3 / "logs"
    qa_dir = P2_3 / "qa"
    out = {"logs": {}, "qa_files": sorted(p.name for p in qa_dir.glob("*"))}
    for path in sorted(log_dir.glob("*")):
        info = {"size": path.stat().st_size, "sha256": sha256_path(path)}
        if path.suffix == ".json":
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                info["top_keys"] = list(data.keys()) if isinstance(data, dict) else None
                info["agent"] = data.get("agent") if isinstance(data, dict) else None
                info["notebook"] = data.get("notebook") if isinstance(data, dict) else None
                info["run_started_at"] = data.get("run_started_at") if isinstance(data, dict) else None
                info["run_completed_at"] = data.get("run_completed_at") if isinstance(data, dict) else None
                info["runtime_seconds"] = data.get("runtime_seconds") if isinstance(data, dict) else None
                info["outputs_keys"] = list(data.get("outputs", {}).keys()) if isinstance(data, dict) and isinstance(data.get("outputs"), dict) else None
            except Exception as exc:  # pragma: no cover
                info["json_error"] = repr(exc)
        elif path.suffix == ".jsonl":
            records = []
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    obj = {"_raw": line[:200]}
                records.append(obj)
            info["records"] = len(records)
            info["agents"] = sorted({str(r.get("agent")) for r in records if isinstance(r, dict) and "agent" in r})
            info["notebooks"] = sorted({str(r.get("notebook")) for r in records if isinstance(r, dict) and "notebook" in r})
            info["datasets"] = sorted({str(r.get("dataset")) for r in records if isinstance(r, dict) and "dataset" in r})
            info["first"] = records[0] if records else None
            info["last"] = records[-1] if records else None
        out["logs"][path.name] = info
    return out


def main() -> None:
    pd.set_option("display.max_columns", 200)
    pd.set_option("display.width", 240)
    print("\n=== SHAPE_HASH ===")
    print(shape_hash_report().to_string(index=False))
    print("\n=== BRIDGE ===")
    print(json.dumps(bridge_audit(), ensure_ascii=False, indent=2, default=str))
    print("\n=== MAJOR ===")
    print(json.dumps(major_audit(), ensure_ascii=False, indent=2, default=str))
    print("\n=== CONTEXT_REGISTRY ===")
    print(json.dumps(context_registry_audit(), ensure_ascii=False, indent=2, default=str))
    print("\n=== D07_D08_LINEAGE ===")
    print(json.dumps(d07_d08_lineage_audit(), ensure_ascii=False, indent=2, default=str))
    print("\n=== SPLIT_SAMPLE ===")
    print(json.dumps(split_sample_audit(), ensure_ascii=False, indent=2, default=str))
    print("\n=== LOGS ===")
    print(json.dumps(log_audit(), ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
