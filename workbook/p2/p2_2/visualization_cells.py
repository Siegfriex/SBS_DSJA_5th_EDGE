"""Visualization cell manifest for workbook/p2/p2_2/h1_h2.ipynb.

The executable notebook cells have already been appended to h1_h2.ipynb.
This file documents the expected generated artifacts and can be used as a
lightweight checklist by notebook-generation or review scripts.
"""

from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


VISUAL_BLOCKS = [
    {
        "id": "V1",
        "title": "피처 성격·결측 행렬",
        "csv": "data/analysis_csv/enhanced_feature_dictionary_2024.csv",
        "figure": "figures/enhanced_missing_feature_matrix_2024.png",
        "question": "어떤 변수는 수치형이고 어떤 변수는 범주형인가?",
    },
    {
        "id": "V2",
        "title": "기술통계 행렬",
        "csv": "data/analysis_csv/enhanced_descriptive_metrics_2024.csv",
        "figure": "figures/enhanced_numeric_distribution_grid_2024.png",
        "question": "A비율과 성과 지표의 기본 분포는 어떤가?",
    },
    {
        "id": "V3",
        "title": "상관 행렬",
        "csv": "data/analysis_csv/enhanced_correlation_long_matrix_2024.csv",
        "figure": "figures/enhanced_spearman_correlation_heatmap_2024.png",
        "question": "핵심 변수들은 서로 어떤 방향으로 움직이는가?",
    },
    {
        "id": "V4",
        "title": "변수-타겟 추세선",
        "csv": "data/analysis_csv/enhanced_trendline_metrics_2024.csv",
        "figure": "figures/enhanced_target_trendline_panel_2024.png",
        "question": "변수와 타겟의 추세선은 기사 가설과 맞는가?",
    },
    {
        "id": "V5",
        "title": "100% 성적구성 누적막대",
        "csv": "data/analysis_csv/enhanced_grade_composition_100pct_by_group_2024.csv",
        "figure": "figures/enhanced_grade_100pct_stacked_bars_2024.png",
        "question": "A비율 차이는 전체 성적구성에서 어떻게 나타나는가?",
    },
    {
        "id": "V6",
        "title": "범주형-타겟 효과 행렬",
        "csv": "data/analysis_csv/enhanced_categorical_target_effect_matrix_2024.csv",
        "figure": "figures/enhanced_categorical_target_effect_heatmap_2024.png",
        "question": "범주형 그룹은 타겟을 얼마나 가르는가?",
    },
    {
        "id": "V7",
        "title": "3D PCA",
        "csv": "data/analysis_csv/enhanced_pca_scores_2024.csv",
        "figure": "figures/enhanced_pca_3d_university_feature_space_2024.png",
        "question": "여러 변수를 함께 보면 대학들은 어떤 공간에 놓이는가?",
    },
    {
        "id": "V9-A",
        "title": "수치형·순서형 검정 행렬",
        "csv": "data/deep_contrast_2024/deep_numeric_ordinal_target_tests_2024.csv",
        "figure": "figures/deep_contrast_2024/deep_v9_numeric_ordinal_test_heatmap_2024.png",
        "question": "수치형/순서형 피처와 A비율·잔차의 관계는 어디가 강한가?",
    },
    {
        "id": "V9-B",
        "title": "범주형·이진형 효과 행렬",
        "csv": "data/deep_contrast_2024/deep_categorical_binary_target_tests_2024.csv",
        "figure": "figures/deep_contrast_2024/deep_v10_categorical_binary_effect_matrix_2024.png",
        "question": "범주형/이진형 피처는 타겟을 얼마나 가르는가?",
    },
    {
        "id": "V11",
        "title": "H1 실제 입결/대학 내 비교 대시보드",
        "csv": "data/deep_contrast_2024/deep_h1_selectivity_quartile_summary_2024.csv",
        "figure": "figures/deep_contrast_2024/deep_v11_h1_actual_within_contrast_dashboard_2024.png",
        "question": "실제 입결과 A비율의 대학 간/대학 내 패턴은 다른가?",
    },
    {
        "id": "V12",
        "title": "H2/H3 정책·잔차·성과 대시보드",
        "csv": "data/deep_contrast_2024/deep_h3_residual_group_outcome_summary_2024.csv",
        "figure": "figures/deep_contrast_2024/deep_v12_h2_h3_policy_residual_outcome_dashboard_2024.png",
        "question": "학점포기제와 실제 입결 잔차는 취업·진학성과와 어떻게 연결되는가?",
    },
    {
        "id": "V13",
        "title": "구성비·매핑품질 대시보드",
        "csv": "data/deep_contrast_2024/deep_grade_composition_by_selectivity_quartile_2024.csv",
        "figure": "figures/deep_contrast_2024/deep_v13_grade_composition_crosswalk_dashboard_2024.png",
        "question": "입결 분위별 성적 구성과 매핑 품질은 동시에 안전한가?",
    },
    {
        "id": "V16",
        "title": "대학-학과 버블 벡터 3D 맵",
        "csv": "data/deep_contrast_2024/v16_university_department_bubble_vector_dataset_2024.csv",
        "figure": "figures/deep_contrast_2024/deep_v16_university_department_bubble_vector_3d_2024.png",
        "question": "대학-학과 element의 입결순위, A비율 bin, 성과점수, 졸업자규모, 대학 내 편차 방향은 어떻게 배치되는가?",
    },
    {
        "id": "V16-2D",
        "title": "대학-학과 버블 벡터 2D 라벨 투영",
        "csv": "data/deep_contrast_2024/v16_university_label_centroids_2024.csv",
        "figure": "figures/deep_contrast_2024/deep_v16_university_department_bubble_vector_xy_labeled_2024.png",
        "question": "대학 라벨과 강한 학과 벡터 라벨을 2D 투영에서 읽을 수 있는가?",
    },
    {
        "id": "V17-A",
        "title": "읽히는 전체 버블 지도",
        "csv": "data/deep_contrast_2024/v17_readable_bubble_plot_dataset_2024.csv",
        "figure": "figures/deep_contrast_2024/deep_v17a_readable_overall_bubble_map_2024.png",
        "question": "벡터를 제거한 전체 지도에서 대학별 centroid와 A비율 5% bin이 읽히는가?",
    },
    {
        "id": "V17-B",
        "title": "짧은 벡터 glyph 지도",
        "csv": "data/deep_contrast_2024/v17_short_vector_glyph_dataset_2024.csv",
        "figure": "figures/deep_contrast_2024/deep_v17b_short_vector_glyph_map_2024.png",
        "question": "선별된 학과의 대학 내 입결 편차와 A비율 편차 방향이 과밀하지 않게 읽히는가?",
    },
    {
        "id": "V17-C",
        "title": "대학별 small multiples",
        "csv": "data/deep_contrast_2024/v17_small_multiple_university_selection_2024.csv",
        "figure": "figures/deep_contrast_2024/deep_v17c_university_small_multiples_2024.png",
        "question": "대학 내부 구조를 분리했을 때 학과별 위치와 주요 벡터가 더 명확한가?",
    },
    {
        "id": "V17-D",
        "title": "깨끗한 3D 보조 개관",
        "csv": "data/deep_contrast_2024/v17_visual_manifest_2024.csv",
        "figure": "figures/deep_contrast_2024/deep_v17d_clean_3d_overview_2024.png",
        "question": "z축 성과점수를 포함한 전체 공간을 보조 그림으로만 안정적으로 제시할 수 있는가?",
    },
]


def missing_artifacts() -> list[str]:
    missing: list[str] = []
    for block in VISUAL_BLOCKS:
        for key in ("csv", "figure"):
            path = BASE_DIR / block[key]
            if not path.exists() or path.stat().st_size == 0:
                missing.append(str(path.relative_to(BASE_DIR)))
    return missing


if __name__ == "__main__":
    missing = missing_artifacts()
    if missing:
        print("missing artifacts:")
        for item in missing:
            print("-", item)
        raise SystemExit(1)
    print("all visualization artifacts exist")
