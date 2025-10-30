## Quiz 4 AK

This quiz covers cumulative material from weeks 1-4, including functions as first-class objects, decorators, `*args` and `**kwargs`, and function attributes (`__name__`, `__doc__`, `__module__`).

Common errors to watch for:

1. Forgetting to add docstrings inside the function (not before or after)
2. Not understanding that functions can be passed around as objects
3. Not properly iterating through lists or dictionaries
4. Using `type()` checking instead of `isinstance()` for type checking
5. Confusion between when to call a function `func()` vs. when to reference it as an object `func`
6. Mixing up positional args (`*args`) with keyword args (`**kwargs`)
7. Not understanding the difference between essential and accidental complexity

---

## Quiz 4A Answers

**Question 1:** Rewrite `calculate_sum` so that `calculate_sum.__doc__` returns `"Adds two numbers together"`

**Answer:**
```python
def calculate_sum(a, b):
    """Adds two numbers together"""
    return a + b
```

Alternative (less common):
```python
def calculate_sum(a, b):
    '''Adds two numbers together'''
    return a + b
```

**Explanation:** 
- Docstrings are defined as the first statement in a function using triple quotes
- Can use either `"""` or `'''`
- The docstring must be inside the function body, not before the function definition
- Access it via `function_name.__doc__`

---

**Question 2:** Write `apply_to_all` function that takes a list of functions and applies each to a value

**Answer:**
```python
def apply_to_all(func_list, x):
    return [func(x) for func in func_list]
```

Alternative (using a loop):
```python
def apply_to_all(func_list, x):
    results = []
    for func in func_list:
        results.append(func(x))
    return results
```

Alternative (using map):
```python
def apply_to_all(func_list, x):
    return list(map(lambda func: func(x), func_list))
```

**Explanation:** 
- Iterate through the list of functions
- Apply each function to `x` by calling `func(x)` (note the parentheses to call the function)
- Collect all results and return as a list
- List comprehension is the most Pythonic approach
- The key insight is that functions are first-class objects that can be stored in lists and called

**Common mistakes:**
- Returning the functions themselves instead of calling them
- Not understanding that `func` in the loop is itself a function that needs to be called with `(x)`

---

**Question 3:** Write `flex_print` that accepts keyword arguments and prints them with special handling for integers

**Answer:**
```python
def flex_print(**kwargs):
    for key, value in kwargs.items():
        if isinstance(value, int):
            print(f"Key: {key}, Value: Integer")
        else:
            print(f"Key: {key}, Value: {value}")
```

Alternative (using type checking):
```python
def flex_print(**kwargs):
    for key, value in kwargs.items():
        if type(value) == int:
            print(f"Key: {key}, Value: Integer")
        else:
            print(f"Key: {key}, Value: {value}")
```

**Explanation:** 
- Use `**kwargs` to accept any number of keyword arguments (stored as a dictionary)
- Use `.items()` to iterate through key-value pairs
- Use `isinstance(value, int)` to check if the value is an integer
- Format strings with f-strings showing the key and value
- No positional arguments should be accepted (only `**kwargs` in the function signature)

**Common mistakes:**
- Including `*args` in the signature when the problem says no positional arguments
- Forgetting to iterate through the dictionary
- Not checking for integer type before printing

---

**Question 4:** List two sources of accidental code complexity

**Answer:**

Any two of the following (from the lecture on Separation of Concerns/Abstraction):

1. **Inexperience** - Lack of knowledge about language features, libraries, or best practices leads to more complicated solutions
2. **Poor Abstraction** - Creating inconsistent or uneven interfaces that are hard to use or understand
3. **Technical Debt** - Taking shortcuts to meet deadlines, resulting in code that needs refactoring
4. **Feature Creep** - Adding functionality to existing code beyond its original purpose without proper refactoring
5. **Lack of Coding Standards** - Not following consistent conventions across a codebase

**Grading notes:**
- Each valid source is worth 2 points
- Students need to list two sources for full credit (4 points total)
- Accept reasonable paraphrasing as long as the concept is correct
- Deduct points if students list essential complexity examples (e.g., "the problem is hard", "taxes are complicated")

---

## Quiz 4B Answers

**Question 1:** Write `transform_all` function that applies a list of functions to a value

**Answer:**
```python
def transform_all(x, operations):
    return [func(x) for func in operations]
```

Alternative (using a loop):
```python
def transform_all(x, operations):
    results = []
    for func in operations:
        results.append(func(x))
    return results
```

Alternative (using map):
```python
def transform_all(x, operations):
    return list(map(lambda func: func(x), operations))
```

**Explanation:** 
- Same concept as `apply_to_all` from Quiz 4A, just with parameter order switched
- Iterate through the list of functions and apply each to `x`
- List comprehension is the most Pythonic approach
- Note: `triple(6)` returns `18`, `halve(6)` returns `3.0`, `negate(6)` returns `-6`

**Common mistakes:**
- Mixing up the parameter order (operations and x)
- Forgetting to call the functions with `(x)`
- Returning the functions themselves instead of the results

---

**Question 2:** Rewrite `multiply_values` so that `multiply_values.__doc__` returns `"Multiplies two values together"`

**Answer:**
```python
def multiply_values(x, y):
    """Multiplies two values together"""
    return x * y
```

Alternative:
```python
def multiply_values(x, y):
    '''Multiplies two values together'''
    return x * y
```

**Explanation:** 
- Identical concept to Quiz 4A Question 1
- Docstrings must be the first statement inside the function
- Can use either `"""` or `'''`

---

**Question 3:** Write `display_info` that accepts keyword arguments and prints them with special handling for strings

**Answer:**
```python
def display_info(**kwargs):
    for key, value in kwargs.items():
        if isinstance(value, str):
            print(f"{key}: Text")
        else:
            print(f"{key}: {value}")
```

Alternative (using type checking):
```python
def display_info(**kwargs):
    for key, value in kwargs.items():
        if type(value) == str:
            print(f"{key}: Text")
        else:
            print(f"{key}: {value}")
```

**Explanation:** 
- Use `**kwargs` to accept any number of keyword arguments
- Iterate through key-value pairs with `.items()`
- Check if value is a string using `isinstance(value, str)`
- Format output as `key: value` or `key: Text` for strings
- Note the format is slightly different from Quiz 4A (no "Key:" or "Value:" prefix)

**Common mistakes:**
- Using `isinstance(value, int)` instead of `isinstance(value, str)`
- Including `*args` when only keyword arguments should be accepted
- Incorrect format string (Quiz 4A had different format)

---

**Question 4:** Define accidental complexity and provide one example

**Answer:**

Accidental complexity is complexity that arises from how we write and structure our code, rather than from the inherent difficulty of the problem we're solving. It can be reduced or eliminated through better coding practices, design, and tooling.

Examples of sources of accidental complexity (any one of these is acceptable):

1. **Inexperience** - Lack of knowledge about language features, libraries, or best practices leads to more complicated solutions
2. **Poor Abstraction** - Creating inconsistent or uneven interfaces that are hard to use or understand
3. **Technical Debt** - Taking shortcuts to meet deadlines, resulting in code that needs refactoring
4. **Feature Creep** - Adding functionality to existing code beyond its original purpose without proper refactoring
5. **Lack of Coding Standards** - Not following consistent conventions across a codebase

**Grading notes:**
- Student should provide a definition (2 points)
- Student should provide one valid example (2 points)
- Definition doesn't need to be word-for-word but should capture the essence: complexity from *how we code* not from *what we're solving*

---

