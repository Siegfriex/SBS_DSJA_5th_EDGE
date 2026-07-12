# Methodology

## Grain

최종 D08은 `outcome_row_id`를 key로 하는 2024 대학-학과 spine이다. 구조자료는 학교명, 캠퍼스, 주야구분, 학위과정, KEDI 학과코드를 포함한 D01 grain으로 관리한다.

## Matching Ladder

1. 학교 alias normalization
2. 캠퍼스 alias normalization
3. 학과 strict key
4. suffix/token key
5. high confidence인 경우만 자동확정
6. 다중 후보, campus conflict, modifier conflict는 review/pending으로 보존

## Major Mapping

`major_group_7 = HUM, SOC, EDU, ENG, NAT, MED, ART`를 사용했다. 구조자료 상속을 최우선으로 하고, exact dictionary와 keyword rule은 보조로 쓴다. ambiguous/unknown은 모델 sample에서 분리된다.

## GOMS Context

GOMS는 2007-2019 long table에서 D06 `major x year` baseline을 만들고, 2017-2019 weighted recent profile을 D07로 만든다. 2017년 이후 직업분류가 안정적이므로 recent window를 그 구간으로 제한했다.
