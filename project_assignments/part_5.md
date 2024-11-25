# Project Part #5

This document outlines the requirements for the next part of our data serving API.

### Coding Standards

During the quarter, you will be expected to adhere to the coding standards found [here](https://github.com/dsi-clinic/the-clinic/blob/main/coding-standards/coding-standards.md) and we will frequently use [this rubric](https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/final-technical-cleanup.md) as a checklist for your code.

### Branches

During this quarter we will be using branches and pull requests in order to submit code. **Any commits directly to the main branch will result in points being deducted.** The one exception to this is the initial commit in the repo.

### Grading

All grading will be done based off a specific commit hash off of the main branch. At the time that an assignment is due students must submit the commit hash associated with their commit to canvas. You need to submit the _full_ commit hash which is a 40 digit long hash of letters and numbers. It will generally look something like this: `2a2a59af9feacbdd2cd772884b24641c3b75dff7`.

To find the commit hash, you can either use the command line or check GitHub’s commit history.

Note that any changes requested in the grading of the previous part need to be corrected.

## Part V: Adding a DB

The goal of this assignment is to _remove the dependency on `pandas` for storing data_.

While you are welcome to use `pandas` to manipulate data _after_ a select statement, you may NOT use it to load data into the database.

**IMPORTANT NOTE:** Depending on the age of your group members computers you may struggle to load and use all the data. If this is the case for your group, you can create an environment variable called "DOWNSAMPLE" which when set equal to 1 will only load data from 2016 and 2017. This smaller subset of the data should be performant on everyone's computer. Using "DOWNSAMPLE" is optional, the environment variable is a flag for the grader to know what is testable.

Your code must conform to all the requirements of all previous parts, including [Part IV](./part_4.md) 

### Specific Details:

#### Updates to Make / Docker
- You will need to install all necessary packages (`sqlite3`) inside your container by updating your dockerfile.
- You need to add the following `make` commands:
  - `make db_create`: This creates the database file (`stocks.db`) and associated tables.
    - This creates a database file (but only if one does not exist, it should raise an error if the file exists)
    - This should also create a table (`stocks`) for storing the stocks data. 
    - Should be placed in a location that makes sense given your overall file structure
    - Should be in a location that is _mounted as a volume_ so that when your container is destroyed the data is not lost. 
  - `make db_load`: this loads the data from zip files to the table in `stocks`.
  - `make db_rm`: this deletes the database file.
  - `make db_clean`: this deletes the sqlite database file and reloads the data. In other words it should run the `rm`, `create` and `load` commands in order. If the database does not already exist it should _not_ return an error.
  - `make db_interactive`: This should run an interactive session of the database with the correct database open.
- All of the above make commands should be accessed via a python script `db_manage.py` that is called from the makefile and executed _inside the docker container_.
  - `db_manage.py` should take a single argument (`db_create`, `db_load`, etc.) and then run python code to achieve the goals of the program. So it will be called, via `make` with a command of the form below which will depend on where the file is located, etc. 

```
db_load: build
	docker run $(COMMON_DOCKER_FLAGS) $(IMAGE_NAME) \
		python /app/src/app/data_utils/db_manage.py db_load
```

#### Updates to Flask

- None of the end point definitions should change.
- `pandas` should _not_ be used in any of the creation, loading or direct accessing commands. E.g. when you need data there should (eventually, behind some levels of abstraction) an SQL query executed (and specifically an SQL query that _you_ wrote). 
- Do NOT use the `pandas.read_sql` command (or any other `pandas` command that directly communicates with the database). Part of the task at hand is building your own non-pandas connector.
- Make sure to think through the code before writing it down. What abstraction level do you want? How do you define it? Where are you defining your separation of concerns?
- There should not be a global data frame variable or a global connection. When a route calls the database it should be using sql.
- When running flask via `make flask` the server should start up quickly (less than 10 seconds). Responses should should all take less than 2 seconds.

#### Other Notes:

- As mentioned in class I strongly advise you to add an index to the `stocks` table to make sure that your code is performant.
- No request should take more than a few seconds (say 5). If it does you should add an index to the table to make sure that the query is faster.

### Additional Fixes

Please correct all of the feedback for Part IV. A portion of the grade will be set to making sure that your code continues to pass those standards.

## How will this be graded

- We will check out the code at the commit hash that you submit.
- All of the previous coding standards will be checked and the API as in [Part III](../project_assignments/part_3.md) should be functional. This includes testing the `Makefile` behavior and the flask API endpoints that were required in Part IV
- We will run `ruff`, using the `pyproject.toml` file above to make sure that your code conforms to the standards therein.
- We will also verify that the `.pre-commit-hook.yaml` is in the repo and able to be installed and used.
- Your code will also be read over to make sure that it conforms to the standards laid out in class. If you want to receive full credit make sure that your code has sound logic, is easy to read, maintains a good separation of concerns and does not violate the DRY principle.
- We will run the `make` commands outlined above and verify that they work according to the standards set out above. 
- We will run an autograder on the endpoints to make sure that they return the correct data and information.
- Finally, your code will also be read to make sure that all documentation is up to date and that the code has a consistent set of abstraction standards. 
- No errors or warning should occur in normal operations.
- The database file itself should _NOT_ be committed to the repo.
- You should never load the entire dataset into a dataframe. You need to use sql commands to only select the relevant data.