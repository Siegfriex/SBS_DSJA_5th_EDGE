# h1_h2.ipynb 심화 시각화 설계서

## 목적

`h1_h2.ipynb`를 기사형 EDA 노트북으로 보강한다. 모든 시각화는 H1/H2/H3 중 하나의 질문에 답해야 하며, 장식용 그래프는 제외한다.

## 공통 원칙

- 데이터 기준: 2024년 정규 1·2학기, 대학 단위 주 분석 47개교.
- 순위 해석: 실제 입결점수가 아니라 `대학 서열 프록시`.
- 인코딩: CSV는 `utf-8-sig`.
- 한글 폰트: `NanumGothic`, `Noto Sans CJK KR`, `Malgun Gothic`, `AppleGothic` 순으로 자동 선택.
- 피처 성격: numerical, ordinal, nominal, binary, target, engineered signal을 명시.
- 구성비: A/B/C/D/F처럼 합계가 100%인 변수는 100% 누적막대로 시각화.
- 차원축소: PCA 입력에는 `a_rate_pct`와 `a_rate_residual_pctp`를 제외하고, 색상/라벨로만 사용.

## 시각화 블록

### V1. 피처 성격·결측 행렬

- 시각화 목적: 측정수준과 결측 구조 확인.
- 사용할 데이터: `university_analysis_table_2024.csv`.
- 필요 전처리: 변수별 역할, 측정수준, 결측 수, 고유값 수 산출.
- 코드 셀 설계: `enhanced_feature_dictionary_2024.csv`, `enhanced_missing_feature_matrix_2024.png`.
- 그래프 해석 포인트: `rank_2024_raw`는 숫자형처럼 보여도 의미상 ordinal.
- 자주 하는 오해: `credit_forfeit_bin`을 순수 연속형처럼 해석.
- 체크포인트 질문: 이 변수는 타겟인가, 설명변수인가, 품질 플래그인가?

### V2. 기술통계 행렬

- 시각화 목적: 중심, 산포, 왜도, 분위수를 한 표로 확인.
- 사용할 데이터: 대학 단위 핵심 수치형 변수.
- 필요 전처리: 모든 비율은 % 단위 유지.
- 코드 셀 설계: `enhanced_descriptive_metrics_2024.csv`, `enhanced_numeric_distribution_grid_2024.png`.
- 그래프 해석 포인트: 평균과 중앙값의 차이, IQR, 극단값.
- 자주 하는 오해: 평균만으로 대학 간 차이 설명.
- 체크포인트 질문: 평균과 중앙값이 같은 결론을 주는가?

### V3. 상관 행렬

- 시각화 목적: 선형관계와 단조관계를 구분.
- 사용할 데이터: 순위, 성적, 취업, 진학 변수.
- 필요 전처리: Spearman을 서열형 변수의 주 해석으로 사용.
- 코드 셀 설계: `enhanced_correlation_long_matrix_2024.csv`, `enhanced_spearman_correlation_heatmap_2024.png`.
- 그래프 해석 포인트: 순위 원점수는 숫자가 커질수록 하위권.
- 자주 하는 오해: 상관을 인과로 서술.
- 체크포인트 질문: 이 상관은 통제분석 이전의 관계인가?

### V4. 변수-타겟 추세선

- 시각화 목적: 변수와 타겟 간 방향과 산포를 동시에 확인.
- 사용할 데이터: 대학 단위 47개교.
- 필요 전처리: 패널별 결측 쌍별 제거.
- 코드 셀 설계: `enhanced_trendline_metrics_2024.csv`, `enhanced_target_trendline_panel_2024.png`.
- 그래프 해석 포인트: 추세선 기울기와 점 산포를 함께 본다.
- 자주 하는 오해: 산점도 한 장으로 정책효과 단정.
- 체크포인트 질문: H3의 A잔차-취업률 선은 충분히 기울어져 있는가?

### V5. 100% 성적구성 누적막대

- 시각화 목적: A/B/C/D/F 구성비 이동 확인.
- 사용할 데이터: `a_rate_pct`, `b_rate_pct`, `c_rate_pct`, `d_rate_pct`, `f_rate_pct`.
- 필요 전처리: 그룹 평균 후 100% 재정규화.
- 코드 셀 설계: `enhanced_grade_composition_100pct_by_group_2024.csv`, `enhanced_grade_100pct_stacked_bars_2024.png`.
- 그래프 해석 포인트: A비율 차이가 B/C/D/F 중 어디에서 이동하는지 본다.
- 자주 하는 오해: 막대 폭을 대학 수로 오해.
- 체크포인트 질문: 상위권 A비율 증가는 F 감소 때문인가, B/C 이동 때문인가?

### V6. 범주형-타겟 효과 행렬

- 시각화 목적: 범주형/순서형 피처가 타겟을 얼마나 가르는지 효과크기로 확인.
- 사용할 데이터: `rank_quartile`, `credit_forfeit_label`, `a_residual_group`.
- 필요 전처리: 그룹별 n>=2인 경우만 검정.
- 코드 셀 설계: `enhanced_categorical_target_effect_matrix_2024.csv`, `enhanced_categorical_target_effect_heatmap_2024.png`.
- 그래프 해석 포인트: p값과 eta squared를 같이 본다.
- 자주 하는 오해: 효과크기를 원인 효과로 해석.
- 체크포인트 질문: 학점포기제 효과크기는 순위 급간 효과크기보다 큰가?

### V7. 3D PCA

- 시각화 목적: 여러 변수를 함께 본 대학별 다변량 위치 확인.
- 사용할 데이터: 상위도, 정책, B~F 성적구성, 취업·진학성과.
- 필요 전처리: 결측 중앙값 대체, StandardScaler, PCA 3성분.
- 코드 셀 설계: `enhanced_pca_scores_2024.csv`, `enhanced_pca_loadings_2024.csv`, `enhanced_pca_explained_variance_2024.csv`, `enhanced_pca_3d_university_feature_space_2024.png`.
- 그래프 해석 포인트: 색상은 A비율이며 PCA 입력에는 A비율을 넣지 않는다.
- 자주 하는 오해: 가까운 점들을 같은 원인으로 묶음.
- 체크포인트 질문: PC축 해석을 loading 표와 함께 읽고 있는가?

### V9-A. 수치형·순서형 검정 행렬

- 시각화 목적: 실제 입결 확장표에서 수치형·순서형 피처와 A비율/잔차의 관계를 한 화면에서 비교한다.
- 사용할 데이터: `department_actual_selectivity_residuals_2024.csv`.
- 필요 전처리: 실제 입결 분석 표본만 필터링하고, Spearman/Kendall/OLS slope를 변수-타겟 쌍별로 산출한다.
- 코드 셀 설계: `deep_numeric_ordinal_target_tests_2024.csv`, `deep_v9_numeric_ordinal_test_heatmap_2024.png`.
- 그래프 해석 포인트: 별표는 p값, 숫자는 Spearman rho, 표는 OLS 기울기까지 함께 보여준다.
- 자주 하는 오해: 학기별 A비율처럼 타겟의 구성요소를 독립 설명변수처럼 해석.
- 체크포인트 질문: 실제 입결 변수의 단순 rho와 대학군집 회귀 계수가 같은 강도를 보이는가?

### V9-B. 범주형·이진형 효과 행렬

- 시각화 목적: 전공계열, 학점포기제, 입결 분위, 매핑 품질이 타겟을 얼마나 가르는지 효과크기로 비교한다.
- 사용할 데이터: 실제 입결 학과 표본.
- 필요 전처리: 이진형은 Mann-Whitney/Hedges g, 다집단은 Kruskal-Wallis/epsilon squared를 사용한다.
- 코드 셀 설계: `deep_categorical_binary_target_tests_2024.csv`, `deep_v10_categorical_binary_effect_matrix_2024.png`.
- 그래프 해석 포인트: p값보다 효과크기와 중앙값 차이, 표본수를 함께 본다.
- 자주 하는 오해: 명목형 그룹의 차이를 원인 효과로 단정.
- 체크포인트 질문: 학점포기제 효과크기는 전공계열이나 입결 분위 효과보다 큰가?

### V11. H1 실제 입결/대학 내 비교 대시보드

- 시각화 목적: 실제 입결과 A비율의 대학 간 패턴, 같은 대학 내부 패턴, 검정 요약을 동시에 제시한다.
- 사용할 데이터: 실제 입결 분석 표본과 H1 결과 요약.
- 필요 전처리: 입결 4분위, 대학 내 입결 편차, 대학 내 A비율 편차를 생성한다.
- 코드 셀 설계: `deep_h1_selectivity_quartile_summary_2024.csv`, `deep_v11_h1_actual_within_contrast_dashboard_2024.png`.
- 그래프 해석 포인트: 전체 산점도와 within-university 산점도의 기울기를 분리해서 본다.
- 자주 하는 오해: 대학 간 서열효과를 같은 대학 내부 학과효과로 해석.
- 체크포인트 질문: H1-Main과 H1-Within의 부호와 p값이 같은가?

### V12. H2/H3 정책·잔차·성과 대시보드

- 시각화 목적: 학점포기제 O/X, 실제 입결 기대 A잔차, 취업·진학성과의 관계를 한 화면에서 대조한다.
- 사용할 데이터: H2/H3 실제 입결 결과표와 대학별 잔차 요약.
- 필요 전처리: 학점포기제 O/X 라벨, 대학별 평균 잔차, 잔차 3분위 그룹을 생성한다.
- 코드 셀 설계: `deep_h3_residual_group_outcome_summary_2024.csv`, `deep_v12_h2_h3_policy_residual_outcome_dashboard_2024.png`.
- 그래프 해석 포인트: A잔차와 취업/진학률의 산점도는 탐색 신호이며 기사 결론의 보조 근거다.
- 자주 하는 오해: 잔차가 낮은 대학을 엄격한 대학으로 확정하거나 취업 성과 원인으로 단정.
- 체크포인트 질문: 취업성과와 진학성과가 같은 방향으로 움직이는가?

### V13. 구성비·매핑품질 대시보드

- 시각화 목적: 입결 분위별 A/B/C이하 성적 구성과 모집단위-학점학과 crosswalk 품질을 동시에 점검한다.
- 사용할 데이터: 실제 입결 학과 표본, crosswalk 전체표.
- 필요 전처리: A/B/C이하를 100%로 재정규화하고 F는 C이하의 부분비율 보조선으로 표시한다.
- 코드 셀 설계: `deep_grade_composition_by_selectivity_quartile_2024.csv`, `deep_v13_grade_composition_crosswalk_dashboard_2024.png`.
- 그래프 해석 포인트: A비율 차이가 B 또는 C이하 구성 이동인지, 매핑 제외 행이 얼마나 있는지 함께 본다.
- 자주 하는 오해: F 비율을 A/B/C이하 100% 막대와 별도 축임을 놓침.
- 체크포인트 질문: 주 분석에 포함된 1:1 매핑과 검토 대상 매핑이 명확히 분리되어 있는가?

### V16. 대학-학과 버블 벡터 3D 맵

- 시각화 목적: 하나의 버블에 대학명, 표준 학과, 입결순위, A비율 bin, 학과별 졸업자규모, 성과점수, 대학 내 편차 벡터를 동시에 담는다.
- 사용할 데이터: `department_actual_selectivity_residuals_2024.csv`, `p2_취업률_데이터.csv`.
- 필요 전처리: 학과별 졸업자/건보취업/창업프리랜서/진학자를 대학-학과 단위로 집계하고, 실제 입결 표본에 병합한다.
- 코드 셀 설계: `v16_university_department_bubble_vector_dataset_2024.csv`, `deep_v16_university_department_bubble_vector_3d_2024.png`, `deep_v16_university_department_bubble_vector_xy_labeled_2024.png`, `deep_v16_university_department_bubble_vector_interactive_2024.html`.
- 그래프 해석 포인트: 색상 hue는 대학명, 같은 대학 내부 채도/명도는 학과 bin, 크기는 졸업자규모 0~1 정규화, x/y/z는 각각 입결순위/A비율/성과 정규화다.
- 자주 하는 오해: x축을 원 백분위 연속값으로 읽거나, y축을 5% bin이 아닌 연속 A비율로 읽음.
- 체크포인트 질문: 같은 대학 안에서 입결 편차와 A비율 편차가 같은 방향인가, 반대 방향인가?

### V17. 읽히는 대학-학과 버블 지도

- 시각화 목적: V16의 과밀한 3D·벡터 표현을 본문용으로 분해해, 대학 라벨과 주요 학과 방향성을 실제로 읽을 수 있게 만든다.
- 사용할 데이터: `v16_university_department_bubble_vector_dataset_2024.csv`.
- 필요 전처리: 대학별 숫자 인덱스, deterministic jitter, bubble size sqrt 스케일링, 대학 centroid 라벨, 짧은 벡터 glyph 선별, 상위 대학 small multiples를 만든다.
- 코드 셀 설계: `v17_readable_bubble_plot_dataset_2024.csv`, `v17_short_vector_glyph_dataset_2024.csv`, `deep_v17a_readable_overall_bubble_map_2024.png`, `deep_v17b_short_vector_glyph_map_2024.png`, `deep_v17c_university_small_multiples_2024.png`, `deep_v17d_clean_3d_overview_2024.png`.
- 그래프 해석 포인트: V17-A는 전체 분포와 대학 위치, V17-B는 대학 내 x-y 편차 방향, V17-C는 대학별 내부 구조, V17-D는 z축 성과를 포함한 보조 개관으로 읽는다.
- 자주 하는 오해: V17의 짧은 벡터를 실제 이동량 전체로 해석하거나, 대학별 색상을 정밀한 순위 정보로 해석.
- 체크포인트 질문: 본문 핵심 그림은 V17-C 또는 V17-A로 두고, V16/V17-D는 부록·탐색용으로 제한했는가?
