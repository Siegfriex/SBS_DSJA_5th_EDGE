# P2-G4 Visual EDA Checklist

- [x] 원본 노트북 `workbook/p2/p2_4/p2_G4_source_parquet_csv_eda.ipynb`를 읽어 dataset call을 추출했다.
- [x] 원본 `eda_one(...)` dataset call 96개를 모두 `visual_eda_one(...)` 셀로 매핑했다.
- [x] 외부 다운로드 없이 로컬 CSV/Parquet 변환 산출물만 사용한다.
- [x] default stack은 `numpy`, `pandas`, `matplotlib`만 사용한다.
- [x] 각 데이터셋 블록은 시각화 목적, 사용할 데이터, 전처리, 코드 셀 설계, 해석 포인트, 오해, 체크포인트 질문을 포함한다.
- [x] 각 데이터셋 그래프는 dtype mix, 결측, 수치 분포, 범주/상태 분포 중 실제 데이터에 맞는 진단을 출력한다.
- [x] 비교/진단 셀에는 `관찰`, `원인`, `제한`, `결론` 해석 scaffold를 출력한다.
- [x] 그림 파일은 `workbook/p2/p2_4/source_eda/figures_visual/` 아래에 저장된다.
