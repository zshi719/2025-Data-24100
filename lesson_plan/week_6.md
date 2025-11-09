# Week #6 Lesson Plan

## Overview

- Wednesday night the next part of the project is due (Part IV). You can find the assignment [here](../project_assignments/part_4.md).
- Wednesday there will be a quiz. Quizzes are cumulative and cover the material up to and including the previous week (Week 5).

## Resources

- The [Ruff docs](https://docs.astral.sh/ruff/) are very well written and a great place to start. 
- Same with the docs for [pre-commit](https://pre-commit.com/).
- Wikipedia page on [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)
- Python [logging documentation](https://docs.python.org/3/library/logging.html)

## Learning objectives

- Define static analysis tools. Why do we use them?
- What are the things that static analysis can look for?
- What are the different types of static analysis tools? How does `ruff` fit in?
- What is a pre-commit hook and how does it interact with Git?
- How do we install `ruff` and `pre-commit` and use them?
- What is a `toml` file?
- Using `ruff check` and `ruff format` commands
- Using other request types (DELETE, PUT/PATCH) and combining request types to the same endpoint
- How to access different parts of HTTP requests in Flask:
  - Query parameters (`request.args`)
  - URL parameters (route parameters)
  - Body data (`request.get_json()`)
  - Headers (`request.headers`)
- What is logging and why is it important?
- Components of a log (timestamp, message, severity, source, context)
- Python's `logging` module and how to use it
- Severity levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- Setting up custom loggers in Flask applications

  
## Lecture notes

[Day 11](../class_notes/11_static_analysis_more_crud.md)

[Day 12](../class_notes/12_crud_and_logging.md)


## Quizzable concepts

- What is linting? What is static analysis?
- What is `ruff` and what does it do?
- Provide a list of examples of things that static analysis tools can do to provide feedback on your code.
- What is a pre-commit hook and why is it useful?
- What is CRUD and how does it map to HTTP request types?
- Be able to write Flask routes that handle multiple request types (GET, POST, DELETE, PUT/PATCH) at the same endpoint
- Given Flask code, identify how different parts of the request are being accessed (query params, URL params, body, headers)
- What are the components that should be in a log entry?
- What are the different severity levels in Python's logging module and when should each be used?
- Be able to read and understand code that sets up a custom logger
- Example: Write a Flask route that accepts both GET and POST requests. For GET, it should return all items. For POST, it should accept JSON data and create a new item.
- (Review) What are the parts of an HTTP request? Given code for processing and returning a request, be able to describe what the code does.

```python
@app.route('/api/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        items = get_all_items()
        return jsonify({"items": items}), 200
    
    if request.method == 'POST':
        data = request.get_json()
        if not data.get('name'):
            return jsonify({"error": "name is required"}), 400
        
        create_item(data)
        return jsonify({"message": "Item created"}), 201
```