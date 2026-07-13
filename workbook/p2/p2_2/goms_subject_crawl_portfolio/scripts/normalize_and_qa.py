"""
GOMS 원본 다운로드(raw_downloads/*.xls, 실제로는 HTML 표) → long-format 정규화 + QA 검증.

crawl_goms_subjects.py 실행 이후에 이 스크립트를 실행한다.
출력: 03_schema_audit.csv, 04_parse_issues.csv, normalized/*.{csv,parquet}, qa/*.csv
"""

import re
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent / "data"
NORM_DIR = ROOT / "normalized"
QA_DIR = ROOT / "qa"
NORM_DIR.mkdir(parents=True, exist_ok=True)
QA_DIR.mkdir(parents=True, exist_ok=True)


def load_table(path):
    raw = path.read_text(encoding="utf-8-sig")
    fixed = raw.replace("&quot;", '"')
    tables = pd.read_html(StringIO(fixed))
    return tables[0]


def parse_categorical(path, topic_meta):
    df = load_table(path)
    new_cols = list(df.columns)
    new_cols[0] = ("dim", "dim", "dim")
    df.columns = pd.MultiIndex.from_tuples(new_cols)
    df = df.set_index(("dim", "dim", "dim"))
    df.index.name = "dimension_value"

    records = []
    for (year, subgroup, measure_kr), col in df.items():
        if year == "Unnamed: 0_level_0":
            continue
        measure_type = "frequency" if measure_kr == "빈도" else "share"
        for dim_val, val in col.items():
            records.append({
                "topic_id": topic_meta["topic_id"],
                "topic_group": topic_meta["group_name"],
                "topic_name": topic_meta["topic"],
                "classification_version": topic_meta["classification_version"],
                "dimension_value": dim_val,
                "year": int(year),
                "subgroup": subgroup,
                "measure_type": measure_type,
                "value": pd.to_numeric(str(val).replace(",", ""), errors="coerce"),
            })
    return pd.DataFrame(records)


def parse_continuous(path, topic_meta):
    df = load_table(path)
    df = df.rename(columns={df.columns[0]: "dimension_value"})
    long = df.melt(id_vars="dimension_value", var_name="year", value_name="value")
    long["year"] = long["year"].astype(int)
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    long["topic_id"] = topic_meta["topic_id"]
    long["topic_group"] = topic_meta["group_name"]
    long["topic_name"] = topic_meta["topic"]
    long["classification_version"] = topic_meta["classification_version"]
    long["measure_type"] = "mean_income_or_hours"
    return long[["topic_id", "topic_group", "topic_name", "classification_version",
                 "dimension_value", "year", "measure_type", "value"]]


def main():
    manifest = pd.read_csv(ROOT / "02_download_manifest.csv")
    reg = pd.read_csv(ROOT / "00_topic_registry.csv")
    reg = reg.set_index("topic_id")

    audit_rows = []
    cat_frames = []
    cont_frames = []
    parse_issues = []

    for _, row in manifest.iterrows():
        path = ROOT / row["file_path"]
        meta = reg.loc[row["topic_id"]].to_dict()
        meta["topic_id"] = row["topic_id"]
        try:
            if row["kind"] == "categorical":
                long_df = parse_categorical(path, meta)
                cat_frames.append(long_df)
            else:
                long_df = parse_continuous(path, meta)
                cont_frames.append(long_df)

            audit_rows.append({
                "topic_id": row["topic_id"], "topic_name": row["topic_name"], "kind": row["kind"],
                "n_records": len(long_df), "n_years": long_df["year"].nunique(),
                "year_min": long_df["year"].min(), "year_max": long_df["year"].max(),
                "n_dimension_values": long_df["dimension_value"].nunique(),
                "n_null_values": long_df["value"].isna().sum(),
                "parse_status": "ok",
            })
        except Exception as exc:
            parse_issues.append({"topic_id": row["topic_id"], "topic_name": row["topic_name"],
                                  "error_type": type(exc).__name__, "error_message": str(exc)[:300]})
            audit_rows.append({
                "topic_id": row["topic_id"], "topic_name": row["topic_name"], "kind": row["kind"],
                "parse_status": "failed",
            })

    pd.DataFrame(audit_rows).to_csv(ROOT / "03_schema_audit.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(parse_issues).to_csv(ROOT / "04_parse_issues.csv", index=False, encoding="utf-8-sig")

    cat_long = pd.concat(cat_frames, ignore_index=True)
    cont_long = pd.concat(cont_frames, ignore_index=True)

    cat_long.to_csv(NORM_DIR / "goms_distribution_long.csv", index=False, encoding="utf-8-sig")
    cat_long.to_parquet(NORM_DIR / "goms_distribution_long.parquet", index=False)
    cont_long.to_csv(NORM_DIR / "goms_continuous_long.csv", index=False, encoding="utf-8-sig")
    cont_long.to_parquet(NORM_DIR / "goms_continuous_long.parquet", index=False)

    print("categorical long rows:", len(cat_long))
    print("continuous long rows:", len(cont_long))
    print("parse issues:", len(parse_issues))

    # QA 1: proportion sums per topic/year/subgroup should be ~100 (allow NA/모름 slack -> 95~101)
    share = cat_long[cat_long["measure_type"] == "share"]
    # exclude the '전체' aggregate row itself from the sum-of-subcategories check
    share_no_total = share[share["dimension_value"] != "전체"]
    sums = (share_no_total.groupby(["topic_id", "topic_name", "year", "subgroup"])["value"]
            .sum().reset_index(name="share_sum"))
    sums["qa_status"] = np.where(sums["share_sum"].between(90.0, 101.5), "PASS", "REVIEW")
    sums.to_csv(QA_DIR / "proportion_sum_check.csv", index=False, encoding="utf-8-sig")
    print("proportion sum check:", sums["qa_status"].value_counts().to_dict())

    # QA 2: year coverage per topic
    year_cov = manifest.merge(
        pd.concat([
            cat_long.groupby("topic_id")["year"].agg(["min", "max", "nunique"]),
            cont_long.groupby("topic_id")["year"].agg(["min", "max", "nunique"]),
        ]).reset_index(),
        on="topic_id", how="left"
    )
    year_cov = year_cov[["topic_id", "topic_name", "min", "max", "nunique"]]
    year_cov.columns = ["topic_id", "topic_name", "year_min", "year_max", "n_years"]
    year_cov["qa_status"] = np.where(year_cov["n_years"] >= 1, "PASS", "REVIEW")
    year_cov.to_csv(QA_DIR / "year_coverage_check.csv", index=False, encoding="utf-8-sig")
    print("year coverage check:", year_cov["qa_status"].value_counts().to_dict())

    # QA 3: duplicate check (topic_id + measure_type + dimension_value + year + subgroup should be unique)
    cat_dup = cat_long.duplicated(subset=["topic_id", "dimension_value", "year", "subgroup", "measure_type"]).sum()
    cont_dup = cont_long.duplicated(subset=["topic_id", "dimension_value", "year"]).sum()
    dup_df = pd.DataFrame([
        {"dataset": "categorical", "duplicate_rows": int(cat_dup)},
        {"dataset": "continuous", "duplicate_rows": int(cont_dup)},
    ])
    dup_df.to_csv(QA_DIR / "duplicate_check.csv", index=False, encoding="utf-8-sig")
    print("duplicate check:", dup_df.to_dict("records"))

    # QA 4: cross-file duplicate sha256 (should be none post-fix)
    cross_dup = manifest.groupby("sha256").filter(lambda g: len(g) > 1)
    cross_dup_status = "PASS" if cross_dup.empty else "REVIEW"

    final_summary = pd.DataFrame([{
        "total_topics": len(manifest),
        "categorical_topics": (manifest["kind"] == "categorical").sum(),
        "continuous_topics": (manifest["kind"] == "continuous").sum(),
        "parse_failures": len(parse_issues),
        "proportion_review_count": (sums["qa_status"] == "REVIEW").sum(),
        "year_coverage_review_count": (year_cov["qa_status"] == "REVIEW").sum(),
        "duplicate_rows_categorical": int(cat_dup),
        "duplicate_rows_continuous": int(cont_dup),
        "cross_file_hash_duplicates": cross_dup_status,
        "stddev_available": False,
        "stddev_reason": "site JS bug (callbackGOMSSubject unconditionally resets viewType2 to index 0 on every render) makes 분산/표준편차 unreachable via official UI/CSV flow",
    }])
    final_summary.to_csv(QA_DIR / "final_qa_summary.csv", index=False, encoding="utf-8-sig")
    print(final_summary.T)


if __name__ == "__main__":
    main()
