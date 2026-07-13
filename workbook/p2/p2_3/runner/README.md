# P2-G3 Final Package

이 패키지는 P2-G4 모델링 이전의 통일 데이터 계약과 두 로컬 에이전트 실행 지침을 포함한다.

## 파일

1. `P2_G3_FINAL_BLUEPRINT.md`
   - 전체 아키텍처, 실행 순서, acceptance gate, 로그 정책

2. `P2_G3_UNIFIED_DATA_SPEC.md`
   - 8개 canonical/model dataset의 grain, shape, 컬럼, dtype, 해석 규칙

3. `P2_G3_AGENT_PROMPT_LOCAL1.md`
   - `p3_1.ipynb` 담당 에이전트 실행 프롬프트

4. `P2_G3_AGENT_PROMPT_LOCAL2.md`
   - `p3_2.ipynb` 담당 에이전트 실행 프롬프트

## 핵심 확정

- 최종 학과 spine: 10,242행
- P4 grain: 2024 학교×캠퍼스×학과
- GOMS recent context: 2017~2019
- `major_group_7` bridge: Local 1 소유
- 자격증 직무 자료: 이번 라운드 직접 조인 금지
- P3에서 모델링·결측대체·스케일링 금지
- 모든 판단은 decision/transformation/merge 로그로 제출
