### Part 1 Rubric Grading Task List

NOTE: Rewrite rubrics to help graders. Be more specific about several ongoing issues (branch protection violations, separation of concerns, unused code, inconsistent abstractions, etc.).


## Repository organization
- [ ] Used only branches -- there should be no commits directly to main
- [ ] There was a pull request
  - The branch can still exist, but we will take off points in future grading if it is reused.
- [ ] Sent a proper commit hash

## File organization

- [ ] `README.md`
  - Tells us a little about your group, and the different folders/files
- [ ] `DockerFile`
  - Has proper instructions to run code and set up proper environment conditions (not too much for this part)
- [ ] `pyproject.toml`
  - Has any and all python/library versions
- [ ] `utils folder`
  - All code should be in this folder
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
      - Identify the date on which the stock IBM had it's highest `close` price.

## Code quality (rough outline, read instructions for more info)

- [ ] Everything in functions
- [ ] Proper naming conventions for files, functions, variables.
  - We will not test `black` or `flake8`/any linting, just an eye check
- [ ] Descriptive comments if any

## Grader Instructions for getting code and verifying branches

1. Clone the repo locally.
1. Verify that there are no commits directly to the main branch. You can do this by either clicking on the main repo page the link which says something like `12 commits`, or you can just go to `https://github.com/[ORG]/[REPO]/commits/main/` to see the commit history. Look to make sure that _everything_ is "Merge pull request #..." and not a direct commit. The initial commit into the repo may be a single commit.
2. Use the commit hash provided by the students in canvas. To checkout at a single location type in, at the command line, in the repository directory: `git checkout COMMIT HASH`.
3. You will be in a detached head state. If you want to verify you are at the correct location, type in `git log -1 --format=%H` which should display the last commit. `git status` should mention that head is detached and the tree is clean.

## Rubric

| Category | Criteria | Points |
|----------|----------|---------|
| **Repository Setup** | Proper hash in Canvas | 5 |
| | Review Commits -- Everything a PR on Main | 5 |
| | README with basic info | 5 |
| **Directory / File** | General Hygiene (no unnecessary files, directories, no name, v2, etc.) | 5 |
| | pyproject.toml | 5 |
| | Dockerfile | 5 |
| **Code Execution** | Code Run -> generates output | 10 |
| | Output Correct | 10 |
| **Code Quality** | Everything in functions | 5 |
| | Comments exist and make sense | 5 |
| | All calling done with main block (`if __name__ == "__main__"`) | 5 |
| **Total** | | **65** |

