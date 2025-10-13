# Week #3 Lesson Plan

VERIFY LEARNING OBJECTIVES ARE DEEP ENOUGH

## Overview
- Monday night the first part of the project is due.
- Wednesday there will be a quiz. Quizzes are cumulative and cover the material up to and including the previous week (Week 2).

## Resources

## Learning objectives

- Sharing files and network ports from the host to a container using `-e` and `-v`. Use `-v` to mount the present working directory to the container.
  - For each type of data sharing, understand whether it is done at build time, at run time, or live.
- Build a container that can run Jupyter and access it from the host.
- Use `make` and Makefiles to simplify interactions with Docker.
- Three components of our (simplified) Makefile: environment variables, PHONY definition, and commands.
- Reference environment variables in a Makefile.
- Reference the current working directory in a Makefile.
- How to write basic `make` commands and how to create basic dependencies between make commands.
- Build a container that can run Flask and set a simple route that accepts GET and returns data.
- Parts of an HTTP request (type, headers, body, etc.). Know how to reference them on the server side using Flask.
- Use basic Python logic (not a Flask library) for header-based authentication and return a 401 if not authorized.
- Understand the line continuation marker in Bash (`\\`).
- Get Jupyter and Flask running on your own machine inside a Docker container using Make. Be able to explain the options and flags required to get each running.

## Lecture notes

[Day 5](../class_notes/05_docker_make.md)

[Day 6](../class_notes/06_flask_1.md)


## Quizzable concepts
- As always, the quiz is cumulative.
- Given a Bash-based command, how do I create a Make command based on it?
- List the parts of a request and response object. Describe what each is.
- In Flask, create a route that responds to a GET request with a particular status code.
- In Flask, create a route that parses the headers of a GET request and applies a specific Python-based transformation/change to the body.
- In Flask, create a route that returns a particular status code conditional on the header.
- Note #1: While you are expected to understand headers, query parameters, and the body, during the quiz you will only be expected to recall the specifics of how to work with the headers. However, you are also expected to know the information in [this note](../class_notes/06_flask_1.md#important-notes-on-headers).
- Things I will NOT quiz: specific options to Jupyter or Flask that are required to get them started inside Docker. While I may provide code that presents this information, you will not be required to recall what they are doing.
- Example question: The file `logs/process.log` is a text file that contains information about our process. If a line contains the phrase `ERROR`, this means that our process had an error. Given the Makefile below, please write what needs to change to add a make command `last_10_errors` that shows the last ten errors.

```makefile
ENV_NAME=development
API_KEY=12345

.PHONY=run_process

run_process:
    python run_process.py
```

We will need to update one line and add another:

```makefile
ENV_NAME=development
API_KEY=12345

.PHONY=run_process last_10_errors

run_process:
    python run_process.py

last_10_errors:
    cat logs/process.log | grep ERROR | tail
```

- Example: We have a working Flask server and we wish to add a route `/check_api_status`. This should call the Python function (`api_status`) that was imported and, if it returns `True` (boolean), respond with a 200; if it returns `False` (boolean), respond with a 500. Please complete the code below. In both cases, the body and headers can be empty/None.

```python
from flask import (
    Flask,
    request,
    Response
)

from api_status_module import (
  api_status,
  api_data
)

app = Flask(__name__)

### INSERT YOUR CODE HERE

@app.route('/data', methods=['GET'])
def return_data_from_api():

    text_data = api_data()

    return Response(text_data, status=200,
                    headers={'Content-Type': 'text/html'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Answer: We can model our answer off the `Response` object presented:

```python
@app.route('/check_api_status')
def check_api_status():
    if api_status():
        return Response(status=200)
    else:
        return Response(status=500)
```

- Example: Using the same problem setup as above, also check that the `/check_api_status` route verifies the existence of a key in the headers called `API-KEY` (case-insensitive). It does not matter what the value is; only verify that the key exists. If the key does not exist, return a 401 status code.

Updated Answer:

```python
@app.route('/check_api_status')
def check_api_status():
    if 'API-KEY' not in [key.upper() for key in request.headers.keys()]:
        return Response(status=401)

    if api_status():
        return Response(status=200)
    else:
        return Response(status=500)
```

- As a reminder, headers should not have underscores and we should handle case on the processing side.