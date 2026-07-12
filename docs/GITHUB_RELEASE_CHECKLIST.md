# GitHub Release Checklist

## Before Commit

```bash
cd /home/sieg/projects-wsl/SBS_dataScience
.venv/bin/python scripts/build_p2_3_portfolio_package.py
cd fortpolio/p2/p2_3
git check-ignore -v P2_G2_메인_입결_A_취업진학.CSV
git check-ignore -v p3_2.ipynb
git status --short
```

## Commit Scope

권장 commit 대상:

- `README.md`
- `.gitignore`
- `docs/`
- `data/`
- `src/`

권장 제외 대상:

- 원본 `P2_G2_*.CSV`
- `*.ipynb`
- `*.parquet`
- 전체 EDA output dump
- audit bundle zip

## Public Narrative

이 프로젝트는 모델 성능 과시가 아니라, messy higher-education data를 model-ready mart로 만드는 데이터 엔지니어링/감사 포트폴리오다.
