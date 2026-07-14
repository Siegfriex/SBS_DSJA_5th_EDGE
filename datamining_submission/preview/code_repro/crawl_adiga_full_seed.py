"""ADIGA 크롤링 확장 Gate0~Gate4: 227개 전체 대학 대상 ADIGA 코드 탐색 seed 생성.

기존 51개 대학(workbook/p2/p2_2/data/crawl_2024_admission)은 그대로 보존하고,
raw_rows==0인 미수집 대학만 대상으로 ADIGA 검색을 수행해 신규 seed를 만든다.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import pandas as pd
from curl_cffi import requests as creq

PROJECT_DIR = Path("/home/sieg/projects-wsl/SBS_dataScience")
BASE_DIR = PROJECT_DIR / "workbook/p2/p2_2"
OLD_CRAWL_DIR = BASE_DIR / "data/crawl_2024_admission"
FULL_DIR = BASE_DIR / "data/crawl_2024_admission_full"
FULL_DIR.mkdir(parents=True, exist_ok=True)

FINAL_CSV_PATH = BASE_DIR / "final/data/P2_G1_concat.csv"
COVERAGE_V2_PATH = BASE_DIR / "final/admission/P2_admission_coverage_by_university_v2.csv"
OLD_SEED_PATH = OLD_CRAWL_DIR / "00_crawl_seed_university_2024.csv"

sys.path.insert(0, str(PROJECT_DIR / "scripts"))
from build_p2_admission_v2 import compact_key, normalize_text  # noqa: E402

REQUEST_DELAY_SEC = 0.4
SEARCH_SYR = 2025


# ---------------------------------------------------------------------------
# Gate0 — target universe + coverage diff
# ---------------------------------------------------------------------------
def gate0_target_coverage() -> pd.DataFrame:
    final = pd.read_csv(FINAL_CSV_PATH, low_memory=False)
    targets = pd.DataFrame({"학교명": sorted(final["학교명"].unique())})

    coverage = pd.read_csv(COVERAGE_V2_PATH, low_memory=False)
    out = targets.merge(
        coverage[["학교명", "raw_rows", "raw_metric_nonnull", "final_admission_department_labels"]],
        on="학교명", how="left",
    )
    out[["raw_rows", "raw_metric_nonnull", "final_admission_department_labels"]] = out[
        ["raw_rows", "raw_metric_nonnull", "final_admission_department_labels"]
    ].fillna(0).astype(int)
    out["already_crawled_flag"] = out["raw_rows"] > 0
    out["needs_adiga_search"] = ~out["already_crawled_flag"]

    out_path = FULL_DIR / "00_full_target_university_coverage.csv"
    out.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"[Gate0] target universities={len(out)}  already_crawled={out['already_crawled_flag'].sum()}  "
          f"needs_search={out['needs_adiga_search'].sum()}  -> {out_path}")
    return out


# ---------------------------------------------------------------------------
# Gate1 — 대학명 정규화 + 검색 seed
# ---------------------------------------------------------------------------
CLOSED_PATTERN = re.compile(r"폐교")
BRANCH_SUFFIX_PATTERN = re.compile(r"_(분교|제\d+캠퍼스)$")
PAREN_PATTERN = re.compile(r"\(([^)]*)\)")


def split_university_name(name: str) -> tuple[str, str | None, list[str], bool]:
    """학교명 -> (search_query 본체, branch_suffix, paren campus tokens, is_closed)."""
    text = str(name)
    is_closed = bool(CLOSED_PATTERN.search(text))
    text_wo_closed = text.replace("(폐교)", "")

    paren_tokens = [normalize_text(p) for p in PAREN_PATTERN.findall(text_wo_closed) if normalize_text(p)]
    base = PAREN_PATTERN.sub("", text_wo_closed)

    branch_suffix = None
    m = BRANCH_SUFFIX_PATTERN.search(base)
    if m:
        branch_suffix = m.group(1)
        base = base[: m.start()]

    base = normalize_text(base)
    return base, branch_suffix, paren_tokens, is_closed


def gate1_search_seed(coverage: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in coverage[coverage["needs_adiga_search"]].iterrows():
        name = r["학교명"]
        base, branch_suffix, paren_tokens, is_closed = split_university_name(name)
        rows.append({
            "학교명": name,
            "university_key": compact_key(base),
            "search_query": base,
            "branch_suffix": branch_suffix or "",
            "paren_tokens": "|".join(paren_tokens),
            "already_crawled_flag": False,
            "existing_univ_id": "",
            "existing_adiga_code": "",
            "needs_adiga_search": not is_closed,
            "manual_review_required": is_closed,
            "manual_review_reason": "institution_closed_no_source" if is_closed else "",
        })
    seed = pd.DataFrame(rows)
    out_path = FULL_DIR / "00_adiga_search_seed_2024_full.csv"
    seed.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"[Gate1] search seed rows={len(seed)}  closed_excluded={seed['manual_review_required'].sum()}  -> {out_path}")
    return seed


# ---------------------------------------------------------------------------
# Gate2 — ADIGA univAjax.do 검색
# ---------------------------------------------------------------------------
def adiga_search_univ(session, csrf: str, query: str, syr: int = SEARCH_SYR) -> list[tuple[str, str]]:
    from bs4 import BeautifulSoup
    data = {
        "_csrf": csrf, "pagination.currentPage": 1, "pagination.cntPerPage": 30,
        "searchSyr": syr, "unvSeCd": 10, "sortOrder": "true", "favoriteYn": "N",
        "searchTitleInput": query, "searchTitle": query,
    }
    resp = session.post("https://www.adiga.kr/ucp/uvt/uni/univAjax.do", data=data)
    soup = BeautifulSoup(resp.text, "lxml")
    return [(a.get("code"), a.get_text(strip=True)) for a in soup.select("a.selectUniv")]


def gate2_search_candidates(seed: pd.DataFrame) -> pd.DataFrame:
    from bs4 import BeautifulSoup
    session = creq.Session(impersonate="safari")
    home = session.get("https://www.adiga.kr/ucp/uvt/uni/univDetailSelection.do?menuId=PCUVTINF2000")
    csrf = BeautifulSoup(home.text, "lxml").find("input", {"name": "_csrf"})["value"]

    to_search = seed[seed["needs_adiga_search"]]
    cache: dict[str, list[tuple[str, str]]] = {}
    rows = []
    for _, r in to_search.iterrows():
        query = r["search_query"]
        if query not in cache:
            cache[query] = adiga_search_univ(session, csrf, query)
            time.sleep(REQUEST_DELAY_SEC)
        matches = cache[query]
        for rank, (code, label) in enumerate(matches, start=1):
            rows.append({
                "학교명": r["학교명"],
                "search_query": query,
                "candidate_code": code,
                "candidate_label": label,
                "candidate_rank": rank,
            })
        if not matches:
            rows.append({
                "학교명": r["학교명"], "search_query": query,
                "candidate_code": None, "candidate_label": None, "candidate_rank": 0,
            })

    candidates = pd.DataFrame(rows)
    out_path = FULL_DIR / "00_adiga_search_candidates_2024_full.csv"
    candidates.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"[Gate2] search_query unique={len(cache)}  candidate rows={len(candidates)}  -> {out_path}")
    return candidates


# ---------------------------------------------------------------------------
# Gate3 — 자동확정 / 수동검토 분류
# ---------------------------------------------------------------------------
def label_tokens(label: str) -> tuple[str, str | None, list[str]]:
    """ADIGA 후보 label -> (base, bracket token(본교/분교/제N캠퍼스), paren tokens)."""
    text = normalize_text(label)
    bracket = re.search(r"\[([^\]]*)\]", text)
    bracket_token = bracket.group(1) if bracket else None
    text_wo_bracket = re.sub(r"\[[^\]]*\]", "", text)
    paren_tokens = [normalize_text(p) for p in PAREN_PATTERN.findall(text_wo_bracket) if normalize_text(p)]
    base = normalize_text(PAREN_PATTERN.sub("", text_wo_bracket))
    return base, bracket_token, paren_tokens


def gate3_classify(seed: pd.DataFrame, candidates: pd.DataFrame, existing_codes: set[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    seed_by_name = seed.set_index("학교명")
    decisions = []
    for name, group in candidates.groupby("학교명"):
        srow = seed_by_name.loc[name]
        target_base_key = compact_key(srow["search_query"])
        raw_branch = srow["branch_suffix"]
        target_branch = raw_branch if isinstance(raw_branch, str) and raw_branch else None
        raw_parens = srow["paren_tokens"]
        target_paren = [t for t in (raw_parens.split("|") if isinstance(raw_parens, str) and raw_parens else []) if t]

        valid = group[group["candidate_code"].notna()]
        decision = "manual_review"
        note = ""
        chosen_code = None
        chosen_label = None

        if len(valid) == 1:
            code, label = valid.iloc[0]["candidate_code"], valid.iloc[0]["candidate_label"]
            base, _bracket, _parens = label_tokens(label)
            if compact_key(base) == target_base_key:
                decision, chosen_code, chosen_label = "auto_confirm", code, label
                note = "단일 후보 + 대학명 본체 일치"
            else:
                note = f"단일 후보이나 대학명 불일치: {label}"
        elif len(valid) > 1:
            if target_branch or target_paren:
                # ADIGA label에 정보가 없는 축(bracket/paren)은 "모순 없음"으로 간주하고,
                # 정보가 있는 축끼리 명확히 어긋날 때만(conflict) 후보를 제외한다.
                target_paren_keys = {compact_key(tp) for tp in target_paren}
                kept = []
                for _, c in valid.iterrows():
                    base, bracket_token, parens = label_tokens(c["candidate_label"])
                    if compact_key(base) != target_base_key:
                        continue
                    branch_conflict = bool(target_branch and bracket_token and bracket_token != target_branch)
                    paren_conflict = bool(
                        target_paren and parens and not ({compact_key(p) for p in parens} & target_paren_keys)
                    )
                    if branch_conflict or paren_conflict:
                        continue
                    matched_branch = bool(target_branch and bracket_token == target_branch)
                    matched_paren = bool(target_paren and any(compact_key(p) in target_paren_keys for p in parens))
                    kept.append((c, matched_branch or matched_paren))
                confirmed_hits = [c for c, matched in kept if matched]
                if len(confirmed_hits) == 1:
                    decision = "auto_confirm"
                    chosen_code = confirmed_hits[0]["candidate_code"]
                    chosen_label = confirmed_hits[0]["candidate_label"]
                    note = "캠퍼스 신호(분교/제N캠퍼스/괄호) 명확히 일치"
                elif len(kept) == 1:
                    decision = "auto_confirm"
                    chosen_code = kept[0][0]["candidate_code"]
                    chosen_label = kept[0][0]["candidate_label"]
                    note = "캠퍼스 신호와 모순 없는 후보 유일 (약한 확정)"
                else:
                    note = f"캠퍼스 신호로도 후보 {len(kept)}건(확정신호 {len(confirmed_hits)}건) — 불확실"
            else:
                note = f"후보 {len(valid)}건 — 캠퍼스 신호 없음"
        else:
            note = "검색 결과 없음"

        if chosen_code is not None and chosen_code in existing_codes:
            note += " | 기존 51개와 동일 code — raw_html 재사용"

        decisions.append({
            "학교명": name,
            "search_query": srow["search_query"],
            "candidate_count": len(valid),
            "decision": decision,
            "decision_note": note,
            "chosen_adiga_code": chosen_code,
            "chosen_adiga_label": chosen_label,
            "manual_review_required": decision != "auto_confirm",
        })

    dec_df = pd.DataFrame(decisions)

    closed_rows = seed[~seed["needs_adiga_search"]][["학교명"]].copy()
    closed_rows["search_query"] = ""
    closed_rows["candidate_count"] = 0
    closed_rows["decision"] = "excluded_closed_institution"
    closed_rows["decision_note"] = "폐교 — ADIGA 결과 없음, 검색 스킵"
    closed_rows["chosen_adiga_code"] = None
    closed_rows["chosen_adiga_label"] = None
    closed_rows["manual_review_required"] = True

    dec_df = pd.concat([dec_df, closed_rows], ignore_index=True)

    manual = dec_df[dec_df["manual_review_required"]].copy()
    manual_path = FULL_DIR / "00_adiga_manual_review_required_2024_full.csv"
    manual.to_csv(manual_path, index=False, encoding="utf-8-sig")

    dup_codes = dec_df.loc[dec_df["decision"].eq("auto_confirm"), "chosen_adiga_code"]
    dup_mask = dup_codes.duplicated(keep=False)
    if dup_mask.any():
        dup_names = dec_df.loc[dup_codes[dup_mask].index, "학교명"].tolist()
        print(f"[Gate3][주의] 동일 code가 여러 학교명에 매핑됨 — 수동검토 전환 대상: {dup_names}")
        dec_df.loc[dup_codes[dup_mask].index, "decision"] = "manual_review"
        dec_df.loc[dup_codes[dup_mask].index, "manual_review_required"] = True
        dec_df.loc[dup_codes[dup_mask].index, "decision_note"] += " | 동일 code 중복 매핑으로 수동검토 전환"
        manual = dec_df[dec_df["manual_review_required"]].copy()
        manual.to_csv(manual_path, index=False, encoding="utf-8-sig")

    print(f"[Gate3] auto_confirm={sum(dec_df['decision']=='auto_confirm')}  "
          f"manual_review={sum(dec_df['manual_review_required'])}  -> {manual_path}")
    return dec_df, manual


# ---------------------------------------------------------------------------
# Gate4 — 확정 seed (기존 스키마 호환)
# ---------------------------------------------------------------------------
def gate4_final_seed(decisions: pd.DataFrame) -> pd.DataFrame:
    confirmed = decisions[decisions["decision"] == "auto_confirm"].copy()
    rows = []
    for _, r in confirmed.iterrows():
        code = r["chosen_adiga_code"]
        rows.append({
            "univ_id": f"U{code}",
            "univ_name_raw": r["학교명"],
            "univ_name_std": r["학교명"],  # 분교 매칭 위해 P2_G1_concat.csv 원문 그대로 사용
            "campus_id": code,
            "campus_name_std": r["chosen_adiga_label"],
            "adiga_univ_code": code,
            "adiga_label": r["chosen_adiga_label"],
            "target_institution_flag": True,
            "branch_status": "auto_resolved",
            "crawl_priority": 9999,
            "manual_review_required": False,
            "seed_note": r["decision_note"],
        })
    final_seed = pd.DataFrame(rows)

    dup_mask = final_seed["adiga_univ_code"].duplicated(keep="first")
    final_seed.loc[dup_mask, "target_institution_flag"] = False
    final_seed.loc[dup_mask, "seed_note"] = "중복 code — 이전 행과 동일 페이지, 크롤링 대상에서 제외"

    out_path = FULL_DIR / "00_crawl_seed_university_2024_full.csv"
    final_seed.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"[Gate4] final seed rows={len(final_seed)}  target_institution={final_seed['target_institution_flag'].sum()}  -> {out_path}")
    return final_seed


def main() -> None:
    # adiga_univ_code는 7자리 zero-padded 코드(예: "0000019")이므로 dtype=str을 강제해야
    # pandas가 숫자로 오인해 앞자리 0을 지우는 것을 막을 수 있다.
    old_seed = pd.read_csv(OLD_SEED_PATH, low_memory=False, dtype={"adiga_univ_code": str})
    existing_codes = set(old_seed["adiga_univ_code"].dropna().astype(str))

    coverage = gate0_target_coverage()
    seed = gate1_search_seed(coverage)
    candidates = gate2_search_candidates(seed)
    decisions, manual = gate3_classify(seed, candidates, existing_codes)
    gate4_final_seed(decisions)


if __name__ == "__main__":
    main()
