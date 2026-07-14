# FINAL 브랜치 검증 요약

## 실행 검증

최종 제출 패키지는 로컬 원본에서 새로 실행한 뒤 이 브랜치에 복사했다.

| 노트북 | nbformat | 코드 셀 | 실행 셀 | 에러 출력 | 상태 |
|---|---|---:|---:|---:|---|
| `P2_FINAL_SUBMISSION.ipynb` | 통과 | 15 | 15 | 0 | 통과 |
| `P2_INTEGRATED_ENGINEERING_BLUEPRINT_CELL_BY_CELL.ipynb` | 통과 | 16 | 16 | 0 | 통과 |

## 패키지 manifest 검증

`FINAL_SUBMISSION_PACKAGE_MANIFEST.csv`에 기록된 파일 해시를 실제 파일 전체와 대조했다.

| 항목 | 값 |
|---|---:|
| manifest 행 수 | 207 |
| 해시 불일치 | 0 |
| 누락 파일 | 0 |
| manifest 자기참조 파일 제외 | 적용 |
| 실행 노트북 자기 자신 해시 제외 | 적용 |
| `__pycache__` / `.pyc` 제외 | 적용 |

## 최종 상태

- 최종 상태: `PASS_WITH_WARNINGS`
- 실행 ID: `20260714T062549Z`
- Gate 상태: PASS 7개, WARN 1개
- 활성 D08 shape: `10242 x 151`
- 활성 D08 SHA-256: `598b68b31b5358dfd23839d4c138cc64838d05876b7791980b376c0453f29962`

## WARN 해석

경고는 제출 차단 오류가 아니라, 최종 해석의 경계를 명시한 것이다.

- `WARN_D08_SPLIT_EXTERNAL`: D08에 직접 split 컬럼이 없어 외부 split merge를 사용했다.
- `WARN_DIRECT_URL_LIMIT`: 일부 원자료 URL은 파일 직접 링크가 아니라 공식 포털 수준 URL이다.
- `WARN_Q_BRANCH_BLOCKED`: Q/selectivity branch는 최종 launch-ready 근거로 해석하지 않는다.
- `WARN_REGISTRY_COVERAGE`: registry와 D08 컬럼이 완전 대칭은 아니므로 누락/미등록 컬럼을 QA에 기록했다.

## 제출 판단

최종 결론 포트폴리오는 제출 가능하다. 단, 결론 문장은 인과효과가 아니라 대학-학과 단위 조건부 연관성으로 제한해야 한다.
