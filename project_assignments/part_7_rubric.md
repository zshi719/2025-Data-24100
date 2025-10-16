## Part 7 Rubric

THIS IS NOT UPDATED FOR 2025.

NOTE: Rewrite rubrics to help graders. Be more specific about several ongoing issues (branch protection violations, separation of concerns, unused code, inconsistent abstractions, etc.).


| Category | Criteria | Points |
|----------|----------|---------|
| Directory / File | General Hygiene (no unnecessary files, directories, no name, v2, etc.) | 5 |
| | Correct Makefile, Dockerfile, and requirements.txt | 5 |
| | .pre_commit_hook.yaml in directory | 5 |
| | README.md is up to date with all details up to Part 7, including details on v4 endpoint | 5 |
| Linting | Passes ruff with pyproject.toml | 10 |
| Logging | manage_db commands that describe: <br>- When a command starts/what command<br>- When a command ends<br>- Timing of command | 8 |
| | manage_db table creation gives a notification that table was created | 4 |
| | All routes debug (time, body, header, response) | 4 |
| | All routes info (non 2xx responses) | 4 |
| | All routes warn (incorrect API keys) | 4 |
| API Calls (Backtesting) | v1,v2,v3 calls | 6 |
| | v4/back_test | 15 |
| Code Quality | Code quality | 5 |
| | Fixing Previous Issues | 10 |
| Other | | |
| **Total** | | **90** |