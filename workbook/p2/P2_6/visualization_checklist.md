# P2-G6_1 Visualization Checklist

## Notebook Stability

- [x] 외부 다운로드 없음.
- [x] P3/P4 strict 산출물만 읽음.
- [x] 새 모델 재적합 없음.
- [x] `OUT_ROOT`를 `workbook/p2/P2_6`로 고정.
- [x] 추가 figure는 `workbook/p2/P2_6/figures`에 저장.
- [x] 시각화 manifest와 reading guide를 별도 저장.

## Required Visual Blocks

- [x] V00 helper: figure manifest, 관찰/원인/제한/결론 scaffold.
- [x] V01 status/lineage: READY/WARNING/BLOCKED와 hash chain.
- [x] V02 P3 residual: X/y식 observed/expected/residual 구조와 fold metric.
- [x] V03 P4 sample: train/validation/test split과 outcome availability.
- [x] V04 P4 AME: fractional logit primary AME와 bootstrap CI.
- [x] V05 D: employment vs progression 차이와 bootstrap CI.
- [x] V06 locked test: base 대비 signal improvement.
- [x] V07 equivalence: RAW_A/residual delta와 scatter.
- [x] V08 P6 dashboard: 결과론적 decision matrix.
- [x] V09 manifest: 후속 에이전트용 artifact list.

## Interpretation Guardrails

- [x] P3 residual을 인과적 shock으로 쓰지 말라는 경고 포함.
- [x] RAW_A와 OOF residual 동등성 경고 포함.
- [x] slope 유의성과 locked-test improvement를 분리.
- [x] 취업률보다 대학원 진학률과 더 정렬된다는 제한적 결론으로 표현.
- [x] P2-Q/P3-Q branch 차단 상태 유지.