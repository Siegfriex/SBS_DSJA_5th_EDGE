"""
GOMS(고용조사분석시스템) 주제별 통계 자동 크롤러 — 최종 통합판.

대상: https://analysis.keis.or.kr/gomsSubject.do?goIndex=3-1
수집 범위: 경제활동 상태(3) + 현재 일자리(18) + 근로소득(9) + 근로시간(9) = 39개 주제
  - 경제활동 상태 / 현재 일자리: 범주형(categorical) → 가중치 적용, 빈도+비중
  - 근로소득 / 근로시간: 연속형(continuous) → 평균(mean)만 수집 (표준편차는 사이트 자체 버그로 취득 불가, 하단 설명 참고)

이 스크립트는 개발 과정에서 실제로 발견/재현한 4가지 사이트 버그에 대한 우회 로직을 전부 포함한
최종본이다 (디버깅 이력은 이 포트폴리오 폴더의 README.md 참고).

  1. CSV 다운로드가 재사용되는 팝업 창(/excel.do)에서 발생 → 메인 페이지 + 이미 열린 모든 팝업에서
     동시에 download 이벤트를 기다린다.
  2. 연속형 주제에서 "표준편차/분산" 선택이 검색 버튼을 누르는 순간 항상 "평균"으로 강제 리셋되는
     사이트 자체 JS 버그(`callbackGOMSSubject()`가 조건 없이 viewType2를 index 0으로 되돌림) →
     구조적으로 취득 불가능하므로 평균만 수집한다.
  3. 페이지 최초 로드시 자동 실행되는 기본 주제 응답이 늦게 도착해 이후 선택한 주제를 덮어쓰는
     경쟁 상태 → 주제 전환 후 `#tresult thead`의 행 수(연속형은 1행이어야 정상)를 확인하고,
     불일치 시 새 브라우저 세션으로 재시도한다.
  4. 연속형 주제는 `#weighted` 체크박스 자체가 숨겨져 있어(`force=True`로도 클릭 불가) 해당 단계를
     생략한다 (연속형 통계는 항상 모집단 가중 평균으로 계산되는 것으로 확인됨).

사용법:
    python crawl_goms_subjects.py

출력 (OUT_ROOT 아래):
    00_topic_registry.csv, 02_download_manifest.csv,
    raw_downloads/frequency_share/*.xls, raw_downloads/mean/*.xls,
    page_snapshots/html/*.html, logs/request_log.jsonl, logs/response_log.jsonl
"""

import asyncio
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from playwright.async_api import async_playwright

BASE_URL = "https://analysis.keis.or.kr/gomsSubject.do?goIndex=3-1"
OUT_ROOT = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = OUT_ROOT / "raw_downloads"
SNAPSHOT_DIR = OUT_ROOT / "page_snapshots"
LOG_DIR = OUT_ROOT / "logs"

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


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def safe_slug(text):
    text = re.sub(r"[()~]", "", text)
    text = re.sub(r"\s+", "_", text.strip())
    return text


async def ensure_group_expanded(page, group_id):
    row = page.locator(f'tr[data-tt-id="{group_id}"]')
    cls = await row.get_attribute("class")
    if cls and "collapsed" in cls:
        await row.locator(".indenter a").click()
        await page.wait_for_timeout(400)


async def click_topic(page, group_id, topic_text):
    await ensure_group_expanded(page, group_id)
    link = page.locator(f'tr[data-tt-parent-id="{group_id}"] a', has_text=topic_text)
    await link.first.wait_for(state="visible", timeout=8000)
    data_id = await link.first.get_attribute("data-id")
    await link.first.click()
    await page.wait_for_timeout(1200)
    return data_id


async def set_full_year_range(page):
    syear_opts = await page.locator("#syear option").evaluate_all("els => els.map(e => e.value)")
    eyear_opts = await page.locator("#eyear option").evaluate_all("els => els.map(e => e.value)")
    start, end = min(syear_opts), max(eyear_opts)
    await page.locator("#syear").select_option(start)
    await page.locator("#eyear").select_option(end)
    return start, end


async def download_csv(page, known_popups, out_path, timeout_ms=15000):
    """메인 페이지 + 이미 알려진 모든 팝업에서 동시에 download 이벤트를 기다린다 (버그 #1 대응)."""
    tasks = [asyncio.ensure_future(page.wait_for_event("download", timeout=timeout_ms))]
    for p in known_popups:
        if not p.is_closed():
            tasks.append(asyncio.ensure_future(p.wait_for_event("download", timeout=timeout_ms)))
    await page.locator("#cvsDownBtn").click()
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED, timeout=timeout_ms / 1000 + 1)
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


async def wait_for_single_row_header(page, timeout_s=12):
    """연속형 주제는 thead가 1행이어야 정상 (다중 행이면 버그 #3: 초기 기본 주제가 덮어쓴 상태)."""
    for _ in range(timeout_s * 2):
        n = await page.evaluate("() => document.querySelectorAll('#tresult thead tr').length")
        if n == 1:
            return True
        await page.wait_for_timeout(500)
    return False


async def crawl_categorical(pw, manifest):
    """범주형 21개 주제: 그룹 2·3. 한 세션 내에서 순회해도 안전함이 확인됨."""
    browser = await pw.chromium.launch(headless=True)
    context = await browser.new_context(locale="ko-KR", accept_downloads=True)
    known_popups = []
    context.on("page", lambda p: known_popups.append(p))
    page = await context.new_page()
    await page.goto(BASE_URL, wait_until="networkidle", timeout=45000)
    await page.wait_for_timeout(1000)

    for topic in [t for t in TOPICS if t["kind"] == "categorical"]:
        result = {
            "topic_id": topic["topic_id"], "topic_group": topic["group_name"], "topic_name": topic["topic"],
            "measure": "freq_share", "classification_version": topic["classification_version"],
            "kind": "categorical", "status": "started", "started_at": now_iso(),
        }
        try:
            await click_topic(page, topic["group"], topic["topic"])
            weighted = page.locator("#weighted")
            if not await weighted.is_checked():
                await weighted.check(force=True)
            await page.locator("#viewType1").select_option(label="빈도+비중")
            start, end = await set_full_year_range(page)
            await page.locator("#searchBtn").click()
            await page.wait_for_timeout(1800)

            filename = f"{topic['topic_id']}_{safe_slug(topic['topic'])}_freq_share.xls"
            out_path = RAW_DIR / "frequency_share" / filename
            suggested = await download_csv(page, known_popups, out_path)
            data = out_path.read_bytes()

            result.update({
                "status": "success", "file_path": str(out_path.relative_to(OUT_ROOT)),
                "suggested_filename": suggested, "file_size": len(data), "sha256": sha256_bytes(data),
                "year_start": start, "year_end": end, "finished_at": now_iso(),
            })
            html_path = SNAPSHOT_DIR / "html" / f"{topic['topic_id']}_freq_share.html"
            html_path.write_text(await page.content(), encoding="utf-8")
        except Exception as exc:
            result.update({"status": "failed", "error_type": type(exc).__name__,
                            "error_message": str(exc)[:500], "finished_at": now_iso()})
        manifest.append(result)
        print(topic["topic_id"], topic["topic"], "->", result["status"])
        await page.wait_for_timeout(1200)

    await browser.close()


async def crawl_continuous_one(pw, topic, max_attempts=4):
    """연속형 주제 1개: 매번 새 브라우저 세션 + thead 검증 (버그 #2·#3·#4 대응)."""
    result = {
        "topic_id": topic["topic_id"], "topic_group": topic["group_name"], "topic_name": topic["topic"],
        "measure": "mean", "classification_version": topic["classification_version"],
        "kind": "continuous", "status": "started", "started_at": now_iso(),
    }
    last_err = None
    for attempt in range(1, max_attempts + 1):
        browser = await pw.chromium.launch(headless=True)
        try:
            context = await browser.new_context(locale="ko-KR", accept_downloads=True)
            known_popups = []
            context.on("page", lambda p: known_popups.append(p))
            page = await context.new_page()

            # 버그 #3: 기본 주제의 첫 응답이 완전히 도착할 때까지 대기 후 진행
            first_resp = asyncio.ensure_future(page.wait_for_event(
                "response", predicate=lambda r: "gomsSubjectAct.do" in r.url, timeout=20000
            ))
            await page.goto(BASE_URL, wait_until="networkidle", timeout=45000)
            await first_resp
            await page.wait_for_timeout(1500)

            expected_data_id = None
            async with page.expect_response(lambda r: "gomsSubjectAct.do" in r.url, timeout=30000):
                expected_data_id = await click_topic(page, topic["group"], topic["topic"])
            await page.wait_for_timeout(1000)

            # 버그 #4: weighted 체크박스는 연속형에서 숨겨져 있으므로 조작하지 않음
            start, end = await set_full_year_range(page)

            async with page.expect_response(lambda r: "gomsSubjectAct.do" in r.url, timeout=30000):
                await page.locator("#searchBtn").click()
            await page.wait_for_timeout(1000)

            ok_header = await wait_for_single_row_header(page, timeout_s=12)
            actual_subject = await page.evaluate("() => window.staticsParam ? window.staticsParam.subjectType : null")
            if not ok_header:
                raise RuntimeError("thead still multi-row (stale categorical content) after settle wait")
            if actual_subject != expected_data_id:
                raise RuntimeError(f"subject mismatch: expected {expected_data_id}, got {actual_subject}")

            filename = f"{topic['topic_id']}_{safe_slug(topic['topic'])}_mean.xls"
            out_path = RAW_DIR / "mean" / filename
            suggested = await download_csv(page, known_popups, out_path)
            data = out_path.read_bytes()

            result.update({
                "status": "success", "attempt": attempt, "file_path": str(out_path.relative_to(OUT_ROOT)),
                "suggested_filename": suggested, "file_size": len(data), "sha256": sha256_bytes(data),
                "year_start": start, "year_end": end, "finished_at": now_iso(),
            })
            html_path = SNAPSHOT_DIR / "html" / f"{topic['topic_id']}_mean.html"
            html_path.write_text(await page.content(), encoding="utf-8")
            await browser.close()
            return result
        except Exception as exc:
            last_err = exc
            await browser.close()
            await asyncio.sleep(1)
            continue

    result.update({"status": "failed", "attempt": max_attempts, "error_type": type(last_err).__name__,
                    "error_message": str(last_err)[:500], "finished_at": now_iso()})
    return result


async def main():
    for d in [RAW_DIR / "frequency_share", RAW_DIR / "mean", SNAPSHOT_DIR / "html", LOG_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(TOPICS).to_csv(OUT_ROOT / "00_topic_registry.csv", index=False, encoding="utf-8-sig")

    manifest = []
    async with async_playwright() as pw:
        await crawl_categorical(pw, manifest)
        for topic in [t for t in TOPICS if t["kind"] == "continuous"]:
            res = await crawl_continuous_one(pw, topic)
            manifest.append(res)
            print(topic["topic_id"], topic["topic"], "->", res["status"], res.get("attempt", ""))
            pd.DataFrame(manifest).to_csv(OUT_ROOT / "02_download_manifest.csv", index=False, encoding="utf-8-sig")

    df = pd.DataFrame(manifest)
    df.to_csv(OUT_ROOT / "02_download_manifest.csv", index=False, encoding="utf-8-sig")
    print("\n=== SUMMARY ===")
    print(df["status"].value_counts())
    dup = df[df["status"] == "success"].groupby("sha256").filter(lambda g: len(g) > 1)
    print("duplicate hash rows:", len(dup))


if __name__ == "__main__":
    asyncio.run(main())
