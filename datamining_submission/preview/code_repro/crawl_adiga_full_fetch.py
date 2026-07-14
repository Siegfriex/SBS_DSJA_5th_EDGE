"""ADIGA 크롤링 확장 Gate5~Gate6: 확정 seed HTML fetch + 결과표 파싱 + 기존 51개와 병합.

기존 data/crawl_2024_admission(51개)의 raw_html/registry/raw row는 그대로 두고,
새로 확정된 158개 seed 중 기존과 코드가 겹치지 않는 대학만 실제로 fetch한다.
코드가 겹치는 대학(분교/약칭 오매칭으로 이미 크롤됐던 케이스)은 재요청하지 않고,
merged seed에서 올바른 univ_name_std(P2_G1_concat.csv 원문 학교명)로 덮어써
기존 raw row가 올바른 학교명에 매칭되도록 고친다.
"""
from __future__ import annotations

import hashlib
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from curl_cffi import requests as creq

import sys
PROJECT_DIR = Path("/home/sieg/projects-wsl/SBS_dataScience")
sys.path.insert(0, str(PROJECT_DIR / "scripts"))
from adiga_crawl_lib import detail_url, parse_detail_html  # noqa: E402

BASE_DIR = PROJECT_DIR / "workbook/p2/p2_2"
OLD_CRAWL_DIR = BASE_DIR / "data/crawl_2024_admission"
FULL_DIR = BASE_DIR / "data/crawl_2024_admission_full"
RAW_HTML_DIR = FULL_DIR / "raw_html"
RAW_HTML_DIR.mkdir(parents=True, exist_ok=True)

FINAL_SEED_PATH = FULL_DIR / "00_crawl_seed_university_2024_full.csv"
OLD_SEED_PATH = OLD_CRAWL_DIR / "00_crawl_seed_university_2024.csv"
OLD_REGISTRY_PATH = OLD_CRAWL_DIR / "01_crawl_source_registry.csv"
OLD_RAW_PATH = OLD_CRAWL_DIR / "02_admission_result_raw_2024.csv"
OLD_RAW_HTML_DIR = OLD_CRAWL_DIR / "raw_html"

SEARCH_SYR = 2025
RESULT_YEAR = 2024
REQUEST_DELAY_SEC = 0.4

try:
    from zoneinfo import ZoneInfo
    KST = ZoneInfo("Asia/Seoul")
except Exception:
    KST = None


def now_kst() -> datetime:
    return datetime.now(KST) if KST else datetime.now()


def gate5_gate6_fetch_and_parse() -> tuple[pd.DataFrame, pd.DataFrame]:
    final_seed = pd.read_csv(FINAL_SEED_PATH, dtype={"adiga_univ_code": str, "univ_id": str})
    old_seed = pd.read_csv(OLD_SEED_PATH, dtype={"adiga_univ_code": str, "univ_id": str})
    existing_codes = set(old_seed["adiga_univ_code"].dropna())

    targets = final_seed[final_seed["target_institution_flag"]].reset_index(drop=True)
    to_fetch = targets[~targets["adiga_univ_code"].isin(existing_codes)].reset_index(drop=True)
    already_covered = targets[targets["adiga_univ_code"].isin(existing_codes)]

    print(f"[Gate5] 확정 대상={len(targets)}  신규 fetch 필요={len(to_fetch)}  "
          f"기존 51개와 code 중복(재요청 생략)={len(already_covered)}")

    session = creq.Session(impersonate="safari")
    registry_rows = []
    raw_rows_all: list[dict] = []
    _source_seq = 0

    for _, seed in to_fetch.iterrows():
        code = seed["adiga_univ_code"]
        univ_id = seed["univ_id"]
        html_path = RAW_HTML_DIR / f"{code}_{SEARCH_SYR}.html"
        url = detail_url(code, SEARCH_SYR)

        cached_old = OLD_RAW_HTML_DIR / f"{code}_{SEARCH_SYR}.html"
        if cached_old.exists():
            html = cached_old.read_text(encoding="utf-8")
            html_path.write_text(html, encoding="utf-8")
            http_status = 200
            fetched_fresh = False
        else:
            resp = session.get(url)
            http_status = resp.status_code
            html = resp.text if http_status == 200 else ""
            if html:
                html_path.write_text(html, encoding="utf-8")
            time.sleep(REQUEST_DELAY_SEC)
            fetched_fresh = True

        _source_seq += 1
        source_id = f"SRC_{code}_{SEARCH_SYR}_{_source_seq:04d}"
        reg_row = {
            "source_id": source_id,
            "crawl_run_id": f"RUN_{now_kst():%Y%m%d}_full",
            "univ_id": univ_id,
            "campus_id": seed["campus_id"],
            "source_type": "adiga_html",
            "source_priority": 1,
            "source_search_year": SEARCH_SYR,
            "source_result_year": RESULT_YEAR,
            "source_section": "Ⅳ. 수능위주전형 / Q2. 2024학년도 전형 결과",
            "source_url": url,
            "retrieved_at": now_kst().isoformat(),
            "http_status": http_status,
            "content_type": "text/html",
            "content_sha256": hashlib.sha256(html.encode("utf-8")).hexdigest() if html else "",
            "raw_file_path": str(html_path.relative_to(BASE_DIR)) if html else "",
            "parser_version": "adiga_v1",
            "parse_status": "pending",
            "parse_note": "",
            "fetched_fresh": fetched_fresh,
        }

        if not html:
            reg_row["parse_status"] = "failed"
            reg_row["parse_note"] = f"http_status={http_status}"
            registry_rows.append(reg_row)
            continue

        rows, n_tables, parse_note = parse_detail_html(html, source_id, univ_id, RESULT_YEAR)
        reg_row["parse_status"] = "success" if n_tables else "partial"
        reg_row["parse_note"] = parse_note
        registry_rows.append(reg_row)
        raw_rows_all.extend(rows)

    registry_df = pd.DataFrame(registry_rows)
    raw_df = pd.DataFrame(raw_rows_all)

    registry_path = FULL_DIR / "01_crawl_source_registry.csv"
    registry_df.to_csv(registry_path, index=False, encoding="utf-8-sig")
    raw_parquet_path = FULL_DIR / "02_admission_result_raw_2024.parquet"
    raw_csv_path = FULL_DIR / "02_admission_result_raw_2024.csv"
    raw_df.to_csv(raw_csv_path, index=False, encoding="utf-8-sig")
    raw_df.to_parquet(raw_parquet_path, index=False)

    if len(registry_df):
        print(f"[Gate6] sources fetched={len(registry_df)}  raw rows={len(raw_df)}")
        print(f"        success={sum(registry_df['parse_status']=='success')}  "
              f"partial={sum(registry_df['parse_status']=='partial')}  "
              f"failed={sum(registry_df['parse_status']=='failed')}")
        _failed = registry_df[registry_df["parse_status"] == "failed"]
        if len(_failed):
            print("[Gate6][주의] 파싱 실패:")
            print(_failed[["univ_id", "http_status", "parse_note"]].to_string(index=False))

    return registry_df, raw_df


def merge_with_old(new_registry: pd.DataFrame, new_raw: pd.DataFrame) -> None:
    final_seed = pd.read_csv(FINAL_SEED_PATH, dtype={"adiga_univ_code": str, "univ_id": str})
    old_seed = pd.read_csv(OLD_SEED_PATH, dtype={"adiga_univ_code": str, "univ_id": str})
    old_registry = pd.read_csv(OLD_REGISTRY_PATH, dtype={"univ_id": str})
    old_raw = pd.read_csv(OLD_RAW_PATH, low_memory=False, dtype={"univ_id": str})

    # 새 seed(158개, 올바른 univ_name_std=P2_G1_concat.csv 원문 학교명)를 먼저 두고
    # 기존 seed에서 겹치지 않는 univ_id만 뒤에 붙인다 — 겹치는 code(예: 한양대ERICA)는
    # 새 seed의 정확한 학교명이 우선 채택된다.
    merged_seed = pd.concat([final_seed, old_seed], ignore_index=True)
    merged_seed = merged_seed.drop_duplicates(subset=["univ_id"], keep="first")

    merged_registry = pd.concat([new_registry, old_registry], ignore_index=True)
    merged_raw = pd.concat([new_raw, old_raw], ignore_index=True)

    merged_seed_path = FULL_DIR / "00_crawl_seed_university_2024_merged.csv"
    merged_registry_path = FULL_DIR / "01_crawl_source_registry_merged.csv"
    merged_raw_csv_path = FULL_DIR / "02_admission_result_raw_2024_merged.csv"
    merged_raw_parquet_path = FULL_DIR / "02_admission_result_raw_2024_merged.parquet"

    merged_seed.to_csv(merged_seed_path, index=False, encoding="utf-8-sig")
    merged_registry.to_csv(merged_registry_path, index=False, encoding="utf-8-sig")
    merged_raw.to_csv(merged_raw_csv_path, index=False, encoding="utf-8-sig")
    merged_raw.to_parquet(merged_raw_parquet_path, index=False)

    print(f"[Merge] seed rows={len(merged_seed)} (unique univ_id)  "
          f"registry rows={len(merged_registry)}  raw rows={len(merged_raw)}")
    print(f"        -> {merged_seed_path}")
    print(f"        -> {merged_registry_path}")
    print(f"        -> {merged_raw_csv_path} / {merged_raw_parquet_path}")


def main() -> None:
    new_registry, new_raw = gate5_gate6_fetch_and_parse()
    merge_with_old(new_registry, new_raw)


if __name__ == "__main__":
    main()
