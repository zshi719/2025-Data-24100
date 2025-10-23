## Quiz 3 AK

This quiz covers cumulative material from weeks 1-3, including shell commands, Make, Docker, and Flask.

There were a few common errors:

1. Forgetting to use `grep` to filter the log file before counting or displaying lines
2. Using `head` instead of `tail` to get the newest (last) entries from a log file
3. Forgetting the `@app.route()` decorator on Flask routes
4. Not handling all three cases (`True`, `False`, `None`) in the Flask route
5. Forgetting to import `Response` or not using the correct syntax for returning status codes
6. Not understanding that `tail` defaults to 10 lines, so no `-n 10` flag is needed
7. Incorrect Make command syntax (forgetting the command name and colon)

---

## Quiz 3A Answers

**Question 1a:** Write a Make command that returns the number of times the `api/v1/data` endpoint is called

Note that in the below you can have `wc -l` or just `wc`

```makefile
count_endpoint_calls:
	cat /logs/flask.log | grep "api/v1/data" | wc -l
```

Alternative (more concise):
```makefile
count_endpoint_calls:
	grep "api/v1/data" /logs/flask.log | wc -l
```

Alternative (using grep -c for counting):
```makefile
count_endpoint_calls:
	grep -c "api/v1/data" /logs/flask.log
```

**Explanation:** 
- The log message is `"REQUEST: api/v1/data endpoint"`, so we grep for `"api/v1/data"` to find matching lines
- Use `wc -l` to count the number of lines (or `grep -c` to count matches directly)
- Don't forget the tab character before the command (Make requires tabs, not spaces)

---

**Question 1b:** Write a Make command that shows the newest entries (last 10 lines) from the log

```makefile
show_newest_logs:
	tail /logs/flask.log
```

Alternative (explicit):
```makefile
show_newest_logs:
	tail -n 10 /logs/flask.log
```

**Explanation:** 
- Use `tail` to get the last lines of the file (newest entries in a log file)
- `tail` defaults to 10 lines, so no flag is needed, but `-n 10` can be added for clarity
- Don't forget the tab character before the command

---

**Question 2:** Write a route `/api/v1/dark_out` that returns different status codes based on `is_night()` function

```python
@app.route('/api/v1/dark_out', methods=['GET'])
def check_if_dark():
    result = is_night()
    if result is True:
        return Response(status=200)
    elif result is False:
        return Response(status=201)
    else:
        return Response(status=202)
```

Alternative (more compact):
```python
@app.route('/api/v1/dark_out', methods=['GET'])
def check_if_dark():
    result = is_night()
    if result is True:
        return Response(status=200)
    elif result is False:
        return Response(status=201)
    return Response(status=202)
```

Alternative (using dictionary mapping):
```python
@app.route('/api/v1/dark_out', methods=['GET'])
def check_if_dark():
    status_codes = {True: 200, False: 201, None: 202}
    return Response(status=status_codes[is_night()])
```

**Explanation:** 
- Must include the `@app.route()` decorator with the path and methods
- Must handle all three cases: `True` (200), `False` (201), `None` (202)
- Use `is True` and `is False` (identity comparison) or `== True` and `== False` to distinguish from `None`
- Can use `else` for the final case since only three values are possible
- `Response(status=XXX)` is the correct syntax for returning just a status code
- The body and headers can be empty, so we don't need to provide them

**Common mistakes:**
- Forgetting the decorator
- Not handling the `None` case
- Using `if result:` which would treat both `True` and `None` differently than expected
- Not specifying `methods=['GET']` in the decorator

---


