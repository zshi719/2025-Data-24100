# Week #4 Lesson Plan

## Overview
- Monday night the next part of the project is due.
- Thursday there will be a quiz. Quizzes are cumulative and cover the material up to and including the previous week (Week 3).

## Resources

## Learning objectives
- Understand and write code that adheres to the following best practices.
  - DRY
  - File organization
  - Separation of concerns
- What is a decorator in Python and why do we use them?
- Be able to write a decorator that implements logic before and after a function is called.
- Work with functions as objects.
- Positional vs. keyword arguments: How are they different? How to pack and unpack with (`*` and `**`)? How to use them to pass arbitrary argument information to functions.
- Understand the `dir` command.
 
## Lecture notes

[Day 7](../class_notes/07_decorators.md)

[Day 8](../class_notes/08_flask_soc.md)

## Quizzable concepts

- You will not be expected to reproduce a decorator from scratch, but you should be able to read the code in a decorator, interpret what it is doing, and make minor modifications.
- Define positional vs. keyword arguments.
- Describe and use `**kwargs` and `*args` for manipulating unknown or variable length arguments.
- Be able to use `__name__`, `__doc__`, and `__module__` on functions and know what the result is.
- Define separation of concerns and code complexity.
- Explain what the `dir` command does and use it.
- Use functions as objects. Example question: Please write a function `g` which takes in, as arguments, `f` and `x`, where `f` is a function and `x` is an integer. If `x` is even it should return `x`, and if `x` is odd it should return the function `f` with `x` provided as the first positional argument:

```
def g(f, x):
    if x % 2 == 0:
        return x
    else:
        return f(x)
```

- Use `args` and `kwargs` to work with function arguments. Example: Please write a function `g` which prints out all the keyword arguments that were provided to it. It should print them item by item in the format: `f"Keyword: {key} \t Value: {value}"` where `key` and `value` are the key-value pair associated with the argument. It should not accept any positional arguments.

```
def g(**kwargs):
    for k, v in kwargs.items():
        print(f"Keyword: {k} \t Value: {v}")
```