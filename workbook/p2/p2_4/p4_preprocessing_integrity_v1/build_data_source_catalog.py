from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path("/home/sieg/projects-wsl/SBS_dataScience")
OUT_ROOT = PROJECT_ROOT / "workbook/p2/p2_4/p4_preprocessing_integrity_v1"
QA_DIR = OUT_ROOT / "qa"
REPORT_DIR = OUT_ROOT / "reports"
MANIFEST_PATH = PROJECT_ROOT / "workbook/p2/p2_3/p4_handoff_candidate/shared/P4_HANDOFF_MANIFEST.json"
REGISTRY_V4_PATH = PROJECT_ROOT / "workbook/p2/p2_4/p4_modeling_readiness_v4/artifacts/department_model_column_registry_v4.csv"
D08_PATH = PROJECT_ROOT / "workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet"
DIM_SPLIT_PATH = PROJECT_ROOT / "workbook/p2/p2_3/p4_handoff_candidate/shared/dim_school_split.csv"
PHASE_SAMPLE_REGISTRY_PATH = PROJECT_ROOT / "workbook/p2/p2_4/p4_modeling_readiness_v4/artifacts/P4_PHASE_SAMPLE_REGISTRY_FINAL.csv"


OFFICIAL_LINKS = {
    "KEDI_EDUCATION_STATISTICS": "https://kess.kedi.re.kr/",
    "ACADEMYINFO": "https://www.academyinfo.go.kr/",
    "ADIGA": "https://www.adiga.kr/",
    "KEIS_GOMS": "https://survey.keis.or.kr/",
    "KEIS_GOMS_TOPIC_STATS": "https://analysis.keis.or.kr/",
}


SOURCE_FILES = [
    ("KEDI_raw_excel", "workbook/p2/p2_2/final/data/2024년 고등 학교별X학과별 입학정원 지원 입학 학생 외국인학생 졸업 교원_240912H.xlsx"),
    ("grade_raw", "workbook/p2/p2_2/P2__전체대학학점비율.csv"),
    ("employment_raw", "workbook/p2/p2_2/p2_취업률_데이터.csv"),
    ("progression_raw", "workbook/p2/p2_2/p2_상위대학_진학률.csv"),
    ("policy_raw", "workbook/p2/p2_2/학점포기제도현황.xlsx"),
    ("adiga_raw", "workbook/p2/p2_2/data/crawl_2024_admission_full/02_admission_result_raw_2024_merged.csv"),
    ("adiga_registry", "workbook/p2/p2_2/data/crawl_2024_admission_full/01_crawl_source_registry_merged.csv"),
    ("adiga_seed", "workbook/p2/p2_2/data/crawl_2024_admission_full/00_crawl_seed_university_2024_merged.csv"),
    ("adiga_department_proxy", "workbook/p2/p2_2/final/admission/P2_admission_proxy_v3_by_department.csv"),
    ("outcome_spine", "workbook/p2/p2_3/P2_G2_정시입결.csv"),
    ("wage_reference", "workbook/p2/p2_3/P2_G2_임금분류_학부대학원.CSV"),
    ("wage_quartile", "workbook/p2/p2_3/P2_G2_임금분류_학부대학원_사분위기준.CSV"),
    ("wage_contract", "workbook/p2/p2_3/P2_G2_임금분류_학부대학원_컬럼설명.CSV"),
    ("job_cert_bridge_raw", "workbook/p2/p2_3/P2_G2_직무별_자격증매핑.CSV"),
    ("goms_distribution_long", "workbook/p2/p2_2/data/goms_subject_crawl/normalized/goms_distribution_long.csv"),
    ("goms_continuous_long", "workbook/p2/p2_2/data/goms_subject_crawl/normalized/goms_continuous_long.csv"),
    ("goms_topic_registry", "workbook/p2/p2_2/data/goms_subject_crawl/00_topic_registry.csv"),
    ("goms_d07_profile", "workbook/p2/p2_3/shared_handoff/goms_major_profile_recent.parquet"),
    ("D01_headcount_master", "workbook/p2/p2_3/p4_handoff_candidate/local1/dept_headcount_master_2024.parquet"),
    ("D02_outcomes", "workbook/p2/p2_3/p4_handoff_candidate/local1/dept_outcomes_2024.parquet"),
    ("D03_core", "workbook/p2/p2_3/p4_handoff_candidate/local1/dept_master_2024_core.parquet"),
    ("D04_wage_reference", "workbook/p2/p2_3/p4_handoff_candidate/local1/wage_reference_by_major.parquet"),
    ("D05_job_cert_bridge", "workbook/p2/p2_3/p4_handoff_candidate/local1/job_cert_bridge.parquet"),
    ("bridge_school_alias", "workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_school_alias.csv"),
    ("bridge_campus_alias", "workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_campus_alias.csv"),
    ("bridge_department_alias", "workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_department_alias.csv"),
    ("bridge_outcome_headcount", "workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_outcome_headcount_v2.csv"),
    ("bridge_department_major7", "workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_department_major7_v2.csv"),
    ("dim_school_split", "workbook/p2/p2_3/p4_handoff_candidate/shared/dim_school_split.csv"),
    ("D08_analysis_mart", "workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet"),
]


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def shape_for_file(path: Path) -> tuple[Any, str | None]:
    if not path.exists():
        return None, None
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        return list(pd.read_parquet(path).shape), "parquet"
    if suffix == ".csv":
        for enc in ["utf-8-sig", "utf-8", "cp949", "euc-kr"]:
            try:
                df = pd.read_csv(path, low_memory=False, encoding=enc)
                return list(df.shape), enc
            except UnicodeDecodeError:
                continue
        df = pd.read_csv(path, low_memory=False)
        return list(df.shape), "pandas_default"
    if suffix in {".xlsx", ".xls"}:
        xls = pd.ExcelFile(path)
        sheets = []
        for sheet in xls.sheet_names:
            df = pd.read_excel(path, sheet_name=sheet)
            sheets.append({"sheet": sheet, "shape": list(df.shape)})
        return sheets, "excel"
    if suffix == ".json":
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        return {"top_level_keys": list(data.keys()) if isinstance(data, dict) else None}, "json"
    return None, "unprofiled"


def file_inventory() -> pd.DataFrame:
    rows = []
    expected_hashes = {}
    if MANIFEST_PATH.exists():
        with MANIFEST_PATH.open(encoding="utf-8") as f:
            manifest = json.load(f)
        expected_hashes.update(manifest.get("source_hashes", {}))
        expected_hashes.update(manifest.get("output_hashes", {}))
        expected_hashes["local2_handoff_hash"] = manifest.get("local2_handoff_hash")
    for label, rel in SOURCE_FILES:
        path = PROJECT_ROOT / rel
        shape, loader = shape_for_file(path)
        sha = sha256_file(path)
        rows.append(
            {
                "label": label,
                "official_source_hint": official_hint_for_label(label),
                "relative_path": rel,
                "absolute_path": str(path),
                "exists": path.exists(),
                "size_bytes": path.stat().st_size if path.exists() else None,
                "shape": json.dumps(shape, ensure_ascii=False),
                "loader_or_encoding": loader,
                "sha256": sha,
                "manifest_hash_reference": hash_reference_for_label(label, expected_hashes),
                "hash_matches_known_manifest": sha in set(v for v in expected_hashes.values() if v),
            }
        )
    return pd.DataFrame(rows)


def official_hint_for_label(label: str) -> str:
    if label.startswith("KEDI") or label.startswith("D01"):
        return "KEDI_EDUCATION_STATISTICS"
    if label in {"grade_raw", "employment_raw", "progression_raw", "policy_raw", "outcome_spine", "D02_outcomes"}:
        return "ACADEMYINFO/local_outcome_spine"
    if label.startswith("adiga"):
        return "ADIGA"
    if label.startswith("goms"):
        return "KEIS_GOMS"
    if label.startswith("wage") or label.startswith("job_cert") or label.startswith("D04") or label.startswith("D05"):
        return "ACADEMYINFO/major_context_local_contract"
    if label.startswith("bridge") or label.startswith("dim") or label.startswith("D03") or label.startswith("D08"):
        return "derived_internal_contract"
    return "local"


def hash_reference_for_label(label: str, known_hashes: dict[str, str | None]) -> str | None:
    mapping = {
        "KEDI_raw_excel": "raw_excel",
        "outcome_spine": "outcome_spine_raw",
        "wage_reference": "wage_reference_raw",
        "wage_quartile": "wage_quartile_reference_raw",
        "wage_contract": "wage_column_contract_raw",
        "job_cert_bridge_raw": "job_cert_bridge_raw",
        "goms_d07_profile": "local2_handoff_hash",
        "D01_headcount_master": "D01_v2",
        "D02_outcomes": "D02_v2",
        "D03_core": "D03_v2",
        "D04_wage_reference": "D04_v2",
        "D05_job_cert_bridge": "D05_v2",
        "D08_analysis_mart": "D08_v2_shared_candidate",
        "bridge_school_alias": "bridge_school_alias",
        "bridge_campus_alias": "bridge_campus_alias",
        "bridge_department_alias": "bridge_department_alias",
        "bridge_outcome_headcount": "bridge_outcome_headcount_v2",
        "bridge_department_major7": "bridge_department_major7_v2",
        "dim_school_split": "dim_school_split",
    }
    key = mapping.get(label)
    return known_hashes.get(key) if key else None


def source_catalog(file_df: pd.DataFrame) -> pd.DataFrame:
    def f(label: str, field: str) -> Any:
        row = file_df.loc[file_df["label"].eq(label)]
        return None if row.empty else row.iloc[0][field]

    rows = [
        {
            "catalog_id": "SRC01_KEDI_STRUCTURE",
            "official_source": "KEDI 교육통계서비스 / 고등교육통계",
            "official_url": OFFICIAL_LINKS["KEDI_EDUCATION_STATISTICS"],
            "local_source_files": "KEDI_raw_excel",
            "local_shapes": f("KEDI_raw_excel", "shape"),
            "local_sha256": f("KEDI_raw_excel", "sha256"),
            "derived_outputs": "D01_headcount_master -> D03_core -> D08_analysis_mart",
            "derived_shapes": f("D01_headcount_master", "shape"),
            "grain_used": "school x campus x department/entity x 2024, with original Excel sheet axes restored",
            "final_column_blocks": "S0, B, DENOM, K, QUALITY",
            "used_content": "학교, 캠퍼스, 지역, 설립, 본분교, 학위과정, 학과코드/명, 계열, 입학정원, 모집/지원/입학, 재적/재학/휴학, 외국인, 졸업, 교원 등 구조 및 규모 변수",
            "processing_summary": "손실된 Excel 축 복구, 학교/캠퍼스/학과명 정규화, campus-aware outcome-headcount bridge, 구조 match QA, log/ratio 파생, parent headcount reuse ledger",
            "direct_download_url_status": "not stored in local manifest; official portal URL retained",
        },
        {
            "catalog_id": "SRC02_ACADEMYINFO_GRADE",
            "official_source": "대학알리미 대학정보공시",
            "official_url": OFFICIAL_LINKS["ACADEMYINFO"],
            "local_source_files": "grade_raw",
            "local_shapes": f("grade_raw", "shape"),
            "local_sha256": f("grade_raw", "sha256"),
            "derived_outputs": "outcome_spine -> D02_outcomes -> D08_analysis_mart",
            "derived_shapes": f("outcome_spine", "shape"),
            "grain_used": "school x normalized department x 2024",
            "final_column_blocks": "GRADE, QUALITY",
            "used_content": "성적인정 총학생수, A+/A0/A-, C/D/F 학생수, 1/2학기 학과 단위 성적비율",
            "processing_summary": "2024 주간 1/2학기 필터, A/CD/F count 합산, 학기별 rate 계산 후 학교-학과 평균, D02 spine 생성",
            "direct_download_url_status": "not stored in local manifest; official portal URL retained",
        },
        {
            "catalog_id": "SRC03_ACADEMYINFO_EMPLOYMENT",
            "official_source": "대학알리미 대학정보공시",
            "official_url": OFFICIAL_LINKS["ACADEMYINFO"],
            "local_source_files": "employment_raw",
            "local_shapes": f("employment_raw", "shape"),
            "local_sha256": f("employment_raw", "sha256"),
            "derived_outputs": "outcome_spine -> D02_outcomes -> D08_analysis_mart",
            "derived_shapes": f("outcome_spine", "shape"),
            "grain_used": "school x normalized department x 2024",
            "final_column_blocks": "EMP, QUALITY",
            "used_content": "취업자_total, 건보직장가입_취업자, 공식취업률_분모",
            "processing_summary": "2024 주간 필터, 학교-학과 단위 합산, 전체취업률/건보가입취업률 계산, rate range QA",
            "direct_download_url_status": "not stored in local manifest; official portal URL retained",
        },
        {
            "catalog_id": "SRC04_ACADEMYINFO_PROGRESSION",
            "official_source": "대학알리미 대학정보공시",
            "official_url": OFFICIAL_LINKS["ACADEMYINFO"],
            "local_source_files": "progression_raw",
            "local_shapes": f("progression_raw", "shape"),
            "local_sha256": f("progression_raw", "sha256"),
            "derived_outputs": "outcome_spine -> D02_outcomes -> D08_analysis_mart",
            "derived_shapes": f("outcome_spine", "shape"),
            "grain_used": "school x normalized department x 2024",
            "final_column_blocks": "PROG, QUALITY",
            "used_content": "졸업자, 전체/전문대/대학/대학원/국내/국외 진학자",
            "processing_summary": "2024 주간 필터, 학교-학과 단위 합산, 전체/대학원 진학률 등 rate 계산, missing target flags 생성",
            "direct_download_url_status": "not stored in local manifest; official portal URL retained",
        },
        {
            "catalog_id": "SRC05_ADIGA_ADMISSION",
            "official_source": "대입정보포털 어디가",
            "official_url": OFFICIAL_LINKS["ADIGA"],
            "local_source_files": "adiga_seed; adiga_registry; adiga_raw; adiga_department_proxy",
            "local_shapes": "; ".join(
                f"{label}={f(label, 'shape')}" for label in ["adiga_seed", "adiga_registry", "adiga_raw", "adiga_department_proxy"]
            ),
            "local_sha256": "; ".join(
                f"{label}={f(label, 'sha256')}" for label in ["adiga_seed", "adiga_registry", "adiga_raw", "adiga_department_proxy"]
            ),
            "derived_outputs": "adiga_department_proxy -> outcome_spine -> D02_outcomes -> D08_analysis_mart",
            "derived_shapes": f("adiga_department_proxy", "shape"),
            "grain_used": "university x recruitment unit, collapsed to school x normalized department",
            "final_column_blocks": "Q, QUALITY",
            "used_content": "2024 모집단위별 정시/입시결과에서 추출한 percentile/등급 계열 지표, 최종 selectivity_proxy_pct",
            "processing_summary": "crawl registry/seed 보존, 모집단위명 정규화, alias strict/loose 매칭, 0~100 valid score 필터, 학교-학과 proxy 생성",
            "direct_download_url_status": "crawl registry retained locally; official portal URL retained",
        },
        {
            "catalog_id": "SRC06_CREDIT_FORFEIT_POLICY",
            "official_source": "local curated policy workbook, likely university disclosure-derived",
            "official_url": OFFICIAL_LINKS["ACADEMYINFO"],
            "local_source_files": "policy_raw",
            "local_shapes": f("policy_raw", "shape"),
            "local_sha256": f("policy_raw", "sha256"),
            "derived_outputs": "D02_outcomes -> D08_analysis_mart",
            "derived_shapes": f("D02_outcomes", "shape"),
            "grain_used": "school-level policy joined to department rows",
            "final_column_blocks": "POLICY, QUALITY",
            "used_content": "학점포기제 유무",
            "processing_summary": "학교명 매핑 후 O/X를 credit_forfeit_flag로 변환; v4.1에서 unknown encoded false 여부 별도 audit 대상",
            "direct_download_url_status": "exact external URL not recorded; local Excel hash retained",
        },
        {
            "catalog_id": "SRC07_MAJOR_CONTEXT_WAGE_COMPANY_CERT",
            "official_source": "계열 단위 임금/기업유형/자격증 context local contract",
            "official_url": OFFICIAL_LINKS["ACADEMYINFO"],
            "local_source_files": "wage_reference; wage_quartile; wage_contract; job_cert_bridge_raw",
            "local_shapes": "; ".join(
                f"{label}={f(label, 'shape')}" for label in ["wage_reference", "wage_quartile", "wage_contract", "job_cert_bridge_raw"]
            ),
            "local_sha256": "; ".join(
                f"{label}={f(label, 'sha256')}" for label in ["wage_reference", "wage_quartile", "wage_contract", "job_cert_bridge_raw"]
            ),
            "derived_outputs": "D04_wage_reference; D05_job_cert_bridge -> D08_analysis_mart",
            "derived_shapes": f"D04={f('D04_wage_reference', 'shape')}; D05={f('D05_job_cert_bridge', 'shape')}",
            "grain_used": "major_group_7 x degree_level / job-category bridge",
            "final_column_blocks": "C24, QUALITY",
            "used_content": "계열별 평균/중위 소득, 소득구간, 대/중견/중소/공공/비영리 기업비중, 자격증 취득률, HHI/entropy context",
            "processing_summary": "컬럼 계약 적용, 사분위 기준 결합, 계열 7분류로 many-to-one context 결합, 비율/HHI/entropy 생성",
            "direct_download_url_status": "exact external URL not recorded; local contract/hash retained",
        },
        {
            "catalog_id": "SRC08_KEIS_GOMS_LABOR_CONTEXT",
            "official_source": "한국고용정보원 고용조사분석시스템 / 대졸자직업이동경로조사(GOMS)",
            "official_url": OFFICIAL_LINKS["KEIS_GOMS"],
            "local_source_files": "goms_distribution_long; goms_continuous_long; goms_topic_registry; goms_d07_profile",
            "local_shapes": "; ".join(
                f"{label}={f(label, 'shape')}" for label in ["goms_distribution_long", "goms_continuous_long", "goms_topic_registry", "goms_d07_profile"]
            ),
            "local_sha256": "; ".join(
                f"{label}={f(label, 'sha256')}" for label in ["goms_distribution_long", "goms_continuous_long", "goms_topic_registry", "goms_d07_profile"]
            ),
            "derived_outputs": "D06 major-year panel; D07 recent profile -> D08_analysis_mart",
            "derived_shapes": f("goms_d07_profile", "shape"),
            "grain_used": "major_group_7 x year; D07 uses recent 2017-2019 major profile",
            "final_column_blocks": "GOMS, QUALITY",
            "used_content": "경제활동률, 산업/직업/기업규모/사업체유형/종사상지위 분포, 평균소득, 근로시간, 최근 3년 추세",
            "processing_summary": "39개 topic axis registry 구성, frequency에서 경제활동률 재계산, 직업 pre/post 2017 분리, HHI/entropy 생성, 2017~2019 profile 집계",
            "direct_download_url_status": "official survey portal and topic stats URL retained; local normalized crawl/hash retained",
        },
        {
            "catalog_id": "SRC09_INTERNAL_BRIDGES_SPLITS_REGISTRIES",
            "official_source": "internal deterministic bridge/registry artifacts",
            "official_url": "",
            "local_source_files": "bridge_school_alias; bridge_campus_alias; bridge_department_alias; bridge_outcome_headcount; bridge_department_major7; dim_school_split",
            "local_shapes": "; ".join(
                f"{label}={f(label, 'shape')}"
                for label in [
                    "bridge_school_alias",
                    "bridge_campus_alias",
                    "bridge_department_alias",
                    "bridge_outcome_headcount",
                    "bridge_department_major7",
                    "dim_school_split",
                ]
            ),
            "local_sha256": "; ".join(
                f"{label}={f(label, 'sha256')}"
                for label in [
                    "bridge_school_alias",
                    "bridge_campus_alias",
                    "bridge_department_alias",
                    "bridge_outcome_headcount",
                    "bridge_department_major7",
                    "dim_school_split",
                ]
            ),
            "derived_outputs": "D03_core -> D08_analysis_mart and sample/split registries",
            "derived_shapes": f"D03={f('D03_core', 'shape')}; D08={f('D08_analysis_mart', 'shape')}",
            "grain_used": "stable outcome_row_id and school/campus/department keys",
            "final_column_blocks": "K, S0, QUALITY",
            "used_content": "학교/캠퍼스/학과 alias, outcome-headcount bridge, major7 bridge, school-level train/validation/test split",
            "processing_summary": "행 순서 join 금지, stable key join, match score/candidate count/review flag 보존, school split leakage 0 확인",
            "direct_download_url_status": "not applicable; derived audit artifacts",
        },
    ]
    return pd.DataFrame(rows)


def column_catalog() -> tuple[pd.DataFrame, pd.DataFrame]:
    reg = pd.read_csv(REGISTRY_V4_PATH)
    keep_cols = [
        "column",
        "dtype_actual",
        "semantic_role",
        "feature_block",
        "measurement_level",
        "grain",
        "unit",
        "source_dataset",
        "source_column",
        "derivation_formula",
        "is_identifier",
        "is_target_candidate",
        "is_context",
        "is_quality_metadata",
        "model_default_active",
        "review_required",
        "notes",
    ]
    keep_cols = [c for c in keep_cols if c in reg.columns]
    col_df = reg[keep_cols].copy()
    block_df = (
        reg.groupby(["source_dataset", "feature_block", "semantic_role", "measurement_level"], dropna=False)
        .size()
        .reset_index(name="column_n")
        .sort_values(["source_dataset", "feature_block", "column_n"], ascending=[True, True, False])
    )
    return col_df, block_df


def mart_summary() -> dict[str, Any]:
    d08 = pd.read_parquet(D08_PATH)
    split_counts = d08["split"].value_counts(dropna=False).to_dict() if "split" in d08.columns else {}
    school_split_counts = {}
    if DIM_SPLIT_PATH.exists():
        split_df = pd.read_csv(DIM_SPLIT_PATH)
        if "split" in split_df.columns:
            school_split_counts = split_df["split"].value_counts(dropna=False).to_dict()
    phase_samples = []
    if PHASE_SAMPLE_REGISTRY_PATH.exists():
        sample_df = pd.read_csv(PHASE_SAMPLE_REGISTRY_PATH)
        sample_cols = [c for c in ["sample_id", "row_n", "school_n", "train_n", "validation_n", "test_n"] if c in sample_df.columns]
        phase_samples = sample_df[sample_cols].to_dict(orient="records")
    major_counts = d08["major_group_7"].value_counts(dropna=False).to_dict() if "major_group_7" in d08.columns else {}
    targets = ["a_rate_pct", "health_employment_rate_pct", "graduate_school_progression_rate_pct"]
    target_non_null = {t: int(d08[t].notna().sum()) for t in targets if t in d08.columns}
    return {
        "path": str(D08_PATH),
        "shape": list(d08.shape),
        "sha256": sha256_file(D08_PATH),
        "school_n": int(d08["school_uid"].nunique()) if "school_uid" in d08.columns else None,
        "campus_n": int(d08["campus_uid"].nunique()) if "campus_uid" in d08.columns else None,
        "department_n": int(d08["dept_uid"].nunique()) if "dept_uid" in d08.columns else None,
        "split_counts": split_counts,
        "school_split_counts": school_split_counts,
        "phase_samples": phase_samples,
        "major_group_7_counts": major_counts,
        "target_non_null": target_non_null,
    }


def md_table(df: pd.DataFrame, columns: list[str], max_rows: int | None = None) -> str:
    use = df[columns].copy()
    if max_rows is not None:
        use = use.head(max_rows)
    output = []
    output.append("| " + " | ".join(columns) + " |")
    output.append("| " + " | ".join(["---"] * len(columns)) + " |")
    for _, row in use.iterrows():
        values = []
        for col in columns:
            text = "" if pd.isna(row[col]) else str(row[col])
            text = text.replace("\n", " ").replace("|", "\\|")
            values.append(text)
        output.append("| " + " | ".join(values) + " |")
    return "\n".join(output)


def write_report(source_df: pd.DataFrame, file_df: pd.DataFrame, col_df: pd.DataFrame, block_df: pd.DataFrame, summary: dict[str, Any]) -> Path:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_counts = col_df["source_dataset"].value_counts(dropna=False).rename_axis("source_dataset").reset_index(name="column_n")
    block_counts = col_df["feature_block"].value_counts(dropna=False).rename_axis("feature_block").reset_index(name="column_n")
    lines = [
        "# P2-G4 Data Source Catalog and Data Specification",
        "",
        f"- generated_at_utc: `{now}`",
        f"- active_mart: `{summary['path']}`",
        f"- active_mart_shape: `{summary['shape'][0]} x {summary['shape'][1]}`",
        f"- active_mart_sha256: `{summary['sha256']}`",
        f"- observed_scope: `2024년, {summary['school_n']}개 학교, {summary['campus_n']}개 캠퍼스, {summary['department_n']}개 학과 entity / 10,242 outcome rows`",
        "- grain: `analysis_year x p4_school_uid/school_uid x p4_campus_uid/campus_uid x p4_dept_uid/dept_uid x outcome_row_id`",
        "",
        "## 1. Official Source Links",
        "",
        "- KEDI 교육통계서비스: <https://kess.kedi.re.kr/>",
        "- 대학알리미 대학정보공시: <https://www.academyinfo.go.kr/>",
        "- 대입정보포털 어디가: <https://www.adiga.kr/>",
        "- 한국고용정보원 고용조사분석시스템: <https://survey.keis.or.kr/>",
        "- 한국고용정보원 GOMS 주제별 통계 분석 서비스: <https://analysis.keis.or.kr/>",
        "",
        "주의: 로컬 manifest는 원천 파일의 SHA256과 로컬 경로를 보존하지만, 일부 포털 다운로드의 원본 direct download URL은 저장하지 않았다. 따라서 이 카탈로그는 공식 포털 URL + 로컬 파일 hash를 provenance anchor로 사용한다.",
        "",
        "## 2. Source Catalog",
        "",
        md_table(
            source_df,
            [
                "catalog_id",
                "official_source",
                "official_url",
                "local_source_files",
                "local_shapes",
                "derived_outputs",
                "grain_used",
                "final_column_blocks",
                "used_content",
                "processing_summary",
                "direct_download_url_status",
            ],
        ),
        "",
        "## 3. Local File Inventory",
        "",
        md_table(
            file_df,
            [
                "label",
                "official_source_hint",
                "relative_path",
                "exists",
                "size_bytes",
                "shape",
                "sha256",
                "manifest_hash_reference",
                "hash_matches_known_manifest",
            ],
        ),
        "",
        "## 4. Final Mart Column Source Counts",
        "",
        "### 4.1 By Source Dataset",
        "",
        md_table(source_counts, ["source_dataset", "column_n"]),
        "",
        "### 4.2 By Feature Block",
        "",
        md_table(block_counts, ["feature_block", "column_n"]),
        "",
        "### 4.3 By Source Dataset x Feature Block",
        "",
        md_table(block_df, ["source_dataset", "feature_block", "semantic_role", "measurement_level", "column_n"]),
        "",
        "## 5. Final Mart Target and Split Counts",
        "",
        "```json",
        json.dumps(
            {
                "row_split_counts_in_d08": summary["split_counts"],
                "school_split_counts_from_dim_school_split": summary["school_split_counts"],
                "phase_sample_registry_rows": summary["phase_samples"],
                "target_non_null": summary["target_non_null"],
                "major_group_7_counts": summary["major_group_7_counts"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        "```",
        "",
        "## 6. Processing Ledger Summary",
        "",
        "- 원본 파일 hash·shape 동결: `P4_HANDOFF_MANIFEST.json`, `dataset_inventory.csv`, 이 카탈로그의 `data_source_file_inventory.csv`에 재기록.",
        "- 손실된 Excel 축 복구: KEDI raw Excel sheet `학교별 학과별 주요 현황`을 D01 34,969 x 186으로 정규화.",
        "- 학교·캠퍼스·학과명 정규화: school/campus/department alias bridge 생성.",
        "- campus-aware 학과 매칭: outcome spine 10,242행과 D01 headcount 구조를 stable key/bridge로 결합.",
        "- 중복·후보·충돌 QA: outcome_row_id는 중복 0, composite dept key 충돌은 ledger 보존.",
        "- 7대 계열 bridge: D01 대계열 및 학과 alias로 major_group_7 생성, major7 coverage 10,099 / 10,242.",
        "- GOMS 39개 주제 정규화: distribution/continuous long source를 topic registry로 표준화.",
        "- GOMS 경제활동률 frequency 재계산: share를 그대로 취업률로 쓰지 않고 frequency로 재계산.",
        "- 직업 pre/post 분류 분리: GOMS 2017 전후 직업분류 스키마를 분리.",
        "- 산업·직업·기업분포 HHI·entropy 생성: 계열 단위 context 변수로만 사용.",
        "- 계열별 최근 2017~2019 profile 생성: D07 `goms_major_profile_recent.parquet` 7 x 29.",
        "- D04·D07 many-to-one context 결합: major_group_7 단위 contemporary/context variables를 D08에 결합.",
        "- 학교 단위 split 고정: `dim_school_split.csv` 200 x 6, split leakage 0.",
        "- 모델별 sample mask 생성: readiness v4 membership/sample registry에서 별도 관리.",
        "- column·feature·target registry 생성: `department_model_column_registry_v4.csv` 현 상태 151 x 27.",
        "- SHA256 manifest·decision·transformation·merge log 생성: handoff/preprocessing integrity manifest에 보존.",
        "",
        "## 7. Known Limits",
        "",
        "- 성적 A비율, 취업률, 진학률의 저장 rate는 존재하지만 최종 마트 D08에는 원 count numerator/denominator가 보존되지 않았다. count-binomial 분석은 `NOT_AVAILABLE`로 분리해야 한다.",
        "- 학점포기제 원천은 local curated Excel로 보존되어 있으며 exact external direct URL은 manifest에 없다.",
        "- 임금/기업/자격증 context의 local contract 파일은 hash로 고정되어 있으나, direct download URL은 manifest에 없다.",
        "- GOMS와 D04/C24 context는 학과 outcome이 아니라 7대 계열 단위 context이며, 학과별 결과처럼 해석하면 안 된다.",
        "",
        "## 8. Output Files",
        "",
        "- `qa/data_source_catalog.csv`",
        "- `qa/data_source_file_inventory.csv`",
        "- `qa/data_source_column_catalog.csv`",
        "- `qa/data_source_column_blocks.csv`",
        "- `reports/DATA_SOURCE_CATALOG.md`",
    ]
    report_path = REPORT_DIR / "DATA_SOURCE_CATALOG.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def write_manifest(paths: list[Path]) -> Path:
    rows = []
    for path in paths:
        shape, loader = shape_for_file(path)
        rows.append(
            {
                "path": str(path),
                "relative_path": str(path.relative_to(PROJECT_ROOT)),
                "size_bytes": path.stat().st_size,
                "shape": shape,
                "loader": loader,
                "sha256": sha256_file(path),
            }
        )
    manifest_path = QA_DIR / "data_source_catalog_manifest.json"
    manifest_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest_path


def main() -> None:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    files = file_inventory()
    sources = source_catalog(files)
    columns, blocks = column_catalog()
    summary = mart_summary()

    file_path = QA_DIR / "data_source_file_inventory.csv"
    source_path = QA_DIR / "data_source_catalog.csv"
    column_path = QA_DIR / "data_source_column_catalog.csv"
    block_path = QA_DIR / "data_source_column_blocks.csv"

    files.to_csv(file_path, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)
    sources.to_csv(source_path, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)
    columns.to_csv(column_path, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)
    blocks.to_csv(block_path, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)

    report_path = write_report(sources, files, columns, blocks, summary)
    manifest_path = write_manifest([file_path, source_path, column_path, block_path, report_path])
    outputs = [file_path, source_path, column_path, block_path, report_path, manifest_path]
    print(json.dumps({p.name: sha256_file(p) for p in outputs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
