# P5 Modeling Insight Notes

## AME 단위
모든 AME는 Grade Signal이 10%p 높아질 때 outcome이 몇 percentage point 달라지는지로 읽는다.

## 핵심 관찰
- 대학원 진학률 AME가 가장 큰 계열은 `ENG`이며 RAW_A +10%p당 `+4.57pp`다.
- 건강보험 취업률 AME가 가장 큰 계열은 `HUM`이며 RAW_A +10%p당 `+2.05pp`다.
- 취업률 쪽에서는 음의 AME가 관찰되는 계열이 있다: `MED`(-0.57pp), `NAT`(-0.48pp).
- `진학 AME - 취업 AME`가 가장 큰 계열은 `NAT`이며 `+4.15pp`다.
- 반대로 취업 쪽으로 더 기울어진 계열은 `EDU`이며 차이는 `-1.03pp`다.
- RAW_A와 WITHIN_MAJOR_A의 AME 차이는 최대 `4.248e-15`로, 현재 모델 grid에서는 사실상 같은 기울기를 낸다.

## 해석 제한
- 이 분석은 전공계열별 조건부 기울기 비교이며 인과효과 주장이 아니다.
- context rho heatmap은 N=7 전공계열 점의 기술 통계다. context 효과 검정으로 읽지 않는다.
- 모든 모델 cell에 sparse-level 진단이 붙어 있으므로 계열별 희소 범주와 신뢰구간을 함께 확인해야 한다.