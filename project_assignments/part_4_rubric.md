## Part 4 Rubric

NOTE: Rewrite rubrics to help graders. Be more specific about several ongoing issues (branch protection violations, separation of concerns, unused code, inconsistent abstractions, etc.).


| Category | Criteria | Points |
|----------|----------|---------|
| Directory / File | General Hygiene (no unnecessary files, directories, no name, v2, etc.) | 2 |
| | Correct Makefile (Proper env variable, image name, general format.) | 2 |
| | Correct Dockerfile (Proper conventions, port exposures, file calling, etc) | 2 |
| | .pre_commit_hook.yaml in directory | 10 |
| | README.md is up to date with how to run for Part 4 | 5 |
| Code Execution | make build (properly builds docker container) | 2 |
| | make notebook (should be able to utilize notebook on the web) | 2 |
| | make interactive (starts interactive bash session) | 2 |
| | make flask (initializes app.py properly) | 2 |
| Linting | Passes ruff with pyproject.toml (verify that they didn't change the pyproject.toml) | 20 |
| API Calls | Works Properly | 10 |
| Code Quality | Code quality | 16 |
| | Fixing Previous Issues | 10 |
| **Total** | | **85** |