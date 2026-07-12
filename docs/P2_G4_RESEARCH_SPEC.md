# P2-G4 Research Specification

## Title

**대학별 성적분포는 노동시장과 진학시장에서 서로 다른 신호로 읽히는가**

핵심 질문은 단순하다.

> **같은 A학점은 정말 같은 의미인가?**

P2-G4는 P2-G3에서 독립감사 GREEN을 받은 `mart_department_model_base_2024.parquet`를 사용해, 대학-학과 단위 A비율이 입결·전공구조·학교구조로 얼마나 설명되고, 설명되지 않는 차이가 취업성과와 대학원 진학성과에서 서로 다른 신호를 갖는지 검토한다.

## Scope

| 항목 | 내용 |
|---|---|
| 분석 단계 | P2-G4 Modeling & Integrated Findings |
| 선행조건 | P2-G3 independent audit GREEN, P4 handoff manifest frozen |
| 기본 데이터 | `mart_department_model_base_2024.parquet` |
| 기본 설계 | 2024 다층 단면 관찰연구 |
| 확장 설계 | 2023-2025 short panel, readiness gate 통과 시에만 실행 |
| 관측 단위 | `2024 x school x campus x department` |
| 해석 단위 | 개인이 아니라 학교-학과 집단 수준 조건부 연관성 |

## Core Claim To Test

> 대학별·학과별 성적분포 차이는 단순한 학점 관대성의 차이가 아니라, 대학의 입학생 구성·전공구조·평가환경을 반영하며, 노동시장과 진학시장에서는 서로 다른 신호로 읽힐 수 있다.

이 문장은 최종 결론이 아니라 검증할 주장이다. 인과효과, 의도적 학점 인플레이션, 대학 순위화는 본 프로젝트의 목표가 아니다.

## Research Questions

| ID | 질문 |
|---|---|
| RQ1 | 대학·학과별 A비율은 입결, 전공, 학교유형, 학과규모, 교육여건과 어떻게 연결되는가? |
| RQ2 | A비율 또는 조건 대비 A비율 잔차는 취업성과에 추가 설명력을 제공하는가? |
| RQ3 | A비율 또는 조건 대비 A비율 잔차는 취업보다 대학원 진학에 더 큰 추가 설명력을 제공하는가? |
| RQ4 | 자격증·기업규모·공공부문·산업집중도·전문직 구조에 따라 A비율의 신호가 달라지는가? |
| RQ5 | panel이 준비되면 현재 A비율과 구조변수가 다음 해 A비율 증가·유지·감소를 구분하는가? |

## Hypothesis Set

| ID | 가설 | 핵심 검증 |
|---|---|---|
| H1 | 입결·전공·학과구조를 통제해도 학교별 A비율 차이가 남는다 | MixedLM school variance, school FE |
| H2 | 같은 학교 내부에서도 전공·입결·학과구조와 A비율은 연결된다 | school fixed effects |
| H3 | A비율/leniency residual은 취업보다 대학원 진학에서 더 큰 추가 설명력을 갖는다 | ΔR², ΔMAE, school bootstrap |
| H4 | 취업성과는 A비율보다 전공계열 노동시장 context에 더 크게 설명된다 | block ablation |
| H5 | 자격증·면허 의존 계열에서는 A비율의 취업 신호가 약하다 | interaction, FDR |
| H6 | 대형사업체·공공기관·전문직 구조는 A비율-성과 관계를 조절한다 | marginal effect plot |
| H7 | 관측조건 대비 취업·진학성과가 높은 학과가 존재한다 | OOF outcome residual |
| H8 | panel ready일 때 다음 해 A비율 변화 상태를 구분할 수 있다 | out-of-time Macro-F1 |

## Data Contract

P4는 동결 handoff 파일만 읽는다.

```text
mart_department_model_base_2024.parquet
dim_school_split.csv
model_sample_registry.csv
department_model_column_registry.csv
p4_feature_set_registry.csv
p4_target_candidate_registry.csv
P4_HANDOFF_MANIFEST.json
```

금지사항:

- 원천 CSV 재로드
- P4 내부 재병합
- 학교명·학과명 재정규화
- 임의 fuzzy matching
- manifest hash 불일치 상태에서 분석 계속

## Target Blocks

| 영역 | Primary target | 주의 |
|---|---|---|
| Grade | `a_rate_pct` | `cd_rate_pct`, `f_rate_pct` 등 같은 성적분포 파생값은 feature 금지 |
| Employment | `health_employment_rate_pct` | 평균 대체 금지, 관측표본 명시 |
| Progression | `graduate_school_progression_rate_pct` | 취업성과와 동일 조건으로 증분 비교 |
| Panel | `A_change_class_t+1` | readiness gate 통과 시에만 실행 |

## Feature Blocks

| Block | 예시 | 용도 |
|---|---|---|
| S | major, school_type, region, establishment | 기본 strata |
| B | enrollment, faculty, competition, size | 학과·학교 구조 |
| A | selectivity proxy | 입결·선발력 |
| G | A비율 또는 OOF grade residual | 학점 신호 |
| C24 | wage/reference context | 2024 계열 context |
| CG | GOMS recent context | 노동시장 구조 |

## Core Modeling Plan

### Grade Formation

```text
G0 = mean
G1 = S
G2 = S + B
G3 = S + B + A
G4 = S + B + A + credit_forfeit_flag
```

모형:

- OLS + school cluster-robust SE
- MixedLM random intercept by school
- School fixed effects
- GAM for selectivity/V-shaped nonlinearity

### Employment and Progression

```text
Base = S + B + A
Model A = Base + a_rate_pct
Model L = Base + grade_leniency_oof
Context = Model L + C24 + CG
```

핵심 비교:

```text
ΔR²_employment vs ΔR²_progression
ΔMAE_employment vs ΔMAE_progression
```

### OOF Residual

`grade_leniency_oof`는 A비율 우수성 판정이 아니라, 관측조건 대비 예상보다 높은/낮은 A비율이다.

```text
grade_leniency_oof = observed_a_rate - predicted_a_rate_oof
```

OOF 생성에는 `GroupKFold(group=school_uid)`를 사용하고, school ID·school fixed effect를 feature로 넣지 않는다.

### Interaction

사전 지정 상호작용은 5개로 제한한다.

```text
A × certificate context
A × firm_300plus context
A × public_nonprofit context
A × industry_hhi
A × professional_highskill context
```

다중검정은 Benjamini-Hochberg FDR로 보정한다.

## ML Benchmark

모델:

```text
Mean baseline
Ridge
Elastic Net
HistGradientBoosting
CatBoost or XGBoost 중 1개
```

평가:

```text
MAE, RMSE, R², Spearman
school bootstrap metric CI
```

해석 중심은 개별 feature 순위가 아니라 feature block incremental performance다.

## Panel Gate

Panel/Softmax는 다음을 모두 만족할 때만 실행한다.

```text
2023·2024·2025 동일 schema 존재
department_entity_id history bridge PASS
동일 학과 2개 이상 연도 관측
transition sample 충분
class별 최소 표본 충족
t+1 feature leakage 0
```

미충족 시:

```text
PANEL_STATUS = BLOCKED_PANEL_DATA
```

## Evaluation Gate

가설 판정은 다음 중 하나로 기록한다.

```text
Supported
Partially supported
Not supported
Inconclusive
Not testable with current data
```

결론문은 상관, 조건부 연관, 학교 내부 관계, 패널 시차 관계를 구분해서 작성한다. 준실험 근거 없이 “원인이다”, “영향을 미쳤다”, “전략이다”라고 쓰지 않는다.

## Deployment

Deployment는 서비스 배포가 아니라 기사·보고서·재현 가능한 분석자산으로의 배포다.

예상 산출물:

```text
p4_model_matrix_grade.parquet
p4_model_matrix_employment.parquet
p4_model_matrix_progression.parquet
department_grade_leniency_oof.parquet
department_employment_residual_oof.parquet
department_progression_residual_oof.parquet
p4_hypothesis_verdict_table.csv
p4_visual_exhibit_manifest.csv
```

## Safe Final Claim

최종 결과가 뒷받침할 때만 다음 수준으로 표현한다.

> 대학별 성적분포 차이는 단순한 학점 인플레이션 순위로 해석하기 어렵다. A비율은 입결과 전공구성, 학교·학과구조에 의해 상당 부분 설명되며, 설명되지 않는 차이는 취업시장보다 대학원 진학과 학업지속 경로에서 더 일관된 신호로 나타날 가능성이 있다.
