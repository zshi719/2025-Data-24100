# Week #2 Lesson Plan

## Overview
* First quiz is on Thursday of this week. It will be 20 minutes and cover the material from week #1. You can find information on the quizzable material [here](../lesson_plan/week_1.md#day-1-quizable-concepts) and [here](../lesson_plan/week_1.md#day-2-quizable-concepts).
  - Concepts will only include material from week #1.
* Project assignment Part I is assigned, you can find the assignment [here](../project_assignments/part_1.md). It is due next Monday at midnight.

## Resources
* This week we will cover Docker, Git and Make.
* If you are unfamiliar with git, please look at a basic reference, such as [this one](https://www.freecodecamp.org/news/learn-the-basics-of-git-in-under-10-minutes-da548267cc91/). You will need to be familiar with:
    - Repos, Branches and Merging
    - git commands: pull, push, add, commit, checkout

## Learning Objectives

- Describe why we use Docker
- Components of Docker
  - What is a container registry? 
  - What is "bookworm"?
- Creating a Dockerfile that executes a python script.
- Dockerfile commands:
  - FROM, COPY, ENV, RUN, WORKDIR, CMD
- When to use the `-i` and `-t` flags.
- Building and running Dockerfiles using `docker build` and `docker run`
- Passing information into the container using environment variables at both run time and build time.


## Lecture Notes

[Day 3](../class_notes/03_docker.md)

[Day 4](../class_notes/04_docker_git_expectations.md)

### Quizable Concepts

- This will be a relatively applied quiz based on the concepts above. 
- You should be able to construct a simple Dockerfile, know what commands to `run` and `build` it for both interactive purposes and to just run `CMD`.
  - Other commands that we need to know: `ENV`, `FROM`, `COPY` and `WORKDIR`.
- How to create environment variables at both run and build time. How to access them with Python.
- You'll need to be able to read Dockerfiles and understand the environment that they create. 
- You will _not_ be expected to know specific knowledge about different images that were pulled from the registery (e.g. `alpine`, `slim` or `bookworm`). If a Dockerfile appears in the quiz it will use the `python:3.10.15-bookworm` we have used so far.
- Given a Dockerfile, a `docker build` and a `docker run` command describe the output. For example, consider the following where line numbers have been added for simplification.

#### Dockerfile

```
1. FROM python:3.10.15-bookworm
2. WORKDIR /app
3. COPY quiz.py .
4. ENV DF_ENV="Env Var set in Dockerfile"
5. CMD ["python", "quiz.py"]
```

#### quiz.py 

```
1. import os
2. 
3. if __name__ == '__main__':
4.    df_env = os.environ.get('DF_ENV')
5.    df_env_command_line = os.environ.get('ENV_RUN')
6.    # START SPACE
7.    print(f"DF_ENV is set to: {df_env}")
8.    print(f"ENV_RUN is set to: {df_env_command_line}")
9.    # END SPACE    
```

- We can then execute the command by typing:

```
docker build . -t env_var_test
docker run -e BUILD_ENV="set at env" env_var_test
```

- Question: If we run the above `build` and `run` commands what will appear on the screen?
- Question: Lines 6-9 in the python block above print the environment variables. Please rewrite lines 6-9 so that if the first letter of the environment variables are the same then it (additionally) prints "First letters are the same!"
- Question: Modify lines 6-9 so that if `ENV_RUN` is not set (remember what `.get` does...) that it prints "ENV_RUN is not set"
