from __future__ import annotations

from pathlib import Path
import textwrap

import nbformat as nbf


PROJECT_ROOT = Path("/home/sieg/projects-wsl/SBS_dataScience")
NOTEBOOK_PATH = PROJECT_ROOT / "workbook/p2/p2_2/gate2_final_rule_confirmation.ipynb"


def md(source: str):
    return nbf.v4.new_markdown_cell(textwrap.dedent(source).strip())


def code(source: str):
    return nbf.v4.new_code_cell(textwrap.dedent(source).strip())


cells = [
    md(
        """
        # Gate 2-B. 정시 수능 반영규칙 최종 확정표

        기존 adiga HTML 캐시와 Gate 2 후보 큐를 사용해 대학별 대표 수능 반영규칙을 확정한다.

        확정의 의미:

        - raw HTML의 실제 표 `table_index`를 다시 열어 `수능 성적 산출방법` 계열 표를 대표 규칙으로 선택한다.
        - 학생부/수시/논술 중심 표는 대표 수능 규칙에서 제외한다.
        - 확정 컬럼은 `대표 규칙 표`, `활용지표`, `반영영역`, `비율 토큰`, `영어/한국사/가산점/감점 단서`, `신뢰도`, `검토 액션`으로 구성한다.
        - 대학별 세부 모집단위별 예외까지 완전 구조화한 것은 아니며, H1/H2 모델링 전 최종 수동검토용 표준 입력이다.

        모든 그림은 `NanumGothic`을 명시적으로 사용한다.
        """
    ),
    code(
        """
        from pathlib import Path
        import re
        import json
        from datetime import datetime

        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from matplotlib import font_manager
        from bs4 import BeautifulSoup

        try:
            from IPython.display import display, Markdown
        except Exception:
            display = print
            Markdown = lambda x: x

        PROJECT_ROOT = Path("/home/sieg/projects-wsl/SBS_dataScience")
        BASE_DIR = PROJECT_ROOT / "workbook/p2/p2_2/data/crawl_2024_admission"
        RAW_HTML_DIR = BASE_DIR / "raw_html"
        EDA_DIR = BASE_DIR / "eda_outputs"
        GATE2_DIR = BASE_DIR / "gate2_outputs"
        FINAL_DIR = BASE_DIR / "gate2_final_outputs"
        FIGURE_DIR = FINAL_DIR / "figures"
        FINAL_DIR.mkdir(parents=True, exist_ok=True)
        FIGURE_DIR.mkdir(parents=True, exist_ok=True)

        REGISTRY_PATH = BASE_DIR / "01_crawl_source_registry.csv"
        CANDIDATE_PATH = GATE2_DIR / "gate2_01_rule_table_candidates.csv"
        REVIEW_QUEUE_PATH = GATE2_DIR / "gate2_07_top_rule_candidates_for_review.csv"
        PRIORITY_PATH = GATE2_DIR / "gate2_03_university_rule_collection_priority.csv"
        SCORE_COVERAGE_PATH = EDA_DIR / "eda_13_university_score_coverage.csv"
        QUALITY_PATH = EDA_DIR / "eda_16_university_quality_dashboard.csv"

        RUN_STARTED_AT = datetime.now()
        AUDIT_LOG = []

        nanum = font_manager.findfont("NanumGothic", fallback_to_default=False)
        font_manager.fontManager.addfont(nanum)
        plt.rcParams.update(
            {
                "font.family": "NanumGothic",
                "axes.unicode_minus": False,
                "figure.dpi": 120,
                "savefig.dpi": 170,
                "axes.grid": True,
                "grid.alpha": 0.25,
                "axes.spines.top": False,
                "axes.spines.right": False,
                "font.size": 9,
            }
        )

        def now_iso() -> str:
            return datetime.now().isoformat(timespec="seconds")

        def audit(step, dataset, action, rows_before=None, rows_after=None, status="INFO", note=""):
            AUDIT_LOG.append(
                {
                    "step": step,
                    "dataset": dataset,
                    "action": action,
                    "rows_before": rows_before,
                    "rows_after": rows_after,
                    "status": status,
                    "note": note,
                    "executed_at": now_iso(),
                }
            )

        def save_csv(df: pd.DataFrame, path: Path):
            path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(path, index=False, encoding="utf-8-sig")
            audit("export", path.name, "save_csv", rows_before=len(df), rows_after=len(df), status="PASS", note=str(path))
            return path

        def save_fig(fig, name: str):
            path = FIGURE_DIR / name
            fig.savefig(path, bbox_inches="tight")
            plt.close(fig)
            audit("export", name, "save_png", status="PASS", note=str(path))
            return path

        def normalize_text(value) -> str:
            if pd.isna(value):
                return ""
            text = str(value).replace("\\xa0", " ")
            text = re.sub(r"\\s+", " ", text)
            return text.strip()

        def compact(text: str, limit: int = 900) -> str:
            text = normalize_text(text)
            return text[:limit] + ("..." if len(text) > limit else "")

        def resolve_raw_file_path(value) -> Path:
            text = normalize_text(value)
            p = Path(text)
            if p.is_absolute():
                return p
            for candidate in [PROJECT_ROOT / text, BASE_DIR / p.name, RAW_HTML_DIR / p.name]:
                if candidate.exists():
                    return candidate
            return PROJECT_ROOT / text

        display(pd.DataFrame([
            {"key": "NanumGothic font path", "value": nanum},
            {"key": "BASE_DIR", "value": str(BASE_DIR)},
            {"key": "FINAL_DIR", "value": str(FINAL_DIR)},
            {"key": "RUN_STARTED_AT", "value": RUN_STARTED_AT.isoformat(timespec="seconds")},
        ]))
        audit("setup", "font", "set_nanumgothic", status="PASS", note=nanum)
        """
    ),
    code(
        """
        registry = pd.read_csv(REGISTRY_PATH)
        candidates = pd.read_csv(CANDIDATE_PATH)
        review_queue = pd.read_csv(REVIEW_QUEUE_PATH)
        priority = pd.read_csv(PRIORITY_PATH)
        score_coverage = pd.read_csv(SCORE_COVERAGE_PATH)
        quality = pd.read_csv(QUALITY_PATH)

        registry["raw_html_abs_path"] = registry["raw_file_path"].map(lambda x: str(resolve_raw_file_path(x)))
        registry_lookup = registry.set_index("univ_id")

        display(pd.DataFrame([
            {"dataset": "registry", "shape": str(registry.shape)},
            {"dataset": "candidates", "shape": str(candidates.shape)},
            {"dataset": "review_queue", "shape": str(review_queue.shape)},
            {"dataset": "priority", "shape": str(priority.shape)},
        ]))
        audit("load", "gate2_inputs", "load_candidate_tables", rows_after=len(candidates), status="PASS")
        """
    ),
    code(
        """
        PERCENT_RE = re.compile(r"(?<!\\d)(\\d{1,3}(?:\\.\\d+)?)\\s*%")
        SCORE_TERMS = {
            "표준점수": r"표준점수",
            "백분위": r"백분위",
            "등급": r"등급",
            "변환표준점수": r"변환표준점수|변환 표준점수",
            "환산점수": r"환산점수|환산 점수",
        }
        SUBJECT_TERMS = {
            "국어": r"국어|화법과 작문|언어와 매체",
            "수학": r"수학|미적분|기하|확률과통계|확률과 통계",
            "영어": r"영어",
            "탐구": r"탐구|사회탐구|과학탐구|사탐|과탐",
            "한국사": r"한국사",
            "제2외국어/한문": r"제2외국어|한문",
        }

        def table_grid(table):
            rows = []
            for tr in table.find_all("tr"):
                cells = [normalize_text(cell.get_text(" ", strip=True)) for cell in tr.find_all(["th", "td"])]
                if any(cells):
                    rows.append(cells)
            return rows

        TABLE_TEXT_CACHE = {}

        def all_table_texts_for_univ(univ_id: str) -> list[str]:
            if univ_id in TABLE_TEXT_CACHE:
                return TABLE_TEXT_CACHE[univ_id]
            html_path = Path(registry_lookup.loc[univ_id, "raw_html_abs_path"])
            soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
            texts = []
            for table in soup.find_all("table"):
                rows = table_grid(table)
                texts.append(normalize_text(" | ".join(" / ".join(row) for row in rows)))
            TABLE_TEXT_CACHE[univ_id] = texts
            return texts

        def load_table_text(univ_id: str, table_index: int) -> str:
            texts = all_table_texts_for_univ(univ_id)
            if table_index < 0 or table_index >= len(texts):
                return ""
            return texts[table_index]

        def is_csat_method_text(text: str) -> bool:
            if not text:
                return False
            if "학생부 교과성적 산출방법" in text or "학생부종합" in text[:250]:
                return False
            direct = (
                "수능 성적 산출방법" in text
                or "대학수학능력시험 성적" in text
                or "수능 반영영역" in text
                or "수능 반영 영역" in text
                or ("상대 반영비율" in text and ("성적표" in text or "영역별 평가방법" in text))
            )
            subject_hits = sum(bool(re.search(pattern, text)) for pattern in SUBJECT_TERMS.values())
            ratio_like = bool(PERCENT_RE.search(text)) or "반영비율" in text or "반영 비율" in text
            return direct or (subject_hits >= 4 and ratio_like and "수능" in text)

        def score_metric_summary(text: str) -> str:
            hits = [label for label, pattern in SCORE_TERMS.items() if re.search(pattern, text)]
            return ", ".join(hits) if hits else "미확인"

        def subject_summary(text: str) -> str:
            hits = [label for label, pattern in SUBJECT_TERMS.items() if re.search(pattern, text)]
            return ", ".join(hits) if hits else "미확인"

        def rule_flags(text: str) -> dict:
            return {
                "csat_100_flag": bool(re.search(r"수능\\s*100\\s*%|수능100", text)),
                "practical_mixed_flag": bool(re.search(r"실기\\s*\\d{1,3}\\s*%|수능\\s*\\d{1,3}\\s*%\\s*\\+\\s*실기", text)),
                "english_conversion_flag": bool(re.search(r"영어.{0,40}(등급|환산|변환|감점|가산)", text)),
                "history_bonus_penalty_flag": bool(re.search(r"한국사.{0,50}(가산|감점|등급|필수)", text)),
                "additional_bonus_flag": bool(re.search(r"가산점|가산|감점", text)),
                "designated_subject_flag": bool(re.search(r"지정응시|지정 응시|필수 응시|응시영역|응시 영역", text)),
            }

        def first_sentence_containing(text: str, patterns: list[str], limit: int = 360) -> str:
            parts = re.split(r"(?<=다\\.)| \\| ", text)
            for part in parts:
                if any(re.search(pattern, part) for pattern in patterns):
                    return compact(part, limit)
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    start = max(0, match.start() - 120)
                    end = min(len(text), match.end() + limit)
                    return compact(text[start:end], limit)
            return ""

        candidate_pool = candidates.loc[
            ~candidates["result_table_like"].astype(bool)
            & candidates["candidate_type"].isin(["csat_reflection_ratio", "score_conversion", "english_korean_history", "selection_element"])
        ].copy()
        candidate_pool["full_table_text"] = [
            load_table_text(row.univ_id, int(row.table_index)) for row in candidate_pool.itertuples(index=False)
        ]
        candidate_pool["csat_method_flag"] = candidate_pool["full_table_text"].map(is_csat_method_text)
        candidate_pool["student_record_flag"] = candidate_pool["full_table_text"].str.contains("학생부 교과성적 산출방법|학생부종합", regex=True, na=False)
        candidate_pool["method_title_flag"] = candidate_pool["full_table_text"].str.contains("수능 성적 산출방법|대학수학능력시험 성적", regex=True, na=False)
        candidate_pool["score_metric_hit_n"] = candidate_pool["full_table_text"].map(
            lambda text: sum(bool(re.search(pattern, text)) for pattern in SCORE_TERMS.values())
        )
        candidate_pool["element_only_penalty"] = (
            candidate_pool["full_table_text"].str.contains("교과평가|교과 평가|전형요소", regex=True, na=False)
            & candidate_pool["score_metric_hit_n"].lt(2)
        )
        candidate_pool["final_selection_score"] = (
            candidate_pool["candidate_score"].fillna(0)
            + candidate_pool["csat_method_flag"].astype(int) * 80
            + candidate_pool["method_title_flag"].astype(int) * 30
            + candidate_pool["candidate_type"].eq("score_conversion").astype(int) * 5
            + candidate_pool["score_metric_hit_n"] * 8
            - candidate_pool["student_record_flag"].astype(int) * 100
            - candidate_pool["element_only_penalty"].astype(int) * 35
        )
        candidate_pool = candidate_pool.sort_values(
            ["univ_id", "final_selection_score", "candidate_score"],
            ascending=[True, False, False],
        )
        selected = candidate_pool.groupby("univ_id", as_index=False).head(1).copy()
        audit("select_rules", "candidate_pool", "select_representative_csat_rule_table", rows_before=len(candidate_pool), rows_after=len(selected), status="PASS")
        display(selected[["univ_id", "univ_name_std", "table_index", "candidate_type", "candidate_score", "final_selection_score", "csat_method_flag", "method_title_flag"]].head(20))
        """
    ),
    code(
        """
        final_rows = []
        for row in selected.itertuples(index=False):
            text = row.full_table_text
            percents = PERCENT_RE.findall(text)
            flags = rule_flags(text)
            confidence_score = 0
            confidence_score += 35 if row.csat_method_flag else 0
            confidence_score += 20 if row.method_title_flag else 0
            confidence_score += 15 if len(percents) >= 3 else 0
            confidence_score += 15 if subject_summary(text) != "미확인" else 0
            confidence_score += 10 if score_metric_summary(text) != "미확인" else 0
            confidence_score += 5 if flags["english_conversion_flag"] or flags["history_bonus_penalty_flag"] else 0
            confidence_score += 10 if "상대 반영비율" in text else 0
            confidence = "confirmed" if confidence_score >= 70 else ("high_review" if confidence_score >= 50 else "manual_required")
            final_rows.append(
                {
                    "univ_id": row.univ_id,
                    "univ_name_std": row.univ_name_std,
                    "representative_table_index": int(row.table_index),
                    "confirmation_status": confidence,
                    "confirmation_score": confidence_score,
                    "candidate_type": row.candidate_type,
                    "candidate_score": row.candidate_score,
                    "score_metric_summary": score_metric_summary(text),
                    "subject_area_summary": subject_summary(text),
                    "percent_token_n": len(percents),
                    "percent_tokens_top20": "; ".join(percents[:20]),
                    **flags,
                    "selection_method_excerpt": first_sentence_containing(text, [r"수능\\s*100", r"전형요소", r"일괄합산", r"실기"], 420),
                    "reflection_ratio_excerpt": first_sentence_containing(text, [r"반영비율", r"반영 비율", r"반영영역", r"수능영역"], 520),
                    "score_conversion_excerpt": first_sentence_containing(text, [r"활용지표", r"표준점수", r"백분위", r"변환표준점수", r"환산점수"], 520),
                    "english_history_excerpt": first_sentence_containing(text, [r"영어", r"한국사", r"등급", r"가산점", r"감점"], 520),
                    "final_rule_excerpt": compact(text, 1400),
                }
            )

        final_rules = pd.DataFrame(final_rows)
        final_rules = final_rules.merge(
            priority[["univ_id", "manual_priority_score", "gate2_action", "rule_cache_status"]],
            on="univ_id",
            how="left",
        ).merge(
            score_coverage[["univ_id", "percentile_70cut_available_rate", "univ_score_70cut_available_rate", "univ_score_ratio_available_rate"]],
            on="univ_id",
            how="left",
        ).merge(
            quality[["univ_id", "quality_status", "tier_a_row_n", "tier_b_row_n", "tier_c_row_n", "tier_d_row_n"]],
            on="univ_id",
            how="left",
        )
        final_rules["final_modeling_use"] = np.select(
            [
                final_rules["confirmation_status"].eq("confirmed") & final_rules["percentile_70cut_available_rate"].ge(0.8),
                final_rules["confirmation_status"].isin(["confirmed", "high_review"]) & final_rules["percentile_70cut_available_rate"].ge(0.5),
            ],
            ["primary_candidate", "secondary_candidate"],
            default="rule_confirmed_but_score_data_limited",
        )
        final_rules = final_rules.sort_values(["confirmation_status", "manual_priority_score", "univ_name_std"], ascending=[True, False, True])

        save_csv(final_rules, FINAL_DIR / "gate2_10_final_admission_rule_summary.csv")
        display(final_rules.head(20))
        """
    ),
    code(
        """
        # 구체적 쇼잉: 우선순위 상위 대학과 대표 규칙 발췌
        showcase_cols = [
            "univ_name_std",
            "confirmation_status",
            "score_metric_summary",
            "subject_area_summary",
            "percent_tokens_top20",
            "selection_method_excerpt",
            "reflection_ratio_excerpt",
            "score_conversion_excerpt",
            "english_history_excerpt",
            "final_modeling_use",
        ]
        concrete_showcase = final_rules.sort_values(["manual_priority_score", "univ_name_std"], ascending=[False, True]).head(12)[showcase_cols].copy()
        save_csv(concrete_showcase, FINAL_DIR / "gate2_11_concrete_rule_showcase_top12.csv")
        display(concrete_showcase)
        """
    ),
    code(
        """
        status_summary = (
            final_rules.groupby(["confirmation_status", "final_modeling_use"], dropna=False)
            .agg(
                university_n=("univ_id", "nunique"),
                mean_percentile_coverage=("percentile_70cut_available_rate", "mean"),
                mean_rule_score=("confirmation_score", "mean"),
            )
            .reset_index()
            .sort_values(["confirmation_status", "final_modeling_use"])
        )
        metric_summary = (
            final_rules.assign(score_metric_split=final_rules["score_metric_summary"].str.split(", "))
            .explode("score_metric_split")
            .groupby("score_metric_split", dropna=False)
            .agg(university_n=("univ_id", "nunique"))
            .reset_index()
            .sort_values("university_n", ascending=False)
        )
        subject_summary_df = (
            final_rules.assign(subject_split=final_rules["subject_area_summary"].str.split(", "))
            .explode("subject_split")
            .groupby("subject_split", dropna=False)
            .agg(university_n=("univ_id", "nunique"))
            .reset_index()
            .sort_values("university_n", ascending=False)
        )
        save_csv(status_summary, FINAL_DIR / "gate2_12_final_rule_status_summary.csv")
        save_csv(metric_summary, FINAL_DIR / "gate2_13_score_metric_summary.csv")
        save_csv(subject_summary_df, FINAL_DIR / "gate2_14_subject_area_summary.csv")

        fig, ax = plt.subplots(figsize=(8.2, 4.8), constrained_layout=True)
        counts = final_rules["confirmation_status"].value_counts().reindex(["confirmed", "high_review", "manual_required"]).fillna(0)
        ax.bar(counts.index, counts.values, color=["#54a24b", "#f58518", "#e45756"])
        ax.set_title("대학별 수능 반영규칙 확정 상태")
        ax.set_xlabel("확정 상태")
        ax.set_ylabel("대학 수")
        for i, v in enumerate(counts.values):
            ax.text(i, v, f"{int(v)}", ha="center", va="bottom")
        save_fig(fig, "fig_gate2_final_01_confirmation_status.png")

        fig, ax = plt.subplots(figsize=(8.2, 4.8), constrained_layout=True)
        plot_df = metric_summary.loc[metric_summary["score_metric_split"].ne("미확인")].sort_values("university_n")
        ax.barh(plot_df["score_metric_split"], plot_df["university_n"], color="#4c78a8")
        ax.set_title("활용지표/점수산식 단서별 대학 수")
        ax.set_xlabel("대학 수")
        ax.set_ylabel("점수 단서")
        save_fig(fig, "fig_gate2_final_02_score_metric_terms.png")
        display(status_summary)
        display(metric_summary)
        """
    ),
    code(
        """
        summary = pd.DataFrame(
            [
                {"metric": "final_rule_university_n", "value": final_rules["univ_id"].nunique()},
                {"metric": "confirmed_university_n", "value": int(final_rules["confirmation_status"].eq("confirmed").sum())},
                {"metric": "high_review_university_n", "value": int(final_rules["confirmation_status"].eq("high_review").sum())},
                {"metric": "manual_required_university_n", "value": int(final_rules["confirmation_status"].eq("manual_required").sum())},
                {"metric": "primary_candidate_university_n", "value": int(final_rules["final_modeling_use"].eq("primary_candidate").sum())},
                {"metric": "secondary_candidate_university_n", "value": int(final_rules["final_modeling_use"].eq("secondary_candidate").sum())},
                {"metric": "nanumgothic_font_path", "value": nanum},
            ]
        )
        save_csv(summary, FINAL_DIR / "gate2_15_final_rule_summary.csv")

        report = f'''# Gate 2-B 최종 수능 반영규칙 확정 요약

        ## 폰트

        - Matplotlib font: NanumGothic
        - font path: `{nanum}`

        ## 확정 결과

        - 대학 수: {final_rules["univ_id"].nunique():,}
        - confirmed: {int(final_rules["confirmation_status"].eq("confirmed").sum()):,}
        - high_review: {int(final_rules["confirmation_status"].eq("high_review").sum()):,}
        - manual_required: {int(final_rules["confirmation_status"].eq("manual_required").sum()):,}
        - primary_candidate: {int(final_rules["final_modeling_use"].eq("primary_candidate").sum()):,}
        - secondary_candidate: {int(final_rules["final_modeling_use"].eq("secondary_candidate").sum()):,}

        ## 최종 산출물

        - `gate2_10_final_admission_rule_summary.csv`
        - `gate2_11_concrete_rule_showcase_top12.csv`
        - `gate2_12_final_rule_status_summary.csv`
        - `gate2_13_score_metric_summary.csv`
        - `gate2_14_subject_area_summary.csv`
        - `gate2_15_final_rule_summary.csv`

        ## 해석

        `confirmed`는 HTML 캐시의 대표 표에서 수능 성적 산출방법/수능 반영영역과 점수 활용 단서가 충분히 확인된 상태다.
        `high_review`는 대표 표는 잡혔지만 모집단위 예외, 실기 혼합, 영어/한국사 변환점수 등의 세부 규칙 확인이 필요한 상태다.
        '''
        report = "\\n".join(line.strip() for line in report.splitlines())
        report_path = FINAL_DIR / "gate2_final_rule_confirmation_report.md"
        report_path.write_text(report, encoding="utf-8")
        audit("export", "gate2_final_rule_confirmation_report.md", "write_markdown_report", status="PASS", note=str(report_path))
        display(summary)
        display(Markdown(report))
        """
    ),
    code(
        """
        audit_log = pd.DataFrame(AUDIT_LOG)
        save_csv(audit_log, FINAL_DIR / "gate2_16_final_rule_audit_log.csv")
        required = [
            "gate2_10_final_admission_rule_summary.csv",
            "gate2_11_concrete_rule_showcase_top12.csv",
            "gate2_12_final_rule_status_summary.csv",
            "gate2_13_score_metric_summary.csv",
            "gate2_14_subject_area_summary.csv",
            "gate2_15_final_rule_summary.csv",
            "gate2_16_final_rule_audit_log.csv",
            "gate2_final_rule_confirmation_report.md",
            "figures/fig_gate2_final_01_confirmation_status.png",
            "figures/fig_gate2_final_02_score_metric_terms.png",
        ]
        manifest = pd.DataFrame(
            [
                {
                    "artifact": name,
                    "path": str(FINAL_DIR / name),
                    "exists": (FINAL_DIR / name).exists(),
                    "size_bytes": (FINAL_DIR / name).stat().st_size if (FINAL_DIR / name).exists() else 0,
                }
                for name in required
            ]
        )
        display(manifest)
        """
    ),
]


def main() -> None:
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    nb = nbf.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"]["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb["metadata"]["language_info"] = {"name": "python", "pygments_lexer": "ipython3"}
    for idx, cell in enumerate(nb["cells"]):
        cell.setdefault("id", f"gate2-final-{idx:02d}")
    nbf.validate(nb)
    nbf.write(nb, NOTEBOOK_PATH)
    print(NOTEBOOK_PATH)


if __name__ == "__main__":
    main()
