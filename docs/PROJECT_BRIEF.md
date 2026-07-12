# Project Brief

## Problem

대학 단위 순위가 아니라 **대학-학과 단위**의 2024년 분석 mart를 만들었다. 대상 grain은 `학교 x 캠퍼스 x 학과/outcome row`이며, P4 단계에서 학점분포, 입결 proxy, 취업/진학 성과를 설명하는 모델링 base로 쓰는 것이 목적이다.

## What Was Built

- D01: KEDI 기반 학과 구조 master
- D02: 2024 outcome spine, 10,242행 고정
- D03: outcome spine에 구조 bridge와 major_group_7을 붙인 core
- D06/D07: GOMS 전공계열별 노동시장 context
- D08: P4 모델링 후보 mart, `10,242 x 151`

## Main Engineering Choices

- D02 spine은 삭제하지 않는다. unmatched row도 보존하고 sample mask에서 판단한다.
- 후보가 2개 이상인 bridge는 자동확정하지 않는다.
- 캠퍼스 충돌 자동확정은 금지한다.
- GOMS context는 학과의 실제 취업성과가 아니라 계열 context로만 사용한다.
- P3 단계에서는 imputation, scaling, encoding, modeling을 하지 않는다.
