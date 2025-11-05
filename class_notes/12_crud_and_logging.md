<!---
title: "More CRUD and Logging in Python"
--->

# Logging

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
  
## Log contents

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
  
## Log system

- We will use the built-in `logging` system provided by python.
- Information about it can be found [here](https://docs.python.org/3/library/logging.html).
- While there are other logging libraries in python, the standard `logging` module, which is built-in and therefore does not to be installed separately is relatively robust. 
- In practice I've seen very little use for libraries other than the standard one. Other, non-python, programming languages aren't so lucky and the logging libraries are more diffuse in their use.


### Severity Level

- Logs (generally) use Severity level as a measure of what to track in different environments.
- For example, when I am actively developing and testing things I'll want lots of logs, but when my system is in production then the amount of logs I care about will be different.
  - Why? Because processing and storing logs is costly. 
- To facilitate having different levels of logging we rely on severity, which are ordered levels of critical or significance.
- When we use our logger we can then set the tracked significance to different levels depending on what environment we are in.
- The standard python library provides these default logging severity levels:

| Level | Name | Brief Description | Example |
| --- | --- | --- | --- |
| 10 | `DEBUG` | Basic info for diagnosis | Logging variable values |
| 20 | `INFO` | General Info / Confirmation | "Server Started" |
| 30 | `WARNING` | Something problematic, system still running | Deprecated command | 
| 40 | `ERROR` | Serious issue that may prevents parts of the system from working | DB connection failed |
| 50 | `CRITICAL` | Serious issue that is causing the program to terminate | Out of Memory |

- In our case, where we have a flask server we may want to log all requests and responses at the DEBUG or INFO level. When we are running code locally we can then turn this level on and receive all the requests and responses. When we put the server into production where the volume of events may be higher then we'll set the logging level to WARNING to avoid tracking these.


## Logging Example

- The code in [Example 12](../lecture_examples/12_logging/) provides an overview of the components of the logging system. 
- We will look at the following files:
    - [`logger_utils/custom_logger.py`](../lecture_examples/12_logging/app/logger_utils/custom_logger.py) which contains the definition of the custom logger that we will use
    - [`app.py`](../lecture_examples/12_logging/app.py) Which contains the start up of the log
    - [`route_utils/decorators.py`](../lecture_examples/12_logging/app/route_utils/decorators.py) which contains an application of the logger via decorators


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

```bash
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

```bash
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


## Performance Monitoring via Decorators

- One of the most powerful uses of logging combined with decorators is to monitor the performance of your API endpoints.
- By tracking how long requests take to process, you can:
  - Identify slow endpoints that need optimization
  - Detect performance degradation over time as data grows
  - Set up alerts when endpoints exceed acceptable response times
  - Generate performance metrics for monitoring dashboards

### Basic Request/Response Logging

- The simplest form of logging for API endpoints is to track when requests arrive and when responses are sent.
- Looking at the [`decorators.py`](../lecture_examples/12_logging/app/route_utils/decorators.py) file, we have a `log_request_response` decorator:

```python
def log_request_response(f):
    """Wrapper to log all requests and responses"""
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        custom_logger.debug(
            f"Request received: {request.method} {request.path}"
        )
        
        response = f(*args, **kwargs)
        
        custom_logger.debug(f"Response: {response[1]} - {request.path}")
        return response
    
    return decorated_function
```

- This decorator:
  - Logs when a request is received (with HTTP method and path)
  - Executes the route function
  - Logs the response status code
  - Uses `DEBUG` level since this can be very verbose in production

### Performance Timing Decorator

- A more sophisticated approach is to measure and log execution time:

```python
def log_request_response_time(f):
    """Wrapper to log all requests times"""
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        custom_logger.info(
            f"Request received: {request.method} {request.path}"
        )
        
        response = f(*args, **kwargs)
        # Convert to milliseconds
        execution_time = (time.time() - start_time) * 1000
        custom_logger.info(
            f"Response: {response[1]} - {request.path} "
            f"- Execution time: {execution_time:.2f}ms"
        )
        return response
    
    return decorated_function
```

- Key components:
  - `time.time()` captures the timestamp before execution
  - The route function executes normally
  - Calculate elapsed time in milliseconds for better readability
  - Log at `INFO` level since performance metrics are important even in production
  - Format the time to 2 decimal places for consistency

### Using the Decorator

- To use these decorators on your routes, simply add them above the route definition:

```python
@app.route('/api/players', methods=['GET'])
@log_request_response_time
def list_players():
    return list_players_route()
```

- You can also stack multiple decorators:

```python
@app.route('/api/teams/<team>', methods=['GET'])
@log_request_response_time
@validate_team
def get_team_info(team):
    return get_team_info_route(team)
```

- **Important**: The order matters! Decorators are applied bottom-to-top, so the `validate_team` runs first, then the logging decorator wraps everything.

### Example Log Output

- When using the timing decorator, your logs will look like:

```bash
2024-11-22 14:32:15 | INFO | Request received: GET /api/players
2024-11-22 14:32:15 | INFO | Response: 200 - /api/players - Execution time: 45.23ms

2024-11-22 14:32:20 | INFO | Request received: GET /api/teams/CHI/stats
2024-11-22 14:32:21 | INFO | Response: 200 - /api/teams/CHI/stats - Execution time: 1234.56ms
```

- From this you can immediately see that the stats endpoint is taking over a second to respond, suggesting it might need optimization.

### Performance Monitoring Best Practices

1. **Choose appropriate log levels**:
   - Use `DEBUG` for detailed request/response logging in development
   - Use `INFO` for performance timing that you want in production
   - Use `WARNING` if response time exceeds expected thresholds

2. **Be consistent with units**:
   - Always use milliseconds for response times (humans understand it better than seconds)
   - Always format to the same decimal places for easier parsing

3. **Include context**:
   - Log the HTTP method and path
   - Consider logging query parameters for GET requests
   - Log the status code to correlate failures with slow responses

4. **Consider adding thresholds**:
   - You could modify the decorator to log at different levels based on execution time
   - Example: `WARNING` if > 1000ms, `ERROR` if > 5000ms


## Error Handling and Logging Patterns

- Proper error handling and logging is critical for debugging production issues and understanding system behavior.
- When handling errors in Flask routes, log at appropriate severity levels and include enough context to diagnose the problem.
- The key is to be **consistent** across your codebase - pick a pattern and use it everywhere.

### Common Error Handling Patterns

There are multiple ways to handle errors in Flask routes. Here are the two most common patterns:

**Pattern 1: Catch-all with different error types**

```python
def get_player_route(player_id):
    try:
        df = load_data()
        player = df[df['id'] == player_id]
        
        if player.empty:
            custom_logger.warning(f"Player {player_id} not found")
            return jsonify({"error": "Player not found"}), 404
            
        return jsonify(player.to_dict('records')[0]), 200
        
    except FileNotFoundError as e:
        custom_logger.error(f"Data file missing: {str(e)}")
        return jsonify({"error": "Data temporarily unavailable"}), 503
        
    except Exception as e:
        custom_logger.error(f"Unexpected error retrieving player {player_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
```

- This pattern:
  - Handles expected conditions (missing player) at `WARNING` level - not an error, but noteworthy
  - Handles known error types (missing file) at `ERROR` level with specific context
  - Catches unexpected errors and logs them
  - Returns appropriate HTTP status codes for each case

**Pattern 2: Decorator for centralized error handling**

- You can create a decorator to handle errors consistently across routes:

```python
def handle_errors(f):
    """Decorator to handle common errors in routes"""
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            custom_logger.warning(f"Validation error in {request.path}: {str(e)}")
            return jsonify({"error": "Invalid input"}), 400
        except FileNotFoundError as e:
            custom_logger.error(f"Required file missing: {str(e)}")
            return jsonify({"error": "Service unavailable"}), 503
        except Exception as e:
            custom_logger.error(f"Unexpected error in {request.path}: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    return decorated_function

# Usage
@app.route('/api/players/<int:player_id>', methods=['GET'])
@handle_errors
def get_player(player_id):
    # Your route logic - errors handled automatically
    return get_player_route(player_id)
```

### What NOT to Log

**Security Concerns** - Never log sensitive information:

```python
# BAD - logs password in plain text
custom_logger.info(f"User login: {username} with password {password}")

# BAD - logs API keys
custom_logger.debug(f"Making API call with key: {api_key}")

# BAD - logs credit card or SSN
custom_logger.error(f"Payment failed for card {credit_card_number}")

# GOOD - log enough to debug without sensitive data
custom_logger.info(f"User login attempt: {username}")
custom_logger.debug(f"Making API call to {endpoint}")
custom_logger.error(f"Payment failed for user {user_id} - card ending in {card_last_4}")
```

**Other things to avoid logging**:
- Personally Identifiable Information (PII) - names, emails, addresses, phone numbers
- Authentication tokens, session IDs, or any security credentials
- Large binary data (images, files)
- Redundant information that clutters logs without adding value

