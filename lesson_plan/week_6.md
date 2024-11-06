# Week #6 Lesson Plan

## Overview

- Wednesday night the next part of the project is due (part IV). You can find the assignment [here](../project_assignments/part_4.md).
- Thursday will be a quiz. Note that because lecture \#10 was a bit off we repeated it as lecture \#11 and it will not be part of the quiz.

## Resources

## Learning Objectives

- What are connections and cursors and how do we use them to query a database?
- How do we use the following methods on the cursor:
  - `execute`
  - `executemany`
  - `fetch`
  - `fetchall`
  - `fetchmany` (we won't use this in this course, but it is good to know about)
- When and why do we need to `commit`?
- What is the format of data returned by a `fetch`-like command?
- Install sqlite
  
## Lecture Notes



## Quizzable Concepts

- You should be able to write a simple function which manipulates query results using simple SQL statements. For example: given a database schema, write a query which selects specific rows and columns and then print them to the screen or lightly reshape them.
  - The table `cls` has two columns: `student_age` and `student_name`. Please write a function which returns the names of all students who are between 30 and 32 years old (inclusive). This function should take an sqlite connection and return only the names of the students. If there are no students who meet this criteria the function should print "No students found" while returning an empty list.

```
def return_30_through_32_students(conn):
    cursor = conn.cursor()
    cursor.execute("select student_name from cls where student_age <= 32 and student_age >= 30;")
    
    filtered_student_name_list = cursor.fetchall()

    if len(filtered_student_name_list) == 0:
        print("No students found")
    
    return filtered_student_name_list
```