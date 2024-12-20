### Part 1 Rubric Grading Task List

## Repository organization
- [ ] Used only branches -- there should be no commits directly to main
- [ ] Sent a proper commit hash

## File organization

- [ ] `README.md`
  - Tells us a little about your group, and the different folders/files
- [ ] `DockerFile`
  - Has proper instructions to run code and set up proper environment conditions
- [ ] `requirements.txt`
  - Has any and all python/library versions
- [ ] `utils folder`
  - Most code should be in this folder
- [ ] `data folder`
  - All Data in this folder
- [ ] No intermediate files saved during the process

## Code execution

- [ ] Does it run according to the specs? 
   - Runs with - `docker build . -t data241`, then `docker run -t data241`
   - Returns:
      - Rows in combined files
      - Rows from each market 
      - The date at which `BRK.A` recorded its highest open

## Code quality (rough outline, read instructions for more info)

- [ ] Everything in functions
- [ ] Proper naming conventions for files, functions, variables.
  - We will not test `black` or `flake8`/any linting, just an eye check
- [ ] Descriptive comments if any

## Grader Instructions for getting code and verifying branches

1. Clone the repo locally.
1. Verify that there are no commits directly to the main branch. You can do this by either clicking, on the main repo page the link which says something like `12 commits` or you can just go to `https://github.com/[ORG]/[REPO]/commits/main/` to see the commit history. Look to make sure that _everything_ is "Merge pull request #..." and not a direct commit. The initial commit into the repo maybe a single commit.
2. Use the commit hash provided by the students in canvas. To checkout at a single location type in, at the command line, in the repository directory: `git checkout COMMIT HASH`.
3. You will be in a detached head state. If you want to verify you are at the correct location, type in `git log -1 --format=%H` which should display the last commit. `git status` should mention that head is detached and the tree is clean.

## Part 2 Rubric 

| Category | Criteria | Points |
|----------|----------|---------|
| Repository Rules | Proper hash in Canvas | 2 |
| | No Commits to Main | 5 |
| Directory / File | General Hygiene (no unnecessary files, directories, no name, v2, etc.) | 5 |
| | Correct Makefile (Proper env variable, image name, general format.) | 5 |
| | Correct Dockerfile (Proper conventions, port exposures, file calling, etc) | 5 |
| | README.md is up to date with how to run info | 5 |
| | Code Organization (Most in utils folder) | 3 |
| Code Execution | make build (properly builds docker container) | 5 |
| | make notebook (should be able to utilize notebook on the web) | 10 |
| | make interactive (starts interactive bash session) | 10 |
| | make flask (initializes app.py properly) | 15 |
| API Calls | API rowcount call | 5 |
| | API unique_stock_count call | 5 |
| | API row_by_market_count call | 5 |
| | Handles incorrect API key exception | 5 |
| Code Quality | Follows Part 1 conventions (pep8, functions, main block calling) | 10 |
| **Total** | | **100** |