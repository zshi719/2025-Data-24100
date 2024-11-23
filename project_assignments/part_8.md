# Project Part #8

This document outlines the requirements for the final part of our project.

### Coding Standards

During the quarter, you will be expected to adhere to the coding standards found [here](https://github.com/dsi-clinic/the-clinic/blob/main/coding-standards/coding-standards.md) and we will frequently use [this rubric](https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/final-technical-cleanup.md) as a checklist for your code.

### Branches

During this quarter we will be using branches and pull requests in order to submit code. **Any commits directly to the main branch will result in points being deducted.** The one exception to this is the initial commit in the repo.

### Grading

All grading will be done based off a specific commit hash off of the main branch. At the time that an assignment is due students must submit the commit hash associated with their commit to Canvas. You need to submit the _full_ commit hash which is a 40 digit long hash of letters and numbers. It will generally look something like this: `2a2a59af9feacbdd2cd772884b24641c3b75dff7`.

To find the commit hash, you can either use the command line or check GitHub’s commit history.

Note that any changes requested in the grading of the previous part need to be corrected.

## Part VIII: Adding Tests and Autodocs

- Your code must conform to all the requirements of all previous parts, including [Part VII](./part_7.md) 

### Autodocs


### Tests


### Specifications:

#### Updates to Make / Docker
- There are not changes to the dockerfile, but there are two changes required additional make commands required. 
- `make autodocs` should build and start the `mkdocs` server on port 4040 (externally). When `make autodocs` is running it should be possible to go to the local server and see the autodocs server running.
- `make tests` should run the python test suite as described above making sure to report all required parameters.

#### Additional Details

### Additional Fixes

Please correct all of the feedback for Part VII. A portion of the grade will be set to making sure that your code continues to pass those standards.

## How will this be graded

- We will check out the code at the commit hash that you submit.
- All of the previous coding standards will be checked and the all of the previous APIs (`v1`, `v2` and `v3` and `v4`) will also be tested.
- Your code will also be read over to make sure that it conforms to the standards laid out in class. If you want to receive full credit make sure that your code has sound logic, is easy to read, maintains a good separation of concerns and does not violate the DRY principle.
- We will run the `make` commands outlined above and verify that they work according to the standards set out above. 
- We will run an autograder on the endpoints to make sure that they return the correct data and information. This includes types and casing.
- Finally, your code will also be read to make sure that all documentation is up to date and that the code has a consistent set of abstraction standards. 
- No errors or warning should occur in normal operations.
