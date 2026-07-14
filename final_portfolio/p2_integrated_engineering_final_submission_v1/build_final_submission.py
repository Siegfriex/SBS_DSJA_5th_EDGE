from __future__ import annotations

import csv
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


SUBMISSION_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = SUBMISSION_ROOT.parents[2]

DATA_DIR = SUBMISSION_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
DERIVED_DIR = DATA_DIR / "derived"
PROVENANCE_DIR = SUBMISSION_ROOT / "provenance"
QA_DIR = SUBMISSION_ROOT / "qa"
FIGURES_DIR = SUBMISSION_ROOT / "figures"
REPORTS_DIR = SUBMISSION_ROOT / "reports"
LOGS_DIR = SUBMISSION_ROOT / "logs"

SOURCE_INVENTORY = PROJECT_ROOT / "workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/data_source_file_inventory.csv"
SOURCE_CATALOG = PROJECT_ROOT / "workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa/data_source_catalog.csv"
SOURCE_CATALOG_MD = PROJECT_ROOT / "workbook/p2/p2_4/p4_preprocessing_integrity_v1/reports/DATA_SOURCE_CATALOG.md"
PREPROCESSING_REPORT = PROJECT_ROOT / "workbook/p2/p2_4/p4_preprocessing_integrity_v1/reports/DATA_PREPROCESSING_INTEGRITY_REPORT.md"

BLUEPRINTS = [
    PROJECT_ROOT / "workbook/p2/p2_integrated_engineering_blueprint_v1/P2_INTEGRATED_ENGINEERING_BLUEPRINT_CELL_BY_CELL.ipynb",
    PROJECT_ROOT / "workbook/p2/p2_integrated_engineering_blueprint_v1/P2_INTEGRATED_ENGINEERING_BLUEPRINT_ONE_CELL.ipynb",
]

DERIVED_GROUPS = [
    (
        PROJECT_ROOT / "workbook/p2/p2_3/p4_handoff_candidate",
        DERIVED_DIR / "p4_handoff_candidate",
        "p4_candidate_handoff",
    ),
    (
        PROJECT_ROOT / "workbook/p2/p2_4/p4_preprocessing_integrity_v1/data",
        DERIVED_DIR / "p4_preprocessing_integrity_v1/data",
        "p4_preprocessing_data",
    ),
    (
        PROJECT_ROOT / "workbook/p2/p2_4/p4_preprocessing_integrity_v1/qa",
        DERIVED_DIR / "p4_preprocessing_integrity_v1/qa",
        "p4_preprocessing_qa",
    ),
    (
        PROJECT_ROOT / "workbook/p2/p2_4/p4_modeling_readiness_v4/artifacts",
        DERIVED_DIR / "p4_modeling_readiness_v4/artifacts",
        "p4_modeling_artifacts",
    ),
    (
        PROJECT_ROOT / "workbook/p2/p2_4/p4_modeling_readiness_v4/data",
        DERIVED_DIR / "p4_modeling_readiness_v4/data",
        "p4_modeling_data",
    ),
    (
        PROJECT_ROOT / "workbook/p2/p2_5/p5_major7_heterogeneity_v2_strict/artifacts",
        DERIVED_DIR / "p5_major7_heterogeneity_v2_strict/artifacts",
        "p5_results",
    ),
    (
        PROJECT_ROOT / "workbook/p2/p2_5/p5_major7_heterogeneity_v2_strict/reports",
        DERIVED_DIR / "p5_major7_heterogeneity_v2_strict/reports",
        "p5_reports",
    ),
    (
        PROJECT_ROOT / "workbook/p2/P2_6/artifacts",
        DERIVED_DIR / "p2_g6_strict_chain/artifacts",
        "p6_results",
    ),
    (
        PROJECT_ROOT / "workbook/p2/P2_6/qa",
        DERIVED_DIR / "p2_g6_strict_chain/qa",
        "p6_qa",
    ),
    (
        PROJECT_ROOT / "workbook/p2/P2_6/reports",
        DERIVED_DIR / "p2_g6_strict_chain/reports",
        "p6_reports",
    ),
]

ESSENTIAL_EXTENSIONS = {".csv", ".parquet", ".json", ".md", ".sha256", ".txt", ".xlsx", ".xls", ".png", ".ipynb"}


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(PROJECT_ROOT))


def rel_submission(path: Path) -> str:
    return str(path.resolve().relative_to(SUBMISSION_ROOT))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv_safe(path: Path) -> pd.DataFrame:
    for enc in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
        try:
            return pd.read_csv(path, low_memory=False, encoding=enc)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path, low_memory=False)


def profile_file(path: Path) -> dict:
    row = {
        "relative_path": rel_submission(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "shape": "",
        "loader": "unprofiled",
        "load_error": "",
    }
    try:
        suffix = path.suffix.lower()
        if suffix == ".csv":
            df = read_csv_safe(path)
            row["shape"] = f"{df.shape[0]} x {df.shape[1]}"
            row["loader"] = "csv"
        elif suffix == ".parquet":
            df = pd.read_parquet(path)
            row["shape"] = f"{df.shape[0]} x {df.shape[1]}"
            row["loader"] = "parquet"
        elif suffix in {".xlsx", ".xls"}:
            xls = pd.ExcelFile(path)
            shapes = []
            for sheet in xls.sheet_names:
                df = pd.read_excel(path, sheet_name=sheet)
                shapes.append({"sheet": sheet, "shape": [int(df.shape[0]), int(df.shape[1])]})
            row["shape"] = json.dumps(shapes, ensure_ascii=False)
            row["loader"] = "excel"
        elif suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                row["shape"] = f"dict:{len(data)}"
            elif isinstance(data, list):
                row["shape"] = f"list:{len(data)}"
            row["loader"] = "json"
    except Exception as exc:
        row["load_error"] = repr(exc)
    return row


def ensure_dirs() -> None:
    for path in [DATA_DIR, RAW_DIR, DERIVED_DIR, PROVENANCE_DIR, QA_DIR, FIGURES_DIR, REPORTS_DIR, LOGS_DIR]:
        path.mkdir(parents=True, exist_ok=True)
    (PROVENANCE_DIR / "source_catalog").mkdir(parents=True, exist_ok=True)
    (PROVENANCE_DIR / "blueprints").mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def clone_raw_sources() -> list[dict]:
    inventory = read_csv_safe(SOURCE_INVENTORY)
    rows = []
    for _, item in inventory.iterrows():
        if not bool(item.get("exists", False)):
            continue
        label = str(item["label"]).strip()
        src = PROJECT_ROOT / str(item["relative_path"])
        dst = RAW_DIR / label / src.name
        copy_file(src, dst)
        prof = profile_file(dst)
        rows.append(
            {
                "source_label": label,
                "source_relative_path": str(item["relative_path"]),
                "submission_relative_path": prof["relative_path"],
                "source_size_bytes": int(item["size_bytes"]),
                "copied_size_bytes": prof["size_bytes"],
                "source_shape": str(item.get("shape", "")),
                "copied_shape": prof["shape"],
                "source_sha256": str(item["sha256"]),
                "copied_sha256": prof["sha256"],
                "size_match": int(int(item["size_bytes"]) == int(prof["size_bytes"])),
                "hash_match": int(str(item["sha256"]) == prof["sha256"]),
                "loader": prof["loader"],
                "load_error": prof["load_error"],
            }
        )
    return rows


def clone_derived_sources() -> list[dict]:
    rows = []
    for src_root, dst_root, group in DERIVED_GROUPS:
        if not src_root.exists():
            continue
        for src in sorted(src_root.rglob("*")):
            if not src.is_file() or src.suffix.lower() not in ESSENTIAL_EXTENSIONS:
                continue
            dst = dst_root / src.relative_to(src_root)
            copy_file(src, dst)
            prof = profile_file(dst)
            rows.append(
                {
                    "derived_group": group,
                    "source_relative_path": rel(src),
                    "submission_relative_path": prof["relative_path"],
                    "size_bytes": prof["size_bytes"],
                    "shape": prof["shape"],
                    "sha256": prof["sha256"],
                    "loader": prof["loader"],
                    "load_error": prof["load_error"],
                }
            )
    return rows


def clone_provenance() -> list[dict]:
    sources = [
        SOURCE_INVENTORY,
        SOURCE_CATALOG,
        SOURCE_CATALOG_MD,
        PREPROCESSING_REPORT,
        PROJECT_ROOT / "workbook/p2/p2_3/p4_handoff_candidate/P4_CANDIDATE_HANDOFF_LOCK.json",
        PROJECT_ROOT / "workbook/p2/p2_3/p4_handoff_candidate/P4_CANDIDATE_HANDOFF_LOCK.sha256",
        PROJECT_ROOT / "workbook/p2/p2_3/p4_handoff_candidate/shared/P4_HANDOFF_MANIFEST.json",
        PROJECT_ROOT / "workbook/p2/p2_integrated_engineering_blueprint_v1/cell_runs/20260713T091641Z_5b1a3d5/HANDOFF_TO_CHATGPT.md",
        PROJECT_ROOT / "workbook/p2/p2_integrated_engineering_blueprint_v1/runs/20260713T084211Z_5b1a3d5/HANDOFF_TO_CHATGPT.md",
    ]
    rows = []
    for src in sources:
        if not src.exists():
            continue
        if src.name.startswith("data_source"):
            dst = PROVENANCE_DIR / "source_catalog" / src.name
        elif src.suffix == ".ipynb":
            dst = PROVENANCE_DIR / "blueprints" / src.name
        else:
            dst = PROVENANCE_DIR / src.name
        copy_file(src, dst)
        prof = profile_file(dst)
        rows.append(
            {
                "source_relative_path": rel(src),
                "submission_relative_path": prof["relative_path"],
                "size_bytes": prof["size_bytes"],
                "shape": prof["shape"],
                "sha256": prof["sha256"],
                "loader": prof["loader"],
                "load_error": prof["load_error"],
            }
        )
    for src in BLUEPRINTS:
        if src.exists():
            dst = PROVENANCE_DIR / "blueprints" / src.name
            copy_file(src, dst)
            prof = profile_file(dst)
            rows.append(
                {
                    "source_relative_path": rel(src),
                    "submission_relative_path": prof["relative_path"],
                    "size_bytes": prof["size_bytes"],
                    "shape": prof["shape"],
                    "sha256": prof["sha256"],
                    "loader": prof["loader"],
                    "load_error": prof["load_error"],
                }
            )
    return rows


def write_manifest(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")
    path.with_suffix(".json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.strip("\n").splitlines(keepends=True),
    }


def markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.strip("\n").splitlines(keepends=True),
    }


def build_notebook() -> None:
    cells = [
        markdown_cell(
            """
# P2 최종 제출용 통합 엔지니어링 노트북

이 노트북은 제출 폴더 내부의 `data/raw`와 `data/derived`만 참조한다. 원본 프로젝트 경로를 다시 읽지 않고, 복사된 원자료와 파생자료의 해시/형상/키 무결성을 재검증한 뒤 최종 보고서를 생성한다.
"""
        ),
        markdown_cell(
            """
## 1. 실행 환경과 제출 폴더 기준점

상대경로 기준점을 제출 폴더로 고정한다. 노트북을 프로젝트 루트에서 실행하거나 제출 폴더에서 직접 실행해도 같은 `data` 폴더를 읽도록 방어한다.
"""
        ),
        code_cell(
            """
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SUBMISSION_ROOT = Path.cwd()
if not (SUBMISSION_ROOT / "data").exists():
    candidate = Path("workbook/p2/p2_integrated_engineering_final_submission_v1").resolve()
    if candidate.exists():
        SUBMISSION_ROOT = candidate
if not (SUBMISSION_ROOT / "data").exists():
    raise FileNotFoundError("Cannot locate submission data folder")

DATA_DIR = SUBMISSION_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
DERIVED_DIR = DATA_DIR / "derived"
PROVENANCE_DIR = SUBMISSION_ROOT / "provenance"
QA_DIR = SUBMISSION_ROOT / "qa"
FIGURES_DIR = SUBMISSION_ROOT / "figures"
REPORTS_DIR = SUBMISSION_ROOT / "reports"
LOGS_DIR = SUBMISSION_ROOT / "logs"
for path in [QA_DIR, FIGURES_DIR, REPORTS_DIR, LOGS_DIR]:
    path.mkdir(parents=True, exist_ok=True)

RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def command_text(args):
    try:
        return subprocess.check_output(args, cwd=SUBMISSION_ROOT, stderr=subprocess.STDOUT, text=True).strip()
    except Exception as exc:
        return f"unavailable: {exc!r}"

ENV = {
    "run_id": RUN_ID,
    "submission_root": str(SUBMISSION_ROOT),
    "python": sys.version,
    "platform": platform.platform(),
    "pandas": pd.__version__,
    "git_head": command_text(["git", "rev-parse", "--short", "HEAD"]),
    "created_at_utc": datetime.now(timezone.utc).isoformat(),
}
(LOGS_DIR / "execution_environment.json").write_text(json.dumps(ENV, ensure_ascii=False, indent=2), encoding="utf-8")
ENV
"""
        ),
        markdown_cell(
            """
## 2. 공통 로더와 해시 함수

CSV 인코딩, Excel sheet shape, Parquet row/column shape를 같은 규칙으로 읽어 원자료와 복사본을 비교한다.
"""
        ),
        code_cell(
            """
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_csv_safe(path: Path) -> pd.DataFrame:
    for enc in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
        try:
            return pd.read_csv(path, low_memory=False, encoding=enc)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path, low_memory=False)

def shape_of(path: Path) -> tuple[str, str, str]:
    try:
        suffix = path.suffix.lower()
        if suffix == ".csv":
            df = read_csv_safe(path)
            return f"{df.shape[0]} x {df.shape[1]}", "csv", ""
        if suffix == ".parquet":
            df = pd.read_parquet(path)
            return f"{df.shape[0]} x {df.shape[1]}", "parquet", ""
        if suffix in {".xlsx", ".xls"}:
            xls = pd.ExcelFile(path)
            shapes = []
            for sheet in xls.sheet_names:
                df = pd.read_excel(path, sheet_name=sheet)
                shapes.append({"sheet": sheet, "shape": [int(df.shape[0]), int(df.shape[1])]})
            return json.dumps(shapes, ensure_ascii=False), "excel", ""
        if suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return f"dict:{len(data)}", "json", ""
            if isinstance(data, list):
                return f"list:{len(data)}", "json", ""
        return "", "unprofiled", ""
    except Exception as exc:
        return "", "load_error", repr(exc)

def pct_range_violations(df: pd.DataFrame) -> int:
    pct_cols = [c for c in df.columns if str(c).endswith("_pct") or str(c).endswith("_rate")]
    violations = 0
    for col in pct_cols:
        vals = pd.to_numeric(df[col], errors="coerce").dropna()
        if vals.empty:
            continue
        violations += int(((vals < 0) | (vals > 100)).sum())
    return violations

def save_csv(df: pd.DataFrame, path: Path) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return df
"""
        ),
        markdown_cell(
            """
## 3. 제출 패키지 원자료 카탈로그

`data/raw`는 원자료 30개를 label별 하위 폴더에 복사한 영역이다. 아래 표는 복사 당시 원본 경로, 복사본 경로, 해시, 크기, shape를 고정한 manifest다.
"""
        ),
        code_cell(
            """
raw_manifest = read_csv_safe(RAW_DIR / "FINAL_RAW_DATA_MANIFEST.csv")
derived_manifest = read_csv_safe(DERIVED_DIR / "FINAL_DERIVED_DATA_MANIFEST.csv")
provenance_manifest = read_csv_safe(PROVENANCE_DIR / "FINAL_PROVENANCE_MANIFEST.csv")
source_catalog = read_csv_safe(PROVENANCE_DIR / "source_catalog/data_source_catalog.csv")

catalog_summary = pd.DataFrame([
    {"area": "raw", "files": len(raw_manifest), "bytes": int(raw_manifest["copied_size_bytes"].sum())},
    {"area": "derived", "files": len(derived_manifest), "bytes": int(derived_manifest["size_bytes"].sum())},
    {"area": "provenance", "files": len(provenance_manifest), "bytes": int(provenance_manifest["size_bytes"].sum())},
    {"area": "source_catalog_entries", "files": len(source_catalog), "bytes": None},
])
save_csv(catalog_summary, QA_DIR / "catalog_summary.csv")
catalog_summary
"""
        ),
        markdown_cell(
            """
## 4. 원자료 복사 무결성 검증

제출 폴더 내부 복사본의 해시와 크기가 원본 inventory와 일치하는지 다시 계산한다. 이 검증이 통과해야 제출 폴더의 `data/raw`를 원자료 묶음으로 신뢰할 수 있다.
"""
        ),
        code_cell(
            """
raw_checks = []
for _, row in raw_manifest.iterrows():
    path = SUBMISSION_ROOT / row["submission_relative_path"]
    copied_sha = sha256_file(path)
    copied_shape, loader, load_error = shape_of(path)
    raw_checks.append({
        "source_label": row["source_label"],
        "submission_relative_path": row["submission_relative_path"],
        "exists": path.exists(),
        "source_sha256": row["source_sha256"],
        "copied_sha256_recomputed": copied_sha,
        "hash_match": copied_sha == row["source_sha256"],
        "source_size_bytes": int(row["source_size_bytes"]),
        "copied_size_bytes_recomputed": int(path.stat().st_size),
        "size_match": int(path.stat().st_size) == int(row["source_size_bytes"]),
        "source_shape": str(row["source_shape"]),
        "copied_shape_recomputed": copied_shape,
        "loader": loader,
        "load_error": load_error,
    })
raw_integrity = save_csv(pd.DataFrame(raw_checks), QA_DIR / "raw_data_integrity.csv")
raw_integrity_pass = bool(raw_integrity["hash_match"].all() and raw_integrity["size_match"].all() and raw_integrity["load_error"].fillna("").eq("").all())
raw_integrity_pass, raw_integrity[["source_label", "hash_match", "size_match", "copied_shape_recomputed"]].head(10)
"""
        ),
        markdown_cell(
            """
## 5. 파생자료와 provenance 무결성 검증

`data/derived`는 D01-D08 handoff, preprocessing integrity outputs, modeling/sample registries, P5/P6 결과 읽기용 파일을 담는다. 여기서는 manifest 해시와 현재 파일 해시가 일치하는지 확인한다.
"""
        ),
        code_cell(
            """
derived_checks = []
for _, row in derived_manifest.iterrows():
    path = SUBMISSION_ROOT / row["submission_relative_path"]
    actual_sha = sha256_file(path)
    actual_shape, loader, load_error = shape_of(path)
    derived_checks.append({
        "derived_group": row["derived_group"],
        "submission_relative_path": row["submission_relative_path"],
        "exists": path.exists(),
        "manifest_sha256": row["sha256"],
        "sha256_recomputed": actual_sha,
        "hash_match": actual_sha == row["sha256"],
        "manifest_shape": row.get("shape", ""),
        "shape_recomputed": actual_shape,
        "loader": loader,
        "load_error": load_error,
    })
derived_integrity = save_csv(pd.DataFrame(derived_checks), QA_DIR / "derived_data_integrity.csv")
derived_integrity_pass = bool(derived_integrity["hash_match"].all() and derived_integrity["load_error"].fillna("").eq("").all())
derived_integrity_pass, derived_integrity.groupby("derived_group").size().reset_index(name="files")
"""
        ),
        markdown_cell(
            """
## 6. D08 분석 mart 키/범위 무결성

최종 분석의 기준 grain은 `school x normalized department x 2024`이며, `outcome_row_id`는 행 단위 안정 키다. 중복 키와 퍼센트 범위 위반이 없어야 한다.
"""
        ),
        code_cell(
            """
d08_path = DERIVED_DIR / "p4_handoff_candidate/shared/mart_department_model_base_2024.parquet"
d08 = pd.read_parquet(d08_path)
d08_sha = sha256_file(d08_path)

key_audit = pd.DataFrame([
    {
        "dataset": "D08_analysis_mart",
        "rows": int(d08.shape[0]),
        "columns": int(d08.shape[1]),
        "sha256": d08_sha,
        "outcome_row_id_duplicates": int(d08["outcome_row_id"].duplicated().sum()) if "outcome_row_id" in d08.columns else None,
        "pct_range_violations": pct_range_violations(d08),
        "school_uid_nunique": int(d08["school_uid"].nunique()) if "school_uid" in d08.columns else None,
        "major_group_7_nunique": int(d08["major_group_7"].nunique()) if "major_group_7" in d08.columns else None,
    }
])
mart_integrity_pass = bool(
    key_audit.loc[0, "rows"] == 10242
    and key_audit.loc[0, "columns"] == 151
    and key_audit.loc[0, "outcome_row_id_duplicates"] == 0
    and key_audit.loc[0, "pct_range_violations"] == 0
)
save_csv(key_audit, QA_DIR / "active_mart_integrity.csv")
mart_integrity_pass, key_audit
"""
        ),
        markdown_cell(
            """
## 7. 원천 계보 요약

source catalog 9개 항목을 기준으로 어떤 원천이 어떤 final column block과 D08 산출물에 들어왔는지 제출용 표로 정리한다.
"""
        ),
        code_cell(
            """
source_lineage = source_catalog[[
    "catalog_id",
    "official_source",
    "official_url",
    "local_source_files",
    "derived_outputs",
    "grain_used",
    "final_column_blocks",
    "used_content",
    "direct_download_url_status",
]].copy()
save_csv(source_lineage, QA_DIR / "source_lineage_summary.csv")
source_lineage
"""
        ),
        markdown_cell(
            """
## 8. 변수 역할/feature registry 검증

모델링과 해석에서 쓸 수 있는 컬럼은 registry로 제한한다. registry에 있지만 D08에 없는 컬럼과 D08에는 있지만 registry에 없는 컬럼을 분리해 기록한다.
"""
        ),
        code_cell(
            """
registry_path = DERIVED_DIR / "p4_handoff_candidate/shared/department_model_column_registry.csv"
feature_set_path = DERIVED_DIR / "p4_handoff_candidate/shared/p4_feature_set_registry.csv"
registry = read_csv_safe(registry_path)
feature_sets = read_csv_safe(feature_set_path)

column_field = next((c for c in ["column", "column_name", "feature", "variable"] if c in registry.columns), None)
if column_field is None:
    registry_columns = set()
else:
    registry_columns = set(registry[column_field].dropna().astype(str))

d08_columns = set(map(str, d08.columns))
registry_audit = pd.DataFrame([
    {"metric": "registry_rows", "value": int(len(registry))},
    {"metric": "feature_set_rows", "value": int(len(feature_sets))},
    {"metric": "registry_columns_in_d08", "value": int(len(registry_columns & d08_columns))},
    {"metric": "registry_columns_missing_from_d08", "value": int(len(registry_columns - d08_columns))},
    {"metric": "d08_columns_missing_from_registry", "value": int(len(d08_columns - registry_columns)) if registry_columns else None},
])
registry_missing = pd.DataFrame({"column": sorted(registry_columns - d08_columns)})
d08_unregistered = pd.DataFrame({"column": sorted(d08_columns - registry_columns)})
save_csv(registry_audit, QA_DIR / "registry_audit.csv")
save_csv(registry_missing, QA_DIR / "registry_missing_from_d08.csv")
save_csv(d08_unregistered, QA_DIR / "d08_columns_missing_from_registry.csv")

registry_pass = bool(len(registry_columns - d08_columns) == 0)
registry_pass, registry_audit
"""
        ),
        markdown_cell(
            """
## 9. sample/split 일관성 검증

D08에는 split 컬럼을 직접 넣지 않는다. 학교 단위 split은 `school_uid`로 `dim_school_split`에 결합해 사용한다.
"""
        ),
        code_cell(
            """
split = read_csv_safe(DERIVED_DIR / "p4_handoff_candidate/shared/dim_school_split.csv")
membership = pd.read_parquet(DERIVED_DIR / "p4_handoff_candidate/shared/model_sample_membership.parquet")
sample_registry = read_csv_safe(DERIVED_DIR / "p4_handoff_candidate/shared/model_sample_registry.csv")

split_key = "school_uid" if "school_uid" in split.columns and "school_uid" in d08.columns else None
if split_key:
    d08_split = d08[["outcome_row_id", split_key]].merge(split, on=split_key, how="left", validate="many_to_one")
    split_missing_rows = int(d08_split["split"].isna().sum()) if "split" in d08_split.columns else int(d08_split.iloc[:, -1].isna().sum())
    school_leakage = int(split.groupby(split_key).size().gt(1).sum())
else:
    split_missing_rows = None
    school_leakage = None

membership_key = "outcome_row_id" if "outcome_row_id" in membership.columns else None
membership_duplicates = int(membership[membership_key].duplicated().sum()) if membership_key else None
membership_not_in_d08 = int((~membership[membership_key].isin(d08["outcome_row_id"])).sum()) if membership_key and "outcome_row_id" in d08.columns else None

sample_audit = pd.DataFrame([
    {"metric": "split_rows", "value": int(len(split))},
    {"metric": "split_school_uid_duplicates", "value": int(split["school_uid"].duplicated().sum()) if "school_uid" in split.columns else None},
    {"metric": "d08_rows_without_split_after_school_merge", "value": split_missing_rows},
    {"metric": "school_split_duplicate_assignments", "value": school_leakage},
    {"metric": "membership_rows", "value": int(len(membership))},
    {"metric": "membership_outcome_row_id_duplicates", "value": membership_duplicates},
    {"metric": "membership_rows_not_in_d08", "value": membership_not_in_d08},
    {"metric": "sample_registry_rows", "value": int(len(sample_registry))},
])
sample_split_pass = bool(
    sample_audit.loc[sample_audit["metric"].eq("split_school_uid_duplicates"), "value"].iloc[0] == 0
    and sample_audit.loc[sample_audit["metric"].eq("d08_rows_without_split_after_school_merge"), "value"].iloc[0] == 0
    and sample_audit.loc[sample_audit["metric"].eq("membership_outcome_row_id_duplicates"), "value"].iloc[0] == 0
    and sample_audit.loc[sample_audit["metric"].eq("membership_rows_not_in_d08"), "value"].iloc[0] == 0
)
save_csv(sample_audit, QA_DIR / "sample_split_integrity.csv")
sample_split_pass, sample_audit
"""
        ),
        markdown_cell(
            """
## 10. target coverage와 분포 확인

핵심 target 후보 3개를 기준으로 결측, 최소/최대, 평균을 확인한다. 값의 범위 검증은 앞선 D08 무결성 gate에 포함되어 있다.
"""
        ),
        code_cell(
            """
target_cols = [c for c in ["a_rate_pct", "health_employment_rate_pct", "graduate_school_progression_rate_pct"] if c in d08.columns]
target_profile_rows = []
for col in target_cols:
    vals = pd.to_numeric(d08[col], errors="coerce")
    target_profile_rows.append({
        "target": col,
        "non_null": int(vals.notna().sum()),
        "missing": int(vals.isna().sum()),
        "min": float(vals.min()) if vals.notna().any() else None,
        "mean": float(vals.mean()) if vals.notna().any() else None,
        "median": float(vals.median()) if vals.notna().any() else None,
        "max": float(vals.max()) if vals.notna().any() else None,
    })
target_profile = save_csv(pd.DataFrame(target_profile_rows), QA_DIR / "target_coverage_profile.csv")
target_pass = bool(len(target_cols) == 3 and target_profile["non_null"].min() > 0)
target_pass, target_profile
"""
        ),
        markdown_cell(
            """
## 11. 결측/상수 컬럼과 문맥 변수 점검

결측은 삭제 대상만이 아니라 source coverage와 join grain의 증거다. 전체 결측률 상위 컬럼과 all-null 컬럼을 분리한다.
"""
        ),
        code_cell(
            """
missing = pd.DataFrame({
    "column": d08.columns,
    "missing_count": [int(d08[c].isna().sum()) for c in d08.columns],
    "missing_pct": [float(d08[c].isna().mean() * 100) for c in d08.columns],
    "nunique_dropna": [int(d08[c].nunique(dropna=True)) for c in d08.columns],
})
missing = missing.sort_values(["missing_pct", "column"], ascending=[False, True]).reset_index(drop=True)
all_null_constant = missing[(missing["missing_pct"].eq(100.0)) | (missing["nunique_dropna"].le(1))].copy()
save_csv(missing, QA_DIR / "missingness_profile.csv")
save_csv(all_null_constant, QA_DIR / "all_null_constant_columns.csv")
missing.head(20)
"""
        ),
        markdown_cell(
            """
## 12. 제출용 시각화

검증 결과를 한눈에 확인할 수 있도록 target 분포, 원천 계보, split 분포를 그림으로 저장한다.
"""
        ),
        code_cell(
            """
plt.rcParams["axes.unicode_minus"] = False

fig, axes = plt.subplots(1, len(target_cols), figsize=(5 * max(1, len(target_cols)), 4))
if len(target_cols) == 1:
    axes = [axes]
for ax, col in zip(axes, target_cols):
    vals = pd.to_numeric(d08[col], errors="coerce").dropna()
    ax.hist(vals, bins=30, color="#2F6F73", alpha=0.85)
    ax.set_title(col)
    ax.set_xlabel("percent")
    ax.set_ylabel("rows")
fig.tight_layout()
fig.savefig(FIGURES_DIR / "target_distributions.png", dpi=160)
plt.close(fig)

lineage_counts = source_catalog[["catalog_id", "final_column_blocks"]].copy()
lineage_counts["block_count"] = lineage_counts["final_column_blocks"].fillna("").astype(str).str.split(",").map(len)
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.barh(lineage_counts["catalog_id"], lineage_counts["block_count"], color="#5975A4")
ax.set_xlabel("declared column block count")
ax.set_title("Source lineage coverage")
fig.tight_layout()
fig.savefig(FIGURES_DIR / "source_lineage_blocks.png", dpi=160)
plt.close(fig)

if split_key and "split" in split.columns:
    split_counts = d08[[split_key]].merge(split[[split_key, "split"]], on=split_key, how="left")["split"].value_counts(dropna=False).reset_index()
    split_counts.columns = ["split", "rows"]
    save_csv(split_counts, QA_DIR / "split_row_counts.csv")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(split_counts["split"].astype(str), split_counts["rows"], color="#6B8E23")
    ax.set_ylabel("D08 rows")
    ax.set_title("School split row distribution")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "split_row_distribution.png", dpi=160)
    plt.close(fig)

sorted(p.name for p in FIGURES_DIR.glob("*.png"))
"""
        ),
        markdown_cell(
            """
## 13. 기존 P5/P6 결과 읽기

최종 제출 노트북은 모델 결과를 재학습하지 않고, 검증된 strict-chain 결과 파일을 읽어 해석에 필요한 숫자만 재표준화한다.
"""
        ),
        code_cell(
            """
p5_insight_path = DERIVED_DIR / "p5_major7_heterogeneity_v2_strict/artifacts/P5_STRICT_INSIGHT_SUMMARY.csv"
p5_diff_path = DERIVED_DIR / "p5_major7_heterogeneity_v2_strict/artifacts/P5_TABLE3_PROGRESSION_MINUS_EMPLOYMENT_AME.csv"
p6_key_numbers_path = DERIVED_DIR / "p2_g6_strict_chain/artifacts/P2_G6_1_KEY_NUMBERS.csv"
p6_status_path = DERIVED_DIR / "p2_g6_strict_chain/qa/P2_G6_1_STATUS_TABLE.csv"

p5_insight = read_csv_safe(p5_insight_path) if p5_insight_path.exists() else pd.DataFrame()
p5_diff = read_csv_safe(p5_diff_path) if p5_diff_path.exists() else pd.DataFrame()
p6_key_numbers = read_csv_safe(p6_key_numbers_path) if p6_key_numbers_path.exists() else pd.DataFrame()
p6_status = read_csv_safe(p6_status_path) if p6_status_path.exists() else pd.DataFrame()

phase_result_readout = pd.DataFrame([
    {"artifact": "P5_STRICT_INSIGHT_SUMMARY", "exists": p5_insight_path.exists(), "rows": len(p5_insight), "columns": len(p5_insight.columns)},
    {"artifact": "P5_TABLE3_PROGRESSION_MINUS_EMPLOYMENT_AME", "exists": p5_diff_path.exists(), "rows": len(p5_diff), "columns": len(p5_diff.columns)},
    {"artifact": "P2_G6_1_KEY_NUMBERS", "exists": p6_key_numbers_path.exists(), "rows": len(p6_key_numbers), "columns": len(p6_key_numbers.columns)},
    {"artifact": "P2_G6_1_STATUS_TABLE", "exists": p6_status_path.exists(), "rows": len(p6_status), "columns": len(p6_status.columns)},
])
phase_results_pass = bool(phase_result_readout["exists"].all() and (phase_result_readout["rows"] > 0).all())
save_csv(phase_result_readout, QA_DIR / "phase_result_readout.csv")
phase_results_pass, phase_result_readout
"""
        ),
        markdown_cell(
            """
## 14. 최종 gate matrix와 issue register

PASS는 제출 폴더가 자체적으로 원자료 복사본, 파생자료, D08 mart, sample/split, target coverage를 검증했다는 뜻이다. WARN은 해석 시 명시해야 할 제한이다.
"""
        ),
        code_cell(
            """
status_rows = [
    {"gate": "G01_raw_data_clone", "status": "PASS" if raw_integrity_pass else "FAIL", "evidence": "qa/raw_data_integrity.csv"},
    {"gate": "G02_derived_data_clone", "status": "PASS" if derived_integrity_pass else "FAIL", "evidence": "qa/derived_data_integrity.csv"},
    {"gate": "G03_active_mart_integrity", "status": "PASS" if mart_integrity_pass else "FAIL", "evidence": "qa/active_mart_integrity.csv"},
    {"gate": "G04_source_lineage", "status": "PASS" if len(source_lineage) == 9 else "WARN", "evidence": "qa/source_lineage_summary.csv"},
    {"gate": "G05_registry_coverage", "status": "PASS" if registry_pass else "WARN", "evidence": "qa/registry_audit.csv"},
    {"gate": "G06_sample_split", "status": "PASS" if sample_split_pass else "FAIL", "evidence": "qa/sample_split_integrity.csv"},
    {"gate": "G07_target_coverage", "status": "PASS" if target_pass else "FAIL", "evidence": "qa/target_coverage_profile.csv"},
    {"gate": "G08_phase_result_readout", "status": "PASS" if phase_results_pass else "WARN", "evidence": "qa/phase_result_readout.csv"},
]
status_matrix = save_csv(pd.DataFrame(status_rows), QA_DIR / "final_status_matrix.csv")

issues = [
    {
        "issue_id": "WARN_D08_SPLIT_EXTERNAL",
        "severity": "WARN",
        "evidence": "D08 has no direct split column; use school_uid merge to dim_school_split",
        "submission_handling": "sample/split integrity gate verifies the external split merge",
    },
    {
        "issue_id": "WARN_DIRECT_URL_LIMIT",
        "severity": "WARN",
        "evidence": "some source direct download URLs are portal-level in the local source catalog",
        "submission_handling": "local file hashes and official portal URLs are retained as provenance anchors",
    },
    {
        "issue_id": "WARN_Q_BRANCH_BLOCKED",
        "severity": "WARN",
        "evidence": "P6 Q/selectivity branch is not interpreted as launch-ready",
        "submission_handling": "final report restricts claims to validated D08 and strict-chain readout",
    },
]
if not registry_pass:
    issues.append({
        "issue_id": "WARN_REGISTRY_COVERAGE",
        "severity": "WARN",
        "evidence": "registry and D08 columns are not perfectly symmetric",
        "submission_handling": "missing/unregistered columns are written to qa/",
    })
issue_register = save_csv(pd.DataFrame(issues), QA_DIR / "final_issue_register.csv")

if (status_matrix["status"] == "FAIL").any():
    FINAL_STATUS = "FAIL"
elif (status_matrix["status"] == "WARN").any() or len(issue_register) > 0:
    FINAL_STATUS = "PASS_WITH_WARNINGS"
else:
    FINAL_STATUS = "PASS"

FINAL_STATUS, status_matrix
"""
        ),
        markdown_cell(
            """
## 15. 최종 보고서와 패키지 manifest 생성

마지막 셀은 제출 폴더의 최종 상태를 Markdown 보고서와 package manifest로 저장한다.
"""
        ),
        code_cell(
            """
def df_to_markdown_table(df):
    if df.empty:
        return "_행 없음_"
    text_df = df.copy().astype(str)
    headers = list(text_df.columns)
    rows = text_df.values.tolist()
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\\n".join(lines)

report_lines = [
    "# P2 최종 제출 패키지 보고서",
    "",
    f"- FINAL_STATUS: `{FINAL_STATUS}`",
    f"- RUN_ID: `{RUN_ID}`",
    f"- submission_root: `{SUBMISSION_ROOT}`",
    f"- active D08: `data/derived/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet`",
    f"- active D08 shape: `{d08.shape[0]} x {d08.shape[1]}`",
    f"- active D08 sha256: `{d08_sha}`",
    f"- raw source files: `{len(raw_manifest)}`",
    f"- derived/provenance files: `{len(derived_manifest)} / {len(provenance_manifest)}`",
    "",
    "## Gate Matrix",
    "",
    df_to_markdown_table(status_matrix),
    "",
    "## Issue Register",
    "",
    df_to_markdown_table(issue_register),
    "",
    "## Key Evidence Files",
    "",
    "- `qa/raw_data_integrity.csv`",
    "- `qa/derived_data_integrity.csv`",
    "- `qa/active_mart_integrity.csv`",
    "- `qa/sample_split_integrity.csv`",
    "- `qa/target_coverage_profile.csv`",
    "- `qa/final_status_matrix.csv`",
    "- `FINAL_SUBMISSION_PACKAGE_MANIFEST.csv`",
    "",
    "## Re-run",
    "",
    "```bash",
    "MPLCONFIGDIR=/tmp/mplconfig .venv/bin/jupyter nbconvert --to notebook --execute workbook/p2/p2_integrated_engineering_final_submission_v1/P2_FINAL_SUBMISSION.ipynb --inplace --ExecutePreprocessor.timeout=900",
    "```",
]
(REPORTS_DIR / "FINAL_SUBMISSION_REPORT.md").write_text("\\n".join(report_lines), encoding="utf-8")
(LOGS_DIR / "final_status.json").write_text(
    json.dumps({"final_status": FINAL_STATUS, "run_id": RUN_ID, "status_counts": status_matrix["status"].value_counts().to_dict()}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

manifest_skip = {
    "P2_FINAL_SUBMISSION.ipynb",
    "FINAL_SUBMISSION_PACKAGE_MANIFEST.csv",
    "FINAL_SUBMISSION_PACKAGE_MANIFEST.json",
}
package_rows = []
for path in sorted(SUBMISSION_ROOT.rglob("*")):
    if path.is_file():
        relative_path = str(path.relative_to(SUBMISSION_ROOT))
        if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        if relative_path in manifest_skip:
            continue
        package_rows.append({
            "relative_path": relative_path,
            "size_bytes": int(path.stat().st_size),
            "sha256": sha256_file(path),
        })
package_manifest = save_csv(pd.DataFrame(package_rows), SUBMISSION_ROOT / "FINAL_SUBMISSION_PACKAGE_MANIFEST.csv")
(SUBMISSION_ROOT / "FINAL_SUBMISSION_PACKAGE_MANIFEST.json").write_text(
    json.dumps(package_rows, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
FINAL_STATUS
"""
        ),
    ]

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": ".venv", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    (SUBMISSION_ROOT / "P2_FINAL_SUBMISSION.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")


def write_readme(raw_count: int, derived_count: int, provenance_count: int) -> None:
    lines = [
        "# P2 Integrated Engineering Final Submission",
        "",
        "This folder is a self-contained submission package. The final notebook reads only files inside this folder.",
        "",
        "## Main Files",
        "",
        "- `P2_FINAL_SUBMISSION.ipynb`: final executable notebook",
        "- `data/raw/`: cloned original source files",
        "- `data/derived/`: cloned D01-D08 handoff, integrity outputs, registries, and phase result readouts",
        "- `provenance/`: source catalog, handoff locks, and blueprint notebooks",
        "- `qa/`: integrity check outputs generated by the notebook",
        "- `reports/FINAL_SUBMISSION_REPORT.md`: final status report after notebook execution",
        "",
        "## Build Summary",
        "",
        f"- raw files: `{raw_count}`",
        f"- derived files: `{derived_count}`",
        f"- provenance files: `{provenance_count}`",
        "",
        "## Re-run",
        "",
        "```bash",
        "MPLCONFIGDIR=/tmp/mplconfig .venv/bin/jupyter nbconvert --to notebook --execute workbook/p2/p2_integrated_engineering_final_submission_v1/P2_FINAL_SUBMISSION.ipynb --inplace --ExecutePreprocessor.timeout=900",
        "```",
    ]
    (SUBMISSION_ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    raw_rows = clone_raw_sources()
    derived_rows = clone_derived_sources()
    provenance_rows = clone_provenance()

    write_manifest(raw_rows, RAW_DIR / "FINAL_RAW_DATA_MANIFEST.csv")
    write_manifest(derived_rows, DERIVED_DIR / "FINAL_DERIVED_DATA_MANIFEST.csv")
    write_manifest(provenance_rows, PROVENANCE_DIR / "FINAL_PROVENANCE_MANIFEST.csv")

    build_notebook()
    write_readme(len(raw_rows), len(derived_rows), len(provenance_rows))

    build_summary = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(PROJECT_ROOT),
        "submission_root": str(SUBMISSION_ROOT),
        "python": sys.version,
        "platform": platform.platform(),
        "raw_files": len(raw_rows),
        "derived_files": len(derived_rows),
        "provenance_files": len(provenance_rows),
    }
    (LOGS_DIR / "build_summary.json").write_text(json.dumps(build_summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(build_summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
