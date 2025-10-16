## Part 8 Rubric

THIS IS NOT UPDATED FOR 2025.

NOTE: Rewrite rubrics to help graders. Be more specific about several ongoing issues (branch protection violations, separation of concerns, unused code, inconsistent abstractions, etc.).


| Category | Criteria | Points |
|----------|----------|---------|
| Directory / File | General Hygiene (no unnecessary files, directories, no name, v2, etc.) | 5 |
| | Correct Makefile, Dockerfile, and requirements.txt | 5 |
| | .pre_commit_hook.yaml in directory | 5 |
| | The README file is up to date with all current information | 5 |
| | Only one branch (main) left | 5 |
| Linting | Passes ruff with pyproject.toml | 10 |
| Code Execution | make build, notebook, interactive, flask, autodocs | 10 |
| Autodoc | Autodoc "About" page: Professional, Clean, or otherwise well formatted | 4 |
| | Autodoc "Index" page: describes what was done and brief description of project | 4 |
| | Autodoc "Documentation" page: all docs generated from functions in your code, should be descriptive | 4 |
| Testing | /api/v1/row_count Schema Test | 1 |
| | /api/v1/unique_stock_count Schema Test | 1 |
| | /api/v1/row_by_market_count Schema Test | 1 |
| | /api/v2/{YEAR} Schema Test | 1 |
| | /api/v2/open/{SYMBOL} Schema Test | 1 |
| | /api/v2/close/{SYMBOL} Schema Test | 1 |
| | /api/v2/high/{SYMBOL} Schema Test | 1 |
| | /api/v2/low/{SYMBOL} Schema Test | 1 |
| | /api/v4/back_test Schema Test | 1 |
| | v1, v2 and v4 Missing API Key test | 1 |
| | /api/v2/{YEAR} Incorrect year test | 1 |
| | v1, v2 and v4 Invalid API Key Test | 1 |
| | /api/v4/back_test Exact Test | 1 |
| API Calls | v1-v4 calls work | 10 |
| Code Quality | Code quality + Fixing Previous Issues | 15 |
| **Total** | | **95** |