# Logging in Python and some project issues

## Project Issues

- After reviewing the assignments there were a number of issues that were arising that we should address and fix.
 
 ### Overlapping functionality
 - Multiple groups had code with overlapping functionality, such mounting a drive via the Makefile docker command that was copied into the container. 
 - Another example is having a global variable set via the Makefile docker and then hard coding the path in Python. In the Makefile `DATA_DIR=/app/data` and a `-e DATA_DIR=$(DATA_DIR)` and then in python: `DATA_DIR = '/app/data'` or `RAW_DATA_DIR='/app/data/raw_data`. 
   - In all of these cases the phrase `/app/data` _should only appear once_ so that if things change it does not have to be changed in multiple locations.
 - Make sure to avoid overlapping functionality.

### Repeated Naming
- Many groups have code with naming at multiple places in the file tree, such as having:
  - a file: `/app/api/v2/routes_v2.py`
  - a function inside a file called `routes_v2.py` with the name `load_v2_routes()`
  - or both!
- `v2` should _not_ be repeated multiple times. Generally, proper naming should only exist on a single abstraction level as changing it will require changing multiple locations.

### Not using existing functions
- In some code bases I'll see a function that can do something (such as `create_db_connection`) in conjunction with the raw code that does that action (e.g. `conn = sqlite.connection(...)`)
- The good news about this is that it probably means multiple people in your group are working on the project. The bad news is that it seems that they are not communicating with each other.
- If there is a function defined with specific functionality it needs to be used.

### Things not running
- Multiple groups had code that did not run when typing in `make db_clean` and `make flask`.
- This is going to be severely penalized grade wise. 
- To avoid this test on a clean install!
  - Delete your directory
  - Re-clone your repo
  - Run the relevant commands

### Incomplete features
- Code that has either hard coded options in functions that don't do anything or were not completed.
- Examples like `def load_function(... , downsample=False)` and `downsample` is not used in the function
- Other times there were code blocks that didn't do anything, such as having something defined (`years = [1997]`) and the variable `years` not used throughout the rest of the code or is modified later without it being called in the interim.

### Poorly defined abstractions
- Multiple groups had code in files that didn't have a clear abstraction.
- When we think about what this code is doing (responding to requests) there are clear places where we can break up the code base: connections, SQL related code, route related code, db management commands, etc.
- Each of these has a clear interface with natural breaks. For examples routes should have no information about the location of the zip files and SQL-related functions do not need to know anything about the route.
- There are a few symptoms that are looked for when evaluating the code and abstraction:
  - Replicated definitions across files (especially globals and environment variables)
  - Inconsistent imports, such as importing `pandas` into routes or the `app.py` file.
  - Large functions with multiple layers of complexity.
  - Repeated functionality -- doing the same action in multiple places

Overall, please read over your code and make sure that it follows the above conventions before submitting!

## Logging

- Logging is creating a record of events that occur in a system.
- Logs are important for a number of reasons and they are often the primary way that we have of generating data about and from our systems.
- There are lots of uses of logs:
  - Debugging / Reconstruction of events. 
    - Our server failed at 2AM last night, why?
    - A user was able to cheat in our video game, what do we know about their behavior?
    - Our systems were reporting incorrect data from yesterday.
    - Our users are not buying as much as before, did something change in our checkout flow?
  - Understanding system state:
    - Log when our server experiences issues, such as flask shutting down or starting up.
    - Database connections failing
    - Log when data processing complete or a new table has been added to our database. 
  - Security compliance:
    - Suspicious activity, such as users trying to hack your system.
    - Regulatory requirements, such as for know your customer or reporting when certain things occur. When I worked at Sega we were required to report (by law) certain types of gambling-esque transactions. We created a special log pathway for this.
  - Performance measurement:
    - How fast is our web page loading?
    - How long is it taking our data to load as we add more data over time?
  - Biz Intelligence:
    - Very common data pipeline: System &rarr; Logs &rarr; Log Processor &rarr; Database/Spark &rarr; Data Scientists working on the problem
  
### Log contents

A log should contain the following elements, in no particular order:

1. Timestamp (when did the event occur) preferably in a known or common timezone, such as UTC.
2. Event Description Message: What does the event represent?
3. Source Information: From what system and code base location did the log originate from?
4. Contextual Data: Users, Resources, Processes. Information to provide additional context about the event.
5. Severity: We want to know how much to care (or not).

_Important_

- We want to keep our logs as _structured_ as possible with as much common between different log events so that when we process them we don't have to add a lot of conditional logic.
- What do we mean by structured? 
  - Time stamps the same. If they are `11-10-2024 11:15 PM ...` then we don't see `2024-11-10 23:15` in a different log.
  - Order of data and organization are the same. Events should have information organized with the same words, phrases and systems of communication to minimize the logic required to process.
  
### Log system

- We will use the built-in `logging` system provided by python.
- Information about it can be found [here](https://docs.python.org/3/library/logging.html).
- While there are other logging libraries in python, the standard `logging` module, which is built-in and therefore does not to be installed separately is relatively robust. 
- In practice I've seen very little use for libraries other than the standard one. Other, non-python, programming languages aren't so lucky and the logging libraries are more diffuse in their use.


#### Severity Level

- Logs (generally) use Severity level as a measure of what to track in different environments.
- For example, when I am actively developing and testing things I'll want lots of logs, but when my system is in production then the amount of logs I care about will be different.
  - Why? Because processing and storing logs is costly. 
- To facilitate having different levels of logging we rely on severity, which are ordered levels of critical or significance.
- When we use our logger we can then set the tracked significance to different levels depending on what environment we are in.
- The standard python library provides these default logging severity levels:

| Level | Name | Brief Description | Example |
| --- | --- | --- | --- |
| 10 | DEBUG | Basic info for diagnosis | Logging variable values |
| 20 | INFO | General Info / Confirmation | "Server Started" |
| 30 | WARNING | Something problematic, system still running | Deprecated command | 
| 40 | ERROR | Serious issue that may prevents parts of the system from working | DB connection failed |
| 50 | CRITICAL | Serious issue that is causing the program to terminate | Out of Memory |

- In our case, where we have a flask server we may want to log all requests and responses at the DEBUG or INFO level. When we are running code locally we can then turn this level on and receive all the requests and responses. When we put the server into production where the volume of events may be higher then we'll set the logging level to WARNING to avoid tracking these.


## Logging Example

- The code in [Example 13](../lecture_examples/13_logging/) provides an overview of the components of the logging system. 
- We will look at the following files:
    - [`logger_utils/custom_logger.py`](../lecture_examples/13_logging/app/logger_utils/custom_logger.py) which contains the definition of the custom logger that we will use
    - [`app.py`](../lecture_examples/13_logging/app.py) Which contains the start up of the log
    - [`route_utils/decorators.py`](../lecture_examples/13_logging/app/route_utils/decorators.py) which contains an application of the logger via decorators


### Custom Logger 

- The code in our custom logger looks like the following. The purpose of this is to set up a custom logger that has the information that we want.
- In this case we are doing the following:
  - Setting the default level of logging
  - Setting where the logs are sent (`StreamHander`). Other options could be to specific files or a cloud based collection system.
  - Setting the format of the logs -- what we keep track of.
- Looking at the code below the other thing to note about this code is that it creates (or gets) a specific logger called `flask_app`. You can have multiple logging handlers with different properties. Ours is named `flask_app` and we will attach all of our properties to it.
- The line `if not logger.handlers` makes sure that once the handlers are created, they are only created a single time. Basically the line `logger = logging.getLogger("flask_app")` will either return a new logging object or a previously created one. The conditional below it adds the specific handler to the logger object only if you are in the case when `getLogger` created an object.
- At the end we will import `custom_logger` when we want to have a logger as we will see in the code below.

```python
def setup_logging():
    """Set up logging and return the custom logger"""
    logger = logging.getLogger("flask_app")
    if not logger.handlers:  # Prevent duplicate handlers
        logger.setLevel(logging.INFO)  # set level to track, can be overwritten
        handler = logging.StreamHandler()
        log_format = "%(asctime)s | %(levelname)s | %(message)s"
        formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

custom_logger = setup_logging()
```

### Initialization 

- When we start the app we will initialize the custom logger. There are a number of lines of code that demonstrate how this occurs:

```python
    # Debug Level:
    logging_level = logging.DEBUG
    # Initialize logger
    app.logger = custom_logger  # Attach logger to Flask app
    app.logger.setLevel(logging_level)
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(logging_level)
    werkzeug_logger.handlers = []
    werkzeug_logger.addHandler(app.logger.handlers[0])
```

- The first line in this section sets the `logging_level` to `DEBUG`, we could set it to other levels if we wanted to.
- The lines associated with [werkzeug](https://werkzeug.palletsprojects.com/en/stable/) are done to override the logging mechanism that was already in place. Werkzeug is a library that handles the information interchange between the flask server and the underlying network on the computer. 
    - It is a complex piece of software and because of that it has its own built in logging.
    - When you start a flask server the lines that look like the below are set up as logs from the Werkzeug system:

```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 686-305-594
```
- We want all of our logs to go through the custom logger we built, so we have to override the logging system on this other system. 
- After updating these lines you will see that most of the lines in the flask start up now follow the logging strategy, so similar to:

```
2024-11-22 18:16:15 | INFO | Press CTRL+C to quit
2024-11-22 18:16:15 | INFO |  * Restarting with stat
2024-11-22 18:16:16 | INFO | Application initialized successfully
2024-11-22 18:16:16 | WARNING |  * Debugger is active!
2024-11-22 18:16:16 | INFO |  * Debugger PIN: 686-305-594
```

- **Note** that if we want to set a specific log level to expose we would want to se it in the `app.py`. This is where our other configuration is, so this is where you want to set it.

### Usage
- In the decorators file above you can see the direct usage of the custom logger. To get it running you first need to import it.
- To write logs you call the function `customer_logger.LOG_LEVEL( message )` which will generate the appropriately formatted log file.