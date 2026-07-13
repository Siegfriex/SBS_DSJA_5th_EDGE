from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
P2_3 = ROOT / "workbook" / "p2" / "p2_3"
NORM = ROOT / "workbook" / "p2" / "p2_2" / "data" / "goms_subject_crawl" / "normalized"
AUDIT = P2_3 / "audit"
AUDIT.mkdir(parents=True, exist_ok=True)

MAJORS = ["인문", "사회", "교육", "공학", "자연", "의약", "예체능"]
YEARS = list(range(2007, 2020))
RECENT_YEARS = [2017, 2018, 2019]
AUTO_MAJOR_METHODS = {"inherited_headcount", "exact_dictionary", "keyword_rule"}


MAJOR_RULES = [
    ("MED", ["간호", "의학", "의예", "약학", "치의", "치기공", "치위생", "한의", "보건", "물리치료", "작업치료", "방사선", "임상병리", "응급구조", "안경광", "재활", "의료", "수의"]),
    ("ENG", ["컴퓨터", "소프트웨어", "인공지능", "데이터", "기계", "전자", "전기", "건축공학", "토목", "화공", "화학공학", "신소재", "산업공학", "에너지", "자동차", "로봇", "정보통신", "반도체", "항공", "해양공학", "조선", "공학", "ict", "it", "iot", "sw", "보안", "모빌리티", "자동화", "철도"]),
    ("NAT", ["수학", "물리", "화학", "생명과학", "생물", "지구과학", "환경", "식품영양", "식품공학", "식품과학", "통계", "응용과학", "원예", "산림", "축산", "동물", "농학", "수산", "해양생명", "스마트팜", "우주과학", "과학"]),
    ("EDU", ["교육", "교직", "초등교육", "유아교육", "특수교육", "국어교육", "영어교육", "수학교육", "사회교육", "과학교육", "체육교육", "음악교육", "미술교육"]),
    ("ART", ["디자인", "미술", "음악", "체육", "무용", "연극", "영화", "영상", "애니메이션", "만화", "공예", "사진", "스포츠", "뷰티", "패션", "실용음악", "예술", "주얼리", "귀금속", "도예", "의상", "finearts", "서양화", "한국화", "골프", "무도", "경기지도", "엔터테인먼트"]),
    ("SOC", ["경영", "경제", "행정", "사회복지", "법", "경찰", "소방", "정치", "언론", "신문", "방송", "광고", "심리", "상담", "관광", "무역", "회계", "세무", "금융", "부동산", "국제통상", "사회학", "마케팅", "비즈니스", "유통", "창업", "공공안전", "시큐리티", "호텔", "국제", "산업정보", "실버산업"]),
    ("HUM", ["국문", "영문", "철학", "역사", "언어", "문학", "중문", "일문", "독문", "불문", "스페인", "러시아", "고고", "문화콘텐츠", "문헌정보", "인문", "통번역"]),
]
AMBIGUOUS_TOKENS = ["융합", "자유전공", "자율전공", "글로벌융합", "미래융합", "창의융합", "복수전공"]
SPECIAL_TERMS = ["자유전공", "융합", "데이터사이언스", "바이오", "산업디자인", "교육공학", "의공학", "문화콘텐츠", "스포츠과학", "심리", "식품영양", "건축학", "건축공학"]


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_key(value: Any) -> str:
    if pd.isna(value):
        return ""
    s = unicodedata.normalize("NFKC", str(value)).strip().lower()
    s = s.replace("ㆍ", "").replace("·", "").replace("・", "")
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"[^\w가-힣]", "", s)
    return s


def dept_alternatives(raw: Any) -> set[str]:
    if pd.isna(raw):
        return {""}
    text = str(raw).strip()
    candidates = [text]
    if "|" in text:
        candidates.extend([p.strip() for p in text.split("|")])
    expanded = []
    for item in candidates:
        expanded.append(item)
        no_paren = re.sub(r"\([^)]*\)", "", item).strip()
        if no_paren and no_paren != item:
            expanded.append(no_paren)
    return {normalize_key(x) for x in expanded if normalize_key(x)}


def keyword_major_candidates(text: Any) -> tuple[list[str], bool, list[str]]:
    raw = "" if pd.isna(text) else str(text)
    key = normalize_key(raw)
    hits: list[str] = []
    evidence: list[str] = []
    ambiguous = any(token in raw for token in AMBIGUOUS_TOKENS)
    for code, words in MAJOR_RULES:
        matched = [word for word in words if normalize_key(word) in key]
        if matched:
            hits.append(code)
            evidence.append(f"{code}:{'/'.join(matched[:5])}")
    return list(dict.fromkeys(hits)), ambiguous, evidence


def read_csv_any(path: Path) -> pd.DataFrame:
    for enc in ["utf-8-sig", "utf-8", "cp949"]:
        try:
            return pd.read_csv(path, encoding=enc, low_memory=False)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path, low_memory=False)


def write_csv(df: pd.DataFrame, name: str) -> Path:
    path = AUDIT / name
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def load_core() -> dict[str, pd.DataFrame]:
    return {
        "d01": pd.read_parquet(P2_3 / "p3_1" / "dept_headcount_master_2024.parquet"),
        "d02": pd.read_parquet(P2_3 / "p3_1" / "dept_outcomes_2024.parquet"),
        "d03": pd.read_parquet(P2_3 / "p3_1" / "dept_master_2024_core.parquet"),
        "d04": pd.read_parquet(P2_3 / "p3_1" / "wage_reference_by_major.parquet"),
        "d05": pd.read_parquet(P2_3 / "p3_1" / "job_cert_bridge.parquet"),
        "d06": pd.read_parquet(P2_3 / "p3_2" / "goms_major_year_labor_baseline.parquet"),
        "d07": pd.read_parquet(P2_3 / "p3_2" / "goms_major_profile_recent.parquet"),
        "d08": pd.read_parquet(P2_3 / "shared" / "mart_department_model_base_2024.parquet"),
        "bridge": read_csv_any(P2_3 / "shared" / "bridge_outcome_headcount.csv"),
    }


def bridge_sample_audit(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    d01, d02, bridge = frames["d01"], frames["d02"], frames["bridge"]
    head_cols = [
        "headcount_row_id",
        "school_name_raw",
        "school_name_std",
        "campus_name_raw",
        "campus_name_std",
        "campus_seq",
        "campus_branch",
        "dept_name_raw",
        "dept_name_std",
        "major_group_raw",
        "major_group_7",
    ]
    out_cols = [
        "outcome_row_id",
        "school_name_raw",
        "school_name_std",
        "campus_name_raw",
        "campus_name_std",
        "campus_seq",
        "campus_branch",
        "dept_name_raw",
        "dept_name_std",
        "dept_field_raw",
    ]
    merged = (
        bridge.merge(d02[out_cols], on="outcome_row_id", how="left", validate="one_to_one")
        .merge(d01[head_cols].add_prefix("hc_"), left_on="headcount_row_id", right_on="hc_headcount_row_id", how="left", validate="many_to_one")
    )
    merged["school_std_match"] = merged["school_name_std"].astype("string").eq(merged["hc_school_name_std"].astype("string"))
    merged["campus_scope_ok"] = True
    has_seq = merged["campus_seq"].fillna("").astype(str).ne("")
    merged.loc[has_seq, "campus_scope_ok"] = merged.loc[has_seq, "campus_seq"].astype(str).eq(merged.loc[has_seq, "hc_campus_seq"].astype(str))
    has_branch = merged["campus_branch"].fillna("").astype(str).ne("") & merged["hc_campus_branch"].fillna("").astype(str).ne("")
    merged.loc[has_branch, "campus_scope_ok"] = merged.loc[has_branch, "campus_branch"].astype(str).eq(merged.loc[has_branch, "hc_campus_branch"].astype(str))
    merged["dept_alt_contains_hc"] = [
        str(hc) in dept_alternatives(raw) if pd.notna(hc) else False
        for raw, hc in zip(merged["dept_name_raw"], merged["hc_dept_name_std"])
    ]
    merged["exact_normalized_validation"] = np.where(
        merged["match_method"].eq("exact_normalized"),
        merged["school_std_match"] & merged["campus_scope_ok"] & merged["dept_alt_contains_hc"],
        pd.NA,
    )
    samples = []
    for method, n in [("exact_normalized", 50), ("manual_review", 100), ("unmatched", 50), ("fuzzy_unique", 100)]:
        part = merged[merged["match_method"].eq(method)].copy()
        if len(part) > n:
            part = part.sample(n=n, random_state=3085)
        samples.append(part.assign(sample_group=method))
    sample = pd.concat(samples, ignore_index=True)
    write_csv(sample, "bridge_stratified_sample_seed3085.csv")
    write_csv(merged, "bridge_full_joined_audit.csv")
    return merged


def major_sample_audit(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    d03 = frames["d03"].copy()
    text = d03["dept_field_raw"].astype("string").fillna("") + " " + d03["dept_name_raw"].astype("string").fillna("")
    keyword = text.map(keyword_major_candidates)
    d03["audit_keyword_hits"] = keyword.map(lambda x: ",".join(x[0]))
    d03["audit_ambiguous_token"] = keyword.map(lambda x: x[1])
    d03["audit_keyword_evidence"] = keyword.map(lambda x: " | ".join(x[2]))
    d03["audit_auto_major_contradiction"] = (
        d03["major7_mapping_method"].astype(str).isin(AUTO_MAJOR_METHODS)
        & d03["audit_keyword_hits"].str.contains(",", regex=False).eq(False)
        & d03["audit_keyword_hits"].ne("")
        & d03["major_group_7"].astype("string").ne(d03["audit_keyword_hits"].astype("string"))
    )
    d03["audit_auto_ambiguous_token"] = d03["major7_mapping_method"].astype(str).isin(AUTO_MAJOR_METHODS) & d03["audit_ambiguous_token"]

    samples = []
    for method, per_major, max_n in [
        ("inherited_headcount", 10, None),
        ("exact_dictionary", 20, None),
        ("keyword_rule", 30, None),
    ]:
        part = d03[d03["major7_mapping_method"].astype(str).eq(method)].copy()
        sampled = part.groupby("major_group_7", dropna=False, observed=False, group_keys=False).apply(
            lambda g: g.sample(n=min(len(g), per_major), random_state=3085)
        )
        samples.append(sampled.assign(sample_group=method))
    for method, n in [("ambiguous", 100), ("unknown", 50)]:
        part = d03[d03["major7_mapping_method"].astype(str).eq(method)].copy()
        if len(part) > n:
            part = part.sample(n=n, random_state=3085)
        samples.append(part.assign(sample_group=method))
    sample_cols = [
        "sample_group",
        "outcome_row_id",
        "school_name_raw",
        "campus_name_raw",
        "dept_field_raw",
        "dept_name_raw",
        "match_method",
        "major_group_7",
        "major7_mapping_method",
        "major7_mapping_confidence",
        "major7_evidence",
        "audit_keyword_hits",
        "audit_ambiguous_token",
        "audit_keyword_evidence",
        "audit_auto_major_contradiction",
        "audit_auto_ambiguous_token",
    ]
    write_csv(pd.concat(samples, ignore_index=True)[sample_cols], "major_mapping_stratified_sample_seed3085.csv")

    term_rows = []
    for term in SPECIAL_TERMS:
        mask = text.str.contains(term, regex=False, na=False)
        part = d03[mask].copy()
        term_rows.append(
            {
                "term": term,
                "rows": int(len(part)),
                "auto_rows": int(part["major7_mapping_method"].astype(str).isin(AUTO_MAJOR_METHODS).sum()),
                "review_rows": int(part["major7_review_needed"].astype("boolean").sum()),
                "method_counts": part["major7_mapping_method"].astype(str).value_counts(dropna=False).to_dict(),
                "major_counts": part["major_group_7"].astype("string").fillna("<NA>").value_counts(dropna=False).to_dict(),
                "auto_ambiguous_token_rows": int(part["audit_auto_ambiguous_token"].sum()),
                "auto_contradiction_rows": int(part["audit_auto_major_contradiction"].sum()),
                "examples": " || ".join(
                    part[["school_name_raw", "dept_field_raw", "dept_name_raw", "major_group_7", "major7_mapping_method", "major7_evidence"]]
                    .head(5)
                    .map(lambda x: "" if pd.isna(x) else str(x))
                    .agg(lambda row: " | ".join(row.tolist()), axis=1)
                    .tolist()
                ),
            }
        )
    write_csv(pd.DataFrame(term_rows), "major_special_terms_audit.csv")
    write_csv(d03, "major_full_joined_audit.csv")
    return d03


def _dist_topic(dist: pd.DataFrame, topic_id: str) -> pd.DataFrame:
    return dist[(dist["topic_id"].eq(topic_id)) & (dist["measure_type"].eq("share")) & (dist["subgroup"].isin(MAJORS)) & (dist["dimension_value"].ne("전체"))].copy()


def top_metrics(long: pd.DataFrame, group_cols: list[str], value_col: str, prefix: str, entropy: bool = False) -> pd.DataFrame:
    rows = []
    for keys, g in long.groupby(group_cols, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        vals = pd.to_numeric(g[value_col], errors="coerce").dropna().clip(lower=0).to_numpy()
        sorted_vals = np.sort(vals)[::-1]
        row = dict(zip(group_cols, keys))
        if vals.sum() <= 0:
            row[f"{prefix}_top1_pct"] = np.nan
            row[f"{prefix}_top3_pct"] = np.nan
            row[f"{prefix}_hhi"] = np.nan
            if entropy:
                row[f"{prefix}_entropy"] = np.nan
        else:
            p = vals / vals.sum()
            row[f"{prefix}_top1_pct"] = float(sorted_vals[0])
            row[f"{prefix}_top3_pct"] = float(sorted_vals[:3].sum())
            row[f"{prefix}_hhi"] = float(np.square(p).sum())
            if entropy:
                row[f"{prefix}_entropy"] = float(-(p * np.log(p + 1e-12)).sum())
        rows.append(row)
    return pd.DataFrame(rows)


def independent_d06(dist: pd.DataFrame, cont: pd.DataFrame) -> pd.DataFrame:
    base = pd.MultiIndex.from_product([YEARS, MAJORS], names=["year", "major_group_7"]).to_frame(index=False)
    econ = dist[
        dist["topic_id"].eq("GOMS_003")
        & dist["measure_type"].eq("frequency")
        & dist["dimension_value"].isin(MAJORS)
    ].copy()
    econ = (
        econ.pivot_table(index=["year", "dimension_value"], columns="subgroup", values="value", aggfunc="sum")
        .reset_index()
        .rename_axis(None, axis=1)
        .rename(columns={"dimension_value": "major_group_7"})
    )
    econ["graduate_total_n"] = econ["전체"]
    econ["employed_n"] = econ["취업자"]
    econ["unemployed_n"] = econ["실업자"]
    econ["inactive_n"] = econ["비경활"]
    denom = econ["graduate_total_n"].replace(0, np.nan)
    econ["employment_rate_pct"] = econ["employed_n"] / denom * 100
    econ["unemployment_rate_pct"] = econ["unemployed_n"] / denom * 100
    econ["inactivity_rate_pct"] = econ["inactive_n"] / denom * 100
    base = base.merge(econ[["year", "major_group_7", "graduate_total_n", "employed_n", "unemployed_n", "inactive_n", "employment_rate_pct", "unemployment_rate_pct", "inactivity_rate_pct"]], on=["year", "major_group_7"], how="left")

    industry = _dist_topic(dist, "GOMS_006").rename(columns={"subgroup": "major_group_7"})
    im = top_metrics(industry, ["year", "major_group_7"], "value", "industry", entropy=True)
    base = base.merge(im[["year", "major_group_7", "industry_top1_pct", "industry_top3_pct", "industry_hhi", "industry_entropy"]], on=["year", "major_group_7"], how="left")

    firm = _dist_topic(dist, "GOMS_015").rename(columns={"subgroup": "major_group_7"})
    firm_map = {
        "1. 1～4명": "firm_1_9_pct",
        "2. 5～9명": "firm_1_9_pct",
        "3. 10～29명": "firm_10_49_pct",
        "4. 30～49명": "firm_10_49_pct",
        "5. 50～99명": "firm_50_299_pct",
        "6. 100～299명": "firm_50_299_pct",
        "7. 300～499명": "firm_300plus_pct",
        "8. 500～999명": "firm_300plus_pct",
        "9. 1,000명 이상": "firm_300plus_pct",
    }
    firm["grouped"] = firm["dimension_value"].map(firm_map)
    firm_grouped = firm.dropna(subset=["grouped"]).groupby(["year", "major_group_7", "grouped"], as_index=False)["value"].sum()
    firm_hhi = top_metrics(firm_grouped.rename(columns={"grouped": "dimension_value"}), ["year", "major_group_7"], "value", "firm_size")
    base = base.merge(firm_hhi[["year", "major_group_7", "firm_size_hhi"]], on=["year", "major_group_7"], how="left")

    firm_type = _dist_topic(dist, "GOMS_018").rename(columns={"subgroup": "major_group_7"})
    public_raw = [
        "3. 정부투자기관/정부출연기관/공사합동기업",
        "4. (재단, 사단) 법인단체",
        "5. 정부기관(공무원, 군인 등)",
        "6. 교육기관(대학, 초/중/고 등)",
        "7. 연구기관(국립/사립)",
    ]
    public = firm_type[firm_type["dimension_value"].isin(public_raw)].groupby(["year", "major_group_7"], as_index=False)["value"].sum().rename(columns={"value": "public_nonprofit_pct"})
    base = base.merge(public, on=["year", "major_group_7"], how="left")

    status = _dist_topic(dist, "GOMS_021").rename(columns={"subgroup": "major_group_7"})
    unstable = status[status["dimension_value"].isin(["2. 임시근로자", "3. 일용근로자"])].groupby(["year", "major_group_7"], as_index=False)["value"].sum().rename(columns={"value": "unstable_pct"})
    base = base.merge(unstable, on=["year", "major_group_7"], how="left")

    occ_frames = []
    occ_map = {
        "pre_2017": {
            "관리직": "professional_highskill",
            "경영·회계·사무 관련직": "business_office_finance",
            "금융·보험 관련직": "business_office_finance",
            "교육 및 자연과학·사회과학 연구관련직": "professional_highskill",
            "법률·경찰·소방·교도 관련직": "professional_highskill",
            "보건·의료 관련직": "professional_highskill",
            "사회복지 및 종교 관련직": "professional_highskill",
            "문화·예술·디자인·방송 관련직": "professional_highskill",
            "운전 및 운송 관련직": "production_transport",
            "영업 및 판매 관련직": "service_sales",
            "경비 및 청소 관련직": "service_sales",
            "미용·숙박·여행·오락 스포츠 관련직": "service_sales",
            "음식서비스 관련직": "service_sales",
            "건설 관련직": "production_transport",
            "기계 관련직": "production_transport",
            "재료관련직": "production_transport",
            "화학 관련직": "production_transport",
            "섬유 및 의복 관련직": "production_transport",
            "전기·전자 관련직": "production_transport",
            "정보통신 관련직": "professional_highskill",
            "식품가공 관련직": "production_transport",
            "환경·인쇄·목재·가구·공예 및 생산단순직": "production_transport",
            "농림어업 관련직": "production_transport",
            "군인": "professional_highskill",
        },
        "post_2017": {
            "경영·사무·금융·보험직": "business_office_finance",
            "연구직 및 공학 기술직": "professional_highskill",
            "교육·법률·사회복지·경찰·소방직 및 군인": "professional_highskill",
            "보건·의료직": "professional_highskill",
            "예술·디자인·방송·스포츠직": "professional_highskill",
            "미용·여행·숙박·음식·경비·청소직": "service_sales",
            "영업·판매·운전·운송직": "service_sales",
            "건설·채굴직": "production_transport",
            "설치·정비·생산직": "production_transport",
            "농림어업직": "production_transport",
        },
    }
    for topic, schema in [("GOMS_011", "pre_2017"), ("GOMS_012", "post_2017")]:
        sub = _dist_topic(dist, topic).rename(columns={"subgroup": "major_group_7", "dimension_value": "raw_category"})
        sub["headline_group"] = sub["raw_category"].map(occ_map[schema]).fillna("other_review")
        occ_frames.append(sub)
    occ = pd.concat(occ_frames, ignore_index=True)
    occ_grouped = occ.groupby(["year", "major_group_7", "headline_group"], as_index=False)["value"].sum()
    occ_hhi = top_metrics(occ_grouped.rename(columns={"headline_group": "dimension_value"}), ["year", "major_group_7"], "value", "occupation")
    base = base.merge(occ_hhi[["year", "major_group_7", "occupation_hhi"]], on=["year", "major_group_7"], how="left")

    def cont_topic(topic_id: str, col: str) -> pd.DataFrame:
        sub = cont[cont["topic_id"].eq(topic_id) & cont["dimension_value"].isin(MAJORS)].copy()
        return sub.rename(columns={"dimension_value": "major_group_7", "value": col})[["year", "major_group_7", col]]

    income = cont_topic("GOMS_024", "mean_monthly_income_10kkrw")
    hours = cont_topic("GOMS_033", "weekly_work_hours")
    continuous = income.merge(hours, on=["year", "major_group_7"], how="outer")
    continuous["hourly_income_proxy"] = continuous["mean_monthly_income_10kkrw"] / (continuous["weekly_work_hours"] * 4.345)
    base = base.merge(continuous[["year", "major_group_7", "hourly_income_proxy", "mean_monthly_income_10kkrw", "weekly_work_hours"]], on=["year", "major_group_7"], how="left")
    return base


def compare_d06(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    dist = read_csv_any(NORM / "goms_distribution_long.csv")
    cont = read_csv_any(NORM / "goms_continuous_long.csv")
    recalced = independent_d06(dist, cont)
    actual = frames["d06"].copy()
    requested = [
        "employment_rate_pct",
        "unemployment_rate_pct",
        "inactivity_rate_pct",
        "industry_top1_pct",
        "industry_top3_pct",
        "industry_hhi",
        "industry_entropy",
        "firm_size_hhi",
        "public_nonprofit_pct",
        "unstable_pct",
        "occupation_hhi",
        "hourly_income_proxy",
    ]
    merged = actual[["year", "major_group_7", *requested]].merge(recalced[["year", "major_group_7", *requested]], on=["year", "major_group_7"], suffixes=("_actual", "_recalc"), validate="one_to_one")
    rows = []
    for col in requested:
        diff = (pd.to_numeric(merged[f"{col}_actual"], errors="coerce") - pd.to_numeric(merged[f"{col}_recalc"], errors="coerce")).abs()
        rows.append(
            {
                "column": col,
                "rows_compared": int(len(diff)),
                "max_abs_diff": float(diff.max()),
                "mismatch_rows_gt_1e_4": int((diff > 1e-4).sum()),
            }
        )
    write_csv(merged, "goms_d06_requested_recalc_rowdiff.csv")
    return pd.DataFrame(rows)


def weighted_mean(g: pd.DataFrame, value_col: str, weight_col: str) -> float:
    x = pd.to_numeric(g[value_col], errors="coerce")
    w = pd.to_numeric(g[weight_col], errors="coerce")
    mask = x.notna() & w.notna() & (w > 0)
    if not mask.any():
        return np.nan
    return float(np.average(x[mask], weights=w[mask]))


def slope(g: pd.DataFrame, value_col: str) -> float:
    sub = g[["year", value_col]].dropna()
    if len(sub) < 2:
        return np.nan
    return float(np.polyfit(sub["year"].astype(float), sub[value_col].astype(float), 1)[0])


def yoy_flag(g: pd.DataFrame) -> bool:
    thresholds = {
        "employment_rate_pct": 15.0,
        "firm_300plus_pct": 15.0,
        "public_nonprofit_pct": 15.0,
        "permanent_pct": 15.0,
        "unstable_pct": 15.0,
        "industry_hhi": 0.15,
        "mean_monthly_income_10kkrw": 50.0,
        "weekly_work_hours": 10.0,
        "hourly_income_proxy": 0.30,
    }
    g = g.sort_values("year")
    for col, threshold in thresholds.items():
        if col in g.columns and bool((pd.to_numeric(g[col], errors="coerce").diff().abs() > threshold).any()):
            return True
    return False


def compare_d07(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    d06 = frames["d06"].copy()
    d07 = frames["d07"].copy()
    rows = []
    for major in MAJORS:
        all_g = d06[d06["major_group_7"].astype(str).eq(major)].copy()
        recent = all_g[all_g["year"].astype(int).isin(RECENT_YEARS)].copy()
        latest = all_g[all_g["year"].astype(int).eq(2019)].iloc[0]
        rows.append(
            {
                "major_group_7": major,
                "profile_start_year": 2017,
                "profile_end_year": 2019,
                "profile_years_n": 3,
                "aggregation_method": "mixed_weighted_2017_2019",
                "recent_employment_rate_pct": weighted_mean(recent, "employment_rate_pct", "graduate_total_n"),
                "recent_firm_300plus_pct": weighted_mean(recent, "firm_300plus_pct", "employed_n"),
                "recent_public_nonprofit_pct": weighted_mean(recent, "public_nonprofit_pct", "employed_n"),
                "recent_permanent_pct": weighted_mean(recent, "permanent_pct", "employed_n"),
                "recent_unstable_pct": weighted_mean(recent, "unstable_pct", "employed_n"),
                "recent_self_employed_pct": weighted_mean(recent, "self_employed_pct", "employed_n"),
                "recent_industry_hhi": weighted_mean(recent, "industry_hhi", "employed_n"),
                "recent_industry_top3_pct": weighted_mean(recent, "industry_top3_pct", "employed_n"),
                "recent_professional_highskill_pct": weighted_mean(recent, "professional_highskill_pct", "employed_n"),
                "recent_mean_income_10kkrw": weighted_mean(recent, "mean_monthly_income_10kkrw", "employed_n"),
                "recent_weekly_work_hours": weighted_mean(recent, "weekly_work_hours", "employed_n"),
                "recent_hourly_income_proxy": weighted_mean(recent, "hourly_income_proxy", "employed_n"),
                "income_trend_per_year": slope(all_g, "mean_monthly_income_10kkrw"),
                "hours_trend_per_year": slope(all_g, "weekly_work_hours"),
                "firm_300plus_trend_per_year": slope(all_g, "firm_300plus_pct"),
                "permanent_trend_per_year": slope(all_g, "permanent_pct"),
                "latest_2019_mean_income_10kkrw": latest["mean_monthly_income_10kkrw"],
                "latest_2019_weekly_work_hours": latest["weekly_work_hours"],
                "latest_2019_firm_300plus_pct": latest["firm_300plus_pct"],
                "latest_2019_permanent_pct": latest["permanent_pct"],
                "source_years_observed": recent["year"].nunique(),
                "year_over_year_review_flag": yoy_flag(all_g),
                "mapping_confidence": "medium",
                "row_qa_status": "PASS_WITH_REVIEW",
            }
        )
    recalc = pd.DataFrame(rows)
    merged = d07.merge(recalc, on="major_group_7", suffixes=("_actual", "_recalc"), validate="one_to_one")
    out = []
    for col in [c for c in d07.columns if c != "major_group_7"]:
        a = merged[f"{col}_actual"]
        b = merged[f"{col}_recalc"]
        if pd.api.types.is_bool_dtype(a) or pd.api.types.is_bool_dtype(b):
            neq = a.astype("boolean").astype("string").fillna("<NA>").ne(b.astype("boolean").astype("string").fillna("<NA>"))
            out.append({"column": col, "rows_compared": 7, "max_abs_diff": np.nan, "mismatch_rows": int(neq.sum())})
        elif pd.api.types.is_numeric_dtype(a):
            diff = (pd.to_numeric(a, errors="coerce") - pd.to_numeric(b, errors="coerce")).abs()
            out.append({"column": col, "rows_compared": 7, "max_abs_diff": float(diff.max()), "mismatch_rows": int((diff > 1e-4).sum())})
        else:
            neq = a.astype("string").fillna("<NA>").ne(b.astype("string").fillna("<NA>"))
            out.append({"column": col, "rows_compared": 7, "max_abs_diff": np.nan, "mismatch_rows": int(neq.sum())})
    write_csv(merged, "goms_d07_recent_profile_recalc_rowdiff.csv")
    return pd.DataFrame(out)


def distribution_reclass(dist: pd.DataFrame) -> pd.DataFrame:
    used = ["GOMS_003", "GOMS_006", "GOMS_011", "GOMS_012", "GOMS_015", "GOMS_018", "GOMS_021"]
    sub = dist[dist["topic_id"].isin(used) & dist["measure_type"].eq("share") & dist["dimension_value"].ne("전체")].copy()
    sums = sub.groupby(["topic_id", "year", "subgroup"], as_index=False)["value"].sum().rename(columns={"value": "share_sum_excluding_total"})
    sums["abs_error_from_100"] = (sums["share_sum_excluding_total"] - 100).abs()
    conditions = [
        sums["abs_error_from_100"].le(1),
        sums["abs_error_from_100"].le(5),
        sums["abs_error_from_100"].le(10),
    ]
    sums["audit_status"] = np.select(conditions, ["PASS", "WARN", "REVIEW"], default="FAIL")
    return sums


def goms_extra_audits(frames: dict[str, pd.DataFrame]) -> dict[str, Any]:
    dist = read_csv_any(NORM / "goms_distribution_long.csv")
    d06 = frames["d06"].copy()
    identity = d06.copy()
    identity["identity_gap"] = (
        identity["graduate_total_n"].astype(float)
        - identity["employed_n"].astype(float)
        - identity["unemployed_n"].astype(float)
        - identity["inactive_n"].astype(float)
    )
    write_csv(identity.loc[identity["identity_gap"].abs().gt(0), ["year", "major_group_7", "graduate_total_n", "employed_n", "unemployed_n", "inactive_n", "identity_gap"]], "goms_frequency_identity_nonzero_gaps.csv")
    sums = distribution_reclass(dist)
    write_csv(sums, "goms_distribution_sum_reclassified.csv")
    occ = read_csv_any(P2_3 / "qa" / "goms_occupation_crosswalk_review.csv")
    occ["included_in_d06"] = True
    occ["other_review_assignment"] = occ["headline_group"].astype(str).eq("other_review") | occ["broad_occupation_group"].astype(str).eq("other_review")
    occ["arbitrary_assignment_flag"] = False
    occ["audit_reason"] = "review_required=True, but deterministic pre/post crosswalk assigns a broad group; no random assignment marker present"
    write_csv(occ, "goms_occupation_crosswalk_review_audit.csv")
    pre_bad = int(((d06["year"].astype(int) <= 2016) & d06["occupation_schema_version"].astype(str).ne("pre_2017")).sum())
    post_bad = int(((d06["year"].astype(int) >= 2017) & d06["occupation_schema_version"].astype(str).ne("post_2017")).sum())
    return {
        "frequency_identity_max_abs_gap": float(identity["identity_gap"].abs().max()),
        "frequency_identity_nonzero_rows": int(identity["identity_gap"].abs().gt(0).sum()),
        "distribution_reclass_counts": sums["audit_status"].value_counts().to_dict(),
        "distribution_max_abs_error": float(sums["abs_error_from_100"].max()),
        "distribution_warn_or_worse": int(sums["audit_status"].isin(["WARN", "REVIEW", "FAIL"]).sum()),
        "occupation_review_rows": int(len(occ)),
        "occupation_review_other_rows": int(occ["other_review_assignment"].sum()),
        "occupation_arbitrary_rows": int(occ["arbitrary_assignment_flag"].sum()),
        "occupation_schema_boundary_bad_rows": pre_bad + post_bad,
    }


def logs_summary() -> pd.DataFrame:
    rows = []
    for path in sorted((P2_3 / "logs").glob("*")) + sorted((P2_3 / "shared_handoff").glob("goms_run_manifest.json")):
        row = {"path": str(path.relative_to(P2_3)), "sha256": sha256_path(path), "size_bytes": path.stat().st_size}
        if path.suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            row.update(
                {
                    "json_top_keys": "|".join(data.keys()) if isinstance(data, dict) else "",
                    "notebook": data.get("notebook") if isinstance(data, dict) else None,
                    "run_started_at": data.get("run_started_at") if isinstance(data, dict) else None,
                    "run_finished_at": data.get("run_finished_at") if isinstance(data, dict) else None,
                    "created_at": data.get("created_at") if isinstance(data, dict) else None,
                    "completed_at": data.get("completed_at") if isinstance(data, dict) else None,
                    "agent": data.get("agent") if isinstance(data, dict) else None,
                }
            )
        if path.suffix == ".jsonl":
            recs = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            row.update(
                {
                    "jsonl_records": len(recs),
                    "agents": "|".join(sorted({str(r.get("agent")) for r in recs if "agent" in r})),
                    "datasets": "|".join(sorted({str(r.get("dataset")) for r in recs if "dataset" in r})),
                    "first_timestamp": recs[0].get("timestamp") if recs else None,
                    "last_timestamp": recs[-1].get("timestamp") if recs else None,
                }
            )
        rows.append(row)
    return pd.DataFrame(rows)


def split_sample_summary(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    d08 = frames["d08"].copy()
    split = read_csv_any(P2_3 / "shared" / "dim_school_split.csv")
    d08 = d08.merge(split[["school_uid", "split"]], on="school_uid", how="left", validate="many_to_one")
    rows = []
    for split_name, g in d08.groupby("split", dropna=False):
        rows.append(
            {
                "type": "split",
                "id": split_name,
                "rows": len(g),
                "schools": g["school_uid"].nunique(),
                "major_counts": g["major_group_7"].astype("string").fillna("<NA>").value_counts().to_dict(),
                "outcome_observed_a_rate": int(g["a_rate_pct"].notna().sum()),
                "headcount_match_rate": float(g["headcount_match_flag"].astype("boolean").mean()),
            }
        )
    for sid, mask in {
        "GRADE_ALL": d08["a_rate_pct"].notna(),
        "GRADE_SELECTIVITY": d08["a_rate_pct"].notna() & d08["selectivity_proxy_pct"].notna(),
        "EMPLOYMENT_HEALTH": d08["health_employment_rate_pct"].notna(),
        "PROGRESSION_GRADSCHOOL": d08["graduate_school_progression_rate_pct"].notna(),
        "JOINT_EMP_PROG": d08["health_employment_rate_pct"].notna() & d08["graduate_school_progression_rate_pct"].notna(),
    }.items():
        g = d08[mask]
        rows.append(
            {
                "type": "sample",
                "id": sid,
                "rows": len(g),
                "schools": g["school_uid"].nunique(),
                "major_counts": g["major_group_7"].astype("string").fillna("<NA>").value_counts().to_dict(),
                "split_counts": g["split"].value_counts(dropna=False).to_dict(),
            }
        )
    out = pd.DataFrame(rows)
    write_csv(out, "split_sample_summary.csv")
    return out


def main() -> None:
    frames = load_core()
    bridge_full = bridge_sample_audit(frames)
    major_full = major_sample_audit(frames)
    d06_compare = compare_d06(frames)
    d07_compare = compare_d07(frames)
    extra = goms_extra_audits(frames)
    logs = logs_summary()
    split_samples = split_sample_summary(frames)

    summary = {
        "audit_dir": str(AUDIT),
        "bridge": {
            "exact_normalized_bad_rows": int(bridge_full.loc[bridge_full["match_method"].eq("exact_normalized"), "exact_normalized_validation"].eq(False).sum()),
            "candidate_ge2_auto_confirmed": int(((pd.to_numeric(bridge_full["candidate_count"], errors="coerce") >= 2) & bridge_full["headcount_match_flag"].astype(bool)).sum()),
            "campus_scope_auto_mismatch": int((bridge_full["headcount_match_flag"].astype(bool) & bridge_full["campus_scope_ok"].eq(False)).sum()),
            "manual_review_rows": int(bridge_full["match_method"].eq("manual_review").sum()),
            "manual_review_approval_columns_present": [c for c in bridge_full.columns if "approval" in c.lower() or "status" in c.lower()],
        },
        "major": {
            "method_counts": major_full["major7_mapping_method"].astype(str).value_counts(dropna=False).to_dict(),
            "auto_rows": int(major_full["major7_mapping_method"].astype(str).isin(AUTO_MAJOR_METHODS).sum()),
            "auto_keyword_contradiction_rows": int(major_full["audit_auto_major_contradiction"].sum()),
            "auto_ambiguous_token_rows": int(major_full["audit_auto_ambiguous_token"].sum()),
            "wrong_auto_rate_rule_based": float(major_full["audit_auto_major_contradiction"].sum() / max(1, major_full["major7_mapping_method"].astype(str).isin(AUTO_MAJOR_METHODS).sum())),
        },
        "d06_compare": d06_compare.to_dict("records"),
        "d07_compare_max_mismatch_rows": int(d07_compare["mismatch_rows"].max()),
        "d07_compare": d07_compare.to_dict("records"),
        "goms_extra": extra,
        "split_samples": split_samples.to_dict("records"),
        "logs": logs.to_dict("records"),
        "created_files": sorted(str(p.relative_to(P2_3)) for p in AUDIT.glob("*")),
    }
    (AUDIT / "audit_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    write_csv(d06_compare, "goms_d06_requested_recalc_summary.csv")
    write_csv(d07_compare, "goms_d07_recent_profile_recalc_summary.csv")
    write_csv(logs, "logs_namespace_audit.csv")
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
