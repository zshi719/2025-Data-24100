## Quiz 2 AK

There were two different versions of the quiz with slightly different naming and file structure. The answer keys for both versions "A" and "B" are provided below.

There were a few common errors / changes:

1. Forgetting to use `os.environ.get()` with a default value when an environment variable might not be set
2. Not understanding the difference between build-time (`ENV` in Dockerfile) and run-time (`-e` flag) environment variables
3. Incorrect placement of `COPY` commands in the Dockerfile - they should come after dependency installation (`RUN uv sync`) but before the files are needed
4. Not understanding how `WORKDIR` affects the full path of files inside the container
5. Forgetting to specify where in the Dockerfile a new line should be added
6. Using absolute paths when relative paths were requested
7. Incorrect syntax for `os.environ.get()` - remember the second argument is the default value

---

## Quiz 2A Answers

**Question 1:** What will be printed to the screen when the docker commands execute?

```
ENV_B: SecondValue
ENV_A: FirstValue
```

**Explanation:** 
- `ENV_B` is set at run time using `-e ENV_B="SecondValue"` and is printed first
- `ENV_A` is set at build time using `ENV ENV_A="FirstValue"` in the Dockerfile and is printed second

---

**Question 2:** Add a line to copy `settings.txt` from the `config` directory to `/project/settings.txt` inside the container

```dockerfile
COPY config/settings.txt /project/settings.txt
```

or 

```dockerfile
COPY config/settings.txt settings.txt
```

or

```dockerfile
COPY config/settings.txt .
```

**Where to add:** After `RUN uv sync` and before `COPY src/test.py .`

**Explanation:** 
- The relative path from `/users/maria` (where we run the build) is `config/settings.txt`
- Since `WORKDIR` is `/project`, the destination can be either the full path `/project/settings.txt`, just the filename `settings.txt`, or `.` (which refers to `/project`)
- This should be placed after dependencies are installed but before the Python file that might use it

---

**Question 3:** Rewrite the lines between START SPACE and END SPACE to handle missing `ENV_B`

```python
# START SPACE
env_b = os.environ.get("ENV_B", "ENV_B is not set")
print(f"ENV_B: {env_b}")
# END SPACE
```

**Explanation:** 
- `os.environ.get()` takes two arguments: the environment variable name and a default value if it's not set
- This prevents a `KeyError` if `ENV_B` is not defined

---

**Question 4:** Which environment variable changes only when we build the container?

```
ENV_A
```

**Explanation:** 
- `ENV_A` is set using `ENV` in the Dockerfile, so it's baked into the image at build time
- `ENV_B` is set using `-e` flag at run time, so it can change with each `docker run` command

---

**Question 5:** What is the full path where `test.py` is located inside the container?

```
/project/test.py
```

**Explanation:** 
- `WORKDIR /project` sets the working directory to `/project`
- `COPY src/test.py .` copies the file to the current working directory (`.`), which is `/project`
- So the full path is `/project/test.py`

---

## Quiz 2B Answers

**Question 1:** What will be printed to the screen when the docker commands execute?

```
VAR1: Value abc
VAR2: RunValue
```

**Explanation:** 
- `VAR1` is set at build time using `ENV VAR1="Value abc"` in the Dockerfile and is printed first
- `VAR2` is set at run time using `-e VAR2="RunValue"` and is printed second

---

**Question 2:** Which environment variable changes only when we build the container?

```
VAR1
```

**Explanation:** 
- `VAR1` is set using `ENV` in the Dockerfile, so it's baked into the image at build time
- `VAR2` is set using `-e` flag at run time, so it can change with each `docker run` command

---

**Question 3:** Rewrite the lines between START SPACE and END SPACE to handle missing `VAR2`

```python
# START SPACE
var2 = os.environ.get("VAR2", "VAR2 is not set")
print(f"VAR2: {var2}")
# END SPACE
```

**Explanation:** 
- `os.environ.get()` takes two arguments: the environment variable name and a default value if it's not set
- This prevents a `KeyError` if `VAR2` is not defined

---

**Question 4:** Add a line to copy `input.txt` from the `data` directory to `/app/input.txt` inside the container

```dockerfile
COPY data/input.txt /app/input.txt
```

or 

```dockerfile
COPY data/input.txt input.txt
```

or

```dockerfile
COPY data/input.txt .
```

**Where to add:** After `RUN uv sync` and before `COPY app/check.py .`

**Explanation:** 
- The relative path from `/home/alice` (where we run the build) is `data/input.txt`
- Since `WORKDIR` is `/app`, the destination can be either the full path `/app/input.txt`, just the filename `input.txt`, or `.` (which refers to `/app`)
- This should be placed after dependencies are installed but before the Python file that might use it

---

**Question 5:** What is the full path where `check.py` is located inside the container?

```
/app/check.py
```

**Explanation:** 
- `WORKDIR /app` sets the working directory to `/app`
- `COPY app/check.py .` copies the file to the current working directory (`.`), which is `/app`
- So the full path is `/app/check.py`

