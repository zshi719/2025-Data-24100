# Final Exam Answer Key

## Question 1 (5 Points)
```bash
mv ../docs/*.pdf .
```
Full credit requires:
- Using relative path
- Single command
- Moving all PDF files
- Correct destination (current directory)

## Question 2 (10 Points Total)

### Part A (5 Points)
```bash
grep ERROR 2024.12.11_flask.log > error_logs.log
```
or
```bash
cat 2024.12.11_flask.log | grep ERROR > error_logs.log
```

Key points:
- Case sensitive match
- Correct output redirection
- Correct filename

### Part B (5 Points)
```bash
grep "ERROR131" 2024.12.11_flask.log | wc 
```
or
```bash
cat 2024.12.11_flask.log | grep ERROR131 | wc 
```

Key points:
- `-l` optional or not. 

## Question 3 (5 Points)
```
/app/src/data/pdf/result.pdf
```
Explanation: 
- Base working directory in container is /app (from Dockerfile)
- Volume mount maps current directory to /app/src (from Makefile)
- Relative path to PDF from project root is data/pdf/result.pdf

## Question 4 (5 Points)
Sample answer: "Coverage measures the percentage of code (lines, branches, or statements) that is executed during testing, helping identify untested parts of the codebase."

Key points:
- Mentions code execution measurement
- References what is being measured (lines/branches/statements)

## Question 5 (6 Points Total)

### Part A (3 Points)
Response for GET /exam/1/alice:
```json
{
    "alice": "engineering"
}
```
Status code: 200

### Part B (3 Points)
Response for GET /exam/1/dylan:
```json
{
    "error": "Employee not found"
}
```
Status code: 404

## Question 6 (2 Points)
DRY stands for "Don't Repeat Yourself"

## Question 7 (10 Points)
```python
@app.route('/exam/2/<string:emp_name>', methods=['GET'])
def route_two(emp_name):
    emp_info = workday_api_call(emp_name)
    
    if emp_info:  # If list is not empty
        return jsonify({
            "name": emp_info[0],
            "age": emp_info[1]
        }), 200
    
    return jsonify({"error": "Employee not found"}), 404
```
Key points:
- Correct handling of empty list case
- Proper JSON structure
- Correct status codes
- Correct access of list elements

## Question 8 (8 Points)
CRUD Operations Table:

| Letter | What it stands for | HTTP Method Used |
|--------|-------------------|------------------|
| C | Create | POST |
| R | Read | GET |
| U | Update | PUT/PATCH |
| D | Delete | DELETE |

## Question 9 (5 Points)
Something like the below

```python
def test_math_func():
    # Test basic functionality
    assert math_func(2, 3, 1) == 7
```
Key Points
- Correct use of assert

## Question 10 (5 Points)
```dockerfile
ENV API_KEY=111222
```
Key points:
- Correct ENV syntax
- Exact match of key and value

## Question 11 (5 Points)

```python
def g(odd_func, even_func, x):
    if x % 2 == 0:
        return even_func(x)
    else:
        return odd_func(x)
```
