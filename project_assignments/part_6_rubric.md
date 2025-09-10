## Part 6 Rubric

| Category | Criteria | Points |
|----------|----------|---------|
| Directory / File | General Hygiene (no unnecessary files, directories, no name, v2, etc.) | 5 |
| | Correct Makefile updates (updates Makefile with new specifications to db_create) | 5 |
| | Correct Dockerfile/requirements.txt updates (Proper conventions, port exposures, file calling, installs sqlite3) | 5 |
| | .pre_commit_hook.yaml in directory | 5 |
| | README.md is up to date with all details up to Part 6, including details on v3 endpoints | 5 |
| Linting | Passes ruff with pyproject.toml | 10 |
| Code Execution | make build, notebook, interactive, flask (properly does all steps up until Part 4, finally initializing with app.py) | 10 |
| | make db_create Creates "accounts" and "stocks_owned" table | 10 |
| | A db_manage.py from which make commands are accessed and executed, which now include the addition of the two new tables above | 5 |
| API Calls | v1 and v2 calls | 4 |
| | v3 calls | 20 |
| Code Quality | Code quality | 5 |
| | Fixing Previous Issues | 6 |
| | Query Response Time (no longer than 5 seconds) | 5 |
| Other | | |
| **Total** | | **100** |