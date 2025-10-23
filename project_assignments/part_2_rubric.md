### Part 2 Rubric Grading Task List

## Repository organization
- [ ] Proper hash in Canvas
- [ ] Review Commits -- Everything a PR on Main (no direct commits to main)

## File organization

- [ ] `README.md` with basic info & up to date
- [ ] General Hygiene (no unnecessary files, directories, no name, v2, etc.)
- [ ] `pyproject.toml` - properly configured
- [ ] `Dockerfile` - properly configured
- [ ] `Makefile` - has all commands

## Code execution

- [ ] Code Run -> generates output
- [ ] Output Correct

## Code quality

- [ ] Everything in functions
- [ ] Comments exist and make sense

## Grader Instructions for getting code and verifying branches

1. Clone the repo locally.
1. Verify that there are no commits directly to the main branch. You can do this by either clicking on the main repo page the link which says something like `12 commits`, or you can just go to `https://github.com/[ORG]/[REPO]/commits/main/` to see the commit history. Look to make sure that _everything_ is "Merge pull request #..." and not a direct commit. The initial commit into the repo may be a single commit.
2. Use the commit hash provided by the students in canvas. To checkout at a single location type in, at the command line, in the repository directory: `git checkout COMMIT HASH`.
3. You will be in a detached head state. If you want to verify you are at the correct location, type in `git log -1 --format=%H` which should display the last commit. `git status` should mention that head is detached and the tree is clean.

## Part 2 Rubric 

| Category | Criteria | Points |
|----------|----------|---------|
| Repository Rules | Proper hash in Canvas | 5 |
| | Review Commits -- Everything a PR on Main | 5 |
| | README with basic info & up to date | 5 |
| Directory / File | General Hygiene (no unnecessary files, directories, no name, v2, etc.) | 5 |
| | pyproject.toml | 5 |
| | Dockerfile | 5 |
| | Makefile (has all commands) | 5 |
| Code Execution | Code Run -> generates output | 20 |
| | Output Correct | 10 |
| Code Quality | Everything in functions | 5 |
| | Comments exist and make sense | 5 |
| **Total** | | **75** |