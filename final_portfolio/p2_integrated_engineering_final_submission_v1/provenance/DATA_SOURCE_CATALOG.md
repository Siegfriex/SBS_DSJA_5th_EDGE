# P2-G4 Data Source Catalog and Data Specification

- generated_at_utc: `2026-07-13T05:59:18+00:00`
- active_mart: `/home/sieg/projects-wsl/SBS_dataScience/workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet`
- active_mart_shape: `10242 x 151`
- active_mart_sha256: `598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962`
- observed_scope: `2024년, 200개 학교, 452개 캠퍼스, 10222개 학과 entity / 10,242 outcome rows`
- grain: `analysis_year x p4_school_uid/school_uid x p4_campus_uid/campus_uid x p4_dept_uid/dept_uid x outcome_row_id`

## 1. Official Source Links

- KEDI 교육통계서비스: <https://kess.kedi.re.kr/>
- 대학알리미 대학정보공시: <https://www.academyinfo.go.kr/>
- 대입정보포털 어디가: <https://www.adiga.kr/>
- 한국고용정보원 고용조사분석시스템: <https://survey.keis.or.kr/>
- 한국고용정보원 GOMS 주제별 통계 분석 서비스: <https://analysis.keis.or.kr/>

주의: 로컬 manifest는 원천 파일의 SHA256과 로컬 경로를 보존하지만, 일부 포털 다운로드의 원본 direct download URL은 저장하지 않았다. 따라서 이 카탈로그는 공식 포털 URL + 로컬 파일 hash를 provenance anchor로 사용한다.

## 2. Source Catalog

| catalog_id | official_source | official_url | local_source_files | local_shapes | derived_outputs | grain_used | final_column_blocks | used_content | processing_summary | direct_download_url_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC01_KEDI_STRUCTURE | KEDI 교육통계서비스 / 고등교육통계 | https://kess.kedi.re.kr/ | KEDI_raw_excel | [{"sheet": "학교별 학과별 주요 현황", "shape": [35444, 129]}, {"sheet": "용어 정의", "shape": [16, 3]}, {"sheet": "요약정보", "shape": [25, 13]}] | D01_headcount_master -> D03_core -> D08_analysis_mart | school x campus x department/entity x 2024, with original Excel sheet axes restored | S0, B, DENOM, K, QUALITY | 학교, 캠퍼스, 지역, 설립, 본분교, 학위과정, 학과코드/명, 계열, 입학정원, 모집/지원/입학, 재적/재학/휴학, 외국인, 졸업, 교원 등 구조 및 규모 변수 | 손실된 Excel 축 복구, 학교/캠퍼스/학과명 정규화, campus-aware outcome-headcount bridge, 구조 match QA, log/ratio 파생, parent headcount reuse ledger | not stored in local manifest; official portal URL retained |
| SRC02_ACADEMYINFO_GRADE | 대학알리미 대학정보공시 | https://www.academyinfo.go.kr/ | grade_raw | [31743, 53] | outcome_spine -> D02_outcomes -> D08_analysis_mart | school x normalized department x 2024 | GRADE, QUALITY | 성적인정 총학생수, A+/A0/A-, C/D/F 학생수, 1/2학기 학과 단위 성적비율 | 2024 주간 1/2학기 필터, A/CD/F count 합산, 학기별 rate 계산 후 학교-학과 평균, D02 spine 생성 | not stored in local manifest; official portal URL retained |
| SRC03_ACADEMYINFO_EMPLOYMENT | 대학알리미 대학정보공시 | https://www.academyinfo.go.kr/ | employment_raw | [9951, 95] | outcome_spine -> D02_outcomes -> D08_analysis_mart | school x normalized department x 2024 | EMP, QUALITY | 취업자_total, 건보직장가입_취업자, 공식취업률_분모 | 2024 주간 필터, 학교-학과 단위 합산, 전체취업률/건보가입취업률 계산, rate range QA | not stored in local manifest; official portal URL retained |
| SRC04_ACADEMYINFO_PROGRESSION | 대학알리미 대학정보공시 | https://www.academyinfo.go.kr/ | progression_raw | [9951, 62] | outcome_spine -> D02_outcomes -> D08_analysis_mart | school x normalized department x 2024 | PROG, QUALITY | 졸업자, 전체/전문대/대학/대학원/국내/국외 진학자 | 2024 주간 필터, 학교-학과 단위 합산, 전체/대학원 진학률 등 rate 계산, missing target flags 생성 | not stored in local manifest; official portal URL retained |
| SRC05_ADIGA_ADMISSION | 대입정보포털 어디가 | https://www.adiga.kr/ | adiga_seed; adiga_registry; adiga_raw; adiga_department_proxy | adiga_seed=[214, 12]; adiga_registry=[214, 19]; adiga_raw=[6316, 18]; adiga_department_proxy=[3737, 8] | adiga_department_proxy -> outcome_spine -> D02_outcomes -> D08_analysis_mart | university x recruitment unit, collapsed to school x normalized department | Q, QUALITY | 2024 모집단위별 정시/입시결과에서 추출한 percentile/등급 계열 지표, 최종 selectivity_proxy_pct | crawl registry/seed 보존, 모집단위명 정규화, alias strict/loose 매칭, 0~100 valid score 필터, 학교-학과 proxy 생성 | crawl registry retained locally; official portal URL retained |
| SRC06_CREDIT_FORFEIT_POLICY | local curated policy workbook, likely university disclosure-derived | https://www.academyinfo.go.kr/ | policy_raw | [{"sheet": "종합", "shape": [54, 3]}] | D02_outcomes -> D08_analysis_mart | school-level policy joined to department rows | POLICY, QUALITY | 학점포기제 유무 | 학교명 매핑 후 O/X를 credit_forfeit_flag로 변환; v4.1에서 unknown encoded false 여부 별도 audit 대상 | exact external URL not recorded; local Excel hash retained |
| SRC07_MAJOR_CONTEXT_WAGE_COMPANY_CERT | 계열 단위 임금/기업유형/자격증 context local contract | https://www.academyinfo.go.kr/ | wage_reference; wage_quartile; wage_contract; job_cert_bridge_raw | wage_reference=[14, 66]; wage_quartile=[23, 10]; wage_contract=[66, 10]; job_cert_bridge_raw=[24, 26] | D04_wage_reference; D05_job_cert_bridge -> D08_analysis_mart | major_group_7 x degree_level / job-category bridge | C24, QUALITY | 계열별 평균/중위 소득, 소득구간, 대/중견/중소/공공/비영리 기업비중, 자격증 취득률, HHI/entropy context | 컬럼 계약 적용, 사분위 기준 결합, 계열 7분류로 many-to-one context 결합, 비율/HHI/entropy 생성 | exact external URL not recorded; local contract/hash retained |
| SRC08_KEIS_GOMS_LABOR_CONTEXT | 한국고용정보원 고용조사분석시스템 / 대졸자직업이동경로조사(GOMS) | https://survey.keis.or.kr/ | goms_distribution_long; goms_continuous_long; goms_topic_registry; goms_d07_profile | goms_distribution_long=[29160, 9]; goms_continuous_long=[2230, 8]; goms_topic_registry=[39, 6]; goms_d07_profile=[7, 29] | D06 major-year panel; D07 recent profile -> D08_analysis_mart | major_group_7 x year; D07 uses recent 2017-2019 major profile | GOMS, QUALITY | 경제활동률, 산업/직업/기업규모/사업체유형/종사상지위 분포, 평균소득, 근로시간, 최근 3년 추세 | 39개 topic axis registry 구성, frequency에서 경제활동률 재계산, 직업 pre/post 2017 분리, HHI/entropy 생성, 2017~2019 profile 집계 | official survey portal and topic stats URL retained; local normalized crawl/hash retained |
| SRC09_INTERNAL_BRIDGES_SPLITS_REGISTRIES | internal deterministic bridge/registry artifacts |  | bridge_school_alias; bridge_campus_alias; bridge_department_alias; bridge_outcome_headcount; bridge_department_major7; dim_school_split | bridge_school_alias=[1919, 6]; bridge_campus_alias=[229, 10]; bridge_department_alias=[19990, 10]; bridge_outcome_headcount=[10242, 17]; bridge_department_major7=[10242, 8]; dim_school_split=[200, 6] | D03_core -> D08_analysis_mart and sample/split registries | stable outcome_row_id and school/campus/department keys | K, S0, QUALITY | 학교/캠퍼스/학과 alias, outcome-headcount bridge, major7 bridge, school-level train/validation/test split | 행 순서 join 금지, stable key join, match score/candidate count/review flag 보존, school split leakage 0 확인 | not applicable; derived audit artifacts |

## 3. Local File Inventory

| label | official_source_hint | relative_path | exists | size_bytes | shape | sha256 | manifest_hash_reference | hash_matches_known_manifest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KEDI_raw_excel | KEDI_EDUCATION_STATISTICS | workbook/p2/p2_2/final/data/2024년 고등 학교별X학과별 입학정원 지원 입학 학생 외국인학생 졸업 교원_240912H.xlsx | True | 21218132 | [{"sheet": "학교별 학과별 주요 현황", "shape": [35444, 129]}, {"sheet": "용어 정의", "shape": [16, 3]}, {"sheet": "요약정보", "shape": [25, 13]}] | c767832c42fb2be505c4d9bb8ae0bc39891091f86c6ae8762d5b1cd2eed0a190 | c767832c42fb2be505c4d9bb8ae0bc39891091f86c6ae8762d5b1cd2eed0a190 | True |
| grade_raw | ACADEMYINFO/local_outcome_spine | workbook/p2/p2_2/P2__전체대학학점비율.csv | True | 10924406 | [31743, 53] | ae47aa8d18c30ebd389622883658fbce37d27171d6c554568da31a89aa081924 |  | False |
| employment_raw | ACADEMYINFO/local_outcome_spine | workbook/p2/p2_2/p2_취업률_데이터.csv | True | 5023581 | [9951, 95] | cba63d5b44940d2fc67fa9797d1cc2288ffc7401ac29304d702f874b03fb08c2 |  | False |
| progression_raw | ACADEMYINFO/local_outcome_spine | workbook/p2/p2_2/p2_상위대학_진학률.csv | True | 3720533 | [9951, 62] | f700ceb0e68d45a4299f45c9a0a14b23c99bb0c42e7018584477e5a9c69853b5 |  | False |
| policy_raw | ACADEMYINFO/local_outcome_spine | workbook/p2/p2_2/학점포기제도현황.xlsx | True | 11672 | [{"sheet": "종합", "shape": [54, 3]}] | b09ca42d36579269d6e0ab9624d42e814bb54415f15c4f0ed868860ba3c15406 |  | False |
| adiga_raw | ADIGA | workbook/p2/p2_2/data/crawl_2024_admission_full/02_admission_result_raw_2024_merged.csv | True | 3321454 | [6316, 18] | c01db6881c09c8b22faa44931279825b8ce893f0f5a7a7c44369dd40bef087ff |  | False |
| adiga_registry | ADIGA | workbook/p2/p2_2/data/crawl_2024_admission_full/01_crawl_source_registry_merged.csv | True | 96870 | [214, 19] | 619a6cdc5c34c2aa83e8b44bfbbe1f72884838e23c7d87000aba3d95dd23b6ad |  | False |
| adiga_seed | ADIGA | workbook/p2/p2_2/data/crawl_2024_admission_full/00_crawl_seed_university_2024_merged.csv | True | 38749 | [214, 12] | 341b630f620251225aef1a4c66aa0cbe71f0b6afe20b9db8c13f12d541b899e0 |  | False |
| adiga_department_proxy | ADIGA | workbook/p2/p2_2/final/admission/P2_admission_proxy_v3_by_department.csv | True | 360002 | [3737, 8] | 8e69e132322f075d8cbebee55fc937855c73e85632efb2c684cf7e7b0de7a4c0 |  | False |
| outcome_spine | ACADEMYINFO/local_outcome_spine | workbook/p2/p2_3/P2_G2_정시입결.csv | True | 1810159 | [10242, 17] | 2530f88a0d923edf11c83e5884d2bb47d1811679cc9b6198b0d3384c50950b04 | 2530f88a0d923edf11c83e5884d2bb47d1811679cc9b6198b0d3384c50950b04 | True |
| wage_reference | ACADEMYINFO/major_context_local_contract | workbook/p2/p2_3/P2_G2_임금분류_학부대학원.CSV | True | 12461 | [14, 66] | 90f94f0b781d88a45a168a3b60095b16537a532de1dbee0b54dfb3d1cf3efb85 | 90f94f0b781d88a45a168a3b60095b16537a532de1dbee0b54dfb3d1cf3efb85 | True |
| wage_quartile | ACADEMYINFO/major_context_local_contract | workbook/p2/p2_3/P2_G2_임금분류_학부대학원_사분위기준.CSV | True | 7434 | [23, 10] | c46a158b418c8ec114af62a95d978692cc75890ff550064db9333d6b91848ddf | c46a158b418c8ec114af62a95d978692cc75890ff550064db9333d6b91848ddf | True |
| wage_contract | ACADEMYINFO/major_context_local_contract | workbook/p2/p2_3/P2_G2_임금분류_학부대학원_컬럼설명.CSV | True | 21866 | [66, 10] | 2431de62f6b0b8d3276b603d64f94c7cbdeaa4450aa79f549dd7ff43a4eaa491 | 2431de62f6b0b8d3276b603d64f94c7cbdeaa4450aa79f549dd7ff43a4eaa491 | True |
| job_cert_bridge_raw | ACADEMYINFO/major_context_local_contract | workbook/p2/p2_3/P2_G2_직무별_자격증매핑.CSV | True | 15660 | [24, 26] | e88fe083e07430f96f5549071cde674021048c3f482f69d2981c02b9f882c471 | e88fe083e07430f96f5549071cde674021048c3f482f69d2981c02b9f882c471 | True |
| goms_distribution_long | KEIS_GOMS | workbook/p2/p2_2/data/goms_subject_crawl/normalized/goms_distribution_long.csv | True | 3706427 | [29160, 9] | 5da4c46cf438bea5f7cac5c3f1f489ae297b838ff38d14b4d335a700f9ddaf6b |  | False |
| goms_continuous_long | KEIS_GOMS | workbook/p2/p2_2/data/goms_subject_crawl/normalized/goms_continuous_long.csv | True | 278598 | [2230, 8] | 8d304f82656915d08ea88e8aa0435c6044a0375995f01bc6a4851d0fd292575c |  | False |
| goms_topic_registry | KEIS_GOMS | workbook/p2/p2_2/data/goms_subject_crawl/00_topic_registry.csv | True | 3339 | [39, 6] | 7cf9368b079760952c2caded8a39f8ccfc098de2ffae11dc9252687c3be19cb7 |  | False |
| goms_d07_profile | KEIS_GOMS | workbook/p2/p2_3/shared_handoff/goms_major_profile_recent.parquet | True | 20580 | [7, 29] | f44c6f9e7a7539361dce301686144780e0ce588deb929b625ebe811674bb621f | f44c6f9e7a7539361dce301686144780e0ce588deb929b625ebe811674bb621f | True |
| D01_headcount_master | KEDI_EDUCATION_STATISTICS | workbook/p2/p2_3/p4_handoff_candidate/local1/dept_headcount_master_2024.parquet | True | 6274643 | [34969, 186] | 2f187b5af44c828d4107af12368029caf6b83b6254af75b9653b6402b8f1b0ce | 2f187b5af44c828d4107af12368029caf6b83b6254af75b9653b6402b8f1b0ce | True |
| D02_outcomes | ACADEMYINFO/local_outcome_spine | workbook/p2/p2_3/p4_handoff_candidate/local1/dept_outcomes_2024.parquet | True | 848641 | [10242, 37] | 45f8aa40f31e14b83b5d97f594abf89bb4a5aaa4bc67735767e19077d189f493 | 45f8aa40f31e14b83b5d97f594abf89bb4a5aaa4bc67735767e19077d189f493 | True |
| D03_core | derived_internal_contract | workbook/p2/p2_3/p4_handoff_candidate/local1/dept_master_2024_core.parquet | True | 1934037 | [10242, 108] | c6fd569052684502e5bab5758510d3cd945f68ddeaa47fdfb3e9bab803889dca | c6fd569052684502e5bab5758510d3cd945f68ddeaa47fdfb3e9bab803889dca | True |
| D04_wage_reference | ACADEMYINFO/major_context_local_contract | workbook/p2/p2_3/p4_handoff_candidate/local1/wage_reference_by_major.parquet | True | 77696 | [14, 87] | 489caf15edbefa1ed0c30fdfa98dbe31096b36c219f6610dae69a2d5e49c47e5 | 489caf15edbefa1ed0c30fdfa98dbe31096b36c219f6610dae69a2d5e49c47e5 | True |
| D05_job_cert_bridge | ACADEMYINFO/major_context_local_contract | workbook/p2/p2_3/p4_handoff_candidate/local1/job_cert_bridge.parquet | True | 31466 | [24, 32] | f4447cf519bdf366e36851a68e6ec6b6605f9c9a591d96c911de4eece2327246 | f4447cf519bdf366e36851a68e6ec6b6605f9c9a591d96c911de4eece2327246 | True |
| bridge_school_alias | derived_internal_contract | workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_school_alias.csv | True | 337935 | [1919, 6] | c4ea27cd4a71a4b93189578c0f6f28463bfd1981fb9a5abb5f9f2b8768499dc3 | c4ea27cd4a71a4b93189578c0f6f28463bfd1981fb9a5abb5f9f2b8768499dc3 | True |
| bridge_campus_alias | derived_internal_contract | workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_campus_alias.csv | True | 35943 | [229, 10] | 8033c6f596aec13af52dd3cb255ba4414b6a03299cd0a9cb7c6e8c91a3f7a0fa | 8033c6f596aec13af52dd3cb255ba4414b6a03299cd0a9cb7c6e8c91a3f7a0fa | True |
| bridge_department_alias | derived_internal_contract | workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_department_alias.csv | True | 4097995 | [19990, 10] | 2d380712d1220dab414976a8b0cc67708285dafe6f413e030e61fa953a1c936c | 2d380712d1220dab414976a8b0cc67708285dafe6f413e030e61fa953a1c936c | True |
| bridge_outcome_headcount | derived_internal_contract | workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_outcome_headcount_v2.csv | True | 2046842 | [10242, 17] | 0ee76ab52f2f78e841ef341d740e9098cfafb1d7c1d277f577657d1b3d454bea | 0ee76ab52f2f78e841ef341d740e9098cfafb1d7c1d277f577657d1b3d454bea | True |
| bridge_department_major7 | derived_internal_contract | workbook/p2/p2_3/p4_handoff_candidate/local1/bridge_department_major7_v2.csv | True | 1047119 | [10242, 8] | 7a92574bd2d8928304cffb08ecbafa4a3ce2c3112a3afe19ae2852e16138fbab | 7a92574bd2d8928304cffb08ecbafa4a3ce2c3112a3afe19ae2852e16138fbab | True |
| dim_school_split | derived_internal_contract | workbook/p2/p2_3/p4_handoff_candidate/shared/dim_school_split.csv | True | 10962 | [200, 6] | 85c2c851ddcfd02d5ead41dbd9424124e4ef1993347842c031e487e8f2a13583 | 85c2c851ddcfd02d5ead41dbd9424124e4ef1993347842c031e487e8f2a13583 | True |
| D08_analysis_mart | derived_internal_contract | workbook/p2/p2_3/p4_handoff_candidate/shared/mart_department_model_base_2024.parquet | True | 2103297 | [10242, 151] | 598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962 | 598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962 | True |

## 4. Final Mart Column Source Counts

### 4.1 By Source Dataset

| source_dataset | column_n |
| --- | --- |
| D01_v2 | 51 |
| D03_v2 | 32 |
| D07_HANDOFF | 28 |
| D02_v2 | 25 |
| D04_v2 | 15 |

### 4.2 By Feature Block

| feature_block | column_n |
| --- | --- |
| QUALITY | 33 |
| GOMS | 28 |
| K | 27 |
| DENOM | 15 |
| C24 | 15 |
| S0 | 12 |
| PROG | 6 |
| B | 5 |
| Q | 4 |
| GRADE | 3 |
| EMP | 2 |
| POLICY | 1 |

### 4.3 By Source Dataset x Feature Block

| source_dataset | feature_block | semantic_role | measurement_level | column_n |
| --- | --- | --- | --- | --- |
| D01_v2 | B | department_structure_feature | school_department | 5 |
| D01_v2 | DENOM | count_or_denominator_candidate | school_department | 15 |
| D01_v2 | K | identifier_or_label | department | 14 |
| D01_v2 | Q | admission_selectivity_feature | school_department | 3 |
| D01_v2 | QUALITY | grain_lineage_metadata | department | 2 |
| D01_v2 | QUALITY | match_or_review_metadata | row_quality | 2 |
| D01_v2 | S0 | stratification_feature | school_department | 10 |
| D02_v2 | EMP | target_candidate_or_phase_signal | department | 2 |
| D02_v2 | GRADE | target_candidate_or_phase_signal | department | 3 |
| D02_v2 | K | identifier_or_label | department | 7 |
| D02_v2 | POLICY | policy_feature | department | 1 |
| D02_v2 | PROG | target_candidate_or_phase_signal | department | 6 |
| D02_v2 | Q | selectivity_feature | department | 1 |
| D02_v2 | QUALITY | target_family_observation_flag | row_quality | 2 |
| D02_v2 | QUALITY | match_or_review_metadata | row_quality | 1 |
| D02_v2 | QUALITY | sample_observation_flag | row_quality | 1 |
| D02_v2 | S0 | stratification_feature | school_department | 1 |
| D03_v2 | K | identifier_or_label | department | 6 |
| D03_v2 | QUALITY | match_or_review_metadata | row_quality | 21 |
| D03_v2 | QUALITY | sample_observation_flag | row_quality | 2 |
| D03_v2 | QUALITY | major_mapping_lineage_metadata | department | 1 |
| D03_v2 | QUALITY | sample_exclusion_metadata | department | 1 |
| D03_v2 | S0 | stratification_feature | school_department | 1 |
| D04_v2 | C24 | major7_2024_context | major7_year | 15 |
| D07_HANDOFF | GOMS | major7_historical_context | major7 | 28 |

## 5. Final Mart Target and Split Counts

```json
{
  "row_split_counts_in_d08": {},
  "school_split_counts_from_dim_school_split": {
    "train": 140,
    "test": 30,
    "val": 30
  },
  "phase_sample_registry_rows": [
    {
      "sample_id": "P1_STRUCTURE_READY",
      "row_n": 5600,
      "school_n": 185,
      "train_n": 4080,
      "validation_n": 871,
      "test_n": 649
    },
    {
      "sample_id": "P1_SELECTIVITY_READY",
      "row_n": 2355,
      "school_n": 130,
      "train_n": 1742,
      "validation_n": 360,
      "test_n": 253
    },
    {
      "sample_id": "P2_STRUCTURE_READY",
      "row_n": 7592,
      "school_n": 197,
      "train_n": 5534,
      "validation_n": 1168,
      "test_n": 890
    },
    {
      "sample_id": "P2_SELECTIVITY_READY",
      "row_n": 3119,
      "school_n": 146,
      "train_n": 2293,
      "validation_n": 514,
      "test_n": 312
    },
    {
      "sample_id": "P3_STRUCTURE_READY",
      "row_n": 7592,
      "school_n": 197,
      "train_n": 5534,
      "validation_n": 1168,
      "test_n": 890
    },
    {
      "sample_id": "P3_SELECTIVITY_READY",
      "row_n": 3119,
      "school_n": 146,
      "train_n": 2293,
      "validation_n": 514,
      "test_n": 312
    },
    {
      "sample_id": "P4_E_STRUCTURE_READY",
      "row_n": 5600,
      "school_n": 185,
      "train_n": 4080,
      "validation_n": 871,
      "test_n": 649
    },
    {
      "sample_id": "P4_P_STRUCTURE_READY",
      "row_n": 5674,
      "school_n": 194,
      "train_n": 4129,
      "validation_n": 884,
      "test_n": 661
    },
    {
      "sample_id": "P4_JOINT_STRUCTURE_READY",
      "row_n": 5600,
      "school_n": 185,
      "train_n": 4080,
      "validation_n": 871,
      "test_n": 649
    },
    {
      "sample_id": "P4_E_SELECTIVITY_READY",
      "row_n": 2355,
      "school_n": 130,
      "train_n": 1742,
      "validation_n": 360,
      "test_n": 253
    },
    {
      "sample_id": "P4_P_SELECTIVITY_READY",
      "row_n": 2376,
      "school_n": 136,
      "train_n": 1756,
      "validation_n": 365,
      "test_n": 255
    },
    {
      "sample_id": "P4_JOINT_SELECTIVITY_READY",
      "row_n": 2355,
      "school_n": 130,
      "train_n": 1742,
      "validation_n": 360,
      "test_n": 253
    }
  ],
  "target_non_null": {
    "a_rate_pct": 10242,
    "health_employment_rate_pct": 7477,
    "graduate_school_progression_rate_pct": 7587
  },
  "major_group_7_counts": {
    "ENG": 2642,
    "SOC": 2165,
    "ART": 1566,
    "NAT": 1258,
    "HUM": 1108,
    "EDU": 728,
    "MED": 632,
    "NaN": 143
  }
}
```

## 6. Processing Ledger Summary

- 원본 파일 hash·shape 동결: `P4_HANDOFF_MANIFEST.json`, `dataset_inventory.csv`, 이 카탈로그의 `data_source_file_inventory.csv`에 재기록.
- 손실된 Excel 축 복구: KEDI raw Excel sheet `학교별 학과별 주요 현황`을 D01 34,969 x 186으로 정규화.
- 학교·캠퍼스·학과명 정규화: school/campus/department alias bridge 생성.
- campus-aware 학과 매칭: outcome spine 10,242행과 D01 headcount 구조를 stable key/bridge로 결합.
- 중복·후보·충돌 QA: outcome_row_id는 중복 0, composite dept key 충돌은 ledger 보존.
- 7대 계열 bridge: D01 대계열 및 학과 alias로 major_group_7 생성, major7 coverage 10,099 / 10,242.
- GOMS 39개 주제 정규화: distribution/continuous long source를 topic registry로 표준화.
- GOMS 경제활동률 frequency 재계산: share를 그대로 취업률로 쓰지 않고 frequency로 재계산.
- 직업 pre/post 분류 분리: GOMS 2017 전후 직업분류 스키마를 분리.
- 산업·직업·기업분포 HHI·entropy 생성: 계열 단위 context 변수로만 사용.
- 계열별 최근 2017~2019 profile 생성: D07 `goms_major_profile_recent.parquet` 7 x 29.
- D04·D07 many-to-one context 결합: major_group_7 단위 contemporary/context variables를 D08에 결합.
- 학교 단위 split 고정: `dim_school_split.csv` 200 x 6, split leakage 0.
- 모델별 sample mask 생성: readiness v4 membership/sample registry에서 별도 관리.
- column·feature·target registry 생성: `department_model_column_registry_v4.csv` 현 상태 151 x 27.
- SHA256 manifest·decision·transformation·merge log 생성: handoff/preprocessing integrity manifest에 보존.

## 7. Known Limits

- 성적 A비율, 취업률, 진학률의 저장 rate는 존재하지만 최종 마트 D08에는 원 count numerator/denominator가 보존되지 않았다. count-binomial 분석은 `NOT_AVAILABLE`로 분리해야 한다.
- 학점포기제 원천은 local curated Excel로 보존되어 있으며 exact external direct URL은 manifest에 없다.
- 임금/기업/자격증 context의 local contract 파일은 hash로 고정되어 있으나, direct download URL은 manifest에 없다.
- GOMS와 D04/C24 context는 학과 outcome이 아니라 7대 계열 단위 context이며, 학과별 결과처럼 해석하면 안 된다.

## 8. Output Files

- `qa/data_source_catalog.csv`
- `qa/data_source_file_inventory.csv`
- `qa/data_source_column_catalog.csv`
- `qa/data_source_column_blocks.csv`
- `reports/DATA_SOURCE_CATALOG.md`
