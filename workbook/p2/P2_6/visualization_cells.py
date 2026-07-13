# Auto-generated notebook visual blocks for workbook/p2/P2_6/P2_G6_1.ipynb
# These snippets expect the preceding P2_G6_1 notebook variables to exist.

# %% V00_HELPER

# P2-G6 visual development helper.
# 기존 P3/P4 strict 산출물을 다시 적합하지 않고, 결과 구조를 읽는 그림만 만든다.
VISUAL_FIGURE_RECORDS = []


def save_visual_figure(fig, filename: str, block_id: str, question: str, data_used: str):
    path = OUT_ROOT / "figures" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    VISUAL_FIGURE_RECORDS.append(
        {
            "block_id": block_id,
            "figure_path": str(path.relative_to(ROOT)),
            "question": question,
            "data_used": data_used,
        }
    )
    return path


def status_to_score(value) -> float:
    text = str(value).upper()
    if "BLOCKED" in text or "FAIL" in text:
        return 0.0
    if "WARNING" in text or "WARN" in text:
        return 0.5
    if "READY" in text or "PASS" in text or "OK" in text:
        return 1.0
    return 0.25


def display_reading_note(title: str, observation: str, cause: str, limitation: str, conclusion: str):
    display(
        Markdown(
            f"""**{title}**

- 관찰: {observation}
- 원인: {cause}
- 제한: {limitation}
- 결론: {conclusion}
"""
        )
    )


# %% V01_STATUS_LINEAGE

# V01. P3/P4 상태와 lineage hash를 한눈에 확인한다.
status_plot = df_status.copy()
status_plot["score"] = status_plot["status"].map(status_to_score)
status_wide = status_plot.pivot(index="namespace", columns="status_key", values="score")

fig, axes = plt.subplots(1, 2, figsize=(14, 4.8), gridspec_kw={"width_ratios": [1.25, 1]})
im = axes[0].imshow(status_wide.fillna(0.25), aspect="auto", cmap="RdYlGn", vmin=0, vmax=1)
axes[0].set_title("P3/P4 readiness status matrix")
axes[0].set_yticks(range(len(status_wide.index)))
axes[0].set_yticklabels(status_wide.index)
axes[0].set_xticks(range(len(status_wide.columns)))
axes[0].set_xticklabels(status_wide.columns, rotation=45, ha="right")
for y, namespace in enumerate(status_wide.index):
    for x, key in enumerate(status_wide.columns):
        raw_status = df_status.loc[
            (df_status["namespace"].eq(namespace)) & (df_status["status_key"].eq(key)), "status"
        ]
        label = raw_status.iloc[0] if len(raw_status) else ""
        axes[0].text(x, y, str(label).replace("_", "\n"), ha="center", va="center", fontsize=8)
fig.colorbar(im, ax=axes[0], fraction=0.035, pad=0.02, label="ready score")

axes[1].axis("off")
hash_text = ["Lineage hash chain"]
for row in hash_rows.itertuples(index=False):
    sha = str(row.sha256)
    hash_text.append(f"{row.item}: {sha[:10]}...{sha[-8:] if len(sha) > 18 else sha}")
axes[1].text(0, 1, "\n".join(hash_text), va="top", ha="left", family="monospace", fontsize=9)
axes[1].set_title("Read-only lineage anchors")
fig.tight_layout()
path = save_visual_figure(
    fig,
    "P2_G6_1_V01_STATUS_LINEAGE.png",
    "V01_STATUS_LINEAGE",
    "P3/P4 strict 상태와 hash가 같은 실행 사슬을 가리키는가?",
    "P3_P4_CONFIRMATORY_STATUS.json, P3/P4 status json",
)
plt.show()
print(f"saved visual: {path.relative_to(ROOT)}")

display_reading_note(
    "V01 해석",
    "P3/P4는 READY 계열 상태지만 P6로 넘길 때 WARNING과 BLOCKED branch를 분리해서 읽어야 한다.",
    "이 노트북은 새 적합이 아니라 이미 잠긴 strict 산출물의 lineage와 상태를 재확인한다.",
    "hash는 재현성 anchor이지 통계적 타당성 자체를 증명하지 않는다.",
    "P6 입력은 준비됐지만 P2-Q/P3-Q 차단과 residual/raw 동등성 경고를 유지한다.",
)


# %% V02_P3_RESIDUAL_DIAGNOSTIC

# V02. P3 residual 모델의 실제 구조를 expected-vs-observed, residual, fold metric으로 읽는다.
p3_full_residual = pd.read_parquet(PATHS["p3_full_residual"])
p3_fold_metrics_path = P3_ROOT / "qa/P3_FULL_FOLD_METRICS.csv"
p3_fold_metrics = pd.read_csv(p3_fold_metrics_path) if p3_fold_metrics_path.exists() else pd.DataFrame()

fig, axes = plt.subplots(2, 2, figsize=(12, 9))
ax = axes[0, 0]
sample_for_scatter = p3_full_residual.sample(min(2500, len(p3_full_residual)), random_state=42)
ax.scatter(
    sample_for_scatter["expected_a_rate_full_pct"],
    sample_for_scatter["a_rate_pct"],
    s=8,
    alpha=0.35,
    color="#4C78A8",
)
low = min(sample_for_scatter["expected_a_rate_full_pct"].min(), sample_for_scatter["a_rate_pct"].min())
high = max(sample_for_scatter["expected_a_rate_full_pct"].max(), sample_for_scatter["a_rate_pct"].max())
ax.plot([low, high], [low, high], color="black", linewidth=1)
ax.set_title("Observed A-rate vs P3 expected A-rate")
ax.set_xlabel("expected A-rate from P3 FULL (%)")
ax.set_ylabel("observed A-rate (%)")

ax = axes[0, 1]
ax.hist(p3_full_residual["grade_residual_structure_full_oof_pp"], bins=45, color="#59A14F", alpha=0.85)
ax.axvline(0, color="black", linewidth=1)
ax.set_title("OOF residual distribution")
ax.set_xlabel("observed - expected A-rate (percentage points)")
ax.set_ylabel("department rows")

ax = axes[1, 0]
perf_plot = p3_oof.melt(
    id_vars="model_label",
    value_vars=["oof_r2", "test_r2"],
    var_name="metric",
    value_name="value",
)
for idx, metric in enumerate(["oof_r2", "test_r2"]):
    sub = perf_plot[perf_plot["metric"].eq(metric)]
    x = np.arange(len(sub)) + (idx - 0.5) * 0.32
    ax.bar(x, sub["value"], width=0.3, label=metric)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_xticks(np.arange(p3_oof["model_label"].nunique()))
ax.set_xticklabels(p3_oof["model_label"].unique())
ax.set_title("OOF vs locked-test R2")
ax.set_ylabel("R2")
ax.legend()

ax = axes[1, 1]
if len(p3_fold_metrics):
    ax.plot(p3_fold_metrics["fold"], p3_fold_metrics["mae"], marker="o", label="MAE")
    ax2 = ax.twinx()
    ax2.plot(p3_fold_metrics["fold"], p3_fold_metrics["r2"], marker="s", color="#F58518", label="R2")
    ax.set_xlabel("Group fold")
    ax.set_ylabel("MAE")
    ax2.set_ylabel("R2")
    ax.set_title("P3 FULL fold stability")
    lines_1, labels_1 = ax.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax.legend(lines_1 + lines_2, labels_1 + labels_2, loc="best")
else:
    ax.axis("off")
    ax.text(0.02, 0.95, "P3_FULL_FOLD_METRICS.csv not found", va="top")
fig.tight_layout()
path = save_visual_figure(
    fig,
    "P2_G6_1_V02_P3_RESIDUAL_DIAGNOSTIC.png",
    "V02_P3_RESIDUAL_DIAGNOSTIC",
    "P3 residual은 강한 예측모형의 잔차인가, 구조 통제 후 남은 grade signal인가?",
    "P3_STRUCTURE_GRADE_RESIDUAL_FULL.parquet, P3_OOF_PERFORMANCE.csv, P3_FULL_FOLD_METRICS.csv",
)
plt.show()
print(f"saved visual: {path.relative_to(ROOT)}")

display_reading_note(
    "V02 해석",
    f"FULL residual coverage는 {len(p3_full_residual):,}행이고 raw A-residual corr는 {full_diag.raw_residual_corr:.3f}로 높다.",
    "P3 expected A-rate가 A비율의 일부 구조를 설명하지만, residual이 raw A와 강하게 같이 움직인다.",
    "locked test R2가 낮으므로 residual을 순수한 인과적 shock처럼 읽으면 안 된다.",
    "P6에서는 residual topology를 보되 raw A와 거의 같은 축을 공유한다는 경고를 유지한다.",
)


# %% V03_P4_SAMPLE_STRUCTURE

# V03. P4 outcome model이 어떤 표본과 split 위에서 돌아갔는지 시각화한다.
p4_joint = pd.read_parquet(P4_ROOT / "data/P4_STRUCTURE_JOINT_FRAME.parquet")

fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
sample_cols = [c for c in ["train_n", "validation_n", "test_n"] if c in p4_sample.columns]
bottom = np.zeros(len(p4_sample))
x = np.arange(len(p4_sample))
for col, color in zip(sample_cols, ["#4C78A8", "#F58518", "#54A24B"]):
    axes[0].bar(x, p4_sample[col], bottom=bottom, label=col.replace("_n", ""), color=color)
    bottom += p4_sample[col].to_numpy()
axes[0].set_xticks(x)
axes[0].set_xticklabels(p4_sample["sample_id"], rotation=25, ha="right")
axes[0].set_ylabel("rows")
axes[0].set_title("P4 train/validation/test split by sample")
axes[0].legend()

coverage = pd.DataFrame(
    [
        {
            "outcome": "health_employment",
            "non_null_n": p4_joint["health_employment_rate_prop"].notna().sum(),
            "null_n": p4_joint["health_employment_rate_prop"].isna().sum(),
        },
        {
            "outcome": "graduate_progression",
            "non_null_n": p4_joint["graduate_school_progression_rate_prop"].notna().sum(),
            "null_n": p4_joint["graduate_school_progression_rate_prop"].isna().sum(),
        },
        {
            "outcome": "OOF residual",
            "non_null_n": p4_joint["grade_residual_structure_full_oof_10pp"].notna().sum(),
            "null_n": p4_joint["grade_residual_structure_full_oof_10pp"].isna().sum(),
        },
    ]
)
axes[1].bar(coverage["outcome"], coverage["non_null_n"], label="available", color="#72B7B2")
axes[1].bar(coverage["outcome"], coverage["null_n"], bottom=coverage["non_null_n"], label="missing", color="#BAB0AC")
axes[1].set_title("P4 outcome/signal availability")
axes[1].set_ylabel("rows in joint frame")
axes[1].tick_params(axis="x", rotation=20)
axes[1].legend()
fig.tight_layout()
path = save_visual_figure(
    fig,
    "P2_G6_1_V03_P4_SAMPLE_STRUCTURE.png",
    "V03_P4_SAMPLE_STRUCTURE",
    "P4 모형의 비교가 같은 표본 구조와 outcome availability 위에서 이루어졌는가?",
    "P4_SAMPLE_AUDIT.csv, P4_STRUCTURE_JOINT_FRAME.parquet",
)
plt.show()
print(f"saved visual: {path.relative_to(ROOT)}")

display_reading_note(
    "V03 해석",
    "P4는 outcome별 구조 표본과 joint frame의 결측/사용 가능 범위 위에서 읽어야 한다.",
    "취업률·대학원 진학률은 같은 학과 universe에서 항상 동시에 관측되는 변수가 아니다.",
    "표본 수 차이는 효과 크기 차이와 별개의 불확실성 원천이다.",
    "P6 결과 담론에는 slope뿐 아니라 표본 universe와 missing pattern을 함께 명시한다.",
)


# %% V04_P4_AME_FOREST

# V04. P4 fractional logit primary slope를 bootstrap AME CI와 함께 비교한다.
ame_boot = p4_boot_ci.loc[p4_boot_ci["metric"].eq("ame")].copy()
ame_boot["ame_mid_pp"] = ame_boot["median"] * 100
ame_boot["ci_low_pp"] = ame_boot["ci_low"] * 100
ame_boot["ci_high_pp"] = ame_boot["ci_high"] * 100
ame_plot = frac_display.merge(
    ame_boot[["outcome", "grade_signal", "ci_low_pp", "ci_high_pp", "ame_mid_pp"]],
    on=["outcome", "grade_signal"],
    how="left",
)
ame_plot["row_label"] = ame_plot["outcome"].map(
    {"HEALTH_EMPLOYMENT": "Health employment", "GRAD_SCHOOL_PROGRESSION": "Grad progression"}
) + " / " + ame_plot["grade_signal"].map({"RAW_A": "RAW_A", "OOF_RESIDUAL_FULL": "OOF residual"})
ame_plot = ame_plot.sort_values(["outcome", "grade_signal"]).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(9.2, 4.8))
y = np.arange(len(ame_plot))
xerr = np.vstack(
    [
        ame_plot["ame_pp_10pp"] - ame_plot["ci_low_pp"],
        ame_plot["ci_high_pp"] - ame_plot["ame_pp_10pp"],
    ]
)
colors = ["#4C78A8" if signal == "RAW_A" else "#F58518" for signal in ame_plot["grade_signal"]]
ax.errorbar(ame_plot["ame_pp_10pp"], y, xerr=xerr, fmt="none", ecolor="#6B6B6B", elinewidth=1.5, capsize=4)
ax.scatter(ame_plot["ame_pp_10pp"], y, s=80, color=colors, zorder=3)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_yticks(y)
ax.set_yticklabels(ame_plot["row_label"])
ax.set_xlabel("AME per 10pp grade signal (percentage points)")
ax.set_title("P4 primary signal size with generated-regressor bootstrap CI")
ax.grid(axis="x", alpha=0.25)
fig.tight_layout()
path = save_visual_figure(
    fig,
    "P2_G6_1_V04_P4_AME_FOREST.png",
    "V04_P4_AME_FOREST",
    "RAW_A와 OOF residual은 취업률/대학원 진학률에 어느 정도의 추가 신호를 주는가?",
    "P4_COEFFICIENT_RESULTS.csv, P4_BOOTSTRAP_CI.csv",
)
plt.show()
print(f"saved visual: {path.relative_to(ROOT)}")

display_reading_note(
    "V04 해석",
    "대학원 진학률의 AME가 건강보험 취업률보다 더 크게 보이며, RAW_A와 OOF residual의 위치가 거의 겹친다.",
    "같은 P4 controls 안에서는 residual과 raw A가 같은 added-information 방향을 span한다.",
    "bootstrap CI는 generated-regressor approximation 경고가 있으므로 정밀한 확증보다 방향성 판단에 둔다.",
    "P6 담론은 'grade signal은 취업보다 대학원 진학과 더 정렬'이라는 제한적 결론으로 유지한다.",
)


# %% V05_D_BOOTSTRAP

# V05. Employment-vs-progression 차이 D를 별도 결과물로 분리한다.
d_plot = p4_d.copy()
d_plot["D_pp"] = d_plot["D_progression_minus_employment"] * 100
d_ci = p4_boot_ci.loc[p4_boot_ci["outcome"].eq("PROGRESSION_MINUS_EMPLOYMENT")].copy()
d_ci["ci_low_pp"] = d_ci["ci_low"] * 100
d_ci["ci_high_pp"] = d_ci["ci_high"] * 100
d_ci["median_pp"] = d_ci["median"] * 100
d_plot = d_plot.merge(d_ci[["grade_signal", "ci_low_pp", "ci_high_pp", "median_pp"]], on="grade_signal", how="left")
d_plot = d_plot.sort_values("grade_signal").reset_index(drop=True)

fig, ax = plt.subplots(figsize=(8.5, 4.5))
y = np.arange(len(d_plot))
xerr = np.vstack([d_plot["D_pp"] - d_plot["ci_low_pp"], d_plot["ci_high_pp"] - d_plot["D_pp"]])
colors = ["#4C78A8" if signal == "RAW_A" else "#F58518" for signal in d_plot["grade_signal"]]
ax.errorbar(d_plot["D_pp"], y, xerr=xerr, fmt="none", ecolor="#6B6B6B", elinewidth=1.5, capsize=4)
ax.scatter(d_plot["D_pp"], y, s=90, color=colors, zorder=3)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_yticks(y)
ax.set_yticklabels(d_plot["grade_signal"])
ax.set_xlabel("Progression AME - Employment AME (percentage points)")
ax.set_title("Does grade signal align more with progression than employment?")
ax.grid(axis="x", alpha=0.25)
fig.tight_layout()
path = save_visual_figure(
    fig,
    "P2_G6_1_V05_D_BOOTSTRAP.png",
    "V05_D_BOOTSTRAP",
    "grade signal의 추가 효과가 취업률보다 대학원 진학률에서 더 큰가?",
    "P4_EMPLOYMENT_PROGRESSION_DIFFERENCE.csv, P4_BOOTSTRAP_CI.csv",
)
plt.show()
print(f"saved visual: {path.relative_to(ROOT)}")

display_reading_note(
    "V05 해석",
    f"OOF residual 기준 D는 {d_resid:+.3f}%p이고 bootstrap CI가 양의 영역을 중심으로 놓인다.",
    "D는 두 outcome slope의 차이이므로 단일 outcome의 유의성과 다르게 해석해야 한다.",
    "대학원 진학률은 진학 의사·전공별 구조·학교 prestige를 함께 반영할 수 있어 causal label로 읽지 않는다.",
    "P6에서는 '취업 성과 개선'보다 '진학 선택/경로와의 정렬'이라는 결과 담론이 더 안전하다.",
)


# %% V06_LOCKED_TEST_IMPROVEMENT

# V06. Locked test에서 signal 추가가 base 대비 실제로 좋아졌는지 metric별로 본다.
imp_plot = test_frac.loc[test_frac["model_family"].eq("fractional_logit")].copy()
imp_long = imp_plot.melt(
    id_vars=["outcome", "grade_signal"],
    value_vars=["test_deviance_improvement", "test_brier_improvement", "test_mae_improvement"],
    var_name="metric",
    value_name="improvement",
)
imp_long["panel"] = imp_long["outcome"].map(
    {"HEALTH_EMPLOYMENT": "Health employment", "GRAD_SCHOOL_PROGRESSION": "Grad progression"}
).fillna(imp_long["outcome"].astype(str))
imp_long["signal_label"] = imp_long["grade_signal"].map(
    {"RAW_A": "RAW_A", "OOF_RESIDUAL_FULL": "OOF residual"}
).fillna(imp_long["grade_signal"].astype(str))

fig, axes = plt.subplots(1, 3, figsize=(14, 4.6), sharey=False)
for ax, metric in zip(axes, ["test_deviance_improvement", "test_brier_improvement", "test_mae_improvement"]):
    sub = imp_long[imp_long["metric"].eq(metric)].copy()
    sub["label"] = sub["panel"].astype(str) + "\n" + sub["signal_label"].astype(str)
    colors = ["#59A14F" if v > 0 else "#E15759" for v in sub["improvement"]]
    ax.bar(sub["label"], sub["improvement"], color=colors)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title(metric.replace("test_", "").replace("_improvement", " improvement"))
    ax.tick_params(axis="x", rotation=0)
    ax.grid(axis="y", alpha=0.25)
fig.suptitle("Locked-test improvement: positive means signal beats base", y=1.03)
fig.tight_layout()
path = save_visual_figure(
    fig,
    "P2_G6_1_V06_LOCKED_TEST_IMPROVEMENT.png",
    "V06_LOCKED_TEST_IMPROVEMENT",
    "P4 signal 추가가 locked test에서 base 대비 외부 예측을 개선했는가?",
    "P4_LOCKED_TEST_METRICS.csv",
)
plt.show()
print(f"saved visual: {path.relative_to(ROOT)}")

display_reading_note(
    "V06 해석",
    "건강보험 취업률에서는 improvement가 약하거나 음수이고, 대학원 진학률에서는 더 안정적인 개선이 보인다.",
    "P4의 slope 유의성과 locked-test 예측 개선은 같은 질문이 아니다.",
    "test 결과를 사양 선택에 되먹이면 잠금 평가의 의미가 사라진다.",
    "P6 문장에서는 effect-size와 out-of-sample 개선을 분리해서 보고한다.",
)


# %% V07_RAW_RESID_EQUIVALENCE

# V07. RAW_A와 OOF residual이 왜 거의 같은 추가정보 축인지 시각적으로 확인한다.
equiv_plot = p4_equiv.copy()
equiv_plot["log10_delta"] = np.log10(equiv_plot["max_abs_raw_minus_residual"].clip(lower=1e-15))

fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
axes[0].bar(equiv_plot["metric"], equiv_plot["log10_delta"], color="#B279A2")
axes[0].set_title("RAW_A vs OOF residual metric delta")
axes[0].set_ylabel("log10(max absolute delta)")
axes[0].tick_params(axis="x", rotation=20)
axes[0].grid(axis="y", alpha=0.25)

scatter_df = p3_full_residual.sample(min(3000, len(p3_full_residual)), random_state=7)
axes[1].scatter(
    scatter_df["a_rate_pct"],
    scatter_df["grade_residual_structure_full_oof_pp"],
    s=8,
    alpha=0.35,
    color="#4C78A8",
)
axes[1].axhline(0, color="black", linewidth=0.8)
axes[1].set_title(f"Raw A vs residual, corr={full_diag.raw_residual_corr:.3f}")
axes[1].set_xlabel("Raw A-rate (%)")
axes[1].set_ylabel("P3 FULL residual (pp)")
fig.tight_layout()
path = save_visual_figure(
    fig,
    "P2_G6_1_V07_RAW_RESID_EQUIVALENCE.png",
    "V07_RAW_RESID_EQUIVALENCE",
    "현재 P4 설계에서 RAW_A와 OOF residual을 독립적인 두 신호처럼 해석해도 되는가?",
    "P4_WITHIN_RAW_EQUIVALENCE_AUDIT.csv, P3_STRUCTURE_GRADE_RESIDUAL_FULL.parquet",
)
plt.show()
print(f"saved visual: {path.relative_to(ROOT)}")

display_reading_note(
    "V07 해석",
    "end-to-end delta는 극소값이고 raw A-residual 상관은 매우 높다.",
    "residual = raw A - P3 expected A이며, P4에 같은 구조 통제를 넣으면 같은 1차원 추가정보를 공유한다.",
    "이 동등성은 현재 선형 P4 설계 안에서의 성질이며 비선형/상호작용 설계까지 자동 확장되지 않는다.",
    "P6 residual topology는 residual 고유성보다 '어떤 구조에서 raw A 축이 남는가'를 묻는 방향으로 설계한다.",
)


# %% V08_P6_DECISION_DASHBOARD

# V08. P6로 넘길 결과 담론을 구조화된 decision matrix로 고정한다.
decision_matrix = pd.DataFrame(
    [
        {
            "question": "P3 residual handoff",
            "finding": "READY",
            "evidence": f"coverage={int(full_diag.coverage_n):,}, coverage_rate={full_diag.coverage_rate:.3f}",
            "risk": "locked-test R2 is low; residual is not a pure causal shock",
            "next_action": "use as topology signal with warning",
        },
        {
            "question": "P4 employment signal",
            "finding": "WEAK_EXTERNAL_GAIN",
            "evidence": f"OOF residual employment locked-test MAE improvement={emp_resid.test_mae_improvement:+.6f}",
            "risk": "slope and out-of-sample gain diverge",
            "next_action": "avoid strong employment-performance claim",
        },
        {
            "question": "P4 progression signal",
            "finding": "STRONGER_THAN_EMPLOYMENT",
            "evidence": f"OOF residual D={d_resid:+.3f}%p",
            "risk": "progression reflects selection and aspiration, not only educational value",
            "next_action": "frame as progression alignment",
        },
        {
            "question": "RAW_A vs OOF residual",
            "finding": "NEAR_EQUIVALENT_IN_P4",
            "evidence": f"max delta={max_equiv_delta:.3e}, raw-resid corr={full_diag.raw_residual_corr:.3f}",
            "risk": "overclaiming residual as new independent information",
            "next_action": "keep equivalence warning in P6",
        },
        {
            "question": "P2-Q/P3-Q branch",
            "finding": "BLOCKED",
            "evidence": p6_status["P6_Q_BRANCH_STATUS"],
            "risk": "admission/selectivity feature contract not approved",
            "next_action": "do not merge Q branch into confirmatory result",
        },
    ]
)
decision_path = OUT_ROOT / "artifacts/P2_G6_1_VISUAL_DECISION_MATRIX.csv"
decision_matrix.to_csv(decision_path, index=False)

score_map = {"READY": 1.0, "STRONGER_THAN_EMPLOYMENT": 0.75, "WEAK_EXTERNAL_GAIN": 0.45, "NEAR_EQUIVALENT_IN_P4": 0.5, "BLOCKED": 0.0}
fig, ax = plt.subplots(figsize=(11, 4.8))
scores = decision_matrix["finding"].map(score_map).fillna(0.25)
colors = ["#59A14F" if s >= 0.75 else "#F58518" if s >= 0.45 else "#E15759" for s in scores]
ax.barh(decision_matrix["question"], scores, color=colors)
ax.set_xlim(0, 1)
ax.set_xlabel("decision readiness / interpretive strength")
ax.set_title("P2-G6 model-reading decision dashboard")
for y, row in enumerate(decision_matrix.itertuples(index=False)):
    ax.text(0.02, y, row.finding, va="center", ha="left", color="black", fontsize=9)
ax.grid(axis="x", alpha=0.25)
fig.tight_layout()
path = save_visual_figure(
    fig,
    "P2_G6_1_V08_P6_DECISION_DASHBOARD.png",
    "V08_P6_DECISION_DASHBOARD",
    "P6로 넘길 결과론적 판단과 경고를 한 장으로 고정할 수 있는가?",
    "P3/P4 summary objects, P6 status dictionary",
)
plt.show()
print(f"saved visual: {path.relative_to(ROOT)}")
display(decision_matrix)

display_reading_note(
    "V08 해석",
    "P6 진입은 가능하지만 employment claim, residual 독립성, Q branch는 모두 제한을 달고 간다.",
    "모형 결과는 한 숫자가 아니라 handoff-ready signal과 blocked branch가 공존하는 상태다.",
    "dashboard score는 의사결정 표시일 뿐 통계량이 아니다.",
    "다음 노트북은 residual topology를 탐색하되 confirmatory wording은 P4 strict 결과에 묶는다.",
)


# %% V09_VISUAL_MANIFEST

# V09. 시각화 산출물 manifest와 모델 읽기 가이드를 저장한다.
visual_records = pd.DataFrame(VISUAL_FIGURE_RECORDS)
visual_manifest_path = OUT_ROOT / "artifacts/P2_G6_1_VISUAL_ARTIFACTS.csv"
visual_guide_path = OUT_ROOT / "reports/P2_G6_1_VISUAL_MODEL_READING_GUIDE.md"
visual_records.to_csv(visual_manifest_path, index=False)

try:
    visual_records_table = visual_records.to_markdown(index=False)
except Exception:
    visual_records_table = "```csv\n" + visual_records.to_csv(index=False) + "```"

visual_guide_md = f"""# P2-G6_1 Visual Model Reading Guide

## 목적

이 가이드는 P2-G6_1 노트북에 추가한 시각화가 어떤 모델 질문을 답하는지 고정한다.
노트북은 P3/P4를 다시 적합하지 않고, strict-clean 산출물을 읽어 P6 진입 전 판단을 구조화한다.

## 핵심 결론

1. P3 residual handoff는 준비됐지만, locked-test R2가 낮으므로 residual을 강한 예측모형의 순수 잔차처럼 해석하지 않는다.
2. P4에서 grade signal은 건강보험 취업률보다 대학원 진학률과 더 크게 정렬된다.
3. RAW_A와 OOF residual은 현재 P4 선형 설계에서 거의 같은 added-information 축을 제공한다.
4. P2-Q/P3-Q branch는 feature contract 승인 전까지 confirmatory chain에 넣지 않는다.

## 그림 목록

{visual_records_table}

## 구조화 담론

| 항목 | 관찰 | 원인 | 제한 | 결론 |
|---|---|---|---|---|
| P3 residual | coverage는 충분하지만 raw A와 residual 상관이 높다 | residual이 raw A에서 구조 기대값을 뺀 값이기 때문 | causal shock 아님 | topology signal로만 사용 |
| P4 employment | locked-test gain이 약하다 | 취업 outcome은 구조 통제 후 grade signal 추가정보가 제한적 | slope와 예측개선이 다름 | 강한 취업성과 claim 금지 |
| P4 progression | D가 양수 방향이다 | grade signal이 대학원 진학과 더 정렬 | selection/aspiration 혼재 | progression alignment로 표현 |
| RAW_A/residual | end-to-end delta가 극소다 | 같은 controls 안에서 같은 1차원 정보를 span | 현재 P4 선형 설계 한정 | residual 고유효과 과장 금지 |
"""
visual_guide_path.write_text(visual_guide_md, encoding="utf-8")
display(visual_records)
display(Markdown(f"Saved visual manifest: `{visual_manifest_path.relative_to(ROOT)}`  \nSaved visual guide: `{visual_guide_path.relative_to(ROOT)}`"))

