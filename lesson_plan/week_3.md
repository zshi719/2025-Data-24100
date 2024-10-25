# Week #3 Lesson Plan

## Overview
- Monday night the first part of the project is required to be turned in.
- Thursday there will be a quiz. Quizzes are cumulative and cover the material up-to and including the previous week (Week 2).

## Resources

## Learning Objectives

- Sharing files and network ports from the host to a container using `-e` and `-v`. Use `-v` to mount the present working directory to the container.
  - Understand for each type of data sharing if it is done at build, at run or is live.
- Build a container that can run `jupyter` and access it from the host.
- Use `make` and Makefiles to simplify interactions with Docker.
- Three components of our (simplified) Makefile (env vars, Phony definition and commands).
- Reference environment variables in a Makefile
- Reference the current working directory in a Makefile.
- How to write a basic `make` commands and how to create basic dependencies between make files. 
- Build a container that can run `flask` and set a simple route that accepts GET and returns data.
- Parts of an `http` request (type, headers, body, etc.). Know how to reference them on the server side using `flask`.
- Use basic python logic (not a `flask` library) for header-based authentication and return a 400 if not authorized.
- Understand the line continuation marker in bash (`\`)
- Get `jupyter` and `flask` running on your own machine inside a `docker` container using Make. Be able to explain the options and flags required to get each running.

## Lecture Notes

[Day 5](../class_notes/05_docker_make.md)

[Day 6](../class_notes/06_flask_1.md)


## Quizzable Concepts
- As always, the quiz is cumulative.
- Given a `bash` based-command, how do I create a Make command based on it?
- List the parts of a request and response object. Describe what each is.
- In `flask` create a route which responds to a GET command with a particular status code.
- In `flask` create a route which parses the header of a GET request and applies a specific python based transformation / change to the body.
- In `flask` create a route which returns a particular status code conditional on the header.
- Note #1: While you are expected to understand header, query parameters and the body, during the quiz you will _only be expected to recall the specifics of how to work with the headers._  However you are also expected to know the information in [this note](../class_notes/06_flask_1.md#important-notes-on-headers).
- Things which I will NOT quiz: specific options to `jupyter` or `flask` that are required to get it started inside docker. While I may provide code that contains that presents this information you will not be required to recall what they are doing.
- Example question. The file `logs/process.log` is a text file which contains information about our process. If a line contains the phrase `ERROR` this means that our process had an error in it. Given the Makefile below, please write what needs to change to add a make command `last_10_errors` which shows the last ten errors?

```
ENV_NAME=development
API_KEY=12345

.PHONY=run_process

run_process:
    python run_process.py
```

We will need to update one line and add another:

```
ENV_NAME=development
API_KEY=12345

.PHONY=run process last_10_errors

run_process:
    python run_process.py

last_10_errors:
    cat logs/process.log | grep ERROR | tail
```

- Example: We have a working `flask` server and we wish to add a route `/check_api_status`. This should call the python function (`api_status`) which was imported and if it returns `True` (boolean) then respond with a 200 and if returns `False` (boolean) then respond with a 500. Please complete the code below. In both cases the body and headers can be Empty/None.

```
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

    return Response(data, status=200,
                    headers={'Content-type': 'text/html'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Answer: We can model our answer off of the `Response` object presented:

```
@app.route('/check_api_status')
def api_status():
    if api_status():
        return Response(status=200)
    else:
        return Response(status=500)
```

- Example, the same problem setup as above. However, this time we also want the `/check_api_status` route to check for there being a key in the header called `API-KEY` in any case. It does not matter what the value is, we only want to check for this key existing in the header. If the key does not exist, return a _401_ status code.

Updated Answer:

```
@app.route('/check_api_status')
def api_status():
    if 'API-KEY' not in [key.upper() for key in request.headers.keys()]:
        return Response(status=401)

    if api_status():
        return Response(status=200)
    else:
        return Response(status=500)
```

- As a reminder headers should not have underscores and we should handle case on the processing side.