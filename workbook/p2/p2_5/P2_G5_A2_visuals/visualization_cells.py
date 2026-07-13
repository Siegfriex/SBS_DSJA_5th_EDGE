"""Reusable visual-block registry for P2_G5_A2.ipynb."""

VISUAL_BLOCKS = [
    {'id': 'V00', 'title': '환경/경로 지도', 'purpose': 'P2/P5 strict 산출물이 A2 요약 노트북으로 들어오는 read-only 흐름을 고정한다.'},
    {'id': 'V01', 'title': '상태 보드', 'purpose': 'P2/P5 단계별 READY/BLOCKED/WARN 상태를 한 번에 확인한다.'},
    {'id': 'V02', 'title': 'Lineage/hash', 'purpose': '현재 해석이 어떤 파일 SHA와 크기에 묶여 있는지 보여준다.'},
    {'id': 'V03', 'title': 'P2 표본/feature contract', 'purpose': 'P2-S와 P2-Q 표본 차이, target 분포, 계약 차단 사유를 같이 본다.'},
    {'id': 'V04', 'title': 'P2-S 중첩 OLS', 'purpose': '개발 설명력, CV/locked-test 성능, block별 추가 설명력을 분리한다.'},
    {'id': 'V05', 'title': 'P2-S 계수 forest', 'purpose': '핵심 계수의 방향, CI, 표준화 beta를 연결해 읽는다.'},
    {'id': 'V06', 'title': '비선형/분산/공동검정', 'purpose': 'GAM AIC, MixedLM ICC, Wald p-value를 같은 진단 축으로 묶는다.'},
    {'id': 'V07', 'title': '선택편향 감사', 'purpose': '입결 관측 여부별 평균 차이를 시각화해 P2-Q 차단 이유를 설명한다.'},
    {'id': 'V08', 'title': 'P5 strict heterogeneity', 'purpose': 'major7별 RAW_A AME와 V1-vs-strict 민감도를 확인한다.'},
    {'id': 'V09', 'title': 'Context 제한', 'purpose': 'major7 context 프로파일을 heatmap으로 보되 N=7 제한을 명시한다.'},
    {'id': 'V10', 'title': '최종 판정', 'purpose': '실행 가능/차단/대기 항목과 핵심 인사이트를 최종 보드로 묶는다.'},
]

REQUIRED_INTERPRETATION_TEMPLATE = ['관찰', '원인', '제한', '결론']
DEFAULT_STACK = ['numpy', 'pandas', 'matplotlib']
