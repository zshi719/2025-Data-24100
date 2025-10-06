# Project Part #1

This document outlines the requirements for the first part of the project that we will be working on during this quarter.

During this quarter we will build a data-serving API in a number of parts. In this first part we will require you and your team to create an initial repository in GitHub, invite us (TAs and instructor) to it, set it up properly, and put some code inside.

## Coding standards

During the quarter, you will be expected to adhere to the coding standards found [here](https://github.com/dsi-clinic/the-clinic/blob/main/coding-standards/coding-standards.md) and we will frequently use [this rubric](https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/final-technical-cleanup.md) as a checklist for your code.

However, at this point we have NOT covered `black`, `flake8`, or `pyflakes`, so you can ignore all standards regarding those concepts. We also have not covered docstrings, so that will not be graded at this point.

## Branches

During this quarter we will be using branches and pull requests in order to submit code. **Any commits directly to the main branch will result in points being deducted.** The one exception to this is the initial commit in the repo.

### A note on branch protections

Branch protections are turned on for your branch, meaning that all commits must be completed with a pull request. Branch protections are a common method of (1) preventing accidental changes to your most important code, (2) enforcing better documentation, and (3) providing a standard pathway for code deployment.

Because of branch protections it is imperative (unless you like reduplicating your work) that you pull your code frequently and have intentionality around your coding practices.

## Grading

All grading will be done based on a specific commit hash off of the main branch. At the time that an assignment is due, students must submit the commit hash associated with their commit to Canvas. You need to submit the full commit hash, which is a 40-digit hash of letters and numbers. It will generally look something like this: `2a2a59af9feacbdd2cd772884b24641c3b75dff7`.

To find the commit hash, you can either use the command line or check GitHub’s commit history.

### Initial Code

The purpose of this exercise is to start processing the data that we will be using as part of this class. In the [project data directory](../project_data/) you can find the file `NASDAQ_2019.zip` and another file `NYSE_2019.zip`. These files contain information about public stock prices in 2019.

When your `Dockerfile` is built and run, it should unzip these files (in Python), put the data in these two files into a single pandas DataFrame, and then report a number of summary statistics (listed below) to the terminal.

Specifically, your code needs to `unzip` the ZIP files (using a Python library of your choice). The files inside the ZIP file then need to be loaded into a single DataFrame with all of the columns from the original data (with the correct data formats for each column). You should also add an additional column `market`, which should be set to either NASDAQ or NYSE depending on which file the row came from.

Please also make sure that the `README.md` file conforms to the code quality information above.

### Repository setup

Your repository should have the following structure:

```
project_root/
├── README.md
├── Dockerfile
├── pyproject.toml
├── utils/
│   └── eda_2018.py
└── data/
    └── raw_data/
        ├── NYSE_2018.zip
        └── NASDAQ_2018.zip
```

Other files may be appropriate, but the above should be the rough structure. Importantly, no intermediate files should be saved to the repository.

### Summary statistics to report

Your code should report the following information:

* How many rows are in the combined dataset?
* How many rows are sourced from each market (e.g., how many rows from the NYSE dataset and how many rows from the NASDAQ dataset)?
* Identify the date on which the stock BRK.A recorded its lowest `open` price. 
* Identify the date on which the stock IBM had it's highest `close` price.

## Part #1 grading

Code Grading:
  - Your code will be checked out at the Git hash (on main) provided in your submission.
  - We will then run:
    - `docker build . -t data241` 
    - `docker run -t data241`
  - The `run` command should print to the terminal the summary statistics above (please add some logging so that we know which numbers we are looking at).

Repo/Git Grading:
  - We will review your use of GitHub (branches, etc.) to make sure that it conforms with the standards above.
  - Does your code follow the best practices of the coding standards as well as the information laid out above?

Code Quality:
  - We will read your code making sure that it fulfills the code quality checklists above (ignore the sections that we have not gotten to yet).
  - We will also look to make sure that the code followed the requirements above.
  - No errors or warnings should occur in normal operations.
