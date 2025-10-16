## Part 3 Rubric

THIS IS NOT UPDATED FOR 2025.

NOTE: Rewrite rubrics to help graders. Be more specific about several ongoing issues (branch protection violations, separation of concerns, unused code, inconsistent abstractions, etc.).


| Category | Criteria | Points |
|----------|----------|---------|
| Directory / File | General Hygiene (no unnecessary files, directories, no name, v2, etc.) | 5 |
| | Correct Makefile (Proper env variable, image name, general format.) | 5 |
| | Correct Dockerfile (Proper conventions, port exposures, file calling, etc) | 5 |
| | README.md is up to date with how to run for Part 3 | 5 |
| Code Execution | make build (properly builds docker container) | 4 |
| | make notebook (should be able to utilize notebook on the web) | 4 |
| | make interactive (starts interactive bash session) | 4 |
| | make flask (initializes app.py properly) | 4 |
| API Calls | v1 API rowcount call | 4 |
| | v1 API unique_stock_count call | 4 |
| | v1 API row_by_market_count call | 4 |
| | v2 /api/v2/{YEAR} | 4 |
| | v2 /api/v2/open/{SYMBOL} | 4 |
| | v2 /api/v2/close/{SYMBOL} | 4 |
| | v2 /api/v2/high/{SYMBOL} | 4 |
| | v2 /api/v2/low/{SYMBOL} | 4 |
| | Handles incorrect API key exception | 10 |
| Code Quality | Code quality | 22 |
| **Total** | | **100** |