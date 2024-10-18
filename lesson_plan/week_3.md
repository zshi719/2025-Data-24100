# Week #3 Lesson Plan

## Overview
- Monday night the first part of the project is required to be turned in.
- Thursday there will be a quiz. Quizzes are cumulative and while most of the material will be from Week #2 there will be questions from week #1 material on the quiz.

## Resources

## Learning Objectives

- Sharing files and network ports from the host to a container using `-e` and `-v`. Use `-v` to mount the present working directory to the container.
  - Understand for each type of data sharing if it is done at build, at run or is live.
- Build a container that can run `jupyter` and access it from the host.
- Use `make` and Makefiles to simplify interactions with Docker.
- Three components of our (simplified) Makefile (env vars, Phony definition and commands).
- Reference environment variables in a Makefile
- Reference the current working directory in a Makefile.
- How to write a basic `make` commands and how to create basic dependencies between make files. 
- Build a container that can run `flask` and set a simple route that accepts GET and returns data.
- Parts of an `http` request (type, headers, body, etc.). Know how to reference them on the server side using `flask`.
- Use basic python logic (not a `flask` library) for authentication and return a 400 if not authorized.
- Understand the line continuation marker in bash (`\`)

## Lecture Notes

[Day 5](../class_notes/05_docker_make.md)

[Day 6](../class_notes/06_flask_1.md)


## Quizzable Concepts
- As always, the quiz is cumulative.
- Given a `bash` based-command, how do I create a Make command based on it?
- In `flask` create a route which responds to a GET command with a particular status code.
- In `flask` create a route which parses the body of a GET request and applies a specific python based transformation / change to the body.
- In `flask` create a route which returns a particular status code conditional on the body.
- Example:

