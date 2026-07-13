from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import Markdown, display

PROJECT_ROOT = Path.cwd().resolve()
if not (PROJECT_ROOT / "workbook").exists():
    for parent in Path.cwd().resolve().parents:
        if (parent / "workbook").exists() and (parent / "scripts").exists():
            PROJECT_ROOT = parent
            break

P2_3 = PROJECT_ROOT / "workbook" / "p2" / "p2_3"
P2_4 = PROJECT_ROOT / "workbook" / "p2" / "p2_4"
OUT_ROOT = P2_4 / "source_eda"
TABLE_DIR = OUT_ROOT / "tables"
FIGURE_DIR = OUT_ROOT / "figures_visual"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

pd.set_option("display.max_columns", 80)
pd.set_option("display.max_colwidth", 160)
plt.rcParams["font.family"] = ["NanumGothic", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(PROJECT_ROOT))


def safe_slug(text: str, limit: int = 90) -> str:
    slug = re.sub(r"[^0-9A-Za-z가-힣._-]+", "__", str(text)).strip("_")
    return slug[:limit] or "dataset"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv_smart(path: Path, nrows: int | None = None) -> pd.DataFrame:
    last_error: Exception | None = None
    for encoding in ("utf-8-sig", "utf-8", "cp949"):
        try:
            return pd.read_csv(path, encoding=encoding, low_memory=False, nrows=nrows)
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Could not read CSV: {path}") from last_error


def read_table(path: Path, nrows: int | None = None) -> pd.DataFrame:
    if path.suffix.lower() == ".parquet":
        df = pd.read_parquet(path)
        return df.head(nrows) if nrows else df
    return read_csv_smart(path, nrows=nrows)


def dtype_bucket(series: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(series):
        return "bool"
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    return "text/category"


def compact_column_profile(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty and len(df.columns) == 0:
        return pd.DataFrame(
            columns=["column", "dtype", "dtype_bucket", "missing_n", "missing_pct", "unique_n", "sample_values"]
        )
    denom = max(len(df), 1)
    missing = df.isna().sum()
    nunique = df.nunique(dropna=True)
    rows = []
    for col in df.columns:
        sample_values = " | ".join(map(str, df[col].dropna().astype(str).head(3).tolist()))
        rows.append(
            {
                "column": col,
                "dtype": str(df[col].dtype),
                "dtype_bucket": dtype_bucket(df[col]),
                "missing_n": int(missing[col]),
                "missing_pct": round(float(missing[col] / denom), 4),
                "unique_n": int(nunique[col]),
                "sample_values": sample_values,
            }
        )
    return pd.DataFrame(rows)


def dataset_profile(df: pd.DataFrame, path: Path, source_kind: str) -> pd.DataFrame:
    duplicate_rows = int(df.duplicated().sum()) if len(df) <= 200_000 else np.nan
    return pd.DataFrame(
        [
            {
                "path": rel(path),
                "source_kind": source_kind,
                "rows": int(df.shape[0]),
                "columns": int(df.shape[1]),
                "size_mb": round(path.stat().st_size / (1024 * 1024), 3) if path.exists() else np.nan,
                "sha256_12": sha256_file(path)[:12] if path.exists() else "",
                "duplicate_rows": duplicate_rows,
                "missing_cells": int(df.isna().sum().sum()),
                "numeric_columns": int(df.select_dtypes(include="number").shape[1]),
                "bool_columns": int(df.select_dtypes(include=["bool", "boolean"]).shape[1]),
                "text_columns": int(df.select_dtypes(include=["object", "string", "category"]).shape[1]),
            }
        ]
    )


def load_inventory_tables() -> dict[str, pd.DataFrame]:
    paths = {
        "inventory": TABLE_DIR / "source_dataset_inventory.csv",
        "columns": TABLE_DIR / "source_column_inventory.csv",
        "reuse": TABLE_DIR / "source_column_reuse_summary.csv",
        "target_like": TABLE_DIR / "target_like_column_inventory.csv",
        "feature_like": TABLE_DIR / "feature_like_column_inventory.csv",
        "parquet_manifest": TABLE_DIR / "parquet_conversion_manifest.csv",
    }
    missing = [rel(path) for path in paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing source EDA tables. Run scripts/build_p2_g4_source_eda_notebook.py first: "
            + ", ".join(missing)
        )
    return {name: read_csv_smart(path) for name, path in paths.items()}


def short_dataset_label(path_text: str) -> str:
    parts = Path(str(path_text)).parts
    label = "/".join(parts[-3:]) if len(parts) >= 3 else str(path_text)
    if len(label) > 58:
        label = label[:24] + "..." + label[-29:]
    return label


def _plot_no_data(ax, message: str) -> None:
    ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def _priority_numeric_columns(df: pd.DataFrame, limit: int = 8) -> list[str]:
    numeric_cols = [
        col
        for col in df.columns
        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col])
    ]
    if not numeric_cols:
        return []
    priority = re.compile(
        r"rate|pct|ratio|score|count|total|graduates|employment|progression|a_rate|cd_rate|f_rate|"
        r"admission|recruitment|rank|vif|missing|duplicate|n$",
        re.I,
    )
    ranked = []
    for col in numeric_cols:
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        if s.empty or s.nunique(dropna=True) <= 1:
            spread = 0.0
        else:
            spread = float(s.quantile(0.75) - s.quantile(0.25))
        ranked.append((0 if priority.search(str(col)) else 1, -spread, str(col), col))
    ranked.sort()
    return [item[-1] for item in ranked[:limit]]


def _priority_category_column(df: pd.DataFrame) -> str | None:
    candidates = [
        "status",
        "result",
        "check",
        "gate",
        "p4_use",
        "sample",
        "sample_name",
        "split",
        "major_group_7",
        "match_method",
        "feature_group",
        "target_candidate",
        "model_id",
        "source_kind",
    ]
    lower_to_col = {str(col).lower(): col for col in df.columns}
    for key in candidates:
        for lower, col in lower_to_col.items():
            if key in lower and df[col].nunique(dropna=True) <= 40:
                return col
    object_cols = list(df.select_dtypes(include=["object", "string", "category", "bool", "boolean"]).columns)
    ranked = []
    for col in object_cols:
        nunique = int(df[col].nunique(dropna=True))
        if 2 <= nunique <= 40:
            ranked.append((nunique, str(col), col))
    if ranked:
        ranked.sort()
        return ranked[0][-1]
    return object_cols[0] if object_cols else None


def _plot_dtype_mix(ax, df: pd.DataFrame) -> None:
    counts = pd.Series([dtype_bucket(df[col]) for col in df.columns]).value_counts()
    if counts.empty:
        _plot_no_data(ax, "no columns")
        return
    counts.sort_values().plot.barh(ax=ax, color="#4C78A8")
    ax.set_title("Column dtype mix")
    ax.set_xlabel("columns")
    ax.set_ylabel("")


def _plot_missing(ax, colprof: pd.DataFrame) -> None:
    missing = colprof[colprof["missing_n"] > 0].sort_values(["missing_pct", "missing_n"], ascending=False).head(12)
    if missing.empty:
        _plot_no_data(ax, "no missing cells")
        ax.set_title("Missingness")
        return
    y = np.arange(len(missing))
    ax.barh(y, missing["missing_pct"] * 100, color="#E45756")
    ax.set_yticks(y)
    ax.set_yticklabels(missing["column"], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("missing %")
    ax.set_title("Top missing columns")


def _plot_numeric_spread(ax, df: pd.DataFrame) -> list[str]:
    cols = _priority_numeric_columns(df)
    if not cols:
        _plot_no_data(ax, "no numeric columns")
        ax.set_title("Numeric spread")
        return []
    rows = []
    for col in cols:
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        if s.empty:
            continue
        lo, q1, med, q3, hi = np.nanquantile(s.to_numpy(dtype=float), [0, 0.25, 0.5, 0.75, 1])
        denom = hi - lo
        if not np.isfinite(denom) or abs(denom) < 1e-12:
            denom = 1.0
        rows.append(
            {
                "column": col,
                "lo": lo,
                "q1n": (q1 - lo) / denom,
                "medn": (med - lo) / denom,
                "q3n": (q3 - lo) / denom,
                "hi": hi,
            }
        )
    if not rows:
        _plot_no_data(ax, "numeric columns are all empty")
        ax.set_title("Numeric spread")
        return []
    y = np.arange(len(rows))
    for idx, row in enumerate(rows):
        ax.hlines(idx, row["q1n"], row["q3n"], color="#72B7B2", linewidth=8, alpha=0.8)
        ax.scatter(row["medn"], idx, color="#1F2933", s=24, zorder=3)
    labels = [f"{row['column']}\n[{row['lo']:.3g}, {row['hi']:.3g}]" for row in rows]
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7)
    ax.invert_yaxis()
    ax.set_xlim(-0.03, 1.03)
    ax.set_xlabel("normalized min to max per column")
    ax.set_title("Numeric IQR and median")
    return [str(row["column"]) for row in rows]


def _plot_category_counts(ax, df: pd.DataFrame) -> str | None:
    col = _priority_category_column(df)
    if col is None:
        _plot_no_data(ax, "no categorical/status column")
        ax.set_title("Category/status counts")
        return None
    counts = df[col].astype("string").fillna("<NA>").value_counts(dropna=False).head(10)
    if counts.empty:
        _plot_no_data(ax, f"{col}: no values")
        ax.set_title("Category/status counts")
        return str(col)
    counts.sort_values().plot.barh(ax=ax, color="#F58518")
    ax.set_title(f"Top values: {col}")
    ax.set_xlabel("rows")
    ax.set_ylabel("")
    ax.tick_params(axis="y", labelsize=8)
    return str(col)


def _interpretation_block(
    path_text: str,
    df: pd.DataFrame,
    colprof: pd.DataFrame,
    numeric_cols: list[str],
    category_col: str | None,
) -> str:
    missing = colprof[colprof["missing_n"] > 0].sort_values(["missing_pct", "missing_n"], ascending=False)
    if missing.empty:
        missing_sentence = "결측이 관찰되지 않는다."
    else:
        top = missing.iloc[0]
        missing_sentence = f"`{top['column']}` 결측률이 {top['missing_pct']:.1%}로 가장 높다."
    numeric_sentence = (
        f"수치형 후보는 {len(numeric_cols)}개를 우선 표시했다: " + ", ".join(f"`{c}`" for c in numeric_cols[:4])
        if numeric_cols
        else "수치형 컬럼이 없어 dtype/범주/키 품질을 중심으로 본다."
    )
    category_sentence = (
        f"`{category_col}`의 상위값 분포로 상태/그룹 쏠림을 확인한다."
        if category_col
        else "상태나 그룹을 대표할 범주형 컬럼이 뚜렷하지 않다."
    )
    return "\n".join(
        [
            "**관찰:** " + missing_sentence + " " + numeric_sentence,
            "",
            "**원인:** 이 그림은 파일의 row/column grain, 결측 구조, 모델 후보 컬럼의 스케일 차이를 빠르게 찾기 위한 진단이다. "
            + category_sentence,
            "",
            "**제한:** 단일 파일 안의 분포만 보여주므로 조인 후 누락, leakage, sample split 문제는 별도 QA 표와 함께 해석해야 한다.",
            "",
            f"**결론:** `{path_text}`는 P4 계약에서 바로 모델 입력으로 쓸지, QA/레지스트리/중간 산출물로만 볼지 구분해서 다음 단계에 연결한다.",
        ]
    )


def visual_eda_one(path_text: str, source_kind: str, dataset_no: int | None = None, max_plot_rows: int = 50_000) -> dict[str, object]:
    path = PROJECT_ROOT / path_text
    df = read_table(path)
    plot_df = df.sample(max_plot_rows, random_state=3085) if len(df) > max_plot_rows else df
    colprof = compact_column_profile(df)
    profile = dataset_profile(df, path, source_kind)

    display(Markdown(f"### Visual EDA: `{path_text}`"))
    display(profile)
    display(Markdown("**점검 우선 컬럼: 결측률/유니크 수 기준 상위 15개**"))
    display(
        colprof.sort_values(["missing_pct", "unique_n", "column"], ascending=[False, False, True]).head(15)
    )

    fig, axes = plt.subplots(2, 2, figsize=(15, 9), constrained_layout=True)
    axes = axes.ravel()
    _plot_dtype_mix(axes[0], df)
    _plot_missing(axes[1], colprof)
    numeric_cols = _plot_numeric_spread(axes[2], plot_df)
    category_col = _plot_category_counts(axes[3], plot_df)

    no_text = f"{dataset_no:03d}" if dataset_no is not None else "xxx"
    fig.suptitle(f"Dataset {no_text}: {short_dataset_label(path_text)}", fontsize=13)
    fig_path = FIGURE_DIR / f"dataset_{no_text}_{safe_slug(path_text)}.png"
    fig.savefig(fig_path, dpi=140, bbox_inches="tight")
    display(Markdown(f"Saved figure: `{rel(fig_path)}`"))
    plt.show()
    plt.close(fig)

    display(Markdown(_interpretation_block(path_text, df, colprof, numeric_cols, category_col)))
    display(Markdown("**미리보기 5행**"))
    display(df.head(5))

    return {
        "dataset_no": dataset_no,
        "path": path_text,
        "source_kind": source_kind,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "figure": rel(fig_path),
    }


def plot_global_source_map() -> pd.DataFrame:
    tables = load_inventory_tables()
    inventory = tables["inventory"].copy()
    columns = tables["columns"].copy()
    reuse = tables["reuse"].copy()
    target_like = tables["target_like"].copy()

    display(Markdown("## 전체 소스 인벤토리"))
    summary = (
        inventory.groupby("source_kind", dropna=False)
        .agg(
            dataset_n=("path", "count"),
            rows_sum=("rows", "sum"),
            columns_median=("columns", "median"),
            missing_cells_sum=("total_missing_cells", "sum"),
        )
        .reset_index()
    )
    display(summary)

    fig, axes = plt.subplots(2, 2, figsize=(15, 9), constrained_layout=True)
    axes = axes.ravel()

    inv_plot = inventory.dropna(subset=["rows", "columns"]).copy()
    inv_plot["label_short"] = inv_plot["path"].map(short_dataset_label)
    inv_plot.sort_values("rows", ascending=False).head(18).sort_values("rows").plot.barh(
        x="label_short", y="rows", ax=axes[0], legend=False, color="#4C78A8"
    )
    axes[0].set_title("Largest tables by rows")
    axes[0].set_xlabel("rows")
    axes[0].tick_params(axis="y", labelsize=7)

    inv_plot.sort_values("columns", ascending=False).head(18).sort_values("columns").plot.barh(
        x="label_short", y="columns", ax=axes[1], legend=False, color="#54A24B"
    )
    axes[1].set_title("Widest tables by columns")
    axes[1].set_xlabel("columns")
    axes[1].tick_params(axis="y", labelsize=7)

    dtype_counts = columns["dtype"].astype(str).value_counts().head(12).sort_values()
    dtype_counts.plot.barh(ax=axes[2], color="#B279A2")
    axes[2].set_title("Column dtype frequency")
    axes[2].set_xlabel("columns")

    reuse.head(18).sort_values("dataset_n").plot.barh(
        x="column", y="dataset_n", ax=axes[3], legend=False, color="#F58518"
    )
    axes[3].set_title("Columns reused across many files")
    axes[3].set_xlabel("dataset count")
    axes[3].tick_params(axis="y", labelsize=7)

    fig_path = FIGURE_DIR / "global_source_inventory_map.png"
    fig.savefig(fig_path, dpi=150, bbox_inches="tight")
    display(Markdown(f"Saved figure: `{rel(fig_path)}`"))
    plt.show()
    plt.close(fig)

    display(Markdown("## 타깃/성과 후보 컬럼 경로 Top 80"))
    display(target_like.sort_values(["path", "column"]).head(80))
    return summary


def plot_registry_contract_summary() -> dict[str, object]:
    lock_path = P2_3 / "p4_handoff_candidate" / "P4_CANDIDATE_HANDOFF_LOCK.json"
    registry_paths = [
        P2_3 / "p4_handoff_candidate" / "shared" / "department_model_column_registry.csv",
        P2_3 / "p4_handoff_candidate" / "shared" / "p4_feature_set_registry.csv",
        P2_3 / "p4_handoff_candidate" / "shared" / "p4_target_candidate_registry.csv",
        P2_3 / "p4_handoff_candidate" / "shared" / "model_sample_registry.csv",
    ]
    result: dict[str, object] = {}
    if lock_path.exists():
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        result["lock"] = lock
        display(Markdown(f"## Candidate handoff lock: `{rel(lock_path)}`"))
        display(pd.DataFrame([lock]))

    for registry_path in registry_paths:
        if not registry_path.exists():
            continue
        reg = read_csv_smart(registry_path)
        result[registry_path.name] = {"rows": int(reg.shape[0]), "columns": int(reg.shape[1])}
        display(Markdown(f"## Registry: `{rel(registry_path)}`"))
        display(dataset_profile(reg, registry_path, "active registry"))
        display(reg.head(40))

        count_cols = [col for col in reg.columns if str(col).lower() in {"p4_use", "feature_group", "target_family", "sample_name", "status"}]
        if not count_cols:
            count_cols = [col for col in reg.columns if reg[col].nunique(dropna=True) <= 20][:2]
        if count_cols:
            fig, axes = plt.subplots(1, len(count_cols), figsize=(6 * len(count_cols), 4), constrained_layout=True)
            axes = np.atleast_1d(axes)
            for ax, col in zip(axes, count_cols):
                counts = reg[col].astype("string").fillna("<NA>").value_counts(dropna=False).head(15).sort_values()
                counts.plot.barh(ax=ax, color="#4C78A8")
                ax.set_title(f"{registry_path.name}: {col}")
                ax.set_xlabel("rows")
            fig_path = FIGURE_DIR / f"registry_{safe_slug(registry_path.name)}.png"
            fig.savefig(fig_path, dpi=150, bbox_inches="tight")
            display(Markdown(f"Saved figure: `{rel(fig_path)}`"))
            plt.show()
            plt.close(fig)
    return result


print("PROJECT_ROOT:", PROJECT_ROOT)
print("FIGURE_DIR:", FIGURE_DIR)
