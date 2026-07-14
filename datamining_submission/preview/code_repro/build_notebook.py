# -*- coding: utf-8 -*-
"""
notebook/P2_G1_kedi.ipynb 를 코드로 재생성하는 스크립트.

실행 순서: crawl_goms_subjects.py -> normalize_and_qa.py -> build_notebook.py 실행 후
    jupyter nbconvert --to notebook --execute --inplace ../notebook/P2_G1_kedi.ipynb
로 노트북을 실제 실행해야 셀 출력이 채워진다.
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

def md(src):
    cells.append(nbf.v4.new_markdown_cell(src))

def code(src):
    cells.append(nbf.v4.new_code_cell(src))

md("""\
# GOMS 주제별 통계 크롤링 — 전공계열별 노동시장 기준선 (P2_G1_kedi)

**목표**: 한국고용정보원 고용조사분석시스템(GOMS)의 [주제별 통계](https://analysis.keis.or.kr/gomsSubject.do?goIndex=3-1) 화면에서
경제활동상태(3) + 현재 일자리(18) + 근로소득(9) + 근로시간(9) = **39개 주제**의 공식 CSV(실제로는 `.xls` 확장자의 HTML 표)를
자동화 다운로드하고, 정규화된 long-format 데이터로 변환한다.

**중요 caveat (반드시 숙지)**
- GOMS는 **전년도 대졸자 약 1만8천 명의 표본조사**이며 2019년 졸업자 조사를 끝으로 **잠정 중단**된 자료다.
- 따라서 이 데이터는 **2024년 대학·학과 실적이 아니라, 과거(2007~2019) 전국 전공계열별 노동시장 구조 기준선(baseline proxy)** 으로만 사용해야 한다.
- 동일 전공계열의 모든 대학에 같은 GOMS 값이 반복 부여되므로, 대학별 실적의 독립적인 설명변수처럼 통계 해석(p-value 등)을 해서는 안 된다.
- 인용 시 "한국고용정보원 GOMS 분석시스템의 가중 표본분석 결과"로 출처를 명시한다 (사이트 자체가 공식 통계자료가 아님을 명시).

**산출물 위치**: `workbook/p2/p2_2/data/goms_subject_crawl/` (원본 CSV는 절대 수정하지 않고, 정제 결과는 `normalized/`에 별도 저장)
""")

md("""\
## Gate 0 — 사이트 구조 탐색 결과 요약

실제 브라우저 자동화(Playwright, headless Chromium)로 페이지를 열어 확인한 결과:

- 겉보기엔 R Shiny 스타일 CSS(`shiny-bound-input` 클래스, `shiny.min.js`)를 쓰지만, 실제 데이터 호출은 **`POST /gomsSubjectAct.do`** 단일 엔드포인트를 쓰는
  일반 jQuery 기반 트리메뉴 앱이다. (Shiny 웹소켓은 404로 죽어있음 — 순수 장식용 CSS 잔재로 추정)
- 39개 주제는 좌측 트리메뉴에서 그룹 `data-tt-id`: `2`(경제활동 상태, 3개) · `3`(현재 일자리, 18개) · `4`(근로소득, 9개) · `5`(근로시간, 9개)에 분포한다.
- "CSV 다운로드" 버튼(`#cvsDownBtn`)은 실제로는 **HTML 표를 `.xls` 확장자로 감싼 파일**을 내려준다 (진짜 CSV/XLS 바이너리가 아님). 파싱은 `pandas.read_html`로 처리한다.
  단, 원본 마크업에 `colspan=&quot;1&quot;` 처럼 속성값이 이중 이스케이프되어 있어 `&quot;` → `"` 치환 전처리가 필요하다.

### 자동화 중 실제로 발견/수정한 버그 (재현 가능, 근거: 소스코드 + 해시 비교)

1. **다운로드가 재사용되는 팝업 창에서 발생함**: `#cvsDownBtn` 클릭은 새 팝업(`/excel.do`)을 열거나 기존 팝업을 재사용하는데,
   처음에는 메인 페이지에서 `download` 이벤트가 잡히지만 두 번째부터는 그 팝업에서만 발생한다.
   → 메인 페이지 + 알려진 모든 팝업에 대해 동시에 `download` 이벤트를 기다리는 방식으로 해결.
2. **표준편차/분산이 항상 평균으로 되돌아가는 사이트 자체 버그**: 페이지 내장 스크립트의 `callbackGOMSSubject()` 함수가
   연속형(그룹 4·5) 주제에서 `$("#viewType2 option").eq(0).prop("selected", true);` 를 **조건 없이** 실행한다
   (카테고리형은 `if (old_tg != tg)` 가드가 있지만 연속형엔 없음). 즉 "표준편차"를 선택해도 검색 버튼을 누르는 순간 항상 "평균"으로
   리셋되어, **정상적인 UI 흐름으로는 표준편차/분산을 절대 받을 수 없다.** → 실제 다운로드 파일 57개 중 34개가 서로 해시 중복이었던
   근본 원인. 이번 산출물에서는 **표준편차를 제외**하고 이 사실을 QA 요약에 기록했다.
3. **초기 페이지 로드시 기본 주제(`goIndex=3-1`, 취업자의 성별 산업 분포) 응답이 늦게 도착해 이후 선택한 주제를 덮어쓰는 경쟁 상태**:
   빠르게 반복 실행할 때 헤더 구조(연속형은 1행, 범주형은 3행)로 검증하지 않으면 다른 주제의 데이터가 섞여 들어간다.
   → 클릭 직후 항상 `#tresult thead tr` 개수를 확인해 연속형이 1행으로 안정될 때까지 대기·재시도하도록 수정.
4. **연속형 주제는 `#weighted` 체크박스 자체가 숨겨져 있음** (`$(".weighted").hide()`), `force=True`로도 클릭 불가 —
   연속형 통계는 애초에 가중치 옵션이 없고 항상 모집단 가중 평균으로 계산되는 것으로 확인되어 해당 단계를 제거했다.
""")

code("""\
import asyncio
import hashlib
import re
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
from playwright.async_api import async_playwright

BASE_URL = "https://analysis.keis.or.kr/gomsSubject.do?goIndex=3-1"
ROOT = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = ROOT / "raw_downloads"
SNAPSHOT_DIR = ROOT / "page_snapshots"
LOG_DIR = ROOT / "logs"
NORM_DIR = ROOT / "normalized"
QA_DIR = ROOT / "qa"

for d in [RAW_DIR / "frequency_share", RAW_DIR / "mean", SNAPSHOT_DIR / "html",
          SNAPSHOT_DIR / "screenshots", LOG_DIR, NORM_DIR, QA_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def safe_slug(text):
    text = re.sub(r"[()~]", "", text)
    text = re.sub(r"\\s+", "_", text.strip())
    return text
""")

code("""\
# 39개 주제 레지스트리 — 그룹 2(경제활동 상태) + 3(현재 일자리) + 4(근로소득) + 5(근로시간)
TOPICS = [
    {"group": "2", "group_name": "경제활동 상태", "topic": "성별 경제활동 상태", "kind": "categorical"},
    {"group": "2", "group_name": "경제활동 상태", "topic": "학교유형별 경제활동 상태", "kind": "categorical"},
    {"group": "2", "group_name": "경제활동 상태", "topic": "전공계열별 경제활동 상태", "kind": "categorical"},

    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 성별 산업 분포", "kind": "categorical"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 학교유형별 산업 분포", "kind": "categorical"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 전공별 산업 분포", "kind": "categorical"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 성별 직업 분포(~2016)", "kind": "categorical", "classification_version": "pre_2017"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 성별 직업 분포(2017~)", "kind": "categorical", "classification_version": "post_2017"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 학교유형별 직업 분포(~2016)", "kind": "categorical", "classification_version": "pre_2017"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 학교유형별 직업 분포(2017~)", "kind": "categorical", "classification_version": "post_2017"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 전공별 직업 분포(~2016)", "kind": "categorical", "classification_version": "pre_2017"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 전공별 직업 분포(2017~)", "kind": "categorical", "classification_version": "post_2017"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 성별 사업체 규모", "kind": "categorical"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 학교유형별 사업체 규모", "kind": "categorical"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 전공별 사업체 규모", "kind": "categorical"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 성별 사업체 유형", "kind": "categorical"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 학교유형별 사업체 유형", "kind": "categorical"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 전공별 사업체 유형", "kind": "categorical"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 성별 종사상 지위", "kind": "categorical"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 학교유형별 종사상 지위", "kind": "categorical"},
    {"group": "3", "group_name": "현재 일자리", "topic": "취업자의 전공별 종사상 지위", "kind": "categorical"},

    {"group": "4", "group_name": "근로소득", "topic": "성별 월평균 근로소득", "kind": "continuous"},
    {"group": "4", "group_name": "근로소득", "topic": "학교유형별 월평균 근로소득", "kind": "continuous"},
    {"group": "4", "group_name": "근로소득", "topic": "전공계열별 월평균 근로소득", "kind": "continuous"},
    {"group": "4", "group_name": "근로소득", "topic": "산업별 월평균 근로소득", "kind": "continuous"},
    {"group": "4", "group_name": "근로소득", "topic": "직업별 월평균 근로소득(~2016)", "kind": "continuous", "classification_version": "pre_2017"},
    {"group": "4", "group_name": "근로소득", "topic": "직업별 월평균 근로소득(2017~)", "kind": "continuous", "classification_version": "post_2017"},
    {"group": "4", "group_name": "근로소득", "topic": "사업체 규모별 월평균 근로소득", "kind": "continuous"},
    {"group": "4", "group_name": "근로소득", "topic": "사업체 유형별 월평균 근로소득", "kind": "continuous"},
    {"group": "4", "group_name": "근로소득", "topic": "종사상지위별 월평균 근로소득", "kind": "continuous"},

    {"group": "5", "group_name": "근로시간", "topic": "성별 주당 평균 근로시간", "kind": "continuous"},
    {"group": "5", "group_name": "근로시간", "topic": "학교유형별 주당 평균 근로시간", "kind": "continuous"},
    {"group": "5", "group_name": "근로시간", "topic": "전공계열별 주당 평균 근로시간", "kind": "continuous"},
    {"group": "5", "group_name": "근로시간", "topic": "산업별 주당 평균 근로시간", "kind": "continuous"},
    {"group": "5", "group_name": "근로시간", "topic": "직업별 주당 평균 근로시간(~2016)", "kind": "continuous", "classification_version": "pre_2017"},
    {"group": "5", "group_name": "근로시간", "topic": "직업별 주당 평균 근로시간(2017~)", "kind": "continuous", "classification_version": "post_2017"},
    {"group": "5", "group_name": "근로시간", "topic": "사업체 규모별 주당 평균 근로시간", "kind": "continuous"},
    {"group": "5", "group_name": "근로시간", "topic": "사업체 유형별 주당 평균 근로시간", "kind": "continuous"},
    {"group": "5", "group_name": "근로시간", "topic": "종사상지위별 주당 평균 근로시간", "kind": "continuous"},
]
for i, t in enumerate(TOPICS, start=1):
    t["topic_id"] = f"GOMS_{i:03d}"
    t.setdefault("classification_version", "all")

assert len(TOPICS) == 39
topic_registry_df = pd.DataFrame(TOPICS)
topic_registry_df.to_csv(ROOT / "00_topic_registry.csv", index=False, encoding="utf-8-sig")
topic_registry_df.groupby("group_name").size()
""")

md("""\
## 크롤러 핵심 함수

아래 함수들은 실제로 이번 세션에서 사이트를 상대로 검증·수정을 거친 최종 버전이다.
""")

code("""\
async def ensure_group_expanded(page, group_id):
    row = page.locator(f'tr[data-tt-id=\"{group_id}\"]')
    cls = await row.get_attribute("class")
    if cls and "collapsed" in cls:
        await row.locator(".indenter a").click()
        await page.wait_for_timeout(400)

async def click_topic(page, group_id, topic_text):
    await ensure_group_expanded(page, group_id)
    link = page.locator(f'tr[data-tt-parent-id=\"{group_id}\"] a', has_text=topic_text)
    await link.first.wait_for(state="visible", timeout=8000)
    await link.first.click()
    await page.wait_for_timeout(1200)

async def set_full_year_range(page):
    syear_opts = await page.locator("#syear option").evaluate_all("els => els.map(e => e.value)")
    eyear_opts = await page.locator("#eyear option").evaluate_all("els => els.map(e => e.value)")
    start, end = min(syear_opts), max(eyear_opts)
    await page.locator("#syear").select_option(start)
    await page.locator("#eyear").select_option(end)
    return start, end

async def download_csv(page, known_popups, out_path, timeout_ms=15000):
    \"\"\"메인 페이지 + 이미 알려진 모든 팝업에서 동시에 download 이벤트를 기다린다 (팝업 재사용 버그 대응).\"\"\"
    tasks = [asyncio.ensure_future(page.wait_for_event("download", timeout=timeout_ms))]
    for p in known_popups:
        if not p.is_closed():
            tasks.append(asyncio.ensure_future(p.wait_for_event("download", timeout=timeout_ms)))
    await page.locator("#cvsDownBtn").click()
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED, timeout=timeout_ms/1000 + 1)
    download = None
    for d in done:
        try:
            download = d.result()
            break
        except Exception:
            continue
    for p in pending:
        p.cancel()
    if download is None:
        raise TimeoutError("no download event from page or known popups")
    await download.save_as(str(out_path))
    return download.suggested_filename

async def wait_for_single_row_header(page, timeout_s=8):
    \"\"\"연속형 주제는 thead가 1행이어야 정상 (다중 행이면 초기 기본 주제가 덮어쓴 상태).\"\"\"
    for _ in range(timeout_s * 2):
        n = await page.evaluate("() => document.querySelectorAll('#tresult thead tr').length")
        if n == 1:
            return True
        await page.wait_for_timeout(500)
    return False
""")

md("""\
## 라이브 데모 — 대표 2개 주제로 크롤러 동작 검증

전체 39개 주제(57회 다운로드 시도, 버그 수정 재시도 포함) 크롤링은 실제로 15\\~25분이 걸리고 외부 정부 서버에 반복 요청을 보내므로,
이 노트북을 열 때마다 재실행하지 않는다. 아래 셀은 위 함수들이 **지금도 실제로 동작함**을 대표 주제 2개(범주형 1 + 연속형 1)로
라이브 검증한다.
""")

code("""\
async def demo_fetch(group_id, topic_text, kind):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(locale="ko-KR", accept_downloads=True)
        known_popups = []
        context.on("page", lambda p: known_popups.append(p))
        page = await context.new_page()
        await page.goto(BASE_URL, wait_until="networkidle", timeout=45000)
        await page.wait_for_timeout(1500)

        await click_topic(page, group_id, topic_text)
        if kind == "categorical":
            weighted = page.locator("#weighted")
            if not await weighted.is_checked():
                await weighted.check(force=True)
            await page.locator("#viewType1").select_option(label="빈도+비중")
        start, end = await set_full_year_range(page)
        await page.locator("#searchBtn").click()
        await page.wait_for_timeout(1800)
        if kind == "continuous":
            await wait_for_single_row_header(page, timeout_s=8)

        out_path = Path("/tmp") / f"demo_{safe_slug(topic_text)}.xls"
        suggested = await download_csv(page, known_popups, out_path, timeout_ms=15000)
        data = out_path.read_bytes()
        await browser.close()
        return {
            "topic": topic_text, "kind": kind, "year_range": (start, end),
            "file_size": len(data), "sha256": sha256_bytes(data)[:16],
            "suggested_filename": suggested,
        }

demo_results = []
demo_results.append(await demo_fetch("2", "전공계열별 경제활동 상태", "categorical"))
demo_results.append(await demo_fetch("4", "전공계열별 월평균 근로소득", "continuous"))
pd.DataFrame(demo_results)
""")

md("""\
라이브 데모 다운로드 두 건이 서로 다른 `sha256`과 정상적인 `file_size`를 갖는다면, 팝업 다운로드 추적과 연속형 헤더 검증 로직이
현재도 정상 동작함을 의미한다.
""")

md("""\
## 전체 39개 주제(최종 유효 CSV) 크롤링 결과 불러오기

전체 크롤링은 이번 세션에서 백그라운드로 3차에 걸쳐 실행되었다 (자세한 실패/재시도 이력은 `logs/02b~02d_*.csv` 참고):

1. **1차 전체 실행 (57개 시도: 범주형 21 + 연속형 mean 18 + stddev 18)**: 팝업 다운로드 버그를 고친 뒤 실행 → 범주형 21개는 전부 정상,
   연속형 18개는 위 버그 3·4번(경쟁 상태, 숨겨진 weighted 체크박스)으로 인해 다수 오염 (해시 비교로 34/36건 중복 확인).
2. **2~3차 연속형 재수집**: 헤더 구조 검증 + weighted 단계 제거 + 응답 대기 타임아웃 확대로 18개 전부 재수집, 최종 해시 중복 0건 확인.
3. **표준편차는 사이트 자체 버그로 정상 취득이 불가능함을 소스코드 레벨에서 확인**하여 최종 산출물에서 제외했다 (아래 QA 요약 참고).

최종적으로 `02_download_manifest.csv`는 **39/39 성공, 파일 해시 중복 0건**의 검증된 상태다.
""")

code("""\
manifest = pd.read_csv(ROOT / "02_download_manifest.csv")
print(f"총 {len(manifest)}개 주제, kind별:")
print(manifest["kind"].value_counts())
print(f"\\n상태별:")
print(manifest["status"].value_counts())
print(f"\\n중복 sha256 여부:", manifest.groupby("sha256").filter(lambda g: len(g) > 1).empty == False and "있음" or "없음")
manifest.head(10)
""")

md("## 정규화 (Wide HTML 표 → Long format)")

code("""\
def load_table(path):
    raw = path.read_text(encoding="utf-8-sig")
    fixed = raw.replace("&quot;", '"')
    return pd.read_html(StringIO(fixed))[0]

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
                "topic_id": topic_meta["topic_id"], "topic_group": topic_meta["group_name"],
                "topic_name": topic_meta["topic"], "classification_version": topic_meta["classification_version"],
                "dimension_value": dim_val, "year": int(year), "subgroup": subgroup,
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
""")

code("""\
reg = pd.read_csv(ROOT / "00_topic_registry.csv").set_index("topic_id")

audit_rows, cat_frames, cont_frames, parse_issues = [], [], [], []

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
            "n_null_values": long_df["value"].isna().sum(), "parse_status": "ok",
        })
    except Exception as exc:
        parse_issues.append({"topic_id": row["topic_id"], "topic_name": row["topic_name"],
                              "error_type": type(exc).__name__, "error_message": str(exc)[:300]})
        audit_rows.append({"topic_id": row["topic_id"], "topic_name": row["topic_name"],
                            "kind": row["kind"], "parse_status": "failed"})

pd.DataFrame(audit_rows).to_csv(ROOT / "03_schema_audit.csv", index=False, encoding="utf-8-sig")
pd.DataFrame(parse_issues).to_csv(ROOT / "04_parse_issues.csv", index=False, encoding="utf-8-sig")

cat_long = pd.concat(cat_frames, ignore_index=True)
cont_long = pd.concat(cont_frames, ignore_index=True)
cat_long.to_csv(NORM_DIR / "goms_distribution_long.csv", index=False, encoding="utf-8-sig")
cat_long.to_parquet(NORM_DIR / "goms_distribution_long.parquet", index=False)
cont_long.to_csv(NORM_DIR / "goms_continuous_long.csv", index=False, encoding="utf-8-sig")
cont_long.to_parquet(NORM_DIR / "goms_continuous_long.parquet", index=False)

print("파싱 실패:", len(parse_issues))
print("categorical long rows:", len(cat_long), " / continuous long rows:", len(cont_long))
cat_long.head()
""")

code("""\
cont_long.head()
""")

md("## QA 검증")

code("""\
share = cat_long[cat_long["measure_type"] == "share"]
share_no_total = share[share["dimension_value"] != "전체"]
sums = (share_no_total.groupby(["topic_id", "topic_name", "year", "subgroup"])["value"]
        .sum().reset_index(name="share_sum"))
sums["qa_status"] = np.where(sums["share_sum"].between(90.0, 101.5), "PASS", "REVIEW")
sums.to_csv(QA_DIR / "proportion_sum_check.csv", index=False, encoding="utf-8-sig")

year_cov = manifest.merge(
    pd.concat([
        cat_long.groupby("topic_id")["year"].agg(["min", "max", "nunique"]),
        cont_long.groupby("topic_id")["year"].agg(["min", "max", "nunique"]),
    ]).reset_index(),
    on="topic_id", how="left"
)[["topic_id", "topic_name", "min", "max", "nunique"]]
year_cov.columns = ["topic_id", "topic_name", "year_min", "year_max", "n_years"]
year_cov["qa_status"] = np.where(year_cov["n_years"] >= 1, "PASS", "REVIEW")
year_cov.to_csv(QA_DIR / "year_coverage_check.csv", index=False, encoding="utf-8-sig")

cat_dup = cat_long.duplicated(subset=["topic_id", "dimension_value", "year", "subgroup", "measure_type"]).sum()
cont_dup = cont_long.duplicated(subset=["topic_id", "dimension_value", "year"]).sum()
pd.DataFrame([
    {"dataset": "categorical", "duplicate_rows": int(cat_dup)},
    {"dataset": "continuous", "duplicate_rows": int(cont_dup)},
]).to_csv(QA_DIR / "duplicate_check.csv", index=False, encoding="utf-8-sig")

cross_dup = manifest.groupby("sha256").filter(lambda g: len(g) > 1)

final_summary = pd.DataFrame([{
    "total_topics": len(manifest),
    "categorical_topics": (manifest["kind"] == "categorical").sum(),
    "continuous_topics": (manifest["kind"] == "continuous").sum(),
    "parse_failures": len(parse_issues),
    "proportion_review_count": (sums["qa_status"] == "REVIEW").sum(),
    "year_coverage_review_count": (year_cov["qa_status"] == "REVIEW").sum(),
    "duplicate_rows_categorical": int(cat_dup),
    "duplicate_rows_continuous": int(cont_dup),
    "cross_file_hash_duplicates": "PASS" if cross_dup.empty else "REVIEW",
    "stddev_available": False,
    "stddev_reason": "site JS bug (callbackGOMSSubject unconditionally resets viewType2 to index 0 on every render) makes 분산/표준편차 unreachable via official UI/CSV flow",
}])
final_summary.to_csv(QA_DIR / "final_qa_summary.csv", index=False, encoding="utf-8-sig")
final_summary.T
""")

md("""\
## 요약

- **39/39 주제 CSV 수집 성공**, 정규화 후 파싱 실패 0건, 비중 합계(90\\~101.5% 허용) 전량 PASS, 중복 행 0건, 파일 해시 중복 0건.
- **표준편차/분산은 사이트 자체의 JS 버그로 취득 불가**함을 소스코드 레벨에서 확인하여 이번 산출물에서 제외했다 (평균만 제공).
- 이 데이터는 **2007~2019년 GOMS 표본조사 기준**이며, **2024년 대학·학과 실적이 아니라 과거 전국 전공계열별 노동시장 구조의 기준선**으로만
  2024년 프로젝트에 통제변수/맥락자료로 결합해야 한다 (동일 전공계열의 모든 대학에 동일 값이 반복 부여되므로 독립 설명변수로 오용 금지).
- 산출물: `00_topic_registry.csv`, `02_download_manifest.csv`, `03_schema_audit.csv`, `04_parse_issues.csv`,
  `raw_downloads/{frequency_share,mean}/`, `normalized/goms_distribution_long.{csv,parquet}`,
  `normalized/goms_continuous_long.{csv,parquet}`, `qa/*.csv`, `logs/*` (요청/응답 로그 및 디버깅 이력).
""")

nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": "Python (sbs_datascience_webcrawl .venv D3D12)", "language": "python", "name": "sbs_datascience_webcrawl"},
    "language_info": {"name": "python", "version": "3.12"},
}

out_path = Path(__file__).resolve().parent.parent / "notebook" / "P2_G1_kedi.ipynb"
with open(out_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print("wrote", out_path, "cells:", len(cells))
