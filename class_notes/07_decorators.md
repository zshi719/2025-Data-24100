# Metaprogramming

## Code Quality & DRY Code

- Measuring code quality is difficult and there are lots of opinions around what makes good quality good.
- One of the principles that is nearly universally believed to help with code quality is the **DRY** principle of "Don't Repeat Yourself".
- What this means is that you work to not have repetition, such as copy-pasting code sections.
- DRY is one of the top-5 reasons why job applicants are rejected via a take home challenges. It is easy to spot and represents code that will be difficult for others to work with.
- Two of the superpowers that you get when writing code are encapsulation and abstraction, which allow for turning messy tasks into a reusable and repeatable set of processes.
- We are already familiar with the most common way to avoid repeated code -- _Functions_, but in this lecture we will take a larger view of code repeatability by looking at functions which work on function and, in particular, python _decorators_ a meta-programming tool used to manipulate the behavior of functions.

## Functions as object

- Functions in python are first-class citizens. They can be treated as if they are any other object (such as a dictionary, string or number). 
- One way to think about functions is that they are just like any other object in python except that they have a special `call` method denoted by parenthesis which execute an an action defined by itself.
- Consider the following example:

```python
def sq(base):
    '''
    Return the square
    '''

    return base ** 2

def cube(base):
    '''
    Return the cube
    '''
    return base ** 3
```

- In this example we have two functions which return the cube and square of a number.
- We can look at the methods and attributes available to the function using the [`dir` command](https://docs.python.org/3/library/functions.html#dir):

```python
dir(sq)
```

- Among the methods and attributes are three that should be highlighted:

```python
sq.__doc__
sq.__module__
sq.__name__
```

- `__name__` will return the name of the function (`sq` in this case)
- `__module__` will return the module that the function exists in (in this case `__main__` because we created it in this namespace).
- `__doc__` will return the doc string associated with the file (`'\n    Return the square\n    '`) 
- Compare this to the `sin` operation in the `math` library:

```python
>>> import math

>>> math.sin.__module__
'math'
>>> math.sin.__doc__
'Return the sine of x (measured in radians).'
>>> math.sin.__name__
'sin'
```

We can also use the type command see what the object is:

```python
type(sq)
```

which returns `function`. NOTE: If you are unfamiliar with the commands above you should take some time to become familiar with both as they are useful for debugging purposes.

- More powerfully we can refer to functions in the same way that we refer to any other object:

```python
def sq_or_cube(power):
    if power == 2:
        return sq
    elif power == 3:
        return cube
    else:
        raise ValueError(f"Unknown Power: {power}")
```

In this example we return the function as we would return any other object. Given that this is a function we can execute it:

```python
sq_or_cube(3)(4)
```

The result of this will be `4 ** 3 = 64` since the first function call will return the `cube` function while the second will then send 4 to the cube function, resulting in `cube(4)` which is equal to 64.

- We can also do the following:
  
```python
result_function = sq_or_cube(2)
result_function(5)
```

- This will return `5 ** 2 = 25` 

- The important take-away here is that our function behaves like any other variable.
- We can return, route and manipulate them just like any other object.

## Retry loop, part I

- In this section we will build code which implements a retry loop with a timer.
- For our specific situation we will model a function that doesn't behave consistently. You can think of this as a function that may attempt to do something over the internet, dealing with an unhealthy database or if race conditions occasionally arise that retrying is best suited to solve.
- We will use the following code to model our function:

```python
import random

def sus_func(x)
    '''
    Returns the value most of the time
    '''

    if random.uniform(0,1) < .2:
        raise Exception ("Broken Function")
    else:
        return x
```

- This function uses a uniform random number generator to fail 20% of the time. 
- We can test this out by building a quick simulation:

```python
for i in range(0,10):
    try:
        print(sus_func(i))
    except:
        print("Nope")
```

This function executes the function 10 times and print the number of times it fails (as "Nope") and the value of the iteration if it passes. Since it is calling random it does change output each time you run, however when I run it I usually get 2/10 failures.

- Now that we have our function we'll continue to build on our retry loop, but before we do we want to think first, tactically, about what we want our function to take in and what we it to return. Looking at the table below we can create an interface.

| Inputs | Outputs | 
| --- | --- |
| <ul><li>`max_retries`</li><li>`wait_time`</li><li>x (input to `sus_func`)</li></ul> | <ul><li>If passes `sus_func` output</li><li>If fails more than `max_retries` then raise exception</li></ul> | 

- Now that we know the basic structure of the function we can begin writing it.

```python
import time

def retry_sus_func(x, max_attempts=5, wait_time=3):
    '''
    retry logic for sus function
    '''
    attempt_count = 1
    while True:
        try:
            return_value = sus_func(x)
            return return_value
        except Exception as e:
            if attempt_count == max_attempts:
                raise Exception("Max Attempts Met. Error")
            print('Waiting!')
            time.sleep(wait_time)
            attempt_count += 1
```

- The above behaves as expected. It will try to run `sus_func` five times, pausing 3 seconds between each failed run.


- Using our knowledge of functions as objects we can generalize this further to be able to work with _any_ function that accepts a single parameter with the following abstraction:

```python
def retry_sus_func_general(f, x, max_attempts=5, wait_time=3):
    '''
    retry logic for sus function
    '''
    attempt_count = 1
    while True:
        try:
            return_value = f(x)
            return return_value
        except Exception as e:
            if attempt_count == max_attempts:
                raise Exception("Max Attempts Met. Error")
            print('Waiting!')
            time.sleep(wait_time)
            attempt_count += 1
```

- Only two lines in the above function changed. The first was the function definition which now includes `f` as the first positional argument. The second change was on the line that calls the function where `sus_func` was substituted for `f`.

- These two changes mean that we can send any, single argument, function into this and have it apply the retry logic.

- The downside of this is that it does _not_ handle the arguments to the function in a abstracted manner. Any function with more than one argument will not be able to interface with this function. In the next section we'll fix this problem.

## Arg & Kwargs

- Before jumping into how to fix passing arbitrary arguments to another function we first have to understand how python arguments are understood.
- Mentally there are two types of arguments in python:
  - Positional arguments: are those that do not have a default value. They come first in the order and are required by the function. 
  - Keyword arguments: have default values and come after positional arguments.
- For example: `def func(x1, x2, x3, val1='nick', val2='ross')` has three positional arguments and two keyword arguments. 
  - Positional arguments can be thought of as a _tuple_ as they have a specific order and while they do have names, the python interpreter assigns them values based off of their position _not_ their name.
  - Keyword arguments, on the other hand, can be thought of as a dictionary as they are not ordered and are referenced by their name.
- Because we have two different structures for the arguments we'll need to handle both in our code. 
- To this we use `*` and `**` in order to pack and unpack the argument information. Let's do an example of two first to understand how this works:

```python
def arg_print(*args, **kwargs):
    print(args)
    print(kwargs)

> arg_print(3, 4, 5, t=2)
(3, 4, 5)
{'t': 2}
```

- In this example `args` holds all of the positional arguments (as a tuple) and `kwargs` holds all of the keyword arguments as a dictionary. 
- The names `args` and `kwargs` are just like any other variable -- we could call them `bananna` if we want; the important part is the star being used to pack them from the argument into the specific data structures.
- Take a look at this example:

```python
def arg_print_named(v1, *args, v2='nick', **kwargs):
    print(args)
    print(kwargs)

> arg_print_named(3, 4, 5, v2='ttt', t=2)
(4, 5)
{'t': 2}
```

In this example  `args` only contains the 2nd and 3rd positional arguments and `kwargs` only contains `t` and does not contain `v2`.

- In other words -- the `*` and `**` operators act like a vacuum, only taking in those arguments which are not specifically defined already in the function definition. This will help us later.

- The `*` and `**` can also be used to unpack the objects and put them back into a function. This is especially useful if we don't know the structure of the arguments beforehand, such as in the case when we want to operate on an arbitrary function.

- Using this we can update our retry function:

```python
def retry_func(f, **args, max_attempts=5, wait_time=3, **kwargs):
    '''
    retry logic for sus function
    '''
    attempt_count = 1
    while True:
        try:
            return_value = f(**args, **kwargs)
            return return_value
        except Exception as e:
            if attempt_count == max_attempts:
                raise Exception("Max Attempts Met. Error")
            print('Waiting!')
            time.sleep(wait_time)
            attempt_count += 1
```

This looks similar to our last version but we, once again, have changed the function definition line as well as how the function `f` is called. This version will now work on any function with any number and type of arguments!

- We can use it with our `sus_func` as below which will implement the function.

```python
retry_func(sus_func, 3)
```

- One other thing that we will probably want to do is update the error logic to handle the name of the function properly since we can now operate on any function, we can use the `__name__` attribute to do this:


```python
def retry_func(f, **args, max_attempts=5, wait_time=3, **kwargs):
    '''
    retry logic for sus function
    '''
    attempt_count = 1
    while True:
        try:
            return_value = f(**args, **kwargs)
            return return_value
        except Exception as e:
            if attempt_count == max_attempts:
                raise Exception(f"Max Attempts met for {f.__name__}.")
            print(f'Waiting for {f.__name__}')
            time.sleep(wait_time)
            attempt_count += 1
```

- Now we have proper error messages and our retry logic is complete.

## Decorators

- There is a bit of syntactical sugar that we can use to implement the above logic in a more easy to read manner.

- Specifically if we have a number of functions that we want to apply the retry logic to then we would have to do something like:

```python
def sus_func(...)
    ...

def sus_func_with_retries():
    return retry_func( sus_func, ...)

```

Which adds a LOT of names and function definitions to the name space. We avoid this by using the `@` sign and creating a decorator. Lets do a simple one first.


```python
def retry_function(func):
    def wrapper(*args, **kwargs):
        max_attempts=5
        wait_time=3

        attempt = 1
        while True:
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                if attempt == max_attempts:
                    raise Exception(f"Max Attempts met for {f.__name__}.")
                attempt += 1
                print(f'Waiting for {f.__name__}')
                time.sleep(wait_time)
    return wrapper

@retry_function
def sus_func(x):
    if random.uniform(0,1) < .2:
        raise Exception("Function Error")
    else:
        return x
```

- In this example we have created a function which _only takes a function as an input_ and then defined a function inside it (`wrapper`) which is returned by the outer function (this is important). The outer function _only_ accepts the function and the inner function _only_ accepts the arguments that will be part of the function that the decorator is applied to.

- To apply the decorator to the `sus_func` we use the `@` operator and then place the decorator before the function definition we wish to apply it to in the code.

- If we want to add `max_attempts` and `wait_times` as parameters we'll need to add third level of functions to properly return a function with the correct input at each stage in the process:

```python
def retry_function(max_attempts=5, wait_time=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempt = 1
            while True:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    if attempt == max_attempts:
                        raise Exception(f"Max Attempts Reached. Last Error in {func.__name__}")
                    else:
                        attempt += 1
                        print('Waiting!')
                        time.sleep(wait_time)
        return wrapper
    return decorator

@retry_function(wait_time=5)
def sus_func(x):
    if random.uniform(0,1) < .1:
        raise Exception("Function Error")
    else:
        return x

@retry_function()
def sus_func_2(x):
    if random.uniform(0,1) < .1:
        raise Exception("Function Error")
    else:
        return x

```

- In this case we have now added the parameters and we can set them when we define the function, as we do in the later half of this snippet with the `sus_func`. 
- Importantly: when the decorator takes parameters (of either type) then we have to use the parenthesis on the line where the decorator is applied (the one that begins with `@`)
    - Note that in the previous example we just wrote `@retry_function` without the `()` because there were no arguments available to the retry function. 
    - In these later examples, where the `retry_function` has arguments of any type we need add the parenthesis.

## Using functool decorator to preserver metadata

- Take a look at the following example:

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        wait_time=3
        max_attempts=5
        attempt_count = 1
        while True:
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                if attempt_count == max_attempts:
                    raise Exception(f"Max Attempts Met for function {func.__name__} Error")
                else:
                    attempt_count +=1
                    print("Waiting")
                    time.sleep(wait_time)
    return wrapper


@decorator
def sus_func(x):
    '''
    Take in anything (x) and, some percent of the time return x
    otherwise raise an Exception
    '''

    if random.uniform(0,1) < .2:
        raise Exception("Broken Function")
    else: 
        return x

print(sus_func.__name__)
```

- What do we expect the final `print` to display? 
- We would generally expect that this would display `sus_func` -- but unfortunately it does not! This is because the decorator `wrapper` takes precedence and ends up being the entry point for the function and thus the name is now `wrapper`.
- To have the function point to the correctly named function (as well as do some additional clean up) we can use the `wraps` function from `functools`. `wraps` preserves important attributes like:

```python
__name__
__doc__
__module__
```

- To add wraps we do the following:

```python
from functools import wraps

def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wait_time=3
        max_attempts=5
        attempt_count = 1
        while True:
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                if attempt_count == max_attempts:
                    raise Exception(f"Max Attempts Met for function {func.__name__} Error")
                else:
                    attempt_count +=1
                    print("Waiting")
                    time.sleep(wait_time)
    return wrapper


@decorator
def sus_func(x):
    '''
    Take in anything (x) and, some percent of the time return x
    otherwise raise an Exception
    '''

    if random.uniform(0,1) < .2:
        raise Exception("Broken Function")
    else: 
        return x


print(sus_func.__name__)
```

Now, when we run the command we will see that the returned object has the proper meta data

## Logging Example

- Another common reason to use a decorator is for logging. In the example below we will create a logging decorator which acts on a function.

- Lets assume that we have some data process which takes an unknown amount of time and we want to record, in our logs, how long it takes.

```python
import time
import random
from datetime import datetime
from functools import wraps

def log_output(func):
    @wraps(func)
    def wrapper( *args, **kwargs):
        log_format_string = '%Y-%m-%d %H:%M:%S'    
        start_time = time.time()
        start_time_hr = datetime.fromtimestamp(start_time).strftime(log_format_string)
        print(f"Starting {func.__name__} at: {start_time_hr}")
        result = func(*args, **kwargs)
        end_time = time.time()
        end_time_hr = datetime.fromtimestamp(end_time).strftime(log_format_string)

        print(f"Ended {func.__name__} at: {end_time_hr}")
        print(f"Total Duration: {end_time - start_time}")

        return result
    return wrapper


@log_output
def data_process_task(length):
    time.sleep(length)
    return "Success"

for x in range(0,10):
    task_length = random.uniform(1,3)
    data_process_task(task_length)

```

- In the above example we randomly select something between 1 and 3 as our "processing time" of our tasks and then run through it 10 times. 
- Looking at the results you can see that the log file is applied as expected and presents the information as described.
