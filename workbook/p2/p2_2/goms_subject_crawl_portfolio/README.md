# GOMS 주제별 통계 자동 크롤링 · 정규화 · QA — 포트폴리오 패키지

한국고용정보원 고용조사분석시스템(GOMS) [주제별 통계](https://analysis.keis.or.kr/gomsSubject.do?goIndex=3-1) 화면의
39개 주제를 Playwright 브라우저 자동화로 수집하고, 정규화(long-format) + QA 검증까지 수행한 전체 파이프라인이다.
크롤링·정규화 스크립트, 실행된 Jupyter 노트북, 원본/정제 데이터, 디버깅 로그를 이 폴더 하나에 자기완결적으로 담았다.

## 폴더 구조

```
goms_subject_crawl_portfolio/
├── README.md                          (이 문서)
├── scripts/
│   ├── crawl_goms_subjects.py         (39개 주제 전체 크롤러 — 발견한 4가지 사이트 버그 우회 로직 포함 최종본)
│   ├── normalize_and_qa.py            (원본 HTML표 → long-format 정규화 + QA 검증)
│   └── build_notebook.py              (notebook/P2_G1_kedi.ipynb를 코드로 재생성)
├── notebook/
│   └── P2_G1_kedi.ipynb               (실제 실행 완료된 노트북 — 에러 0건)
└── data/
    ├── 00_topic_registry.csv          (39개 주제 정의)
    ├── 02_download_manifest.csv       (39/39 성공, 파일 해시 중복 0건 — 최종 검증본)
    ├── 03_schema_audit.csv
    ├── 04_parse_issues.csv            (0건)
    ├── raw_downloads/
    │   ├── frequency_share/           (21개 .xls — 원본 그대로, 수정 없음)
    │   └── mean/                      (18개 .xls — 원본 그대로, 수정 없음)
    ├── page_snapshots/{html,screenshots}/  (감사용 스냅샷 57개씩)
    ├── normalized/
    │   ├── goms_distribution_long.{csv,parquet}   (29,160행)
    │   └── goms_continuous_long.{csv,parquet}     (2,230행)
    ├── logs/                          (요청/응답 로그 + 디버깅 3차 재시도 이력 원본)
    └── qa/                            (비중합계·연도커버리지·중복·최종요약 검증 결과)
```

## 재현 방법

```bash
cd scripts
python crawl_goms_subjects.py          # 1. 39개 주제 다운로드 (15~25분, 외부 정부 서버 호출)
python normalize_and_qa.py             # 2. long-format 정규화 + QA (수 초)
python build_notebook.py               # 3. 노트북 재생성 (선택)
jupyter nbconvert --to notebook --execute --inplace ../notebook/P2_G1_kedi.ipynb   # 4. 노트북 실행
```

필요 패키지: `playwright`(+ `python -m playwright install chromium`), `pandas`, `numpy`, `nbformat`, `nbconvert`.
이미 수집된 `data/`가 있으므로 재현 없이 바로 `normalize_and_qa.py`부터 실행하거나 `data/`를 그대로 열람해도 된다.

## 대상 및 범위

경제활동 상태(3) + 현재 일자리(18) + 근로소득(9) + 근로시간(9) = **39개 주제**
- 경제활동 상태 / 현재 일자리 → 범주형(categorical): 가중치 적용, 빈도+비중
- 근로소득 / 근로시간 → 연속형(continuous): 평균(mean)만 제공 — **표준편차는 사이트 자체 버그로 취득 불가** (아래 참고)

## 자동화 중 실제로 발견하고 고친 사이트 버그 4가지 (재현 가능)

| # | 증상 | 근본 원인 | 조치 |
|---|------|----------|------|
| 1 | 두 번째 CSV 다운로드부터 계속 타임아웃 | `#cvsDownBtn` 클릭이 새 팝업(`/excel.do`)을 열거나 **기존 팝업을 재사용**하는데, 메인 페이지에서만 `download` 이벤트를 기다리고 있었음 | 메인 페이지 + 이미 열린 모든 팝업에서 동시에 `download` 이벤트를 기다리도록 수정 |
| 2 | "표준편차" 선택 후 다운로드해도 항상 "평균"과 완전히 동일한 파일 | 페이지 내장 스크립트 `callbackGOMSSubject()`가 연속형(그룹 4·5) 주제 렌더링 시 `$("#viewType2 option").eq(0).prop("selected", true)`를 **조건 없이** 실행 (범주형은 `if(old_tg != tg)` 가드가 있으나 연속형엔 없음). UI에서 표준편차 선택 후 검색 버튼을 누르는 순간 항상 "평균"으로 강제 리셋됨 | 사이트 구조적 버그로 결론, **표준편차는 최종 산출물에서 제외**하고 사유를 QA 요약(`qa/final_qa_summary.csv`)에 기록 |
| 3 | 연속형 18개 주제 중 다수가 서로 다른 주제인데 완전히 동일한 파일 (해시 일치) | 페이지 최초 로드시 자동 실행되는 기본 주제(취업자의 성별 산업 분포) 응답이 **늦게 도착**해 이미 선택한 다른 주제의 렌더링을 뒤늦게 덮어씀 (경쟁 상태) | 다운로드 직전 `#tresult thead` 행 수(연속형은 1행이 정상) 검증, 불일치 시 새 브라우저 세션으로 재시도 |
| 4 | 연속형 주제에서 `#weighted` 체크박스를 강제 클릭(`force=True`)해도 실패 | 연속형 주제에서는 사이트가 이 체크박스를 `display:none`으로 숨김 — 연속형 통계는 항상 모집단 가중 평균으로 계산되며 가중치 옵션 자체가 없음 | 연속형 주제에서는 weighted 체크박스 조작 단계를 제거 |

디버깅 전 과정(1차 전체 실행 → 34/36건 오염 발견 → 2차 재수집 8건 실패 → weighted 단계 제거 → 3차 재수집 4건 응답지연 → 타임아웃 확대 후 전량 성공)은
`data/logs/02_download_manifest_initial57_with_bugs.csv`, `data/logs/02b~02d_continuous_refetch_attempt*.csv`에 그대로 남아있다.

## 최종 검증 결과 (`data/qa/final_qa_summary.csv`)

- 39/39 주제 CSV 수집 성공, 파일 해시 교차 중복 **0건**
- long-format 파싱 실패 **0건**
- 비중 합계 검증(90~101.5% 허용, 무응답/모름 결측 고려) 1,131건 전량 **PASS**
- 연도 커버리지 39/39 **PASS**, 중복 행 0건

## 알려진 한계 (반드시 확인)

1. **표준편차(18개)는 제공하지 않는다.** 사이트 자체의 JS 버그로 구조적으로 취득 불가능함을 소스코드 레벨에서 확인했다.
2. "CSV 다운로드" 버튼은 실제로는 **HTML 표를 `.xls` 확장자로 감싼 파일**을 내려준다 (사이트의 공식 동작). 파싱은
   `pandas.read_html` + 원본의 이중 이스케이프(`colspan=&quot;1&quot;`) 치환 전처리로 처리했다.
3. 스크린샷 57개 중 재수집된 13개 연속형 주제분은 3차 재수집 이전(구버전) 화면이라 최종 데이터와 내용이 다를 수 있다
   (데이터 자체엔 영향 없음, 감사용 보조자료의 한계).

## 데이터 사용 시 유의사항

GOMS는 **전년도 대졸자 약 1만8천 명의 표본조사**이며 2019년 졸업자 조사를 끝으로 잠정 중단되었다. 따라서 이 데이터는
**2024년(또는 그 이후) 대학·학과 실적이 아니라, 과거(2007~2019) 전국 전공계열별 노동시장 구조 기준선(baseline proxy)** 으로만
사용해야 한다. 동일 전공계열의 모든 대학에 동일 값이 반복 부여되므로 대학별 실적의 독립적인 설명변수처럼 통계 해석(p-value 등)을
해서는 안 된다. 인용 시 "한국고용정보원 GOMS 분석시스템의 가중 표본분석 결과"로 출처를 명시한다.
