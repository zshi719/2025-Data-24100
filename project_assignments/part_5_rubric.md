## Part 5 Rubric

| Category | Criteria | Points |
|----------|----------|---------|
| Directory / File | General Hygiene (no unnecessary files, directories, no name, v2, etc.) | 5 |
| | Correct Makefile updates (Updates makefile with new specifications) | 5 |
| | Correct Dockerfile/requirements.txt updates (Proper conventions, port exposures, file calling, installs sqlite3) | 5 |
| | .pre_commit_hook.yaml in directory | 5 |
| | README.md is up to date with all details up to Part 5 | 5 |
| Linting | Passes ruff with pyproject.toml | 10 |
| Code Execution | make build, notebook, interactive, flask (properly does all steps up until Part 4, finally initializing with app.py) | 10 |
| | make db_create<br>- Successfully creates stocks.db file<br>- Stocks.db is in a sensible place<br>- Stocks.db has a table called "Stocks"<br>- Mounted as a volume | 10 |
| | make db_load<br>- Successfully loads data from zips into stocks.db | 5 |
| | make db_rm<br>- Removes the database if executed | 5 |
| | make db_clean<br>- Executed the above commands in order (should not return errors if db doesn't exist) | 5 |
| | A db_manage.py from which make commands are accessed and executed | 5 |
| API Calls | Works Properly | 5 |
| | Proper Use of Pandas | 10 |
| Code Quality | Code quality | 5 |
| | Fixing Previous Issues | 10 |
| **Total** | | **105** |