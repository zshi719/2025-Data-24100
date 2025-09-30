# Project Part #3

This document outlines the requirements for the next part of our data serving API.

### Coding standards

During the quarter, you will be expected to adhere to the coding standards found [here](https://github.com/dsi-clinic/the-clinic/blob/main/coding-standards/coding-standards.md) and we will frequently use [this rubric](https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/final-technical-cleanup.md) as a checklist for your code.

At this point we have NOT covered `black`, `flake8`, or `pyflakes`, so you can ignore all standards regarding those concepts.

However, for this assignment, docstrings are required for each function.

### Branches

During this quarter we will be using branches and pull requests in order to submit code. **Any commits directly to the main branch will result in points being deducted.** 

### Grading

All grading will be done based on a specific commit hash off of the main branch. At the time that an assignment is due, students must submit the commit hash associated with their commit to Canvas. You need to submit the full commit hash, which is a 40-digit hash of letters and numbers. It will generally look something like this: `2a2a59af9feacbdd2cd772884b24641c3b75dff7`.

To find the commit hash, you can either use the command line or check GitHub’s commit history.

Note that any changes requested in the grading of the previous part need to be corrected.

## Part III: Running Flask and basic Make commands

The goal of this assignment is to get the basic `make` commands up and running and to create a mini Flask server that sends back information. You will also be required to leverage environment variables to create an API key for validation.

### Required Make commands

Please create a Makefile (in the root) of your repository with the following commands:

1. `build`: Build the image from the Dockerfile in your repo.
2. `interactive`: Start an interactive Bash session with the current working directory mounted to `/app/src`.
3. `notebook`: Start a notebook server with the current working directory mounted to `/app/src` and ports properly set up so that the notebook can be accessed.
4. `flask`: Start the Flask server, exposing port `4000` so that we can ping the API from outside the container.


Other Makefile requirements:
- Each of `interactive`, `notebook`, and `flask` should have a dependency on the `build` phony so that if the image is not built it will be built.
- The image name should be set as an environment variable at the top of the Makefile and used throughout.
- The base directory that we are mounting our host volumes to (`/app/src`) should also be set as an environment variable inside the Makefile.

### Flask

We will be using TWO years of data in the `project_data` (2019 and 2018) directory to build the routes listed below. Make sure that you have only two years running and loaded as part of this project.

**IMPORTANT NOTE** One major change is that you need to set an environment variable, similar to the `DATA_241_API_KEY` called `RAW_DATA_DIR` which should be set to a location on the user's host machine where the ZIP files are stored. Do NOT store any of the zip files in the repo (the previous ones should be removed).

As in Part I, your code will need to load the data, making sure not to store any intermediate files. Once that processing is complete, it should serve the following routes via Flask.

- Note: The `v1` API needs to be corrected with any feedback that was provided. Please look at [Part II](part_2.md) to verify that your code is still compliant.

- `/api/v2/{YEAR}`
  - Your code should accept any of the years in question and return a `404` if a year is passed which is not in the data. There should be a message in the body explaining what the error is.
  - This should return the count of rows for the specific year.
  - It should return as a JSON object of the form `{'year' : INT, 'count': row_count}`.
- `/api/v2/open/{SYMBOL}`
  - This should return all the open prices for a particular stock (across all years) in the following format:
    - `{ 'symbol': XXXX, 'price_info' : [ {'date' : date, 'open': open_price}, {'date' : date, 'open' : open_price}, ...] }`
    - Make sure that the date is formatted as a string in `Y-m-d` format.
  - If the symbol provided is NOT in the data then it should return a `404`.
- `/api/v2/close/{SYMBOL}`
  - This should return all the close prices and should have a similar format as the `open` API end point, but rather than saying `open` it should say `close` and report the `close` price from the data.
- `/api/v2/high/{SYMBOL}`
  - This should return all the close prices and should have a similar format as the `open` API end point, but rather than saying `open` it should say `high` and report the `high` price from the data.
- `/api/v2/low/{SYMBOL}`
  - This should return all the close prices and should have a similar format as the `open` API end point, but rather than saying `open` it should say `low` and report the `low` price from the data.

All of these routes should _only_ respond to a GET request of the following form:
- Has a `DATA-241-API-KEY` in the header, set from an environment variable _inside the host_, so has to be passed from the host through the `Makefile` and into the container (same as in Part 2).

Other requirements:
- Flask needs to be run on port 4000, and that port needs to be exposed when executing Flask through the Makefile.
- Your code must process the data from the original ZIP files; no intermediate files should be stored.
- Your authorization code needs to be in the form of a decorator imported from a different file.
- The code needs to follow the DRY principle as described in class.
- Your repo should use subdirectories to store Python code of differing function. There should be a single `app.py` in the root of the repository, and it should be only a few lines. It should look something like the following:

```
from flask import Flask
from stock_app.api.v1.routes import register_v1_routes
from stock_app.api.v1.routes import register_v2_routes

def create_app():
    app = Flask(__name__)

    # Register routes
    register_v1_routes(app)
    register_v2_routes(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

```

### Environment variable information

- You can assume that on the host machine the environment variable `DATA_241_API_KEY` is set. You will need to pass this in through the `make` command and into the Dockerfile.
- You should return an HTTP status code of 401 if the request does not have the `DATA-241-API-KEY` set, or it is set to the wrong value.
- The directory `RAW_DATA_DIR` needs to be set on the host machine and then pulled through the `make` command. This should be location of where the ZIP files are, on the host machine. ZIP files should NOT be present in the repo (make sure to remove the old ones).

## How will this be graded

- We will check out the code at the commit hash that you submit.
- All of the previous coding standards (as in [Part I](part_1_rubric.md) and Part II) will be checked.
- All of the requirements listed above will be checked individually.
- We will verify that endpoints work and generate the correct response for 2019 and 2020 data.
- Verification of data location.
- Extraneous code, such as that generated by an LLM doing nothing, will be heavily penalized. 
- Testing Makefile. Additionally, we will run the following from the command line. Each should follow the behavior outlined in class and previous versions of the project.
  - `make build` 
  - `make notebook`
  - `make interactive`
  - `make flask`
- Testing Flask. We will run `make flask` and then send API requests to the endpoints above and verify that they return the expected values. We will also send requests that do not have the correct API key set to make sure that these errors are handled gracefully.
- No errors or warnings should occur in normal operations.

## Ways to test your requests

The code below is a light framework for how we will test your results. Note that this code was tested on a slightly different project, so you may need to modify it. It will be run on the host machine.

```
import requests

def make_get_request(endpoint, api_key):
    # Base URL for the Flask app running in Docker
    base_url = "http://localhost:4000"  
    full_url = f"{base_url}{endpoint}"

    # Define the headers
    headers = {
        'DATA-241-API-KEY': api_key,  # API key in the header
        'Content-Type': 'application/json'
    }

    try:
        # Make the GET request
        response = requests.get(full_url, headers=headers)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Print the response status code
        print(f"Status Code: {response.status_code}")
        
        # Print the response content
        print("Response Content:")
        print(response.json)
        
        return response

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    api_key = os.environ['DATA_241_API_KEY']
    endpoint = '/api/v1/row_count'
    make_get_request(endpoint, api_key)

```