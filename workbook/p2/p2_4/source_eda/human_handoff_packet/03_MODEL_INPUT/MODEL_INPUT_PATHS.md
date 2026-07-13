# Model Input Paths

strict 삭제 정책 적용 후 모델링/EDA 기본 입력은 이 폴더의 파일 또는 원본 경로의 동일 파일이다.

- strict Parquet: `03_MODEL_INPUT/mart_department_model_base_2024_strict_drop.parquet`
- strict CSV: `03_MODEL_INPUT/mart_department_model_base_2024_strict_drop.csv`
- 원본 위치 Parquet: `workbook/p2/p2_4/source_eda/strict_clean_v1/mart_department_model_base_2024_strict_drop.parquet`
- 원본 위치 CSV: `workbook/p2/p2_4/source_eda/strict_clean_v1/mart_department_model_base_2024_strict_drop.csv`
- 타깃별 샘플 사용 여부: `02_EVIDENCE/strict_target_sample_counts.csv`와 원본 `strict_target_sample_membership.csv`를 기준으로 한다.

주의: 사람이 `human_required_decision_sheet.csv`에서 source rebuild/provide를 선택한 경우, strict 입력은 재생성해야 한다.
