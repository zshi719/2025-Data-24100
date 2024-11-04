## Quiz 4 AK

1A. 


Like a dictionary


1B.

```
QUESTION 1: {'var3': 'computer', 'var4': 3}
```

2.

`calc_function` 

This question seemed to confuse a lot of people and it is worthwhile to think through why the answer is not `wrapper`, which was what quite a few people put down.

The reason it is now wrapper is because the decorator acts like a wrapper, encapsulating the function. In other words the call to `calc_function` becomes the `wrapper` function because that is what is returned by the `timing_decorator`. However, and this is important, nothing magical happened, `calc_function` was just hidden inside a wrapper.

Inside that wrapper, where `.__name__` is accessed, the function will retain its original name.


3. There were multiple correct answers here, the simplest one that satisfies the criteria is:

```
def F(f, *args):
    return 2 * f(*args)

```