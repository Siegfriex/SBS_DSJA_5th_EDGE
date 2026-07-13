# h1_h2.ipynb 심화 시각화 체크리스트

## 실행 검증

- [x] `h1_h2.ipynb` 실제 Jupyter 커널 실행 완료.
- [x] 노트북 JSON parse 통과.
- [x] `nbformat.validate()` 통과.
- [x] 코드셀 AST parse 통과.
- [x] 저장된 error output 없음.
- [x] 코드셀 36개 모두 실행됨.

## 산출물 검증

- [x] 피처 성격 행렬: `enhanced_feature_dictionary_2024.csv`
- [x] 결측 행렬 그림: `enhanced_missing_feature_matrix_2024.png`
- [x] 기술통계 행렬: `enhanced_descriptive_metrics_2024.csv`
- [x] 분포 grid: `enhanced_numeric_distribution_grid_2024.png`
- [x] 상관 long matrix: `enhanced_correlation_long_matrix_2024.csv`
- [x] Spearman heatmap: `enhanced_spearman_correlation_heatmap_2024.png`
- [x] 추세선 metrics: `enhanced_trendline_metrics_2024.csv`
- [x] 추세선 panel: `enhanced_target_trendline_panel_2024.png`
- [x] 100% 구성비 표: `enhanced_grade_composition_100pct_by_group_2024.csv`
- [x] 100% 누적막대: `enhanced_grade_100pct_stacked_bars_2024.png`
- [x] 범주형 효과 행렬: `enhanced_categorical_target_effect_matrix_2024.csv`
- [x] 범주형 효과 heatmap: `enhanced_categorical_target_effect_heatmap_2024.png`
- [x] PCA scores/loadings/explained variance CSV
- [x] 3D PCA 그림: `enhanced_pca_3d_university_feature_space_2024.png`
- [x] 심화 시각화 매니페스트: `enhanced_visual_manifest_2024.csv`

## 해석 검수

- [x] 순위를 실제 입결점수로 부르지 않음.
- [x] H1은 본문 핵심 증거로 배치.
- [x] H2는 약한 근거로 제한.
- [x] H3 취업성과 주장은 약하게 제한.
- [x] 진학률 보조 신호는 탐색 결과로만 표현.
- [x] PCA는 보조 구조 요약으로만 표현.
- [x] 100% 비율 변수는 누적막대로 표현.
- [x] 범주형/순서형 변수는 효과크기와 비모수 검정을 함께 제시.

## V9~V13 고밀도 비교 대조 산출물

- [x] 색상 인덱스 사전: `data/deep_contrast_2024/deep_color_index_registry_2024.csv`
- [x] 변수유형·검정 사전: `data/deep_contrast_2024/deep_feature_test_dictionary_2024.csv`
- [x] 수치형·순서형 검정표: `data/deep_contrast_2024/deep_numeric_ordinal_target_tests_2024.csv`
- [x] 수치형·순서형 heatmap: `figures/deep_contrast_2024/deep_v9_numeric_ordinal_test_heatmap_2024.png`
- [x] 범주형·이진형 검정표: `data/deep_contrast_2024/deep_categorical_binary_target_tests_2024.csv`
- [x] 범주형·이진형 효과 heatmap: `figures/deep_contrast_2024/deep_v10_categorical_binary_effect_matrix_2024.png`
- [x] H1 실제 입결/대학 내 비교 대시보드: `figures/deep_contrast_2024/deep_v11_h1_actual_within_contrast_dashboard_2024.png`
- [x] H2/H3 정책·잔차·성과 대시보드: `figures/deep_contrast_2024/deep_v12_h2_h3_policy_residual_outcome_dashboard_2024.png`
- [x] 구성비·매핑품질 대시보드: `figures/deep_contrast_2024/deep_v13_grade_composition_crosswalk_dashboard_2024.png`
- [x] 고밀도 시각화 매니페스트: `data/deep_contrast_2024/deep_visual_manifest_2024.csv`

## V9~V13 해석 검수

- [x] 수치형/순서형은 Spearman·Kendall·OLS slope를 함께 제시.
- [x] 범주형/이진형은 Mann-Whitney 또는 Kruskal-Wallis와 효과크기를 함께 제시.
- [x] `major_group`, `credit_forfeit`, `selectivity_quartile`, `mapping_type` 색상 인덱스를 고정.
- [x] 산점도·누적막대·검정표가 같은 블록 안에서 대조되도록 구성.
- [x] `Tier A+B` 표본 한계를 별도 체크포인트로 명시.

## V16 대학-학과 버블 벡터 산출물

- [x] V16 모델 CSV: `data/deep_contrast_2024/v16_university_department_bubble_vector_dataset_2024.csv`
- [x] 대학 centroid 라벨 CSV: `data/deep_contrast_2024/v16_university_label_centroids_2024.csv`
- [x] V16 요약 CSV: `data/deep_contrast_2024/v16_bubble_vector_summary_2024.csv`
- [x] V16 static 3D PNG: `figures/deep_contrast_2024/deep_v16_university_department_bubble_vector_3d_2024.png`
- [x] V16 2D 라벨 투영 PNG: `figures/deep_contrast_2024/deep_v16_university_department_bubble_vector_xy_labeled_2024.png`
- [x] V16 interactive HTML: `figures/deep_contrast_2024/deep_v16_university_department_bubble_vector_interactive_2024.html`
- [x] V16 산출물 매니페스트: `data/deep_contrast_2024/v16_visual_manifest_2024.csv`

## V16 인코딩·스케일 검수

- [x] element는 `대학명 × dept_canonical_id × 학과명` 조합으로 생성.
- [x] 색상 hue는 대학명 nominal class로 매핑.
- [x] 같은 대학 내부 학과는 5개 shade bin으로 명도·채도를 분리.
- [x] bubble size는 학과별 졸업자규모를 0~1 min-max 정규화해 적용.
- [x] x축은 실제 70% cut 백분위 기반 52개 입결순위 bin을 0~1로 정규화.
- [x] y축은 A비율을 5% 단위 bin으로 만든 뒤 0~1로 정규화.
- [x] z축은 건보취업률 + 창업/프리랜서율 + 진학률 합산 성과를 0~1로 정규화.
- [x] 꼬리 벡터는 대학 내부 평균점 대비 x-y 편차 방향과 signed squared z-score를 기록.
- [x] 노트북에는 static 3D, 2D label projection, interactive output이 모두 저장됨.

## V17 읽히는 버블 지도 산출물

- [x] V17 전체 버블 데이터: `data/deep_contrast_2024/v17_readable_bubble_plot_dataset_2024.csv`
- [x] V17 짧은 벡터 glyph 데이터: `data/deep_contrast_2024/v17_short_vector_glyph_dataset_2024.csv`
- [x] V17 대학 색상·숫자 인덱스: `data/deep_contrast_2024/v17_university_color_label_index_2024.csv`
- [x] V17 small multiple 대학 선정표: `data/deep_contrast_2024/v17_small_multiple_university_selection_2024.csv`
- [x] V17 가독성 요약표: `data/deep_contrast_2024/v17_readability_summary_2024.csv`
- [x] V17 산출물 매니페스트: `data/deep_contrast_2024/v17_visual_manifest_2024.csv`
- [x] V17-A 전체 버블 지도: `figures/deep_contrast_2024/deep_v17a_readable_overall_bubble_map_2024.png`
- [x] V17-B 짧은 벡터 glyph 지도: `figures/deep_contrast_2024/deep_v17b_short_vector_glyph_map_2024.png`
- [x] V17-C 대학별 small multiples: `figures/deep_contrast_2024/deep_v17c_university_small_multiples_2024.png`
- [x] V17-D 깨끗한 3D 보조 개관: `figures/deep_contrast_2024/deep_v17d_clean_3d_overview_2024.png`

## V17 가독성 검수

- [x] V16의 긴 vector tail은 본문용 그림에서 제거하거나 짧은 glyph로 축약.
- [x] 전체 지도는 대학명 직접 라벨 대신 숫자 centroid와 우측 색상 인덱스를 사용.
- [x] 학과명 라벨은 대표 벡터 학과로 제한해 과밀도를 낮춤.
- [x] V17-C small multiples를 본문 핵심 후보로 두고, V17-A는 전체 분포, V17-B는 방향성, V17-D는 부록용으로 분리.
- [x] 모든 V17 PNG가 노트북 output 안에 inline으로 저장됨.
