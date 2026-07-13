# H1-H7 원자료 및 의존상속관계 감사

작성 기준: 현재 체크아웃의 `workbook/p2/p2_2` 파일과 `val_outputs` 산출물.

## 최종 검증 판정

`h1_h2_measurement_validation.ipynb`는 실행 자체는 성공했고 `val_outputs` 산출물도 생성했다. 그러나 최종 판정은 `READY`가 아니라 `NOT_READY`다.

| 항목 | 현재 값 | 해석 |
| --- | ---: | --- |
| validation_run_id | `VAL_20260712_151256` | 현재 검증 산출물 기준 실행 ID |
| 실행 성공 여부 | `success` | 노트북 실행과 CSV export는 성공 |
| Gate0_input_freeze | `PASS` | 입력 파일 탐색, 선택, baseline freeze 통과 |
| Gate1_metric_definition | `NOT_READY` | 70% cut 지표 정의 수동 검토 필요 |
| Gate2_alias_mapping | `NOT_READY` | 모집단위-학과 alias 매핑 수동 검토 필요 |
| Gate3_coverage | `NOT_READY` | Gold/Silver 커버리지 표본 없음 |
| Gate4_official_sample_expansion | `NOT_READY` | 신규 공식자료 추가 수집 없음 |
| Gate5_cohort_alignment | `NOT_READY` | 2018-2021 과거 입결 미확보 |
| Gate6_validated_sample_build | `NOT_READY` | 검증 표본 build 결과 비어 있음 |
| Gate7_rerun | `NOT_READY` | 검증 표본 기반 재추정 차단 |
| Final_analysis_readiness | `NOT_READY` | 실제 입결 기반 본분석으로 승격 불가 |

따라서 이 검증 노트북은 "타당성 점검을 했다"는 말은 맞지만, "실제 입결 기반 분석이 최종 검증되어 본문 주증거로 쓸 수 있다"는 뜻은 아니다. 현재 역할은 입력 동결, 오류 탐지, 수동 검토 queue 생성, 그리고 본분석 차단 근거 기록이다.

핵심 수치:

| 구분 | 값 |
| --- | ---: |
| 기존 Tier A 수 | 104 |
| 검증 후 Tier A 수 | 2415 |
| 환산점수 오분류 수 | 43 |
| unknown numeric 수 | 0 |
| metric 수동검토 queue | 354 |
| 전체 alias pair | 1755 |
| alias 자동통과 | 167 |
| alias 미확정 | 1859 |
| Gold 대학 수 | 0 |
| Silver 대학 수 | 0 |
| 제외 대학 수 | 37 |
| 과거 입결 확보 대학 수 | 0 |
| cohort alignment PASS 수 | 0 |

## 브리핑 노트북의 직접 입력

`h1_h7_intelligence_briefing.ipynb` 자체는 아래 3개 요약 CSV만 읽는다.

| 직접 입력 | 행 | 역할 |
| --- | ---: | --- |
| `data/h1_h7_intelligence/h1_h7_hypothesis_matrix.csv` | 7 | H1-H7 판정표 |
| `data/h1_h7_intelligence/h1_h7_metric_summary.csv` | 23 | 핵심 수치 요약 |
| `data/h1_h7_intelligence/h1_h7_visual_manifest.csv` | 6 | 그림 경로와 해석 |

이 3개 파일은 `scripts/build_h1_h7_intelligence_briefing.py`가 만든 2차 산출물이다. 실제 원자료 계보는 아래 직접/상속 입력으로 봐야 한다.

## H1-H7 빌더의 직접 원천

| 파일 | 행/시트 | 빌더 내부 이름 | 사용 위치 | 계보상 성격 |
| --- | ---: | --- | --- | --- |
| `대학별_학점분포_전공교양합산_ 최종.xlsx` / `학점분포(전공+교양)` | 54행 | `grade54` | H1 54개 대학, H2 병합, H7 54개 대학, 헤드라인 수치 | 2025년 54개 대학 전공+교양 집계 직접 입력 |
| `학점포기제도현황.xlsx` / `종합` | 54행 | `policy54` | H2 O/X 평균 차이 | 학점포기제 직접 입력 |
| `data/analysis_csv/university_analysis_table_2024.csv` | 47행 | `u47` | H1 47개 대학 보조, H6 잔차, H7 47개 대학 보조 | `h1_h2.ipynb` 1차 가공표 |
| `data/analysis_csv/department_analysis_table_2024.csv` | 10865행 | `dept` | H3-H5의 246개교 A비율 재집계 기반 | `h1_h2.ipynb` 1차 가공표 |
| `data/analysis_csv/employment_university_2024.csv` | 243행 | `emp` | H3/H4 취업 성과 | 취업 원자료 대학 단위 집계표 |
| `data/analysis_csv/advancement_university_2024.csv` | 243행 | `adv` | H5 진학 성과 | 진학 원자료 대학 단위 집계표 |
| `p2_취업률_데이터.csv` | 9951행 | `raw_emp` | 지역/설립구분 control 생성 | 취업 원자료 |
| `P2__전체대학학점비율.csv` | 31743행 | `raw_grade` | report 원자료 규모 설명, 상속 원천 | 성적분포 원자료 |
| `data/actual_admission_2024/department_h1_h2_actual_admission_2024.csv` | 1216행 | `actual_model` | 실제 입결 표본 규모/status만 표시 | 실제 입결 탐색 산출물, 현재 본분석 주증거 아님 |
| `val_outputs/38_final_validation_summary.csv` | 43행 | `val_summary` | validation readiness 문구 | 검증 노트북 최종 요약 |
| `val_outputs/35_validation_gate_summary.csv` | 9행 | `val_gate` | gate 판정 확인 | 검증 노트북 gate 요약 |

## 1차 가공표의 상속관계

`h1_h2.ipynb`는 아래 원자료를 읽고 `data/analysis_csv`를 만든다.

| 원자료 | 행/시트 | 상속 산출물 | 사용 가설 |
| --- | ---: | --- | --- |
| `P2__전체대학학점비율.csv` | 31743행 | `department_grade_target_2024_regular_term_mean.csv`, `department_term_grade_2024_regular_terms.csv`, `department_analysis_table_2024.csv`, `university_analysis_table_2024.csv` | H1, H3-H7 |
| `P2_학과별_A비율_대학아님.csv` | 4644행 | 학과명/학과 A비율 참조, 실제 입결 crosswalk 보조 | 실제 입결 매핑 검토 |
| `대학순위_상위54개_3개년.xlsx` / `2024_대학순위` | 52행 | `university_analysis_table_2024.csv`, `department_analysis_table_2024.csv`의 `rank_2024_raw`, `prestige_score` | H1, H6, H7 |
| `학점포기제도현황.xlsx` / `종합` | 54행 | `university_analysis_table_2024.csv`, `department_analysis_table_2024.csv`의 `credit_forfeit_*` | H2 |
| `p2_취업률_데이터.csv` | 9951행 | `employment_university_2024.csv`, `university_analysis_table_2024.csv`의 취업 지표 | H3, H4, H6 |
| `p2_상위대학_진학률.csv` | 9951행 | `advancement_university_2024.csv`, `university_analysis_table_2024.csv`의 진학 지표 | H5, H6 |

## 실제 입결 검증 계보

실제 입결 계열은 별도 계보이며, 현재는 탐색/검증용으로만 유지한다.

| 원천/가공표 | 행 | 상속 대상 | 현재 판정 |
| --- | ---: | --- | --- |
| `data/crawl_2024_admission/00_crawl_seed_university_2024.csv` | 52 | 크롤링 대상 대학 seed | 입력 freeze 통과 |
| `data/crawl_2024_admission/01_crawl_source_registry.csv` | 51 | ADIGA source URL, raw HTML registry | 입력 freeze 통과 |
| `data/crawl_2024_admission/02_admission_result_raw_2024.csv` | 3096 | 원 입결 row, `raw_percentile_70cut` 검토 | metric 검토 필요 |
| `data/actual_admission_2024/recruitment_grade_department_crosswalk_2024.csv` | 2026 | 모집단위-학과 crosswalk | alias 미확정 1859행 |
| `data/actual_admission_2024/department_h1_h2_actual_admission_2024.csv` | 1216 | 실제 입결+성적분포 결합 후보 | baseline reference only |
| `val_outputs/20_official_admission_2024_validated_long.csv` | 2415 | 공식 평균 백분위로 자동 분류된 입결 행 | 지표 행은 늘었지만 매핑/커버리지 gate 미통과 |
| `val_outputs/12_crosswalk_validated.csv` | 167 | exact 1:1 auto-pass mapping | 표본 부족 |
| `val_outputs/27_validated_h1_department_sample.csv` | 0 | 검증 H1 표본 | 비어 있음 |
| `val_outputs/28_validated_cohort_outcome_sample.csv` | 0 | H5/H6 cohort outcome 표본 | 비어 있음 |
| `val_outputs/29_validated_h7_nonlinear_sample.csv` | 0 | 검증 H7 표본 | 비어 있음 |

## 가설별 의존상속관계

### H1. 순위/입결라인 프록시와 A비율

1. 본문 54개 대학 버전:
   `대학별_학점분포_전공교양합산_ 최종.xlsx` -> `grade54` -> Pearson/Spearman/Kendall -> `h1_h7_metric_summary.csv`, `h1_h7_hypothesis_matrix.csv`, `h1_h7_rank_a_curve.png`

2. 2024 47개 대학 보조 버전:
   `P2__전체대학학점비율.csv` + `대학순위_상위54개_3개년.xlsx` -> `university_analysis_table_2024.csv` -> H1 보조 상관

3. 실제 입결 버전:
   ADIGA raw + crosswalk + 성적분포 -> `department_h1_h2_actual_admission_2024.csv` -> validation gate 미통과 -> 본문 주증거 제외

### H2. 학점포기제와 A비율

`대학별_학점분포_전공교양합산_ 최종.xlsx` + `학점포기제도현황.xlsx` -> `policy54` -> O/X 평균 차이, Welch test -> `h2_credit_forfeit_a_rate.png`

보조 계보:
`학점포기제도현황.xlsx` -> `university_analysis_table_2024.csv` / `department_analysis_table_2024.csv`의 `credit_forfeit_*`

### H3. A비율과 공식취업률

`P2__전체대학학점비율.csv` -> `department_analysis_table_2024.csv` -> 대학별 `a_rate_weighted_pct`

`p2_취업률_데이터.csv` -> `employment_university_2024.csv` -> `official_employment_rate_pct`

두 축 병합 -> Spearman/부분상관 -> `h3_h4_h5_outcome_correlations.csv`, `h3_h4_h5_outcome_correlation_bar.png`, `h3_vs_h5_scatter_compare.png`

### H4. A비율과 취업의 질 proxy

`P2__전체대학학점비율.csv` -> `department_analysis_table_2024.csv` -> 대학별 A비율

`p2_취업률_데이터.csv` -> `employment_university_2024.csv` -> `health_employment_rate_pct`, `retention_4th_pct`, `startup_freelance_rate_pct`

두 축 병합 -> 대체지표 상관 -> `h3_h4_h5_outcome_correlations.csv`

주의: 공기업/사기업 직접 원자료는 현재 없음.

### H5. A비율과 진학/대학원 진학률

`P2__전체대학학점비율.csv` -> `department_analysis_table_2024.csv` -> 대학별 A비율

`p2_상위대학_진학률.csv` -> `advancement_university_2024.csv` -> `overall_advancement_rate_pct`, `graduate_school_rate_pct`

두 축 병합 -> Spearman/부분상관 -> `h3_h4_h5_outcome_correlations.csv`, `h3_vs_h5_scatter_compare.png`

주의: 2024 입결과 2024 취업/진학 성과의 cohort alignment는 `Gate5 NOT_READY`이므로 실제 입결 기반 H5로 해석하지 않는다.

### H6. 서열 대비 A비율 잔차와 성과

`P2__전체대학학점비율.csv` + `대학순위_상위54개_3개년.xlsx` + 취업/진학 집계 -> `university_analysis_table_2024.csv`

`university_analysis_table_2024.csv`의 `a_rate_expected_by_rank_pct`, `a_rate_residual_pctp`, 성과 지표 -> 잔차 후보 대학 목록 -> `h6_low_residual_universities.csv`, `h6_high_residual_universities.csv`, `h6_residual_university_examples.png`

주의: 전략 가설은 통계 결론이 아니라 후속 취재 후보로만 유지.

### H7. 순위 구간별 곡률/V자 가능성

1. 54개 대학:
   `대학별_학점분포_전공교양합산_ 최종.xlsx` -> `grade54` -> 이차항 회귀, 4분위 평균 -> `h7_rank_quartile_a_rate.csv`, `h7_rank_quartile_a_rate.png`

2. 47개 대학:
   `university_analysis_table_2024.csv` -> 2024 보조 이차항 진단

3. 실제 입결 비선형:
   `val_outputs/29_validated_h7_nonlinear_sample.csv`가 0행이라 현재 미실행.

## 최종 사용 가능성 구분

| 데이터 계열 | 현재 사용 등급 | 기사/본문에서의 안전한 사용 |
| --- | --- | --- |
| 54개 대학 전공+교양 성적분포 + 학점포기제 | 주증거 가능 | H1/H2/H7의 54개 대학 버전 |
| 2024 대학알리미 성적분포 + 취업/진학 집계 | 주증거 가능, 단 연관성 해석 | H3/H4/H5, H6 후보 |
| 대학순위 2024 프록시 | 보조 설명변수 | "입결라인"이 아니라 "대학 서열 프록시"로 표기 |
| ADIGA 2024 실제 입결 크롤링 | 탐색/검증용 | 본문 주증거 금지. `Validation Gate NOT_READY` 병기 필요 |
| 검증 노트북 `val_outputs` | 품질관리 근거 | "현재 왜 실제 입결을 본분석으로 쓰지 않는지"의 근거 |

