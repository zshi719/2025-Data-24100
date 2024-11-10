# Project Part #1

This document outlines the requirements for the first part of the project that we will be working on during this quarter. 

During this quarter we will build a data serving API in a number of parts. In this first part we will require you and your team to create an initial repository in Github, invite us (TAs and professor) to it, set it up properly and put some code inside.

## Coding Standards

During the quarter, you will be expected to adhere to the coding standards found [here](https://github.com/dsi-clinic/the-clinic/blob/main/coding-standards/coding-standards.md) and we will frequently use [this rubric](https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/final-technical-cleanup.md) as a checklist for your code.

However, at this point we have NOT covered `black`, `flake8` or `pyflakes` so you can ignore all standards regarding those concepts. We also have not covered doc strings so that will not be graded at this point.

## Branches

During this quarter we will be using branches and pull requests in order to submit code. **Any commits directly to the main branch will result in points being deducted.** The one exception to this is the initial commit in the repo.

## Grading

All grading will be done based off a specific commit hash off of the main branch. At the time that an assignment is due students must submit the commit hash associated with their commit to canvas. You need to submit the _full_ commit hash which is a 40 digit long hash of letters and numbers. It will generally look something like this: `2a2a59af9feacbdd2cd772884b24641c3b75dff7`.

To find the commit hash, you can either use the command line or check GitHub’s commit history.

## Part #1

Please complete the following:

### Create a group on Canvas

Please organize yourself in a group in Canvas of between 2-4 members. I'd recommend 3 or 4, but will allow down to two. No groups of more than four are allowed. 

### Create a Github repo

The repository needs to:

  - Have the name in the following format: `data_241_autumn_2024_GROUP_NUMBER` is the number from the Canvas group.
  - Must invite both TAs (`rrhuang`, `hszh01`), the grader (`giomhern`) and the Professor (`nickross`).
  - Must be set to _private_.
  - Must have [a branch protection _rule_ on the main branch](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule) set which requires users to submit a pull request before merging. Note that this needs only apply to the _main_ branch.

### Note on branch protections:

If you are on the free tier of GitHub then branch protections are not available to you. There are three options:
  1. Stay on the free plan and NOT use branch protections. No points will be taken away for not having the branch protections, but you will still be deducted points for committing directly to main.
  2 You can pay for github for the quarter.
  3. If **ONE person from your group emails me their github ID by Saturday night** I will create a private repo with them as the owner inside the paid DSI Org. This will allow you to get branch protections and you'll be able to administer the repo yourself.

I'd strongly recommend doing either the second or the third, but it is your group's choice.

### Initial Code

The purpose of this exercise is to start processing the data that we will be using as part of this class. In the [project data directory](../project_data/) you can find the file `NASDAQ_2019.zip` and another file `NYSE_2019.zip`. These files contain information about public stock prices in 2019.

When your `Dockerfile` is built and run it should unzip these files (in python), put the data in these two files into a single Pandas dataframe and then report a number of summary statistics (listed below) to the terminal. 

Specifically, your code needs to `unzip` the zip files (using a python library of your choice). The files inside the zip file need to then be loaded into a single dataframe with all of the columns from the original data (with the correct data formats for each column). You should also add an additional column "market" which should be set to either NASDAQ or NYSE dependent on which file the row came from.

Please also make sure that the `README.md` file conforms to the code quality information above. 

### Repository set up

Your repository should have the following structure:

```
project_root/
├── README.md
├── Dockerfile
├── requirements.txt
├── utils/
│   └── eda_2019.py
└── data/
    └── raw_data/
        ├── NYSE_2019.zip
        └── NASDAQ_2019.zip
```

Other files may be appropriate, but the above should be the rough structure. Importantly, no intermediate files should be saved to the repo.

### Summary Statistics to report. 

Your code should report the following information:

* How many rows are in the combined dataset?
* How many rows are sourced from each market (e.g. How many rows from the NYSE dataset and how many rows from the NASDAQ dataset)? 
* Identify the date on which the stock BRK.A recorded its highest `open` price.

## Part #1 Grading

Code Grading:
  - Your code will be checked out at the git hash (on main) provided in your submission.
  - We will then run:
    - `docker build . -t data241` 
    - `docker run -t data241`
  - The `run` command should print, to the terminal, the summary statistics above (please add some logging so that we know which numbers we are looking at).

Repo/Git Grading:
  - We will review your use of Github (branches, etc.) to make sure that it conforms with the standards above.
  - Does your code follow the best practices of the coding standards as well as the information laid out above?

Code Quality:
  - We will read your code making sure that it fulfills the code quality checklists above (ignore the sections that we have not gotten to yet).
  - We will also look to make sure that the code followed the requirements above.
  - No errors or warning should occur in normal operations.

Other:
  - Add you and your team to Canvas.