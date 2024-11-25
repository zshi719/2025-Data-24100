# Project Part #4

This document outlines the requirements for the next part of our data serving API.

### Coding Standards

During the quarter, you will be expected to adhere to the coding s- You should never load the entire dataset into a dataframe. You need to use sql commands to only select the relevant data.tandards found [here](https://github.com/dsi-clinic/the-clinic/blob/main/coding-standards/coding-standards.md) and we will frequently use [this rubric](https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/final-technical-cleanup.md) as a checklist for your code.

### Branches

During this quarter we will be using branches and pull requests in order to submit code. **Any commits directly to the main branch will result in points being deducted.** The one exception to this is the initial commit in the repo.

### Grading

All grading will be done based off a specific commit hash off of the main branch. At the time that an assignment is due students must submit the commit hash associated with their commit to canvas. You need to submit the _full_ commit hash which is a 40 digit long hash of letters and numbers. It will generally look something like this: `2a2a59af9feacbdd2cd772884b24641c3b75dff7`.

To find the commit hash, you can either use the command line or check GitHub’s commit history.

Note that any changes requested in the grading of the previous part need to be corrected.

## Part IV: Linting and documentation

The goal of this assignment is to get your code up to the standards required by ruff, and specifically the [pyproject.toml](./pyproject.toml) as well as implement a pre-commit hook, as per the [pre-commit-config.yaml](./pre-commit-config.yaml) (Note that this file should be hidden and start with a `"."`, but in the repo and this link it does not).

Your code must conform to all the requirements of [Part III](./part_3.md) and there does not need to be any changes to the API, the goal is to get your code in a good space before we begin our next bit addition.

### Additional Fixes

Please correct all of the feedback for Part III. A portion of the grade will be set to making sure that your code continues to pass the standards set by Part III.

## How will this be graded

- We will check out the code at the commit hash that you submit.
- All of the previous coding standards will be checked and the API as in [Part III](../project_assignments/part_3.md) should be functional. This includes testing the `Makefile` behavior and the flask API endpoints that were required in Part III.
- We will run `ruff`, using the `pyproject.toml` file above to make sure that your code conforms to the standards therein.
- We will also verify that the `.pre-commit-hook.yaml` is in the repo and able to be installed and used.
- Your code will also be read over to make sure that it conforms to the standards laid out in class. If you want to receive full credit make sure that your code has sound logic, is easy to read, maintains a good separation of concerns and does not violate the DRY principle.
- All documented code needs to have good faith level of effort that briefly explains the required purpose. Doc strings that say `This is the doc string` or other low-effort submissions will be graded accordingly.
- Your code should also be responsive to changes requested by previous submissions. If you received feedback previously to make a change to the code this change should be present.
- No errors or warning should occur in normal operations.
- You should never load the entire dataset into a dataframe. You need to use sql commands to only select the relevant data.