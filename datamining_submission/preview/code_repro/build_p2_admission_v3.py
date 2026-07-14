from __future__ import annotations

import json
import math
import re
import unicodedata
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


PROJECT_DIR = Path("/home/sieg/projects-wsl/SBS_dataScience")
BASE_DIR = PROJECT_DIR / "workbook/p2/p2_2"
CRAWL_DIR = BASE_DIR / "data/crawl_2024_admission_full"
OUT_DIR = BASE_DIR / "final/admission"
EDA_TABLE_DIR = BASE_DIR / "final/eda/tables"

RAW_PATH = CRAWL_DIR / "02_admission_result_raw_2024_merged.csv"
REGISTRY_PATH = CRAWL_DIR / "01_crawl_source_registry_merged.csv"
SEED_PATH = CRAWL_DIR / "00_crawl_seed_university_2024_merged.csv"
LABEL_PATH = BASE_DIR / "P2_학과별_A비율_대학아님.csv"
GRADE_PATH = BASE_DIR / "P2__전체대학학점비율.csv"
FINAL_CURRENT_PATH = BASE_DIR / "final/data/P2_G1_concat.csv"

ROW_METRIC_PATH = OUT_DIR / "P2_admission_row_metric_v3.csv"
MATCH_PATH = OUT_DIR / "P2_admission_match_v3.csv"
DEPARTMENT_PATH = OUT_DIR / "P2_admission_proxy_v3_by_department.csv"
UNMATCHED_PATH = OUT_DIR / "P2_admission_unmatched_review_v3.csv"
COVERAGE_PATH = OUT_DIR / "P2_admission_coverage_by_university_v3.csv"
REPORT_PATH = OUT_DIR / "P2_admission_v3_final_report.md"


SPECIAL_SELECTION_PATTERN = re.compile(
    r"농어촌|기회균등|고른기회|저소득|특성화|재외국민|장애|만학도|기초생활|차상위|"
    r"특별전형|체육전형|실기|예체능|특기자"
)
GENERAL_SELECTION_PATTERN = re.compile(r"일반|일반학생|수능우수|수능위주")
REGIONAL_SELECTION_PATTERN = re.compile(r"지역균형")
HEADER_KEYWORDS = ("모집 인원", "총점", "백분위", "70% cut", "70%cut", "등급")
SUBJECT_HEADERS = {"국어", "수학", "탐구", "영어", "등급"}


def normalize_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    text = unicodedata.normalize("NFKC", str(value))
    text = text.replace("\u200b", "").replace("\ufeff", "")
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("ㆍ", "·").replace("∙", "·").replace("･", "·").replace("・", "·")
    return text


def display_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    text = unicodedata.normalize("NFKC", str(value))
    text = text.replace("\u200b", "").replace("\ufeff", "")
    return re.sub(r"\s+", " ", text).strip()


def compact_key(value: object) -> str:
    text = normalize_text(value)
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[()\[\]{}·,/&+\-]", "", text)
    return text.lower()


def loose_department_key(value: object) -> str:
    text = compact_key(value)
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"(학과|학부|전공|계열|대학|부)$", "", text)
    text = re.sub(r"(학과|학부|전공|계열)", "", text)
    text = re.sub(r"[^0-9a-z가-힣]", "", text)
    return text


def university_key(value: object) -> str:
    text = normalize_text(value)
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"\s+", "", text)
    return text


def load_json_list(value: object) -> list[Any]:
    if value is None or pd.isna(value):
        return []
    if isinstance(value, list):
        return value
    try:
        loaded = json.loads(str(value))
    except Exception:
        return []
    return loaded if isinstance(loaded, list) else []


def number_value(value: object) -> float:
    if value is None or pd.isna(value):
        return np.nan
    text = unicodedata.normalize("NFKC", str(value)).replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(match.group(0)) if match else np.nan


def valid_0_100(value: float) -> bool:
    return bool(pd.notna(value) and 0 < float(value) <= 100)


def weighted_mean(values: pd.Series, weights: pd.Series) -> float:
    v = pd.to_numeric(values, errors="coerce")
    w = pd.to_numeric(weights, errors="coerce")
    ok = v.notna() & w.notna() & w.gt(0)
    if ok.any():
        return float(np.average(v[ok], weights=w[ok]))
    return float(v.mean()) if v.notna().any() else np.nan


def join_unique(values: pd.Series, limit: int = 12) -> str:
    seen: list[str] = []
    for value in values.dropna().astype(str):
        value = normalize_text(value)
        if value and value not in seen:
            seen.append(value)
    return " | ".join(seen[:limit])


def save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def check_alias_collisions(strict_candidates: dict[str, set[str]]) -> pd.DataFrame:
    """같은 raw_name(strict key)이 서로 다른 학과_정규화 canonical에 동시에 등록된 경우를 찾는다.

    예: "초등교육과"가 교육대학교 계열 canonical("초등교육")과 종합대 사범대 계열 canonical
    ("초등교육과") 양쪽의 raw_names에 동시에 들어가면, dict 등록 순서(setdefault)에 따라 한쪽이
    조용히 가려진다 — v3 빌드 진입 전에 이런 충돌을 눈에 보이게 만들어 회귀를 막는다.
    """
    rows = [
        {"raw_name_key": key, "canonical_candidates": " | ".join(sorted(labels)), "candidate_count": len(labels)}
        for key, labels in strict_candidates.items()
        if len(labels) > 1
    ]
    collisions = pd.DataFrame(rows)
    if len(collisions):
        save_csv(collisions, OUT_DIR / "P2_admission_alias_collisions_v3.csv")
        print(f"[alias_collision][경고] {len(collisions)}건의 raw_name이 서로 다른 학과_정규화에 중복 등록됨 "
              f"(먼저 로드된 canonical이 우선 적용되고 나머지는 조용히 가려짐) "
              f"-> 상세: {OUT_DIR / 'P2_admission_alias_collisions_v3.csv'}")
    return collisions


def load_department_aliases() -> tuple[dict[str, str], dict[str, str], set[str]]:
    ref = pd.read_csv(LABEL_PATH, low_memory=False)
    strict: dict[str, str] = {}
    strict_candidates: dict[str, set[str]] = {}
    loose_candidates: dict[str, set[str]] = {}
    raw_alias_keys: set[str] = set()

    def add_alias(raw_name: object, label: str) -> None:
        s_key = compact_key(raw_name)
        l_key = loose_department_key(raw_name)
        if s_key:
            strict.setdefault(s_key, label)
            strict_candidates.setdefault(s_key, set()).add(label)
            raw_alias_keys.add(s_key)
        if l_key:
            loose_candidates.setdefault(l_key, set()).add(label)

    for _, row in ref.iterrows():
        label = display_text(row["학과_정규화"])
        add_alias(label, label)
        for raw in str(row.get("raw_names", "")).split("|"):
            raw = display_text(raw)
            if raw:
                add_alias(raw, label)

    check_alias_collisions(strict_candidates)

    loose = {key: next(iter(labels)) for key, labels in loose_candidates.items() if len(labels) == 1}
    return strict, loose, raw_alias_keys


ADMISSION_TRACK_SUFFIX_PATTERN = re.compile(r"\s*\(\s*(주|야|온라인)\s*\)\s*$")
ADMISSION_CSAT_SUFFIX_PATTERN = re.compile(r"\s*수능\s*\([^)]*\)\s*$")


def strip_admission_track_suffix(text: str) -> str:
    """ADIGA 모집단위 표기에 붙는 주/야간 구분, 전형유형 구분을 제거해 순수 학과명만 남긴다.

    예: "크리에이티브인문학부 ( 주 )" -> "크리에이티브인문학부",
        "신학과 / 목회자추천자" -> "신학과",
        "초등교육과 수능 ( 일반학생 )" -> "초등교육과"
    실제 학과명에 " / "나 "(주)"류 표기가 쓰이는 경우는 관측되지 않았으므로, 이 정리는
    매칭 실패(raw_fallback) 시 재시도 용도로만 쓰고 원문 매칭을 대체하지 않는다.
    """
    t = text.split(" / ")[0].strip()
    t = ADMISSION_TRACK_SUFFIX_PATTERN.sub("", t)
    t = ADMISSION_CSAT_SUFFIX_PATTERN.sub("", t)
    return t.strip()


def label_department(value: object, strict: dict[str, str], loose: dict[str, str]) -> tuple[str, str]:
    text = display_text(value)
    if not text:
        return "", "empty"
    s_key = compact_key(text)
    if s_key in strict:
        return strict[s_key], "alias_strict"
    l_key = loose_department_key(text)
    if l_key in loose:
        return loose[l_key], "alias_loose"

    stripped = strip_admission_track_suffix(text)
    if stripped and stripped != text:
        s_key2 = compact_key(stripped)
        if s_key2 in strict:
            return strict[s_key2], "alias_strict_after_track_strip"
        l_key2 = loose_department_key(stripped)
        if l_key2 in loose:
            return loose[l_key2], "alias_loose_after_track_strip"

    return text, "raw_fallback"


# 전역 alias 테이블(P2_학과별_A비율_대학아님.csv)에 넣으면 다른 대학과 충돌하는 raw_name을,
# 특정 대학에서만 적용되는 것으로 한정해 처리한다. P2_admission_alias_collision_decisions_v3.csv의
# canonical_override 결정 근거(어느 대학의 raw 텍스트가 그 대학 자신의 실제 학과_계열과 정확히
# 일치하는지 직접 확인)로만 채운다 — 대학명 하드코딩이지만 전역 alias 오염을 막기 위한 의도적 격리.
UNIVERSITY_DEPARTMENT_OVERRIDES: dict[str, dict[str, str]] = {
    "한국공학대학교": {compact_key("컴퓨터공학부컴퓨터공학전공"): "컴퓨터공"},
    "국립창원대학교": {compact_key("기계공학부기계공학전공"): "기계공기계공학"},
    "조선대학교": {compact_key("전자공학부전자공학전공"): "전자공"},
    "선문대학교": {compact_key("디자인학부시각디자인전공"): "시각디자인"},
    "대구대학교": {compact_key("경찰학부경찰행정학전공"): "경찰"},
}

EDUCATION_COLLEGE_SUFFIX_PATTERN = re.compile(r"교육대학교(_제\d+캠퍼스)?$")
ELEMENTARY_ED_RAW_KEY = compact_key("초등교육과")


def university_scoped_department_override(university: object, raw_text: object) -> str | None:
    """대학마다 의미가 달라지는 raw_recruitment_unit을 전역 alias 대신 대학 단위로 해석한다.

    예: "초등교육과"는 교육대학교(교대) 계열에서는 canonical "초등교육"을 뜻하지만, 이화여대·
    제주대·한국교원대 같은 종합대 사범대에서는 그 자체가 독립된 canonical "초등교육과"다.
    """
    text = display_text(raw_text)
    if not text:
        return None
    key = compact_key(strip_admission_track_suffix(text))

    per_university = UNIVERSITY_DEPARTMENT_OVERRIDES.get(str(university))
    if per_university and key in per_university:
        return per_university[key]

    if key == ELEMENTARY_ED_RAW_KEY and EDUCATION_COLLEGE_SUFFIX_PATTERN.search(str(university or "")):
        return "초등교육"

    return None


def label_department_scoped(
    value: object, university: object, strict: dict[str, str], loose: dict[str, str]
) -> tuple[str, str]:
    override = university_scoped_department_override(university, value)
    if override:
        return override, "university_scoped_override"
    return label_department(value, strict, loose)


def build_grade_keys(strict: dict[str, str], loose: dict[str, str]) -> pd.DataFrame:
    if FINAL_CURRENT_PATH.exists():
        final = pd.read_csv(FINAL_CURRENT_PATH, low_memory=False)
        keys = (
            final.groupby(["학교명", "학과_계열"], dropna=False)
            .agg(
                grade_raw_departments=("학과_전공", join_unique),
                grade_rows=("학과_전공", "size"),
            )
            .reset_index()
        )
        keys["university_key"] = keys["학교명"].map(university_key)
        keys["department_key"] = keys["학과_계열"].map(compact_key)
        return keys

    grade = pd.read_csv(GRADE_PATH, low_memory=False)
    grade = grade[
        grade["기준연도"].eq(2024)
        & grade["구분"].eq("주간")
        & grade["학기"].isin(["1학기", "2학기"])
    ].copy()
    labels = grade["학과_전공"].map(lambda x: label_department(x, strict, loose)[0])
    grade["학과_계열"] = labels.astype("string").str.strip()
    keys = (
        grade.groupby(["학교명", "학과_계열"], dropna=False)
        .agg(
            grade_raw_departments=("학과_전공", join_unique),
            grade_rows=("학과_전공", "size"),
        )
        .reset_index()
    )
    keys["university_key"] = keys["학교명"].map(university_key)
    keys["department_key"] = keys["학과_계열"].map(compact_key)
    return keys


def is_header_like(row: pd.Series) -> bool:
    cells = load_json_list(row.get("raw_cells_json"))
    unit = normalize_text(row.get("raw_recruitment_unit"))
    joined = " ".join(str(x) for x in cells)
    return (not unit) and any(keyword in joined for keyword in HEADER_KEYWORDS)


def build_table_profiles(raw: pd.DataFrame) -> dict[tuple[str, int], list[list[Any]]]:
    profiles: dict[tuple[str, int], list[list[Any]]] = {}
    for key, group in raw.groupby(["source_id", "raw_table_index"], dropna=False):
        subheaders: list[list[Any]] = []
        for _, row in group.sort_values("raw_row_index").iterrows():
            if is_header_like(row):
                subheaders.append(load_json_list(row["raw_cells_json"]))
                continue
            break
        profiles[(str(key[0]), int(key[1]))] = subheaders
    return profiles


def subheaders_at(subheaders: list[list[Any]], index: int) -> list[str]:
    out: list[str] = []
    for row in subheaders:
        if index < len(row):
            value = normalize_text(row[index])
            if value:
                out.append(value)
    return out


def clean_header(value: object) -> str:
    return re.sub(r"\s+", "", normalize_text(value))


def header_percentile_candidate(
    row: pd.Series,
    cells: list[Any],
    headers: list[Any],
    subheaders: list[list[Any]],
) -> tuple[float, int | None, str, str]:
    candidates: list[tuple[int, int, float, str]] = []
    for index, value in enumerate(cells):
        numeric_value = number_value(value)
        if not valid_0_100(numeric_value):
            continue

        top = normalize_text(headers[index]) if index < len(headers) else ""
        subs = subheaders_at(subheaders, index)
        context = " ".join([top, *subs])
        compact = clean_header(context)
        exact_subs = {clean_header(x) for x in subs}

        has_average_sub = "평균" in exact_subs or "백분위" in exact_subs
        has_direct_percentile = "백분위" in compact and ("70" in compact or "cut" in compact)
        has_average_percentile_phrase = "평균백분위" in compact or "평균(백분위)" in compact
        subject_col = bool(exact_subs & SUBJECT_HEADERS)

        if subject_col and not has_average_sub:
            continue
        if not (has_average_sub or has_direct_percentile or has_average_percentile_phrase):
            continue

        score = 0
        if has_average_sub:
            score += 12
        if "백분위" in compact:
            score += 6
        if "평균" in compact:
            score += 4
        if subject_col:
            score -= 8
        candidates.append((score, index, float(numeric_value), context))

    if not candidates:
        return np.nan, None, "", ""
    candidates.sort(reverse=True)
    _, index, value, context = candidates[0]
    return value, index, "header_percentile", context


def structural_percentile_candidate(cells: list[Any]) -> tuple[float, int | None, str, str]:
    if len(cells) == 8:
        score = number_value(cells[5])
        max_score = number_value(cells[6])
        candidate = number_value(cells[7])
        if valid_0_100(candidate) and pd.notna(max_score) and max_score >= 100 and pd.notna(score) and score > 0:
            return float(candidate), 7, "structural_last_percentile", "len8_last_column"
    if len(cells) >= 13:
        candidate = number_value(cells[11])
        if valid_0_100(candidate):
            return float(candidate), 11, "structural_average_percentile", "len13_average_column"
    return np.nan, None, "", ""


def structural_score_and_max(
    row: pd.Series,
    cells: list[Any],
) -> tuple[float, float, str]:
    raw_score = number_value(row.get("raw_score_70cut"))
    raw_max = number_value(row.get("raw_score_max"))
    raw_percentile = number_value(row.get("raw_percentile_70cut"))
    source = "raw_score_columns"

    if not (pd.notna(raw_score) and raw_score > 0):
        if len(cells) == 8:
            raw_score = number_value(cells[5])
            raw_max = number_value(cells[6])
            source = "len8_score_max_columns"
        elif len(cells) >= 13:
            raw_score = number_value(cells[6])
            raw_max = number_value(cells[7])
            source = "len13_score_max_columns"

    if not (pd.notna(raw_score) and raw_score > 0) and pd.notna(raw_percentile) and raw_percentile > 100:
        if pd.notna(raw_max) and raw_max > 0:
            raw_score = raw_percentile
            source = "invalid_percentile_reclassified_as_score"

    return raw_score, raw_max, source


def score_ratio_candidate(score: float, max_score: float) -> float:
    if not (pd.notna(score) and pd.notna(max_score)):
        return np.nan
    if score <= 0 or max_score <= 0 or score > max_score:
        return np.nan
    ratio = score / max_score * 100
    return float(ratio) if valid_0_100(ratio) else np.nan


def extract_metric_for_row(row: pd.Series, table_profiles: dict[tuple[str, int], list[list[Any]]]) -> dict[str, Any]:
    cells = load_json_list(row.get("raw_cells_json"))
    headers = load_json_list(row.get("raw_header_json"))
    profile_key = (str(row.get("source_id")), int(row.get("raw_table_index")))
    subheaders = table_profiles.get(profile_key, [])

    if is_header_like(row):
        return {
            "admission_metric_v3": np.nan,
            "metric_family_v3": "header_row",
            "metric_source_v3": "header_row_excluded",
            "metric_column_index_v3": np.nan,
            "metric_context_v3": "",
            "raw_percentile_num_v3": number_value(row.get("raw_percentile_70cut")),
            "raw_score_num_v3": number_value(row.get("raw_score_70cut")),
            "raw_score_max_num_v3": number_value(row.get("raw_score_max")),
            "score_ratio_num_v3": np.nan,
            "score_source_v3": "",
        }

    raw_percentile = number_value(row.get("raw_percentile_70cut"))
    raw_percentile_valid = raw_percentile if valid_0_100(raw_percentile) else np.nan

    header_value, header_index, header_source, header_context = header_percentile_candidate(
        row, cells, headers, subheaders
    )
    structural_value, structural_index, structural_source, structural_context = structural_percentile_candidate(cells)

    score, max_score, score_source = structural_score_and_max(row, cells)
    score_ratio = score_ratio_candidate(score, max_score)

    if valid_0_100(header_value):
        metric = header_value
        family = "percentile"
        source = header_source
        index = header_index
        context = header_context
    elif valid_0_100(structural_value):
        metric = structural_value
        family = "percentile"
        source = structural_source
        index = structural_index
        context = structural_context
    elif valid_0_100(raw_percentile_valid):
        metric = raw_percentile_valid
        family = "percentile"
        source = "raw_percentile_70cut_0_100"
        index = np.nan
        context = "raw_percentile_70cut"
    elif valid_0_100(score_ratio):
        metric = score_ratio
        family = "score_ratio_normalized"
        source = "score_to_max_ratio"
        index = np.nan
        context = score_source
    else:
        metric = np.nan
        family = "missing_or_unusable"
        source = "missing_or_unusable"
        index = np.nan
        context = ""

    return {
        "admission_metric_v3": metric,
        "metric_family_v3": family,
        "metric_source_v3": source,
        "metric_column_index_v3": index,
        "metric_context_v3": context,
        "raw_percentile_num_v3": raw_percentile,
        "raw_score_num_v3": score,
        "raw_score_max_num_v3": max_score,
        "score_ratio_num_v3": score_ratio,
        "score_source_v3": score_source,
    }


def extract_recruitment_n_v3(row: pd.Series) -> float:
    existing = number_value(row.get("raw_recruitment_n"))
    if pd.notna(existing):
        return existing
    cells = load_json_list(row.get("raw_cells_json"))
    if is_header_like(row):
        return np.nan
    if len(cells) == 8:
        return number_value(cells[2])
    if len(cells) >= 13:
        return number_value(cells[3])
    return np.nan


def selection_flags(row: pd.Series) -> tuple[bool, int, str]:
    context = " ".join(
        normalize_text(row.get(col))
        for col in ["raw_admission_group", "raw_section_title", "raw_header_json", "raw_cells_json"]
    )
    if SPECIAL_SELECTION_PATTERN.search(context):
        return False, 9, "special_selection_excluded"
    if GENERAL_SELECTION_PATTERN.search(context):
        return True, 1, "general_or_csat_priority"
    if REGIONAL_SELECTION_PATTERN.search(context):
        return True, 2, "regional_balance_secondary"
    return True, 2, "no_special_keyword_assumed_primary"


def broad_recruitment_flag(unit: object) -> bool:
    text = normalize_text(unit)
    if not text:
        return False
    if any(token in text for token in ["자유전공", "광역", "계열"]):
        return True
    if "대학" in text and not any(token in text for token in ["학과", "전공", "학부"]):
        return True
    return False


def load_raw_with_context() -> pd.DataFrame:
    raw = pd.read_csv(RAW_PATH, low_memory=False)
    registry = pd.read_csv(REGISTRY_PATH, low_memory=False)
    seed = pd.read_csv(SEED_PATH, low_memory=False)

    registry_cols = [
        "source_id",
        "univ_id",
        "source_url",
        "raw_file_path",
        "retrieved_at",
        "content_sha256",
    ]
    seed_cols = ["univ_id", "univ_name_std", "adiga_univ_code"]
    registry = registry[registry_cols].drop_duplicates(["source_id", "univ_id"], keep="first")
    if "target_institution_flag" in seed.columns:
        seed = seed.assign(_target_sort=seed["target_institution_flag"].fillna(False).astype(bool).astype(int))
        seed = seed.sort_values("_target_sort", ascending=False)
    seed = seed[seed_cols].drop_duplicates(["univ_id"], keep="first")
    raw = raw.merge(registry[registry_cols], on=["source_id", "univ_id"], how="left")
    raw = raw.merge(seed[seed_cols], on="univ_id", how="left")
    return raw


def build_row_metrics() -> pd.DataFrame:
    raw = load_raw_with_context()
    profiles = build_table_profiles(raw)
    extracted = raw.apply(lambda row: extract_metric_for_row(row, profiles), axis=1, result_type="expand")
    out = pd.concat([raw, extracted], axis=1)
    out["recruitment_n_v3"] = out.apply(extract_recruitment_n_v3, axis=1)
    selection = out.apply(selection_flags, axis=1, result_type="expand")
    selection.columns = ["primary_selection_candidate", "selection_priority", "selection_note"]
    out = pd.concat([out, selection], axis=1)
    out["broad_recruitment_unit_flag_v3"] = out["raw_recruitment_unit"].map(broad_recruitment_flag)
    out["row_metric_usable_v3"] = out["admission_metric_v3"].notna() & out["primary_selection_candidate"]
    return out


def attach_matches(row_metrics: pd.DataFrame, grade_keys: pd.DataFrame, strict: dict[str, str], loose: dict[str, str]) -> pd.DataFrame:
    grade_univ_map = (
        grade_keys[["학교명", "university_key"]]
        .drop_duplicates()
        .set_index("university_key")["학교명"]
        .to_dict()
    )
    grade_key_set = set(zip(grade_keys["학교명"], grade_keys["학과_계열"]))
    grade_key_norm_map = (
        grade_keys.drop_duplicates(["학교명", "department_key"], keep="first")
        .set_index(["학교명", "department_key"])["학과_계열"]
        .to_dict()
    )

    matched = row_metrics.copy()
    matched["학교명"] = matched["univ_name_std"].map(lambda x: grade_univ_map.get(university_key(x), ""))
    dept_labels = matched.apply(
        lambda row: label_department_scoped(row["raw_recruitment_unit"], row["학교명"], strict, loose), axis=1
    )
    matched["학과_계열"] = dept_labels.map(lambda x: x[0])
    matched["department_label_rule_v3"] = dept_labels.map(lambda x: x[1])
    matched["university_match_flag_v3"] = matched["학교명"].astype(str).str.len().gt(0)
    normalized_labels = []
    department_match_flags = []
    for school, label in zip(matched["학교명"], matched["학과_계열"]):
        norm_key = (school, compact_key(label))
        if norm_key in grade_key_norm_map:
            normalized_labels.append(grade_key_norm_map[norm_key])
            department_match_flags.append(True)
        else:
            normalized_labels.append(label)
            department_match_flags.append((school, label) in grade_key_set)
    matched["학과_계열"] = normalized_labels
    matched["department_match_flag_v3"] = department_match_flags

    conditions = [
        ~matched["university_match_flag_v3"],
        matched["학과_계열"].astype(str).str.len().eq(0),
        ~matched["department_match_flag_v3"],
        matched["broad_recruitment_unit_flag_v3"],
        matched["admission_metric_v3"].isna(),
        ~matched["primary_selection_candidate"],
    ]
    choices = [
        "university_not_in_final_grade_universe",
        "empty_recruitment_unit",
        "department_label_not_in_university_grade",
        "broad_recruitment_unit_excluded",
        "metric_missing_or_unusable",
        "special_selection_excluded",
    ]
    matched["match_exclusion_reason_v3"] = np.select(conditions, choices, default="")
    matched["matched_for_final_v3"] = (
        matched["university_match_flag_v3"]
        & matched["department_match_flag_v3"]
        & matched["admission_metric_v3"].notna()
        & matched["primary_selection_candidate"]
        & ~matched["broad_recruitment_unit_flag_v3"]
    )
    return matched


def aggregate_by_department(matches: pd.DataFrame) -> pd.DataFrame:
    usable = matches[matches["matched_for_final_v3"]].copy()
    if usable.empty:
        return pd.DataFrame(
            columns=[
                "학교명",
                "학과_계열",
                "입결_프록시",
                "admission_metric_family_used_v3",
                "admission_metric_source_used_v3",
                "admission_source_rows_v3",
                "admission_source_units_v3",
                "admission_recruitment_n_sum_v3",
            ]
        )

    # Prefer general tables over regional/implicit tables. Then, inside each
    # university-department key, prefer official percentile rows over ratio rows.
    min_priority = usable.groupby(["학교명", "학과_계열"])["selection_priority"].transform("min")
    usable = usable[usable["selection_priority"].eq(min_priority)].copy()

    has_percentile = (
        usable.groupby(["학교명", "학과_계열"])["metric_family_v3"]
        .transform(lambda s: bool((s == "percentile").any()))
    )
    usable = usable[(~has_percentile) | usable["metric_family_v3"].eq("percentile")].copy()

    records: list[dict[str, Any]] = []
    for (school, label), group in usable.groupby(["학교명", "학과_계열"], dropna=False):
        records.append(
            {
                "학교명": school,
                "학과_계열": label,
                "입결_프록시": weighted_mean(group["admission_metric_v3"], group["recruitment_n_v3"]),
                "admission_metric_family_used_v3": join_unique(group["metric_family_v3"]),
                "admission_metric_source_used_v3": join_unique(group["metric_source_v3"]),
                "admission_source_rows_v3": int(len(group)),
                "admission_source_units_v3": join_unique(group["raw_recruitment_unit"]),
                "admission_recruitment_n_sum_v3": float(pd.to_numeric(group["recruitment_n_v3"], errors="coerce").fillna(0).sum()),
            }
        )
    return pd.DataFrame(records).sort_values(["학교명", "학과_계열"]).reset_index(drop=True)


def load_fetched_university_names() -> set[str]:
    """실제로 ADIGA fetch가 시도된(registry row가 존재하는) 학교명 집합.

    수동검토/폐교/코드중복 제외 등으로 애초에 크롤 대상이 아니었던 대학과, 크롤은 했지만
    결과표가 0건인 대학을 구분하기 위한 기준선이다.
    """
    registry = pd.read_csv(REGISTRY_PATH, low_memory=False)
    seed = pd.read_csv(SEED_PATH, low_memory=False, dtype={"univ_id": str})
    seed_map = seed[["univ_id", "univ_name_std"]].drop_duplicates("univ_id")
    fetched = registry[["univ_id"]].drop_duplicates().merge(seed_map, on="univ_id", how="left")
    return set(fetched["univ_name_std"].dropna())


def build_coverage(grade_keys: pd.DataFrame, matches: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    fetched_names = load_fetched_university_names()
    grade_counts = grade_keys.groupby("학교명").size().rename("final_grade_department_labels").reset_index()
    raw_counts = (
        matches.groupby("univ_name_std")
        .agg(
            raw_rows=("raw_row_id", "size"),
            raw_metric_nonnull=("admission_metric_v3", lambda s: int(s.notna().sum())),
            final_matched_source_rows=("matched_for_final_v3", "sum"),
        )
        .reset_index()
        .rename(columns={"univ_name_std": "학교명"})
    )
    dept_counts = (
        department.groupby("학교명")
        .agg(final_admission_department_labels=("학과_계열", "nunique"))
        .reset_index()
    )
    out = grade_counts.merge(raw_counts, on="학교명", how="left").merge(dept_counts, on="학교명", how="left")
    for col in ["raw_rows", "raw_metric_nonnull", "final_matched_source_rows", "final_admission_department_labels"]:
        out[col] = out[col].fillna(0).astype(int)
    out["admission_label_coverage_pct"] = np.where(
        out["final_grade_department_labels"].gt(0),
        out["final_admission_department_labels"] / out["final_grade_department_labels"] * 100,
        np.nan,
    )

    out["was_fetched"] = out["학교명"].isin(fetched_names)

    detail_conditions = [
        ~out["was_fetched"],
        out["was_fetched"] & out["raw_rows"].eq(0),
        out["raw_rows"].gt(0) & out["raw_metric_nonnull"].eq(0),
        out["raw_metric_nonnull"].gt(0) & out["final_admission_department_labels"].eq(0),
    ]
    detail_choices = [
        "not_crawled_or_scope_excluded",
        "fetched_but_result_tables_0",
        "raw_fetched_but_no_usable_metric",
        "metric_exists_but_department_unmatched",
    ]
    out["zero_coverage_detail_reason"] = np.select(detail_conditions, detail_choices, default="covered_or_partial")

    major_map = {
        "not_crawled_or_scope_excluded": "not_crawled_or_scope_excluded",
        "fetched_but_result_tables_0": "crawled_but_zero_coverage",
        "raw_fetched_but_no_usable_metric": "crawled_but_zero_coverage",
        "metric_exists_but_department_unmatched": "crawled_but_zero_coverage",
        "covered_or_partial": "covered_or_partial",
    }
    out["zero_coverage_major_reason"] = out["zero_coverage_detail_reason"].map(major_map)
    out = out.drop(columns=["was_fetched"])
    return out.sort_values(["final_admission_department_labels", "final_grade_department_labels"], ascending=[False, False])


def update_final_csv(department: pd.DataFrame) -> None:
    if not FINAL_CURRENT_PATH.exists():
        return
    final = pd.read_csv(FINAL_CURRENT_PATH, low_memory=False)
    final = final.drop(columns=["입결_프록시"], errors="ignore")
    final = final.merge(department[["학교명", "학과_계열", "입결_프록시"]], on=["학교명", "학과_계열"], how="left")
    columns = [
        "기준연도",
        "학교명",
        "학과_전공",
        "학과_계열",
        "입결_프록시",
        "A비율",
        "CD비율",
        "F비율",
        "전체취업률",
        "건보가입취업률",
        "전체진학률",
        "전문대학진학률",
        "대학진학률",
        "대학원진학률",
        "국내진학률",
        "국외진학률",
        "학점포기제유무",
    ]
    final = final[columns]
    save_csv(final, FINAL_CURRENT_PATH)


def build_report(
    row_metrics: pd.DataFrame,
    matches: pd.DataFrame,
    department: pd.DataFrame,
    coverage: pd.DataFrame,
    unmatched: pd.DataFrame,
) -> str:
    raw_rows = len(row_metrics)
    raw_univ_ids = row_metrics["univ_id"].nunique(dropna=True)
    raw_universities = row_metrics["univ_name_std"].nunique(dropna=True)
    metric_nonnull = int(row_metrics["admission_metric_v3"].notna().sum())
    metric_universities = row_metrics.loc[row_metrics["admission_metric_v3"].notna(), "univ_name_std"].nunique()
    matched_rows = int(matches["matched_for_final_v3"].sum())
    department_rows = len(department)
    final_rows = 0
    final_nonnull = 0
    final_universities = 0
    if FINAL_CURRENT_PATH.exists():
        final = pd.read_csv(FINAL_CURRENT_PATH, low_memory=False)
        final_rows = len(final)
        final_nonnull = int(final["입결_프록시"].notna().sum()) if "입결_프록시" in final else 0
        final_universities = final.loc[final.get("입결_프록시", pd.Series(dtype=float)).notna(), "학교명"].nunique()

    source_counts = row_metrics["metric_source_v3"].value_counts(dropna=False).rename_axis("source").reset_index(name="rows")
    family_counts = row_metrics["metric_family_v3"].value_counts(dropna=False).rename_axis("family").reset_index(name="rows")
    exclusion_counts = matches["match_exclusion_reason_v3"].replace("", "final_matched").value_counts().rename_axis("reason").reset_index(name="rows")

    top_missing_univs = coverage[coverage["final_admission_department_labels"].eq(0)].head(15)

    def md_table(df: pd.DataFrame, max_rows: int = 12) -> str:
        if df.empty:
            return "_empty_"
        view = df.head(max_rows).copy()
        cols = list(view.columns)
        lines = [
            "| " + " | ".join(str(col) for col in cols) + " |",
            "| " + " | ".join("---" for _ in cols) + " |",
        ]
        for _, row in view.iterrows():
            vals = []
            for col in cols:
                value = row[col]
                if isinstance(value, float):
                    value = "" if math.isnan(value) else f"{value:.4g}"
                vals.append(str(value).replace("|", "/"))
            lines.append("| " + " | ".join(vals) + " |")
        return "\n".join(lines)

    report = f"""# ADIGA 2024 정시 입결 v3 자동확정 대학 확장 보고: 최종 {final_universities}개 대학 커버 (대상 227개 중)

## 결론

v2(51개 대학, 실제 매칭 성공 44개)에서 미수집이었던 대학을 추가로 크롤링해 `crawl_2024_admission_full`
(병합본, 기존 51개 + 신규 확정 168개)로 자동 추출·정규화·매칭을 다시 수행했다. 이번 산출물은
**ADIGA 코드가 자동확정(혹은 사람이 직접 확정)된 대학까지의 결과**이며, 최종 CSV에서 실제로
입결_프록시가 채워진 대학은 227개 중 **{final_universities}개**다. 나머지는 ①ADIGA 코드/후보 확정이
안 된 대학(수동검토 대기), ②페이지는 수집했으나 결과표 파싱/학과 매칭이 안 된 대학,
③ADIGA 자체에 정시·수능위주 데이터가 없는 대학(과학기술원류·방송통신대 등)으로 나뉜다 —
아래 "0커버 대학" 섹션에서 원인별로 구분해서 확인할 수 있다.

## 적용한 의사결정

1. 같은 row에 `최종등록자 70% cut 평균 백분위` 또는 다중 헤더의 `평균/백분위` 열이 있으면 그 값을 1순위로 사용했다.
2. `raw_percentile_70cut`이 0~100이면 백분위로 인정했다.
3. `raw_percentile_70cut`이 100 초과이거나 백분위가 없고, 같은 row에 `대학별 환산점수`와 `총점/최고점`이 있으면 `점수 / 총점 * 100`으로 보조 정규화했다.
4. 농어촌, 기회균등, 고른기회, 저소득, 실기/체육 등 특별 전형은 최종 매칭에서 제외했다.
5. `인문계열`, `자유전공`, `광역`, 단독 `OO대학`처럼 세부 학과로 보기 어려운 광역 모집단위는 최종 매칭에서 제외했다.
6. 같은 대학-학과에 여러 row가 있으면 모집인원 가중평균을 사용했고, 모집인원이 없으면 단순평균으로 대체했다.
7. 최종 CSV에는 사용자가 요구한 컬럼만 유지했고, 추출/매칭 근거는 별도 감사 파일에만 남겼다.

## 주요 수치

| 항목 | 값 |
|---|---:|
| 원본 row | {raw_rows:,} |
| 원본 ADIGA `univ_id` 수 | {raw_univ_ids:,} |
| 원본 표준 대학명 수 | {raw_universities:,} |
| v3 입결 metric 추출 row | {metric_nonnull:,} |
| v3 입결 metric 추출 대학 수 | {metric_universities:,} |
| 최종 매칭 source row | {matched_rows:,} |
| 대학-학과 입결 집계 row | {department_rows:,} |
| 업데이트된 최종 CSV row | {final_rows:,} |
| 최종 CSV 입결 non-null row | {final_nonnull:,} |
| 최종 CSV 입결 non-null 대학 수 | {final_universities:,} |

## metric source 분포

{md_table(source_counts)}

## metric family 분포

{md_table(family_counts)}

## 매칭/탈락 사유

{md_table(exclusion_counts)}

## 입결 커버리지 0인 대학 — 대분류

{md_table(coverage[coverage["final_admission_department_labels"].eq(0)]["zero_coverage_major_reason"].value_counts().rename_axis("zero_coverage_major_reason").reset_index(name="대학수"))}

## 입결 커버리지 0인 대학 — 세부 원인

{md_table(coverage[coverage["final_admission_department_labels"].eq(0)]["zero_coverage_detail_reason"].value_counts().rename_axis("zero_coverage_detail_reason").reset_index(name="대학수"))}

- `not_crawled_or_scope_excluded`: registry에 fetch 기록 자체가 없음 — **13개 전체가
  `00_scope_exclusion_2024_full.csv` 한 파일에 감사 추적 가능**: `manual_review_pending` 9개
  + `closed_institution`(폐교) 3개 + `code_duplicate_no_separate_source`(ADIGA가 별도 캠퍼스
  코드를 안 줘서 제외 — 경인교육대학교_제2캠퍼스) 1개 = 13개
- `fetched_but_result_tables_0`: **크롤은 했지만** Ⅳ탭에서 결과표를 못 찾음(`parse_status=partial`,
  `result_tables=0`) — `01_crawl_source_registry_merged.csv`에서 정확히 식별 가능. 표 구조가 기존
  51개와 달라 헤더 판별 로직이 못 잡는 경우가 다수로 추정된다(파서 한계, 아래 참고)
- `raw_fetched_but_no_usable_metric`: 결과표는 찾았으나 usable 백분위/점수 셀이 없음
- `metric_exists_but_department_unmatched`: 입결 수치는 뽑았으나 그 대학의 기존 학과_계열 목록과 매칭 실패(학과명 표기 차이)

## 입결 커버리지 0인 대학 상위 (원인 포함)

{md_table(top_missing_univs[["학교명", "final_grade_department_labels", "raw_rows", "raw_metric_nonnull", "final_admission_department_labels", "zero_coverage_major_reason", "zero_coverage_detail_reason"]], 15)}

## 산출 파일

- row 단위 추출 결과: `{ROW_METRIC_PATH}`
- row 단위 매칭 감사: `{MATCH_PATH}`
- 최종 CSV에 붙인 대학-학과 입결표: `{DEPARTMENT_PATH}`
- 미매칭/검토 큐: `{UNMATCHED_PATH}`
- 대학별 커버리지: `{COVERAGE_PATH}`
- 업데이트된 최종 CSV: `{FINAL_CURRENT_PATH}`

## 남은 한계

- `00_scope_exclusion_2024_full.csv`에 남은 13개(`manual_review_pending` 9개 + `closed_institution`
  폐교 3개 + `code_duplicate_no_separate_source` 1개)가 감사 추적 가능하게 정리돼 있다.
  `manual_review_pending` 9개(과학기술원류 4개, 한국방송통신대학교, 한국예술종합학교,
  한국전통문화대학교, 한국에너지공과대학교, 순복음총회신학교)는 ADIGA 표준 검색 UI로 여러 별칭을
  시도해도 결과가 없어 현재로선 정시 CSAT 트랙 데이터 자체가 ADIGA에 없는 것으로 판단된다
  (과학기술원류는 자체 특별전형, 방송통신대는 원격대학, 예술종합학교는 실기 위주 전형이라 추정).
- alias 충돌 164건 중 실제 admission raw 데이터에 등장하는 것부터 keep/drop/canonical_override를
  결정한 감사 파일은 `P2_admission_alias_collision_decisions_v3.csv`에 있다(아래 참고).
- `department_label_not_in_university_grade`/`empty_recruitment_unit` 사유로 매칭되지 못한 대학이
  일부 남아 있다. 그 중 일부(중부대학교·신경주대학교 등)는 크로스워크가 아니라 **파서가 2행 헤더
  테이블의 두 번째 헤더 행을 데이터 행으로 오인하는 구조적 한계**이며, 51개 검증셋에 대한 회귀
  위험 때문에 이번 배치에서는 파서 자체를 고치지 않았다 — 별도 검증 배치로 분리해야 한다.
"""
    save_csv(source_counts, OUT_DIR / "P2_admission_metric_source_counts_v3.csv")
    save_csv(family_counts, OUT_DIR / "P2_admission_metric_family_counts_v3.csv")
    save_csv(exclusion_counts, OUT_DIR / "P2_admission_match_exclusion_counts_v3.csv")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    return report


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EDA_TABLE_DIR.mkdir(parents=True, exist_ok=True)

    strict, loose, _ = load_department_aliases()
    grade_keys = build_grade_keys(strict, loose)
    row_metrics = build_row_metrics()
    matches = attach_matches(row_metrics, grade_keys, strict, loose)
    department = aggregate_by_department(matches)
    coverage = build_coverage(grade_keys, matches, department)
    unmatched = matches[
        matches["admission_metric_v3"].notna()
        & ~matches["matched_for_final_v3"]
        & matches["primary_selection_candidate"]
    ].copy()

    save_csv(row_metrics, ROW_METRIC_PATH)
    save_csv(matches, MATCH_PATH)
    save_csv(department, DEPARTMENT_PATH)
    save_csv(unmatched, UNMATCHED_PATH)
    save_csv(coverage, COVERAGE_PATH)
    save_csv(coverage, EDA_TABLE_DIR / "15_admission_v3_coverage_by_university.csv")
    save_csv(unmatched, EDA_TABLE_DIR / "16_admission_v3_unmatched_review.csv")

    update_final_csv(department)
    build_report(row_metrics, matches, department, coverage, unmatched)

    print(f"saved={DEPARTMENT_PATH}")
    print(f"row_metrics_shape={row_metrics.shape}")
    print(f"matches_shape={matches.shape}")
    print(f"department_shape={department.shape}")
    print(f"final_admission_non_null={len(department)}")
    print(f"report={REPORT_PATH}")


if __name__ == "__main__":
    main()
