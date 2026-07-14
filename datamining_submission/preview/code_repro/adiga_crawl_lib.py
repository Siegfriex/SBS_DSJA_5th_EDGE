"""ADIGA(어디가) 대학 검색 + 상세 페이지 파싱 공용 로직.

workbook/p2/p2_2/crawl.ipynb의 검증된 로직(76~88행, 161~371행)을 그대로 이식한 것으로,
알고리즘 자체는 변경하지 않는다.
"""

from __future__ import annotations

import json
import re
from typing import Any

from bs4 import BeautifulSoup

SEARCH_SYR = 2025
RESULT_YEAR = 2024


def get_csrf_token(session) -> str:
    home = session.get("https://www.adiga.kr/ucp/uvt/uni/univDetailSelection.do?menuId=PCUVTINF2000")
    return BeautifulSoup(home.text, "lxml").find("input", {"name": "_csrf"})["value"]


def adiga_search_univ(session, csrf: str, query: str, syr: int = SEARCH_SYR) -> list[tuple[str, str]]:
    data = {
        "_csrf": csrf, "pagination.currentPage": 1, "pagination.cntPerPage": 30,
        "searchSyr": syr, "unvSeCd": 10, "sortOrder": "true", "favoriteYn": "N",
        "searchTitleInput": query, "searchTitle": query,
    }
    resp = session.post("https://www.adiga.kr/ucp/uvt/uni/univAjax.do", data=data)
    soup = BeautifulSoup(resp.text, "lxml")
    return [(a.get("code"), a.get_text(strip=True)) for a in soup.select("a.selectUniv")]


def detail_url(code: str, syr: int = SEARCH_SYR) -> str:
    return (
        "https://www.adiga.kr/ucp/uvt/uni/univDetailSelection.do"
        f"?menuId=PCUVTINF2000&searchSyr={syr}&unvCd={code}"
    )


def flatten_header(header_trs) -> list[str]:
    grid: dict[tuple[int, int], str] = {}
    max_col = 0
    for r_i, tr in enumerate(header_trs):
        col = 0
        while (r_i, col) in grid:
            col += 1
        for cell in tr.find_all(["th", "td"]):
            while (r_i, col) in grid:
                col += 1
            label = cell.get_text(" ", strip=True)
            rs = int(cell.get("rowspan", 1) or 1)
            cs = int(cell.get("colspan", 1) or 1)
            for dr in range(rs):
                for dc in range(cs):
                    grid[(r_i + dr, col + dc)] = label
            col += cs
        max_col = max(max_col, col)
    n_rows = len(header_trs)
    columns = []
    for c in range(max_col):
        parts = []
        for r_i in range(n_rows):
            v = grid.get((r_i, c), "")
            if v and (not parts or parts[-1] != v):
                parts.append(v)
        columns.append(" / ".join(parts) if parts else f"col{c}")
    return columns


def map_semantic_fields(columns: list[str], cell_texts: list[str]) -> dict[str, Any]:
    """헤더 키워드 기반 best-effort 시맨틱 매핑. 실패해도 raw_cells_json은 그대로 보존."""
    out = {k: None for k in [
        "raw_admission_group", "raw_recruitment_unit", "raw_recruitment_n",
        "raw_competition_rate", "raw_additional_rank", "raw_score_70cut",
        "raw_score_max", "raw_percentile_70cut",
    ]}
    used_pct = used_cut = False
    for col_label, val in zip(columns, cell_texts):
        c = col_label.replace(" ", "")
        if "구분" in c and out["raw_admission_group"] is None and ("군" in val or val == ""):
            out["raw_admission_group"] = val
        elif "모집단위" in c:
            out["raw_recruitment_unit"] = val
        elif ("모집" in c and "인원" in c):
            out["raw_recruitment_n"] = val
        elif "경쟁률" in c:
            out["raw_competition_rate"] = val
        elif "충원" in c:
            out["raw_additional_rank"] = val
        elif "백분위" in c and not used_pct:
            out["raw_percentile_70cut"] = val
            used_pct = True
        elif "총점" in c:
            out["raw_score_max"] = val
        elif ("cut" in c.lower() or "환산" in c) and not used_cut:
            out["raw_score_70cut"] = val
            used_cut = True
    return out


def parse_detail_html(html: str, source_id: str, univ_id: str, result_year: int = RESULT_YEAR) -> tuple[list[dict], int, str]:
    """상세 HTML을 파싱해 (raw_rows, n_result_tables, parse_note)를 반환한다.

    crawl.ipynb의 Gate1 파싱 루프(278~371행)와 동일한 알고리즘.
    """
    soup = BeautifulSoup(html, "lxml")
    tab_containers = soup.select(".tabCon.univInfoCon")
    csat_container = tab_containers[3] if len(tab_containers) >= 4 else None
    if csat_container is None:
        return [], 0, f"Ⅳ탭 컨테이너 미검출 (tabCon 개수={len(tab_containers)})"

    tables = csat_container.find_all("table")
    raw_rows: list[dict] = []
    n_result_tables = 0
    for t_i, table in enumerate(tables):
        table_text = table.get_text(" ", strip=True)
        has_result_signature = (
            "모집단위" in table_text and "경쟁률" in table_text and "충원" in table_text
            and ("cut" in table_text.lower() or "백분위" in table_text)
        )
        if not has_result_signature:
            # 완화된 fallback: 일부 대학은 "모집단위" 대신 "전형명"(단일학과라 학과 구분이 없는
            # 교육대학교류), "경쟁률" 대신 "지원율", "충원" 표기 없이 "이월/후보순위"를 쓴다.
            # 다만 이 조합은 실제 결과표에만 나타나는 조합("70%컷/70%cut" + "백분위"가 동시에
            # 있고, 개별 항목을 나열하는 표 표시인 "모집단위"나 "전형명"도 있음)이라 설명/범례
            # 표를 잘못 집는 위험은 낮다.
            has_loose_signature = (
                ("모집단위" in table_text or "전형명" in table_text)
                and "백분위" in table_text
                and ("70%" in table_text or "70 %" in table_text)
            )
            if not has_loose_signature:
                continue

        rows = table.find_all("tr")
        if not rows:
            continue

        row0_cells = rows[0].find_all(["td", "th"])
        if len(row0_cells) == 1:
            selection_name = row0_cells[0].get_text(" ", strip=True)
            idx = 1
        else:
            selection_name = None
            idx = 0

        MAX_HEADER_ROWS = 3
        header_trs = []
        while idx < len(rows) and len(header_trs) < MAX_HEADER_ROWS:
            cells = rows[idx].find_all(["td", "th"])
            texts = [c.get_text(" ", strip=True) for c in cells]
            row_text = " ".join(texts)
            has_digit_heavy = bool(re.search(r"\d+(\.\d+)?\s*(:1|%|명)?$", texts[-1])) if texts else False
            looks_header = any(k in row_text for k in
                                ["모집단위", "구분", "모집 인원", "경쟁률", "충원", "cut", "백분위", "환산", "총점"])
            if not header_trs and looks_header:
                header_trs.append(rows[idx]); idx += 1
                continue
            if header_trs and not has_digit_heavy and looks_header:
                # 원래는 len(texts) <= 4로 제한했으나, 일부 대학은 2번째 헤더 행이
                # rowspan 없이 컬럼마다 한 셀씩(예: 8개) 채워져 있어 그 경우도 헤더로
                # 인식해야 한다. has_digit_heavy가 이미 실제 데이터 행(끝이 숫자/%/명으로
                # 끝나는 행)을 걸러내므로 길이 제한 없이도 데이터 행을 헤더로 오인할
                # 위험은 낮다.
                header_trs.append(rows[idx]); idx += 1
                continue
            break

        if not header_trs or idx >= len(rows):
            continue
        _flat_check = flatten_header(header_trs)
        if len(_flat_check) > 15:
            continue

        columns = flatten_header(header_trs)
        n_result_tables += 1
        prev_values: dict[int, str] = {}
        for r_i, tr in enumerate(rows[idx:]):
            cells = tr.find_all(["td", "th"])
            cell_texts = [c.get_text(" ", strip=True) for c in cells]
            if not any(cell_texts):
                continue

            deficit = len(columns) - len(cell_texts)
            parse_warning = ""
            if deficit > 0:
                carried = [prev_values.get(i, "") for i in range(deficit)]
                cell_texts = carried + cell_texts
                parse_warning = f"{deficit}개 선두 컬럼 rowspan 승계"
            elif deficit < 0:
                parse_warning = f"컬럼수 불일치 header={len(columns)} data={len(cell_texts)+(-deficit)}"
                cell_texts = cell_texts[: len(columns)]

            for i, v in enumerate(cell_texts):
                prev_values[i] = v

            semantic = map_semantic_fields(columns, cell_texts)
            raw_rows.append({
                "raw_row_id": f"{source_id}_T{t_i}_R{r_i}",
                "source_id": source_id,
                "univ_id": univ_id,
                "admission_year": result_year,
                "raw_table_index": t_i,
                "raw_row_index": r_i,
                "raw_section_title": selection_name,
                "raw_header_json": json.dumps(columns, ensure_ascii=False),
                "raw_cells_json": json.dumps(cell_texts, ensure_ascii=False),
                **semantic,
                "raw_parse_warning": parse_warning,
            })

    parse_note = f"result_tables={n_result_tables}"
    return raw_rows, n_result_tables, parse_note
