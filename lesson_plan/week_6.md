# Week #6 Lesson Plan

## Overview

- Wednesday night the next part of the project is due (Part IV). You can find the assignment [here](../project_assignments/part_4.md).
- Thursday will be a quiz. Note that because Lecture \#10 was a bit off we repeated it as Lecture \#11 and it will not be part of the quiz.

## Resources

- Make sure you understand basic SQL commands. You can find more information on what is required for the course [in this note](../docs/prerequisites.md).

## Learning objectives

- What are connections and cursors and how do we use them to query a database?
- How do we use the following methods on the cursor:
  - `execute`
  - `executemany`
  - `fetchone`
  - `fetchall`
  - `fetchmany` (we won't use this in this course, but it is good to know about)
- When and why do we need to `commit`?
- What is the format of data returned by a `fetch`-like command?
- Install SQLite.
- What is `argparse` and how is it used?
- Why do we use management commands?
- CRUD: sending and receiving a POST request and using it to insert data into a database.

  
## Lecture notes

- [Day 11](../class_notes/11_sqlite.md)

- [Day 12](../class_notes/12_mgmt_and_post.md)


## Quizzable concepts

- You should be able to write a function that manipulates query results using SQL statements. For example: given a database schema, write a query that selects specific rows and columns and then prints them to the screen or lightly reshapes them.
  - The table `cls` has two columns: `student_age` and `student_name`. Please write a function that returns the names of all students who are between 30 and 32 years old (inclusive). This function should take a SQLite connection and return only the names of the students. If there are no students who meet this criteria, the function should print "No students found" while returning an empty list.

```
def return_30_through_32_students(conn):
    cursor = conn.cursor()
    cursor.execute("select student_name from cls where student_age <= 32 and student_age >= 30;")
    
    filtered_student_name_list = cursor.fetchall()

    if len(filtered_student_name_list) == 0:
        print("No students found")
    
    return filtered_student_name_list
```

- As a reminder, you are required to understand and be able to write simple SQL statements such as the above.