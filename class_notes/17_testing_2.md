# Pytest 

- We will continue our discussion of testing by implementing


## Ou

The command that we use to run `pytest` in our `makefile` is a bit complex. In this section we will analyze what each piece of this command does. Note that this does require `pytest-cov` to be installed to handle the coverage reporting.


Currently the command [in our makefile](../lecture_examples/15_testing/Makefile) looks like this:

```
pytest --cov=app /app/src/test/test.py --cov-report=term-missing -v
```

Below you can find a description of each component and what it is used for.


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