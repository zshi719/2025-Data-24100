# Docker and Make

- Previously we looked at how to share information at build and run times using environment vars.
- Today we will look at the how to share file and network information. We will fill in the techniques on [this chart](04_docker_git_expectations.md#passing-data-into-docker-containers) that we have not yet covered.
- We will also cover the basics of `make`.


## Sharing Files

- There are two ways to share files inside a docker container:
  - At build, using the `COPY` command inside a Dockerfile, which we have already covered.
  - We can also _mount_ a volume which is the process of making a file system accessible to a computer.
- What mounting does is connects (almost like a portal) a location inside a container to one outside the container.
- We specify this with the `docker run` command.
- Lets consider the following Dockerfile:
  

```
FROM python:3.10.15-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
```

With the associated `requirements.txt` file:

```
art==6.3
```

- As before we can build and run this container with the following commands which launches the container in interactive mode at the command line.

```bash
docker build . -t voltest
docker run -it voltest /bin/bash
```

- Now we want to _mount_ the volume. In this case we will match our current working directory to the location of `/app/src` inside the container.

- When we specify mounted volumes we always use _absolute_ paths in the specification.
- The way that we specify this is with the command line option `-v` we then add the location _on the host_ first followed by the location _inside_ the container that we want the location to mount to. We colon separate them.
- On my computer I run `pwd` to get the current directory:

```bash
pwd
/Users/nickross/git/2024-Data-24100/lecture_examples/docker_volume
```

- This can then be used in the `docker` command:

```bash
docker run -it \
-v /Users/nickross/git/2024-Data-24100/lecture_examples/docker_volume:/app/src \
voltest /bin/bash
```

- Important -- using the **\\** at the end of a line is a _line continuation_ in `bash` meaning that it is a way to have a single line be written on multiple lines for ease of reading. 
  - The **\\** is, however, _incredibly sensitive to spacing_. I frequently get confusing errors only to find that there is a misplaced space.
- The `docker run` command above is the same command we have run multiple times, but this time we added a flag `-v` to link the volume. The line continuation operator is just designed to make the code more readable.
- If you want to verify that this is working -- we can `touch` a file in the host environment and verify that appears in the container. It is also possible to modify a file in the container and see that change reflect in the container.

### Why is this useful?

- I can now edit files using the tools of my host environment, such as VSCode and see the changes in the container _without rebuilding!_

- So why mount vs. `COPY`?
  - Allow for interactive development with tools on the host that are not in the container.
    - Say you are writing code, you can now build and run the container in interactive mode and re-run your code at the terminal while editing the code in your IDE!
  - Generally we try to use `COPY` for files that are used in defining our environment while we use mounting files for those that we want to actively develop on.

### Be Careful!

- When we mounted the volume in the manner above we actually ended up with _two_ version of `requirements.txt` in our container! One from when we copied the file in the Dockerfile and one from when we mounted the volume in `/app/src`. In other words we have:
  - `/app/requirements.txt` <- From the Dockerfile
  - `/app/src/requirements.txt` <- From the mounted volume
- What would happen if we mounted our path into `/app` rather than `/app/src`? Bad things. When you mount a file in a location where the file already exists then you have a conflict that can result in unexpected behavior. Avoid this by only mounting containers in directories that are you are sure don't have files with similar names in them -- or only mount to new locations!


### Mounting based off of PWD

- In the above example we had a very long string to mount the `PWD` inside the container. This string was also tied to my computer and wouldn't work on another person's computer. 
- To avoid being tied to my own computer we can reference, in the `docker run` command, the present working directory directly:

```bash
docker run -it -v $(pwd):/app/src voltest /bin/bash
```

- In `bash` we use notation like the above to pass commands to be expanded. In this case, this will fully expand the present working directory.
- Why would we do this? Because if we write the above, then anyone who checks out the repository will be able to run build and run the image without having to change anything.


## Sharing Network (ports)

- The last computer resource we wish to share is that of the network. When we share the network we don't open the entire network, but instead open up specific _ports_ of the computer in order to maintain isolation. 
- Ports can be thought of where network connections start and end. I tend to think of them as _channels_ on a TV or mailboxes in an apartment complex. They are specific isolated references related to the computer's network connection.
- Specific applications tend to use specific ports on your computer. 
  - When you go to a website that uses `http` the default port is `80`.
  - `https` (the secure version of `http`) uses the port `443`.
  - If you `ssh` into another machine, the default port is `22`
  - When you run a `jupyter` server, the default port is `8888`. 
- When we use docker we will map a specific port from inside the container to a port on the host that we can access. We use similar notation to the volume, except we use `-p` instead of `-v`.


### Jupyter

- In this example we'll get jupyter up and running inside the container and expose the ports to outside the container.

- First we need to add `jupyter` to the `requirements.txt` file:

```
jupyter==1.0.0
```

- Our Dockerfile will remain the same:

```
FROM python:3.10.15-bookworm
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
```

- We can verify that `docker build` works:

```bash
docker build . -t voltest
```

- To expose the port inside the container for the `docker run` we will need to map the port to the host:

```bash
docker run -it -p 8888:8888 voltest /bin/bash
```

- Just like the `-v` command the format of the `-p` command is that you put the _host_ side first and then the port that is _inside_ the container. For example, if we wrote `-p 4000:5000` this would map port 4000 on the host to port 5000 inside te container.

- Once the container spins up, we can run `jupyter` using the following command.

```bash
jupyter notebook --ip=0.0.0.0 --allow-root --no-browser --port 8888
```

- What does each option do:
  1. Setting the `ip` like this forces the container to map the network to a specific location which will be accessible to the host machine. When referring to the _current_ machine there are three slightly different naming conventions used: `localhost`, `127.0.0.1` and `0.0.0.0` Each of these references the current machine and they each have slightly different meanings. Depending on the context one may or may not work.
  2. `--allow-root` is required because we are running as [a root user](https://support.apple.com/guide/directory-utility/about-the-root-user-dirub32398f1/mac).
  3. `--no-browser` is used to tell the jupyter server to not expect the current environment to have a web browser which is requred for some features.
  4. `--port 8888` Forces the jupyter server to use the `8888` port. The `jupyter` server will default to `8888`, but if that is port is in use will move to a different port. We want the server to return an error if the port is in use rather than move ports.

- If we run this command inside the container now the jupyter server will launch and we will be able to access it, as well as create notebooks and interact as you normally would with the container. 

- Importantly if you look at the `docker run` command we did above you will notice that we did not map a volume, which means that any file that we create inside the container will disappear as soon as shut down the container. Let's put together a full docker run command that includes the volume mount:

```bash
docker run -it -p 8888:8888 -v $(pwd):/app/src voltest \
    jupyter notebook --ip=0.0.0.0 --allow-root --no-browser --port 8888 \ 

```

- This should behave as expected with a container running a jupyter server, the ports mapped properly and the volume mounted so we can save files. 

## Using Make

- Typing the above is both annoying and error prone. 
- We will use a tool called Make to assist in our build process. This tools is frequently used in complex development situations. While our particular situation is not that complex we'll leverage this tool to minimize the likelihood of errors.
- To use `make` we create a `Makefile`, which is a text file that contains the instructions for the `make` command. 
- There are three components of the Makefile as we will use them in this course:
    1. A section containing environment variable information
    2. A section with our `phony` definitions
    3. A section with our commands.

- Consider the following `Makefile` which demonstrates all three of these components:

```
IMAGE_NAME=make_test

.PHONY: build interactive

build: 
    docker build . -t $(IMAGE_NAME)

interactive:
    docker run -it $(IMAGE_NAME) /bin/bash

```

In this example we set an environment variable called `make_test`. We have two commands which we define in our `PHONY` section and with the commands afterward. The first command builds the container while the second (`interactive`) runs an interactive session.

- On the command line we can type `make build` and `make interactive` in order to run these commands in an easier to use manner.

- While the above is interesting, we can layer dependencies and also create much more complex statements to make our lives easier. Consider the following `Makefile` which, while similar, has a number of additional features:

```
IMAGE_NAME=make_test

.PHONY=build notebook interactive

build:
	docker build . -t $(IMAGE_NAME)

interactive: build
	docker run -it \
	-v $(shell pwd):/app/src \
	$(IMAGE_NAME) /bin/bash

notebook: build
	docker run -it -p 8888:8888 \
	-v $(shell pwd):/app/src \
	$(IMAGE_NAME) \
	jupyter notebook --allow-root --no-browser \
	--port 8888 --ip=0.0.0.0

```

- This example has a few differences. First, after the `interactive` and `notebook` commands we have added the phrase `build` after the colon. This is a _dependency_. When we run `make interactive`, before the `docker run` command is run, the `build` command in the Makefile will be executed. 

- This allows us to have to remember to rebuild the container ourselves! Since the `docker build` command will only run if there are changes in the files adding this will ot re-build the image every time -- only if a file changes.

- We have also added `$(shell pwd)` rather than `$(pwd)` to the volume section of the file. One thing to note about Make syntax is that it is not exactly `bash` and we sometimes will have to do something different.

- In this case we use `$(shell pwd)` to tell make to run the `pwd` command in the shell/terminal. Doing this will return the current working directory and substitute it into that volume mount command.

- In this example there are three valid `make` commands: `notebook`, `build` and `interactive`. At the command line we can preface any of those with `make` and the commands defined in the Makefile will be run as expected.

### Passing Environment Variables 

- If we have an environment variable, such as an API key or other secret that we want to pass into the container we can pass them in through the Makefile by specifying it in the `docker run` command.
- For example, assume that the host machine has an environment variable called `API_KEY` and we wish to pass it to the container. If we model our code from the previous Makefile we could do something like this:

```

...

interactive: build
	docker run -it \
	-v $(shell pwd):/app/src \
    -e API_KEY_IN_CONTAINER=$(API_KEY) \
	$(IMAGE_NAME) /bin/bash

...

```

Looking carefully at the example above we can see that denoted the `API_KEY` in the host using the dollar-sign parenthesis notation. This tells Make to look for this in the `bash` environment. 

- Inside the container the `-e` line would create an environment variable called `API_KEY_IN_CONTAINER` which would be equal to the value of `API_KEY` from the host environment.