# Project Part #4

This document outlines the requirements for the next part of our data serving API.

### Coding Standards

During the quarter, you will be expected to adhere to the coding standards found [here](https://github.com/dsi-clinic/the-clinic/blob/main/coding-standards/coding-standards.md) and we will frequently use [this rubric](https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/final-technical-cleanup.md) as a checklist for your code.

### Branches

During this quarter we will be using branches and pull requests in order to submit code. **Any commits directly to the main branch will result in points being deducted.** 

### Grading

All grading will be done based on a specific commit hash off of the main branch. At the time that an assignment is due students must submit the commit hash associated with their commit to Canvas. You need to submit the _full_ commit hash which is a 40-digit-long hash of letters and numbers. It will generally look something like this: `2a2a59af9feacbdd2cd772884b24641c3b75dff7`.

To find the commit hash, you can either use the command line or check GitHub's commit history.

Note that any changes requested in the grading of the previous part need to be corrected.

## Part IV: Adding a DB

The goal of this assignment is to _remove the dependency on `pandas` for storing data_.

While you are welcome to use `pandas` to manipulate data _after_ a select statement, you may NOT use it to load data into the database. The database file itself should not be in the git repo (we recommend using `.gitignore` to avoid this).

Your code must conform to all the requirements of all previous parts, including [Part III](./part_3.md), and must address all feedback received from Part III.

### Specific Details:

#### Updates to Make / Docker
- You will need to ensure that SQLite is available inside your container by updating your Dockerfile if necessary. Note that `sqlite3` is part of Python's standard library, but you may need to ensure the SQLite system library is installed.
- You need to add the following `make` commands:
  - `make db_create`: This creates the database file (`stocks.db`) and associated tables.
    - This should only create a database file if one does not exist. If the file already exists, it should raise an error.
    - This should also create a table (`stocks`) for storing the stocks data. 
    - Should be placed in a location that makes sense given your overall file structure.
    - Should be in a location that is _mounted as a volume_ so that when your container is destroyed the data is not lost. 
  - `make db_load`: This loads the data from ZIP files to the table in `stocks`.
  - `make db_rm`: This deletes the database file.
  - `make db_clean`: This deletes the SQLite database file and reloads the data. In other words, it should run the `rm`, `create` and `load` commands in order. If the database does not already exist it should not return an error.
  - `make db_interactive`: This should run an interactive session of the database with the correct database open.
- All of the above make commands should be accessed via a Python script `db_manage.py` that is called from the Makefile and executed inside the Docker container.
  - `db_manage.py` should take a single argument (`db_create`, `db_load`, etc.) and then run Python code to achieve the goals of the program. So it will be called, via `make`, with a command of the form below which will depend on where the file is located, etc. 

``` makefile
db_load: build
	docker run $(COMMON_DOCKER_FLAGS) $(IMAGE_NAME) \
		uv run python /app/src/app/data_utils/db_manage.py db_load
```

#### Updates to Flask

- None of the endpoint definitions should change.
- `pandas` should _not_ be used in any of the creation, loading or direct accessing commands. For example, when you need data there should (eventually, behind some levels of abstraction) be an SQL query executed (and specifically an SQL query that you wrote). 
- Do NOT use the `pandas.read_sql` command (or any other `pandas` command that directly communicates with the database). Part of the task at hand is building your own non-pandas connector.
- Make sure to think through the code before writing it down. What abstraction level do you want? How do you define it? Where are you defining your separation of concerns?
- There should not be a global DataFrame variable or a global connection. When a route calls the database it should be using SQL.
- When running Flask via `make flask` the server should start up quickly (less than 10 seconds). Responses should all take less than 2 seconds.
- You should never load the entire dataset into a DataFrame. You need to use SQL commands to only select the relevant data.

#### Other Notes

- As mentioned in class, it is strongly advised that you add an index to the `stocks` table to make sure that your code is performant.
- No request should take more than a few seconds (say, 5). If it does, you should add an index to the table to make sure that the query is faster.

### Additional Fixes

Please correct all of the feedback for Part III. A portion of the grade will be set to making sure that your code continues to pass those standards.

## How will this be graded

- We will check out the code at the commit hash that you submit.
- We will then run `make db_clean` and `make flask` in order to get the Flask server up and running.
- All of the previous coding standards will be checked and the API as in [Part III](./part_3.md) should be functional. This includes testing the `Makefile` behavior and the Flask API endpoints that were required in Part III.
- Your code will also be read over to make sure that it conforms to the standards laid out in class. If you want to receive full credit make sure that your code has sound logic, is easy to read, maintains a good separation of concerns and does not violate the DRY principle.
- Extraneous code, such as that generated by an LLM doing nothing, will be heavily penalized. 
- We will run the `make` commands outlined above and verify that they work according to the standards set out above. 
- We will run an autograder on the endpoints to make sure that they return the correct data and information.
- Finally, your code will also be read to make sure that all documentation is up to date and that the code has a consistent set of abstraction standards. 
- No errors or warnings should occur in normal operations.
