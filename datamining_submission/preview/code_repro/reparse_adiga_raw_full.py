"""Task #10: adiga_crawl_lib.py 파서 수정 반영 — 캐시된 raw_html을 전부 재파싱한다.

새로 fetch하지 않고(ADIGA에 재요청 없음), 이미 저장된 HTML만 다시 파싱해
02_admission_result_raw_2024_merged.csv/.parquet와 01_crawl_source_registry_merged.csv의
parse_status/parse_note를 갱신한다. 51개 골든셋 회귀 여부는 별도로 검증한다.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path("/home/sieg/projects-wsl/SBS_dataScience")
sys.path.insert(0, str(PROJECT_DIR / "scripts"))
from adiga_crawl_lib import parse_detail_html  # noqa: E402

BASE_DIR = PROJECT_DIR / "workbook/p2/p2_2"
FULL_DIR = BASE_DIR / "data/crawl_2024_admission_full"
REGISTRY_PATH = FULL_DIR / "01_crawl_source_registry_merged.csv"
RAW_CSV_PATH = FULL_DIR / "02_admission_result_raw_2024_merged.csv"
RAW_PARQUET_PATH = FULL_DIR / "02_admission_result_raw_2024_merged.parquet"


def main() -> None:
    registry = pd.read_csv(REGISTRY_PATH, dtype={"univ_id": str}, low_memory=False)

    all_rows: list[dict] = []
    parse_status = []
    parse_note = []
    missing = 0
    for _, r in registry.iterrows():
        raw_file_path = r.get("raw_file_path")
        html_path = BASE_DIR / raw_file_path if isinstance(raw_file_path, str) and raw_file_path else None
        if not html_path or not html_path.exists():
            missing += 1
            parse_status.append("failed")
            parse_note.append("raw_html_missing_at_reparse")
            continue
        html = html_path.read_text(encoding="utf-8")
        rows, n_tables, note = parse_detail_html(html, r["source_id"], r["univ_id"], 2024)
        all_rows.extend(rows)
        parse_status.append("success" if n_tables else "partial")
        parse_note.append(note)

    registry["parse_status"] = parse_status
    registry["parse_note"] = parse_note
    registry["parser_version"] = "adiga_v2_task10"
    registry.to_csv(REGISTRY_PATH, index=False, encoding="utf-8-sig")

    raw_df = pd.DataFrame(all_rows)
    raw_df.to_csv(RAW_CSV_PATH, index=False, encoding="utf-8-sig")
    raw_df.to_parquet(RAW_PARQUET_PATH, index=False)

    print(f"registry rows={len(registry)}  missing_html={missing}")
    print(f"parse_status={registry['parse_status'].value_counts().to_dict()}")
    print(f"raw rows total={len(raw_df)}")
    print(f"-> {RAW_CSV_PATH}")
    print(f"-> {REGISTRY_PATH}")


if __name__ == "__main__":
    main()
