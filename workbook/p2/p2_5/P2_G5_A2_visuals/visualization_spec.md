# P2-G5 A2 Visualization Spec

이 문서는 `P2_G5_A2.ipynb`의 셀별 시각화 설계서다. 모든 그래프는 저장된 P2/P5 strict 산출물만 읽고 원천 parquet나 upstream notebook을 수정하지 않는다.

## V00. 환경/경로 지도

시각화 목적
: P2/P5 strict 산출물이 A2 요약 노트북으로 들어오는 read-only 흐름을 고정한다.

사용할 데이터
: P2 strict artifacts, P2 QA CSV, P5 strict artifacts 중 해당 셀에서 이미 로딩한 DataFrame.

필요한 전처리
: percentage point 변환, status bucket 정리, major/outcome pivot, 결측 또는 차단 상태 라벨링.

코드 셀 설계
: 표 출력 뒤에 matplotlib 정적 그래프를 배치하고 `P2_G5_A2_visuals/figures`에 PNG를 저장한다.

그래프 해석 포인트
: 막대/heatmap/forest plot에서 방향, 크기, 불확실성, 차단 상태를 분리해서 읽는다.

학생이 자주 하는 오해
: 설명력 상승이나 계수 방향을 곧바로 인과효과 또는 운영 처방으로 읽지 않는다.

체크포인트 질문
: 이 그래프는 현재 모델링 결론을 강화하는가, 아니면 해석 제한을 드러내는가?

## V01. 상태 보드

시각화 목적
: P2/P5 단계별 READY/BLOCKED/WARN 상태를 한 번에 확인한다.

사용할 데이터
: P2 strict artifacts, P2 QA CSV, P5 strict artifacts 중 해당 셀에서 이미 로딩한 DataFrame.

필요한 전처리
: percentage point 변환, status bucket 정리, major/outcome pivot, 결측 또는 차단 상태 라벨링.

코드 셀 설계
: 표 출력 뒤에 matplotlib 정적 그래프를 배치하고 `P2_G5_A2_visuals/figures`에 PNG를 저장한다.

그래프 해석 포인트
: 막대/heatmap/forest plot에서 방향, 크기, 불확실성, 차단 상태를 분리해서 읽는다.

학생이 자주 하는 오해
: 설명력 상승이나 계수 방향을 곧바로 인과효과 또는 운영 처방으로 읽지 않는다.

체크포인트 질문
: 이 그래프는 현재 모델링 결론을 강화하는가, 아니면 해석 제한을 드러내는가?

## V02. Lineage/hash

시각화 목적
: 현재 해석이 어떤 파일 SHA와 크기에 묶여 있는지 보여준다.

사용할 데이터
: P2 strict artifacts, P2 QA CSV, P5 strict artifacts 중 해당 셀에서 이미 로딩한 DataFrame.

필요한 전처리
: percentage point 변환, status bucket 정리, major/outcome pivot, 결측 또는 차단 상태 라벨링.

코드 셀 설계
: 표 출력 뒤에 matplotlib 정적 그래프를 배치하고 `P2_G5_A2_visuals/figures`에 PNG를 저장한다.

그래프 해석 포인트
: 막대/heatmap/forest plot에서 방향, 크기, 불확실성, 차단 상태를 분리해서 읽는다.

학생이 자주 하는 오해
: 설명력 상승이나 계수 방향을 곧바로 인과효과 또는 운영 처방으로 읽지 않는다.

체크포인트 질문
: 이 그래프는 현재 모델링 결론을 강화하는가, 아니면 해석 제한을 드러내는가?

## V03. P2 표본/feature contract

시각화 목적
: P2-S와 P2-Q 표본 차이, target 분포, 계약 차단 사유를 같이 본다.

사용할 데이터
: P2 strict artifacts, P2 QA CSV, P5 strict artifacts 중 해당 셀에서 이미 로딩한 DataFrame.

필요한 전처리
: percentage point 변환, status bucket 정리, major/outcome pivot, 결측 또는 차단 상태 라벨링.

코드 셀 설계
: 표 출력 뒤에 matplotlib 정적 그래프를 배치하고 `P2_G5_A2_visuals/figures`에 PNG를 저장한다.

그래프 해석 포인트
: 막대/heatmap/forest plot에서 방향, 크기, 불확실성, 차단 상태를 분리해서 읽는다.

학생이 자주 하는 오해
: 설명력 상승이나 계수 방향을 곧바로 인과효과 또는 운영 처방으로 읽지 않는다.

체크포인트 질문
: 이 그래프는 현재 모델링 결론을 강화하는가, 아니면 해석 제한을 드러내는가?

## V04. P2-S 중첩 OLS

시각화 목적
: 개발 설명력, CV/locked-test 성능, block별 추가 설명력을 분리한다.

사용할 데이터
: P2 strict artifacts, P2 QA CSV, P5 strict artifacts 중 해당 셀에서 이미 로딩한 DataFrame.

필요한 전처리
: percentage point 변환, status bucket 정리, major/outcome pivot, 결측 또는 차단 상태 라벨링.

코드 셀 설계
: 표 출력 뒤에 matplotlib 정적 그래프를 배치하고 `P2_G5_A2_visuals/figures`에 PNG를 저장한다.

그래프 해석 포인트
: 막대/heatmap/forest plot에서 방향, 크기, 불확실성, 차단 상태를 분리해서 읽는다.

학생이 자주 하는 오해
: 설명력 상승이나 계수 방향을 곧바로 인과효과 또는 운영 처방으로 읽지 않는다.

체크포인트 질문
: 이 그래프는 현재 모델링 결론을 강화하는가, 아니면 해석 제한을 드러내는가?

## V05. P2-S 계수 forest

시각화 목적
: 핵심 계수의 방향, CI, 표준화 beta를 연결해 읽는다.

사용할 데이터
: P2 strict artifacts, P2 QA CSV, P5 strict artifacts 중 해당 셀에서 이미 로딩한 DataFrame.

필요한 전처리
: percentage point 변환, status bucket 정리, major/outcome pivot, 결측 또는 차단 상태 라벨링.

코드 셀 설계
: 표 출력 뒤에 matplotlib 정적 그래프를 배치하고 `P2_G5_A2_visuals/figures`에 PNG를 저장한다.

그래프 해석 포인트
: 막대/heatmap/forest plot에서 방향, 크기, 불확실성, 차단 상태를 분리해서 읽는다.

학생이 자주 하는 오해
: 설명력 상승이나 계수 방향을 곧바로 인과효과 또는 운영 처방으로 읽지 않는다.

체크포인트 질문
: 이 그래프는 현재 모델링 결론을 강화하는가, 아니면 해석 제한을 드러내는가?

## V06. 비선형/분산/공동검정

시각화 목적
: GAM AIC, MixedLM ICC, Wald p-value를 같은 진단 축으로 묶는다.

사용할 데이터
: P2 strict artifacts, P2 QA CSV, P5 strict artifacts 중 해당 셀에서 이미 로딩한 DataFrame.

필요한 전처리
: percentage point 변환, status bucket 정리, major/outcome pivot, 결측 또는 차단 상태 라벨링.

코드 셀 설계
: 표 출력 뒤에 matplotlib 정적 그래프를 배치하고 `P2_G5_A2_visuals/figures`에 PNG를 저장한다.

그래프 해석 포인트
: 막대/heatmap/forest plot에서 방향, 크기, 불확실성, 차단 상태를 분리해서 읽는다.

학생이 자주 하는 오해
: 설명력 상승이나 계수 방향을 곧바로 인과효과 또는 운영 처방으로 읽지 않는다.

체크포인트 질문
: 이 그래프는 현재 모델링 결론을 강화하는가, 아니면 해석 제한을 드러내는가?

## V07. 선택편향 감사

시각화 목적
: 입결 관측 여부별 평균 차이를 시각화해 P2-Q 차단 이유를 설명한다.

사용할 데이터
: P2 strict artifacts, P2 QA CSV, P5 strict artifacts 중 해당 셀에서 이미 로딩한 DataFrame.

필요한 전처리
: percentage point 변환, status bucket 정리, major/outcome pivot, 결측 또는 차단 상태 라벨링.

코드 셀 설계
: 표 출력 뒤에 matplotlib 정적 그래프를 배치하고 `P2_G5_A2_visuals/figures`에 PNG를 저장한다.

그래프 해석 포인트
: 막대/heatmap/forest plot에서 방향, 크기, 불확실성, 차단 상태를 분리해서 읽는다.

학생이 자주 하는 오해
: 설명력 상승이나 계수 방향을 곧바로 인과효과 또는 운영 처방으로 읽지 않는다.

체크포인트 질문
: 이 그래프는 현재 모델링 결론을 강화하는가, 아니면 해석 제한을 드러내는가?

## V08. P5 strict heterogeneity

시각화 목적
: major7별 RAW_A AME와 V1-vs-strict 민감도를 확인한다.

사용할 데이터
: P2 strict artifacts, P2 QA CSV, P5 strict artifacts 중 해당 셀에서 이미 로딩한 DataFrame.

필요한 전처리
: percentage point 변환, status bucket 정리, major/outcome pivot, 결측 또는 차단 상태 라벨링.

코드 셀 설계
: 표 출력 뒤에 matplotlib 정적 그래프를 배치하고 `P2_G5_A2_visuals/figures`에 PNG를 저장한다.

그래프 해석 포인트
: 막대/heatmap/forest plot에서 방향, 크기, 불확실성, 차단 상태를 분리해서 읽는다.

학생이 자주 하는 오해
: 설명력 상승이나 계수 방향을 곧바로 인과효과 또는 운영 처방으로 읽지 않는다.

체크포인트 질문
: 이 그래프는 현재 모델링 결론을 강화하는가, 아니면 해석 제한을 드러내는가?

## V09. Context 제한

시각화 목적
: major7 context 프로파일을 heatmap으로 보되 N=7 제한을 명시한다.

사용할 데이터
: P2 strict artifacts, P2 QA CSV, P5 strict artifacts 중 해당 셀에서 이미 로딩한 DataFrame.

필요한 전처리
: percentage point 변환, status bucket 정리, major/outcome pivot, 결측 또는 차단 상태 라벨링.

코드 셀 설계
: 표 출력 뒤에 matplotlib 정적 그래프를 배치하고 `P2_G5_A2_visuals/figures`에 PNG를 저장한다.

그래프 해석 포인트
: 막대/heatmap/forest plot에서 방향, 크기, 불확실성, 차단 상태를 분리해서 읽는다.

학생이 자주 하는 오해
: 설명력 상승이나 계수 방향을 곧바로 인과효과 또는 운영 처방으로 읽지 않는다.

체크포인트 질문
: 이 그래프는 현재 모델링 결론을 강화하는가, 아니면 해석 제한을 드러내는가?

## V10. 최종 판정

시각화 목적
: 실행 가능/차단/대기 항목과 핵심 인사이트를 최종 보드로 묶는다.

사용할 데이터
: P2 strict artifacts, P2 QA CSV, P5 strict artifacts 중 해당 셀에서 이미 로딩한 DataFrame.

필요한 전처리
: percentage point 변환, status bucket 정리, major/outcome pivot, 결측 또는 차단 상태 라벨링.

코드 셀 설계
: 표 출력 뒤에 matplotlib 정적 그래프를 배치하고 `P2_G5_A2_visuals/figures`에 PNG를 저장한다.

그래프 해석 포인트
: 막대/heatmap/forest plot에서 방향, 크기, 불확실성, 차단 상태를 분리해서 읽는다.

학생이 자주 하는 오해
: 설명력 상승이나 계수 방향을 곧바로 인과효과 또는 운영 처방으로 읽지 않는다.

체크포인트 질문
: 이 그래프는 현재 모델링 결론을 강화하는가, 아니면 해석 제한을 드러내는가?
