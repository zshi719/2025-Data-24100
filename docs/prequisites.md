# Prerequisites

This document contains an outline of the concepts and techniques that are required for this course. _These concepts will not be taught during the course, and you are expected to have full familiarity with them before starting._

## Python

* `if-then-else` syntax, `for` loops
* Variable assignment 
* Importing packages
* Comparison operations
* Defining functions
* [Not on Quiz] Working with Files using `read`, `readlines`
* Basic Python data structures and how to manipulate them:
  * Strings
    * Slicing using square brackets and colons (e.g. `my_string_var[2:4]`)
    * Replacing subsets of a string using `replace`
    * String functions: `lower`, `upper`, `replace`, `strip`, `index`, `find`/`index`, `len`, `join`, `startswith`, `endswith`and string concatenation 
    * Using `in`
  * Lists
    * Creating empty lists and lists from other lists
    * Selecting elements with slice notation `[start:end:increment]`
    * Adding items with `append`/`extend`
    * Removing items with `remove`/`pop`
    * Writing list comprehensions with an `if` clause
    * Using `in`
  * Dictionaries
    * Creating an empty dictionary or a non-empty dictionary from other variables or atomic/basic data types (literals, primitives, etc. )
    * Adding items
    * Removing items with `pop` or `del`
    * using `.get`
    * `.items`, `.keys` and `.values`
    * Writing dictionary comprehensions with an `if` clause
* Pandas
  * [Not on Quiz] Loading and saving CSV files
  * Selecting rows and columns using `.loc`
  * Using type-specific functions with accessor methods `.str`, `.dt`, etc.
  * Merging with `.merge` 
  * Grouping and aggregation with `.groupby`

## SQL

* Working with Relational Databases and writing queries to retrieve, manipulate, and filter data from a database.
* `SELECT`, `FROM`, `WHERE` and `ORDER BY` for row and column selection.
* Aggregation via `GROUP BY`
* Join syntax: `LEFT`, `RIGHT`, `INNER` and `OUTER/FULL` joins. 
* String operations: `UPPER`, `LOWER`, `LENGTH`, `TRIM` and how to concatenate two strings.


If you need a refresher on any of the above Python topics you should consult the information in the [Data 12000 textbook](https://book.cs-apps.org). The section on Data structures specifically, which can be found [here](https://book.cs-apps.org/data_structures/index.html) is particularly useful for this course. 

For refresher on the Pandas topics please refer to your notes from 118 and 119 and for SQL, there are plenty of easy references online. You can check out chapters 1, 2, 3, 5 and 8 of [this book](https://www.nickross.site/datamanagement/), but it is a bit over kill for our purposes.

Other resources for SQL include [Code Academy](https://www.codecademy.com/learn/learn-sql), which has a solid introduction and [This one](https://sqlbolt.com/) which I found on reddit, so ymmv.

## Some example questions

An unscientific selection of questions that you will be expected to answer without using a computer. These questions were given on quizzes so being able to write them efficiently is important:

1. [Python] Given a list of n-elements `['a', 'b', 'c', 'd', 'e']` be able to convert that list to a dictionary of the form `{ 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}`. 
2. [Python] Given a list of tuples, such as `[('a', 3), ('b', 4), ('c', 5)]` be able to convert that to a dictionary of the form `{ 'a' : 3, 'b': 4, 'c': 5}` or `{3 : 'a', 4: 'b', 5: 'c'}` using a dictionary comprehension. 
3. [SQL] The table stocks contains two columns: `ticker` which is a ticker symbol (such as `AAPL` or `MSFT`) which is text and a number, `price` of the form `18.22`. There is one row per symbol, so the symbols are unique. 
   1. Write a function which returns all tickers and tickers only for stocks with a price greater than 50.00.
   2. Write a function which returns all tickers and tickers only for stocks with a price less than 12.