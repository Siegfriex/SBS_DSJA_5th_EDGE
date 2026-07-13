# P5 v2 Strict Modeling Visual Insight Notes

## AME unit
All AME values are outcome percentage-point changes for RAW_A +10 percentage points.

## Key observations
- Grad school progression AME is largest in `ENG`: `+4.57pp`.
- Health employment AME is largest in `HUM`: `+2.05pp`.
- Negative employment AME appears for: `MED`(-0.57pp), `NAT`(-0.48pp), `ART`(-0.43pp).
- Top 3 progression AME: `ENG`(+4.57pp), `NAT`(+3.67pp), `HUM`(+1.37pp).
- Top 3 employment AME: `HUM`(+2.05pp), `ENG`(+1.93pp), `EDU`(+1.56pp).
- Progression-minus-employment contrast is largest in `NAT`: `+4.15pp`.
- The strongest employment-leaning contrast is `EDU`: `-1.03pp`.
- Structure-selectivity sign disagreement appears in: `ART`/GRAD_SCHOOL_PROGRESSION, `MED`/GRAD_SCHOOL_PROGRESSION, `NAT`/HEALTH_EMPLOYMENT.
- Strict-vs-v1 primary structure sensitivity has max absolute AME change `8.2e-15pp`, sign-change cells `0`, and CI-overlap cells `14/14`.

## 발견한 모델링 패턴

1. `RAW_A`는 strict 모델에서 진학률과 취업률에 같은 방식으로 작동하지 않는다. ENG/NAT는 진학률 쪽 AME가 특히 크고, HUM/ENG/EDU는 취업률 쪽 AME가 크다.
2. `MED`, `NAT`, `ART`의 취업률 AME는 음수지만 CI가 0을 가로지르므로 방향을 강하게 단정하지 않는다.
3. `NAT`는 진학 AME와 취업 AME의 차이가 가장 커서, grade signal이 취업보다 진학 쪽 outcome과 더 크게 연결되는 계열로 읽힌다.
4. strict-vs-v1 민감도에서 부호 변화가 0이고 모든 CI가 overlap하므로, strict-clean 계약 적용이 주요 계열별 순위를 뒤집지 않았다.

## Interpretation scaffold

**관찰:** strict-clean 기준에서도 ENG/NAT는 대학원 진학 AME가 크고, HUM/ENG/EDU는 취업 AME가 양의 방향으로 크다.

**원인:** 이 보드는 같은 strict 입력 계약, 같은 primary STRUCTURE/B_CORE 모형, 같은 RAW_A +10pp 단위로 outcome별 조건부 slope를 비교한다.

**제한:** fractional logit AME는 관측 데이터의 조건부 관계를 요약한다. 개인 단위 인과효과, 대학/학과 성과 단정, context 효과 검정으로 해석하지 않는다.

**결론:** strict-clean 재실행 후 v1 대비 부호 변화가 없고 CI가 모두 overlap하므로, 현재 인사이트의 핵심은 strict 계약 아래에서도 계열별 방향 차이가 유지된다는 점이다.

## Interpretation guardrails
- This is a major7-level conditional slope comparison, not a causal effect estimate.
- Context rho is descriptive only because it uses seven major-level points.
- RAW_A is the only strict signal branch; WITHIN_MAJOR_A is intentionally removed as a slope-duplicate branch in this strict notebook.