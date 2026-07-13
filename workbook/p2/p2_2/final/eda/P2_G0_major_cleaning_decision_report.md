# P2_G0 클리닝/샘플 결정 리포트

## 확정 결정

- 메인 분석 테이블: `df_integrated_major`
- 분석 단위: `고등교육기관 x 계열`, 7행
- 1차 타겟: `평균소득만원`
- 보조 타겟: `중위소득만원`
- 급여구간 비율: 타겟 설명 피처가 아니라 타겟 진단/별도 타겟 후보
- 직무별 자격증: 현재 통합 샘플에 조인하지 않음

## 클리닝 상태 판단

현재 `df_integrated_major` 기준 데이터 클리닝은 조건부 완료로 본다.

완료된 점검:

- 원자료 주석/설명 행 제거
- 텍스트 키 정리와 숫자형 변환
- 기업유형, 초임급여 구간, 산업유형, 직무별 자격증 경쟁형 구성 합계 검산
- 통합 샘플 merge 후 pandas NULL 없음 확인
- 원천 코드형 `산업분류=결측값`, `직무분류=미상`을 pandas NULL과 분리

남겨야 할 제한:

- 산업분류 `결측값`은 삭제하지 않고 미상 비율로 주석 처리한다.
- 특히 교육 계열은 산업분류 미상 비율이 높아 산업 믹스 해석에 제한이 있다.
- 직무별 자격증은 계열/산업과 직접 조인하지 않는다.
- `직무분류 -> 산업분류` 매핑표는 후보표이며 수동 검토 전에는 분석 피처로 사용하지 않는다.

## 산출물

- 노트북: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/eda/P2_G0_계열별 기업, 산업, 자격증, 초임급여, 직무별.IPYNB`
- 직무-산업 후보 매핑표: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/eda/tables/23_cert_job_to_industry_mapping_candidates.csv`
- 리포트: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_2/final/eda/P2_G0_major_cleaning_decision_report.md`
