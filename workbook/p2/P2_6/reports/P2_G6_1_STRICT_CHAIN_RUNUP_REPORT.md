# P2-G6_1 Strict P3→P4 Run-up Report

## 한 줄 판정

P3-S OOF residual과 P4 strict confirmatory 결과는 생성 완료이며, P5 residual 재실행과 P6 residual topology 검토로 넘어갈 수 있다. 단, P2-Q/P3-Q는 feature approval 때문에 차단 상태이고, RAW_A와 OOF residual은 현재 선형 P4 설계에서 거의 같은 added-information 차원을 제공한다.

## Lineage

- strict D08 SHA256: `5f56e375fd1c0474a5e55652859ae007e2f45becd6d3350ee4c82e21fab8df9b`
- P2→P3 handoff SHA256: `2bbc7d64784b7b530d57bb6a2096d14cb11c5879f41a5208f9ff3b02f4bdddcb`
- P3 FULL residual SHA256: `d8decd39dca42ccd0dc194fa3813ba0036541098eea08ddfb64627f6fc6cb8cc`
- P4→P5 handoff SHA256: `601c352366a4cd45ac1575daf2836a99dff4711a3f76c8dd9be13b3418790c78`

## P3-S residual

- FULL OOF MAE: `10.473`
- FULL OOF R²: `0.056`
- FULL locked test R²: `-0.067`
- residual coverage: `7,592` / `7,592` rows
- raw A-residual corr: `0.927`
- residual/raw variance ratio: `0.944`

## P4 primary slopes

- RAW_A employment AME: `+0.616%p`
- RAW_A progression AME: `+1.726%p`
- OOF residual employment AME: `+0.636%p`
- OOF residual progression AME: `+1.658%p`

## Employment vs progression difference

- RAW_A D: `+1.110%p`
- OOF residual D: `+1.022%p`
- bootstrap residual D 95% CI: `[+0.292, +1.830]%p`

## Warnings

- 건강보험 취업 locked test improvement는 약하거나 없다.
- 대학원 진학 locked test improvement는 더 뚜렷하다.
- P4 bootstrap은 generated-regressor를 반복 생성하지만 속도를 위해 fixed encoder와 fast least-squares를 사용한 approximation이다.
- RAW_A와 OOF residual은 같은 P4 controls를 넣는 선형 설계에서 거의 등가이므로 residual만의 별도 효과처럼 과장하지 않는다.
- P2-Q/P3-Q는 feature approval 전까지 차단한다.

## P6 status

| status_key | status |
|---|---|
| P6_INPUT_STATUS | READY |
| P6_P3_RESIDUAL_HANDOFF_STATUS | READY |
| P6_P4_CONFIRMATORY_STATUS | READY_WITH_WARNINGS |
| P6_P5_RESIDUAL_RERUN_STATUS | READY |
| P6_RESIDUAL_TOPOLOGY_STATUS | READY_WITH_WARNINGS |
| P6_Q_BRANCH_STATUS | BLOCKED_FEATURE_CONTRACT |
| P6_OVERALL_STATUS | READY_WITH_WARNINGS |
