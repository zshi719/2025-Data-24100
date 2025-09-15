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
    * String functions: `lower`, `upper`, `replace`, `strip`, `find`, `index`, `len`, `join`, `startswith`, `endswith` and string concatenation
    * String formatting with f-strings: `f"Value is {value:.2f}"`
    * Using `in`
  * Lists
    * Creating empty lists and lists from other lists
    * Selecting elements with slice notation `[start:end:increment]`
    * Adding items with `append`/`extend`
    * Removing items with `remove`/`pop`
    * Writing list comprehensions with an `if` clause
    * Sorting lists with `sorted`, including `key=` and `reverse=`
    * Using `enumerate` and `zip`
    * Using `in`
  * Dictionaries
    * Creating an empty dictionary or a non-empty dictionary from other variables or atomic/basic data types (literals, primitives, etc. )
    * Adding items
    * Removing items with `pop` or `del`
    * Using `.get`
    * `.items`, `.keys` and `.values`
  * Tuples
    * Creating tuples; unpacking and swapping values
  * Sets
    * Creating sets; set operations: union, intersection, difference
  * Built-in helpers
    * Truthiness, `None` vs empty objects; `any`/`all`
    * Type conversion: `int`, `float`, `str`
  * Exceptions
    * Basic `try`/`except` (and optionally `else`/`finally`); raising `ValueError`
    * Writing dictionary comprehensions with an `if` clause
* Pandas
  * [Not on Quiz] Loading and saving CSV files
  * Selecting rows and columns using `.loc`
  * Using type-specific functions with accessor methods `.str`, `.dt`, etc.
  * Merging with `.merge` 
  * Grouping and aggregation with `.groupby`

## SQL

* Working with relational databases and writing queries to retrieve, manipulate, and filter data from a database.
* `SELECT`, `FROM`, `WHERE`, and `ORDER BY` for row and column selection.
* Boolean logic: `AND`, `OR`, `NOT`; predicates: `IN`, `BETWEEN`, `LIKE` (with `%` and `_`).
* Aggregation: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`; grouping via `GROUP BY` and filtering with `HAVING`.
* Join syntax: `LEFT`, `RIGHT`, `INNER`, and `FULL OUTER` joins using `JOIN ... ON` with table aliases.
* Handling missing values: `IS NULL` / `IS NOT NULL`, `COALESCE`.
* String operations: `UPPER`, `LOWER`, `LENGTH`, `TRIM` and string concatenation.
* Limiting and de-duplicating: `DISTINCT`, `LIMIT` (and `OFFSET`).
* Conditional logic: `CASE WHEN ... THEN ... ELSE ... END`.
* Dates: storing and comparing date strings (e.g., `YYYY-MM-DD`) and filtering by ranges.


If you need a refresher on any of the above Python topics you should consult the information in the [Data 12000 textbook](https://book.cs-apps.org). The section on Data structures specifically, which can be found [here](https://book.cs-apps.org/data_structures/index.html) is particularly useful for this course. 

For refresher on the Pandas topics please refer to your notes from 118 and 119 and for SQL, there are plenty of easy references online. You can check out chapters 1, 2, 3, 5 and 8 of [this book](https://www.nickross.site/datamanagement/), but it is a bit overkill for our purposes.

Other resources for SQL include [Code Academy](https://www.codecademy.com/learn/learn-sql), which has a solid introduction and [This one](https://sqlbolt.com/) which I found on reddit, so ymmv.

## Some example questions

An unscientific selection of questions that you will be expected to answer without using a computer. These questions were given on quizzes so being able to write them efficiently is important:

1. [Python] Given a list of n-elements `['a', 'b', 'c', 'd', 'e']` convert this to a dictionary of the form `{ 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}`.
2. [Python] Given a list of tuples, such as `[('a', 3), ('b', 4), ('c', 5)]` convert this to a dictionary of the form `{ 'a' : 3, 'b': 4, 'c': 5}` or `{3 : 'a', 4: 'b', 5: 'c'}` using a dictionary comprehension.
3. [Python] Given a dictionary of student scores of the form `{'Alice': 85, 'Bob': 92, 'Charlie': 78, 'Diana': 95, 'Eve': 88}`, return a list (name only) of students who have above a 90. The above should return `[ 'Bob', 'Diana']`.
4. [Python] Given two dictionaries: `temperatures = {'Phoenix': 95, 'Las Vegas': 92, ...}` and `humidity = {'Phoenix': 20,'Miami': 75, ...}` return a list of cities that are high temp (above 90) and low humidity (below 30). Note that not all cities are in both dictionaries; only return those cities that are represented in both.
5. [SQL] The table `stocks` contains two columns: `ticker` (text) and `price` (e.g., `18.22`). There is one row per symbol (unique `ticker`).
   1. Write a SQL query that returns tickers only for stocks with a price greater than 50.00.
   2. Write a SQL query that returns tickers only for stocks with a price less than 12.00.
6. [Python] Given a list of dictionaries `people = [{'name': 'Ana', 'age': 30}, {'name': 'Bo', 'age': 25}, ...]`, return a list of names for people aged 27 or older, sorted alphabetically.
7. [Python] Write a function `normalize(text: str) -> str` that strips leading/trailing spaces, collapses multiple internal spaces to a single space, and lowercases the result using built-in string methods.
8. [Python] Given two lists `a = [1, 2, 3]` and `b = ['x', 'y', 'z']`, produce `{1: 'x', 2: 'y', 3: 'z'}` using `zip` and a dictionary comprehension.
9. [SQL] Given tables `trades(ticker, trade_date, qty, price)` and `stocks(ticker, sector)`, write a query that returns total traded volume by `sector` for January 2020. Only include rows where `qty > 0`. Sort by volume descending.
10. [SQL] Using the `stocks` table with columns `(ticker, price)`, return the count of tickers by price bucket using `CASE`: `< 10`, `10–50`, `> 50`.
11. [SQL] Given a table `prices(ticker, date, close)`, return the 5 most expensive tickers on `2020-01-02` (highest `close`), breaking ties by `ticker` alphabetically.