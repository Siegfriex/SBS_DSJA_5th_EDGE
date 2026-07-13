# D01 Grain Explanation

D01의 한 행은 2024년 × 학교표준명 × 캠퍼스(본분교/제N캠퍼스) × 주야구분 × 학위과정 × KEDI 학과코드의 구조자료 관측치이다.

## 실제 행수 해석
- raw Excel sheet `학교별 학과별 주요 현황`에서 빈 행과 대계열 결측 행을 제거하면 **34,969행**이다.
- 기존 15,727행 CSV는 이 raw Excel을 모두 담은 원천이 아니라, 주야구분·학교상태 등 일부 축이 빠진 prefiltered 중간 산출물이다.
- D01 v2는 15,727행을 복제해 늘린 것이 아니라, raw Excel의 34,969행을 다시 읽어 `주야구분`, `학교상태`, `학위과정`, `본분교` 축을 보존한 구조 master다.

## 확정 grain
- key: `analysis_year|school_name_std|campus_name_std|day_evening_raw|degree_course|kedi_dept_code`
- canonical grain duplicate rows: `0`
- lineage missing rows: `0`

## Count conservation
- raw Excel 대비 D01 count 합계 불일치 metric 수: `0`
- 15,727행 CSV 대비 차이는 범위 복구(scope restoration)로 별도 기록했다.
