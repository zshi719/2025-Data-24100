# Pytest 

- We will continue our discussion of testing by going into the details of how to implement testing inside our system. There are a number of things that we will need to do to get this complete, each will be highlighted below.
  - `requirements.txt` update
  - file structure 
  - `makefile` update
  - `test/test.py` file

## Requirements.txt

- We will need to add two packages to get our testing to work: `pytest` and `pytest-cov`.
- The second of these handles the coverage calculations that we are interested in seeing.
- As per usual, to get these I went into `interactive` mode and ran `pip install` followed by `pip freeze` to identify the package.

```
pytest==8.3.4
pytest-cov==6.0.0
```

## File structure

- When running tests we generally put the test code outside of the main directory of the source code. 
- For big projects this makes lots of sense, there is already so much code in the repo that breaking it apart at a higher abstraction / file system level will make our code a lot easier to read.
- A common framework for how to organize files for testing is a mirror strategy, such as the below:

```
.
├── app/
│   ├── routes/
│   │   └── stock_routes.py
│   └── helpers/
│   │   └── decorators.py
│   └── ...
└── test/
    ├── routes/
    │   └── test_stock_routes.py
    └── helpers/
    │   └── test_decorators.py    
    └── ... 
```

Using a mirror strategy like this works well for unit tests because they align with the code. 

- Unfortunately this does not work as well with integration and E2E tests as those tests tend to cross the lines defined by the file.
- In these case we will just create a separate directory under `test` to handle these specific tests:

```
└── test/
    ├── e2e/
    │   └── test_e2e.py
    ├── routes/
    │   └── test_stock_routes.py
    └── helpers/
    │   └── test_decorators.py    
    └── ... 
```

Depending on the volume of the tests this can be an effective strategy, however I have seen others as test scope expands.

## Our Makefile command

- The command that we use to run `pytest` in our `makefile` is a bit complex. In this section we will analyze what each piece of this command does. Note that this does require `pytest-cov` to be installed to handle the coverage reporting.

- Currently the command [in our makefile](../lecture_examples/15_testing/Makefile) looks like this:

```
pytest --cov=app /app/src/test/test.py --cov-report=term-missing -v
```

- Below you can find a description of each component and what it is used for.

| Component | Description | 
| --- | --- | 
| `pytest` |  The base command to run Python tests | 
| `--cov=app` | <ul><li>This flag enables coverage reporting through the pytest-cov plugin</li><li>The `app` part specifies the package/directory to measure code coverage for</li><li>It will track which lines of code in the `app` directory are executed during tests</li></ul> | 
| `/app/src/test/test.py` | <ul><li>The path to the test file(s) to run</li><li>In this case, it's running tests from a specific file named `test.py`</li><li>The path indicates it's located at `/app/src/test/test.py`</li></ul> | 
| `--cov-report=term-missing` | <ul><li>This configures the coverage report format</li><li>`term-missing` generates a terminal report that shows:</li><li>Coverage percentage for each file</li><li>Line numbers of code that wasn't executed during tests (missing coverage)</li><li>This helps identify which specific lines need additional test coverage</li></ul> |
| `-v` | <ul><li>Enables verbose output</li><li>Shows more detailed test execution information</li><li>Displays the name of each test as it runs</li><li>Shows additional details about test passes/failures</li></ul> |

When run, this command will:
1. Execute all tests in test.py
2. Track which lines of code in the `app` directory are run
3. Display detailed test results in the terminal
4. Show a coverage report with missing lines
5. Provide verbose output of the test execution

- You should verify that the options do what they are expected -- if you run without `-v` what does the output look like? What about the other options?


## PyTest File

- There are a number of features that we want to call out in our `test/test.py` file. We will reproduce the file [here](../lecture_examples/15_testing/test/test.py).

```python
import sys
from pathlib import Path

import pytest
from jsonschema import validate

# Add the src directory to the Python path so we can import the app
sys.path.append(str(Path(__file__).parent.parent.resolve()))

from flask_app import create_app  # noqa E402


@pytest.fixture
def app():
    """Create and configure a test instance of the application."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        # Add any test-specific configuration here
    })
    return app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


def test_app_exists(app):
    """Test that the app exists."""
    assert app is not None


def test_app_is_testing(app):
    """Test that the app is in testing mode."""
    assert app.config["TESTING"]


def test_player_response(client):
    """Test the /api/players endpoint."""
    HTTP_OK = 200

    schema = {
        "type": "object",
        "properties": {
            "players": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "number"},
                        "player_name": {"type": "string"}
                    },
                    "required": ["id", "player_name"]
                }
            }
        },
        "required": ["players"]
    }
    response = client.get("/api/players")
    # Assert response is JSON
    assert response.status_code == HTTP_OK
    assert response.content_type == "application/json"

    # Assert we can parse the response as JSON
    json_data = response.get_json()
    validate(instance=json_data, schema=schema)
```