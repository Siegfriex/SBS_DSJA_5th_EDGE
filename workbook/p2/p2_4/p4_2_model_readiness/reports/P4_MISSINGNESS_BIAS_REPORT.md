# P4 Missingness Bias Report

관측 플래그별 계열·지역·유형·split 관측률과 train-only 수치형 SMD/KS, 범주형 Cramér's V를 계산했다. 이 결과는 선택편향 진단이며 인과해석이 아니다.

| audit_type | flag | group_col | group_value | n | observed_rate | feature | smd | median_diff | ks_statistic | cramers_v |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| group_observation_rate | has_selectivity | major_group_7 | ART | 1566.0 | 0.22413793103448276 |  |  |  |  |  |
| group_observation_rate | has_selectivity | major_group_7 | EDU | 728.0 | 0.5206043956043956 |  |  |  |  |  |
| group_observation_rate | has_selectivity | major_group_7 | ENG | 2642.0 | 0.3785011355034065 |  |  |  |  |  |
| group_observation_rate | has_selectivity | major_group_7 | HUM | 1108.0 | 0.3664259927797834 |  |  |  |  |  |
| group_observation_rate | has_selectivity | major_group_7 | MED | 632.0 | 0.4889240506329114 |  |  |  |  |  |
| group_observation_rate | has_selectivity | major_group_7 | NAT | 1258.0 | 0.4205087440381558 |  |  |  |  |  |
| group_observation_rate | has_selectivity | major_group_7 | SOC | 2165.0 | 0.33856812933025404 |  |  |  |  |  |
| group_observation_rate | has_selectivity | major_group_7 |  | 143.0 | 0.2097902097902098 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 강원 | 497.0 | 0.24346076458752516 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 경기 | 1081.0 | 0.33950046253469013 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 경남 | 413.0 | 0.38256658595641646 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 경북 | 687.0 | 0.27074235807860264 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 광주 | 361.0 | 0.3379501385041551 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 대구 | 219.0 | 0.593607305936073 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 대전 | 489.0 | 0.3803680981595092 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 부산 | 895.0 | 0.36312849162011174 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 서울 | 1629.0 | 0.4174340085942296 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 세종 | 1.0 | 1.0 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 울산 | 92.0 | 0.03260869565217391 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 인천 | 199.0 | 0.5829145728643216 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 전남 | 245.0 | 0.10204081632653061 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 전북 | 413.0 | 0.5447941888619855 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 제주 | 105.0 | 0.5047619047619047 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 충남 | 702.0 | 0.41595441595441596 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido | 충북 | 533.0 | 0.3902439024390244 |  |  |  |  |  |
| group_observation_rate | has_selectivity | region_sido |  | 1681.0 | 0.3206424747174301 |  |  |  |  |  |
| group_observation_rate | has_selectivity | school_type | 각종대학(대학) | 29.0 | 0.0 |  |  |  |  |  |
| group_observation_rate | has_selectivity | school_type | 교육대학 | 123.0 | 0.008130081300813009 |  |  |  |  |  |
| group_observation_rate | has_selectivity | school_type | 대학교 | 8324.0 | 0.38142719846227774 |  |  |  |  |  |
| group_observation_rate | has_selectivity | school_type | 방송통신대학교 | 27.0 | 0.0 |  |  |  |  |  |
| group_observation_rate | has_selectivity | school_type | 산업대학 | 58.0 | 0.3793103448275862 |  |  |  |  |  |
| group_observation_rate | has_selectivity | school_type |  | 1681.0 | 0.3206424747174301 |  |  |  |  |  |
| group_observation_rate | has_selectivity | degree_course | 대학과정 | 8561.0 | 0.3735544912977456 |  |  |  |  |  |
| group_observation_rate | has_selectivity | degree_course |  | 1681.0 | 0.3206424747174301 |  |  |  |  |  |
| group_observation_rate | has_selectivity | split | test | 1199.0 | 0.3035863219349458 |  |  |  |  |  |
| group_observation_rate | has_selectivity | split | train | 7529.0 | 0.37016868109974765 |  |  |  |  |  |
| group_observation_rate | has_selectivity | split | validation | 1514.0 | 0.3870541611624835 |  |  |  |  |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | credit_forfeit_flag | 0.21678886289218396 | 0.0 | 0.0682419142802706 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | employment_rate_pct | -0.050869911909103394 | -0.248138427734375 | 0.04797106981277466 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | progression_rate_pct | 0.20047247409820557 | 2.1719858646392822 | 0.14071977138519287 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | vocational_college_progression_rate_pct | -0.07372236996889114 | 0.0 | 0.012088358402252197 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | university_progression_rate_pct | -0.02722257561981678 | 0.0 | 0.016594648361206055 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | domestic_progression_rate_pct | 0.20214711129665375 | 2.1666665077209473 | 0.14385858178138733 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | overseas_progression_rate_pct | -0.01572021283209324 | 0.0 | 0.009505391120910645 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | has_selectivity |  | 1.0 | 1.0 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | has_employment | 0.10515889402910254 | 0.0 | 0.04631198020211025 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | has_progression | 0.09367623774560949 | 0.0 | 0.04081324738267095 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | candidate_count | -0.12649828220314172 | 0.0 | 0.01761976471770421 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | campus_conflict_flag | 0.046133118643829345 | 0.0 | 0.007024842852812574 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | headcount_match_flag | 0.03437829120177293 | 0.0 | 0.012645398130169044 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | raw_row_lineage | -0.30162684882483926 | -3279.0 | 0.17777440685688345 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | admission_capacity_n | 0.1570098928984071 | 40.0 | 0.6887072177692 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | recruitment_n | 0.15332506448020325 | 42.0 | 0.6547928847032093 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | applicants_n | 0.7901784497911345 | 308.0 | 0.6806534781179718 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | admits_n | 0.7632249674348867 | 41.0 | 0.6248541583626361 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | enrolled_students_n | 0.24539587911900895 | 94.0 | 0.3687921219427048 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | leave_students_n | 0.2283703954878068 | 26.0 | 0.30276847636706533 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | graduates_n | 0.08337173334802378 | 10.0 | 0.18601243547062274 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | fulltime_faculty_n | 0.165711333286842 | 5.0 | 0.4821040140674984 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | nonfulltime_faculty_n | 0.2180349411202234 | 6.0 | 0.3726830611762972 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | international_students_n | 0.04814082320670829 | 0.0 | 0.100480625183899 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | female_students_n | 0.12401816841010799 | 48.0 | 0.32657123015841 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | competition_ratio | 0.26532217860221863 | 1.8379631042480469 | 0.26468485593795776 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | admission_yield_ratio | 0.13595546782016754 | 0.0 | 0.13524962961673737 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | admit_per_applicant_ratio | -0.5712520480155945 | -0.04028598964214325 | 0.23608732223510742 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | leave_rate_pct | -0.20678362250328064 | -1.1603221893310547 | 0.1564016342163086 |  |
| numeric_observed_vs_unobserved | has_selectivity |  |  |  |  | female_student_share_pct | 0.07359127700328827 | 3.6734695434570312 | 0.10737951099872589 |  |
| categorical_cramers_v | has_selectivity |  |  |  |  | major_group_7 |  |  |  | 0.16891730802588675 |
| categorical_cramers_v | has_selectivity |  |  |  |  | region_sido |  |  |  | 0.19300270241364878 |
| categorical_cramers_v | has_selectivity |  |  |  |  | school_type |  |  |  | 0.10994592837249219 |
| categorical_cramers_v | has_selectivity |  |  |  |  | degree_course |  |  |  | 0.04071132333834327 |
| categorical_cramers_v | has_selectivity |  |  |  |  | split |  |  |  | 0.047960715732685344 |
| group_observation_rate | has_employment | major_group_7 | ART | 1566.0 | 0.7164750957854407 |  |  |  |  |  |
| group_observation_rate | has_employment | major_group_7 | EDU | 728.0 | 0.9217032967032966 |  |  |  |  |  |
| group_observation_rate | has_employment | major_group_7 | ENG | 2642.0 | 0.6752460257380772 |  |  |  |  |  |
| group_observation_rate | has_employment | major_group_7 | HUM | 1108.0 | 0.7572202166064982 |  |  |  |  |  |
| group_observation_rate | has_employment | major_group_7 | MED | 632.0 | 0.7689873417721519 |  |  |  |  |  |
| group_observation_rate | has_employment | major_group_7 | NAT | 1258.0 | 0.7456279809220986 |  |  |  |  |  |
| group_observation_rate | has_employment | major_group_7 | SOC | 2165.0 | 0.715473441108545 |  |  |  |  |  |
| group_observation_rate | has_employment | major_group_7 |  | 143.0 | 0.6153846153846154 |  |  |  |  |  |

_... 280 more rows omitted._