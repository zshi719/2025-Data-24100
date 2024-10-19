# Project Part #2

This document outlines the requirements for the next part of the project that we will be working on during this quarter. During this quarter we will build a data serving API in a number of parts.

## Coding Standards

During the quarter, you will be expected to adhere to the coding standards found [here](https://github.com/dsi-clinic/the-clinic/blob/main/coding-standards/coding-standards.md) and we will frequently use [this rubric](https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/final-technical-cleanup.md) as a checklist for your code.

At this point we have NOT covered `black`, `flake8` or `pyflakes` so you can ignore all standards regarding those concepts.

However, for this assignment doc strings are required for each function.

## Branches

During this quarter we will be using branches and pull requests in order to submit code. **Any commits directly to the main branch will result in points being deducted.** The one exception to this is the initial commit in the repo.

## Grading

All grading will be done based off a specific commit hash off of the main branch. At the time that an assignment is due students must submit the commit hash associated with their commit to canvas. You need to submit the _full_ commit hash which is a 40 digit long hash of letters and numbers. It will generally look something like this: `2a2a59af9feacbdd2cd772884b24641c3b75dff7`.

To find the commit hash, you can either use the command line or check GitHub’s commit history.


## Part II: Running Flask and basic Make commands

The goal of this assignment is to get the basic `make` commands up and running and to create a mini flask server which sends us back information. You will also be required to leverage environment variables to create an API key for validation.

### Required Make commands

Please create a makefile (in the root) of your repository with the following commands:

1. `build`: This should build the image from the dockerfile in your repo
2. `interactive`: This should start an interactive bash session with the current working directory mounted to `/app/src`
3. `notebook`: This should start a notebook server with the current working directory mounted `/app/src` and ports properly set up so that the notebook can be accessed.
4. `flask`: This should start the flask server, making sure to expose port `4000` so that we can ping the API from outside the container.

Other `Makefile` requirements:
- Each of `interactive`, `notebook` and `flask` should have a dependency on the `build` phony so that if the image is not built it will be built.
- The image name should be set as an environment variable at the top of the `Makefile` and used throughout. 
- The base directory that we are mounting our host volumes to (`/app/src`) should also be set as an environment variable inside the `Makefile`.

### Flask 

We will use the same data that we loaded in [Part I](part_1.md), the 2019 stock data. As in part I your code will need to load the data, making sure to not store any intermediate files and then, once that processing is complete, should server the following three routes via `flask`: 

- `/api/v1/row_count`:
  - Should return (in the body) a JSON object `{ 'row_count' : XXX }` where XXX is the number of rows from the loaded data (as in part I)
- `/api/v1/unique_stock_count`:
  - Should return (in the body) a JSON object `{ 'unique_stock_count' : XXX }` where XXX is the number of unique stocks in the data.
- `/api/v1/row_by_market_count`: Should return (in the body) a JSON object: `{ 'NYSE': xxx, 'NASDAQ': yyy}` where xxx and yyy represent the number of rows for each. 

These routes should _only_ respond to a GET request of the following form:
- Has a `DATA-241-API-KEY` in the header, set from an environment variable _inside the host_, so has to be passed from the host through the `Makefile` and into the container.

Other requirements:
- `flask` needs to be run on port 4000 and that port needs to be exposed when executing `flask` through the `Makefile`.
- Your code must process the data from the original zip files, no intermediate files should be stored.

### Environment variable information

- You can assume that in the host machine the environment variable `DATA_241_API_KEY` set in the host. You will need to pull this in through the `make` command and into the Dockerfile. 
- You should return an http status code of 401 if the request does NOT have the `DATA-241-API-KEY` set or is set to the wrong value.

## How will this be graded

- We will check out the code at the commit hash that you submit.
- All of the previous coding standards (as in [Part I](part_1_rubric.md)) will be checked. 
- All of the requirements listed above will be checked individually.
- Testing `Makefile`. Additionally we will run the following from the command line:
  - `make build` 
  - `make notebook`
  - `make interactive`
  - `make flask`
  - each of these command should run as expected.
- Testing `Flask`. We will run `make flask` and then send API requests to the endpoints above and verify that the return the expected values. We will also send requests which do do not have the correct api key set to make sure that these errors are handled gracefully.

## Ways to test your Requests

The code below is a light framework for how we will test your results. Note that this code was tested on a slightly different project so you may need to modify this. It will be run the host machine.

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