# Git Expectations and Docker Environment Variables

## Git Expectations

- In this course you will be expected to use git and GitHub, using branches and merges, in order to work with your peers.
- In terms of the commands you would be expected to know:
  - `git pull`
  - `git push`
  - `git checkout`
  - `git commit`
  - `git add`
  - `git status`
  - `git fetch`
- These commands have tons of options so you don't need to know everything about them, but you do need to know their core functionality. If you don't recall these specifically from your previous classes, please spend some time getting up to speed the best way you know how, be that videos, book or your previous class notes.

### Git Grading

- There are a number of important things that we will grade your repository on during this course. These are generally considered best practices, so becoming familiar with the underlying motivation and how to execute on them is useful:
1. No direct commits to the `main` branch. All code _must_ be put on a branch and merged in a pull request ("PR").
2. Branches need to have lifetimes. Branches should have a target, such as a specific feature that you are implementing. 
   - New users to git often create a single branch (`NickBranch`) that they commit over and over again to the `main` branch. This isn't a good practice; branches should have a specific lifetime attached to a specific need.
    - Best practice is to create a branch for each feature or task you are working on. After merging your branch in with `main`... DELETE IT!
3. Branch protections must be turned _on_ for the `main` branch to avoid accidental commits to that branch (more info on how to do this can be found in the assignment folder).
4. When you turn in your assignment you will get the commit hash (`sha` pronounced "shaw") of the specific place in the code that you want graded and provide it via the assignment. (Show how to find on github.com).
   - Because the commit hash is attached to a specific state of the code future changes will not effect it and we can be assured that we are both looking at the same place.
   - When grading your code we will checkout that specific code location.

### How to use Git and NOT get in trouble

Git is a complex piece of software and the first time you use it it can feel overwhelming. Here are some best practices that you should use to minimize the likelihood of painting yourself into a corner:

* Always know where you are starting from and verify with `git status` and `git pull` to make sure that you are up to date. When code is pushed to the `main` branch by someone else on your team you'll need to make sure to checkout your own, local, version of `main` and pull before creating a new branch.
* Commit _frequently_ on your own branch.
* Work _together_ on PRs. The code base we are working on isn't that large so everyone should be keeping an eye on all aspect of it.
* Work in isolation: make sure that individuals are working on different sections of the code base. Having two people work on the same section of the code base is a quick way to end up with a confusing set of merges.
* Spend time designing _before_ coding. The most common place in the code where version control issues appear is on interfaces between different pieces of code. Spend time making sure that places where your code touches others is well-defined! Do you know what inputs and outputs are coming into and out of each function / element? How are they intended to interact?

### How to use git an get in trouble

* Don't read the messages that git is sending you on the command line and make sure they are what you expect before continuing.
* Blindly copy code from stack overflow or an LLM without understanding what it is trying to do.

## Passing Data into Docker containers

* We are going to focus on the isolation afforded by Docker.
* One of the powerful features of Docker is that isolates the host computer from the container. This power also means that passing data and information from the host to the container can be complex. In this section we are going to begin a discussion about how to pass data.
* We will focus on three different types of data and identify the three primary times when we want to inject data into the containers.
* We have already covered a few of these options, but in this section we'll specifically cover environment variables.

<figure>
  <figcaption style="text-align: center; font-weight: bold;">Passing Data into Docker containers</figcaption>
<table>
  <tr>
    <th></th>
    <th>Transfer at Build</th>
    <th>Transfer at Run</th>
    <th>Live Container</th>
  </tr>
  <tr>
    <th>ENV Vars</th>
    <td>ENV Command in Dockerfile</td>
    <td>Use <code>-e</code> flag on the <code>run</code> command</td>
    <td style="text-align: center;">✖</td>
  </tr>
  <tr>
    <th>Files</th>
    <td>COPY command in the Dockerfile</td>
    <td style="text-align: center;">✖</td>
    <td>Mount volumes using the <code>-v</code> flag on the <code>run</code> command</td>
  </tr>
  <tr>
    <th>Network</th>
    <td style="text-align: center;">✖</td>
    <td style="text-align: center;">✖</td>
    <td>Mount ports using the <code>-p</code> flag on the <code>run</code> command</td>
  </tr>
</table>
</figure>

### Transfer at build 

- The first time that we can put data into the container is at build.
- We use this frequently when set up our initial environment inside the container, but because of the cons listed below this has very limited use beyond this purpose.
- **PROS:** The biggest pro of putting data into the container at the time of the build is ease. This is, by far, the easiest and most consistent way to get things into the container.
- **CONS:** The major con is that if you put data into the container at the time of the build then every time your data changes you'll need to rebuild the container which is a time consuming process which can impede developer efforts.


### Transfer at run

- The second time we can put data into the container is when we execute `docker run`. 
- Data put into the container at this time will remain static through the lifetime of the container, but can be easily refreshed by exiting and restarting the container.
- This is used frequently when we pass data in that should be relatively stale over the session. Things like API Keys, specific parameters or data locations, etc.
- **PROS:** No need to rebuild the container when data changes
- **CONS:** Requires additional command line arguments that can be fickle to implement. Container restart required when data changes.

### Live container

- The final option, which we really only do for file systems and network data is opening a connection between the host and the container. This type of "live" connection is incredibly powerful since any data change, on either side, is mimicked in the other location. 
- This type of bilateral exchange is very common, but does require us to be careful since we are losing a bit of the security generated from the inherent docker isolation. 
- **PROS:** Everything changes on both sides. Most complete type of data exchange.
- **CONS:** Complex, harder to set up, can create interesting side effects that are hard to track down. Less secure since the connection is open.


## Environment Variables

- In this section we'll demonstrate how to transfer data into a Docker container using environment variables at the time of build and at the time of run.
- We will first start with our basic dockerfile that we have been working with this entire time.

```
FROM python:3.10.15-bookworm
WORKDIR /app

ENV DF_ENV="Env Var set in Dockerfile"
```

- In this example we are creating a debian-based python container with a current working directory of `/app`.
- The only difference is that we have added a new command `ENV` which sets an environment variable inside the container. 
- We can test this by running the following:

```bash
docker build . -t env_var_test
docker run -it env_var_test /bin/bash
```

- Once we are inside the container, we can type `echo $DF_ENV` which will then display the environment variable we set in the Dockerfile.
- Upon Exiting the container lets set a different environment variable at `run` time, rather than build time.

```bash
docker run -it -e BUILD_ENV='Set at Build!' env_var_test /bin/bash
echo $DF_ENV
echo $BUILD_ENV
```

- Running the above we see that the variables are set as expected!

- We can easily change the variable at the time that we run the `docker run` command and see how it changes:

```bash
docker run -it -e BUILD_ENV='Set at Build! -- try 2' env_var_test /bin/bash
echo $DF_ENV
echo $BUILD_ENV
```
- Lets write a python function to print the environment variables to the screen. Consider the following function which we will `env_test.py`:


```python
import os

if __name__ == '__main__':
    df_env = os.environ.get('DF_ENV')
    df_env_command_line = os.environ.get('BUILD_ENV')

    print(f"DF_ENV is set to: {df_env}")
    print(f"BUILD_ENV is set to: {df_env_command_line}")
```


- The python file above uses the `os` module to interact with the environment. We use the `.get()` method on the `environ` attribute of the `os` module. `environ` behaves similar to a dictionary.

- If we want to run this when using `docker run` we can change the Dockerfile to the following:

```
FROM python:3.10.15-bookworm
WORKDIR /app
COPY env_test.py .

ENV DF_ENV="Env Var set in Dockerfile"
CMD ["python", "env_test.py"]
```

- We can then execute the command by typing:

```bash
docker build . -t env_var_test
docker run -e BUILD_ENV="set at env" env_var_test
```

- And we can see the output!