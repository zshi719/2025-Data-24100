# Docker and Make

- Previously we looked at how to share information at build and run times using environment vars.
- Today we will look at how to share file and network information. We will fill in the techniques on [this chart](04_docker_git_expectations.md#passing-data-into-docker-containers) that we have not yet covered.
- We will also cover the basics of `make`.


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

- First we need to add `jupyter` to the `pyproject.toml` file:

```bash
[project]
name = "class4demo"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "jupyter==1.1.0",
]
```

- Our base Dockerfile will remain the same:

```bash
FROM astral/uv:python3.13-bookworm
WORKDIR /app

COPY pyproject.toml .

RUN uv venv
RUN uv sync
```

- We can verify that `docker build` works:

```bash
docker build . -t class5
```

- To expose the port inside the container for the `docker run` we will need to map the port to the host:

```bash
docker run -it -p 8888:8888 class5 /bin/bash
```

- Just like the `-v` command the format of the `-p` command is that you put the _host_ side first and then the port that is _inside_ the container. For example, if we wrote `-p 4000:5000` this would map port 4000 on the host to port 5000 inside the container.

- Once the container spins up, we can run `jupyter` using the following command.

```bash
jupyter notebook --ip=0.0.0.0 --allow-root --no-browser --port 8888
```

- What does each option do:
  1. Setting the `ip` like this forces the container to map the network to a specific location which will be accessible to the host machine. When referring to the _current_ machine there are three slightly different naming conventions used: `localhost`, `127.0.0.1`, and `0.0.0.0`. Each of these references the current machine and they each have slightly different meanings. Depending on the context one may or may not work.
  2. `--allow-root` is required because we are running as [a root user](https://support.apple.com/guide/directory-utility/about-the-root-user-dirub32398f1/mac).
  3. `--no-browser` is used to tell the jupyter server to not expect the current environment to have a web browser which is required for some features.
  4. `--port 8888` Forces the jupyter server to use the `8888` port. The `jupyter` server will default to `8888`, but if that port is in use will move to a different port. We want the server to return an error if the port is in use rather than move ports.

- If we run this command inside the container now the jupyter server will launch and we will be able to access it, as well as create notebooks and interact as you normally would with the container. 

- Importantly if you look at the `docker run` command we did above you will notice that we did not map a volume, which means that any file that we create inside the container will disappear as soon as we shut down the container. Let's put together a full docker run command that includes the volume mount:

```bash
docker run -it -p 8888:8888 -v $(pwd):/app/src class5 \
    jupyter notebook --ip=0.0.0.0 --allow-root --no-browser --port 8888
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

```makefile
IMAGE_NAME=class5

.PHONY: build interactive

build: 
    docker build . -t $(IMAGE_NAME)

interactive:
    docker run -it $(IMAGE_NAME) /bin/bash

```

In this example we set an environment variable called `IMAGE_NAME`. We have two commands which we define in our `PHONY` section and with the commands afterward. The first command builds the container while the second (`interactive`) runs an interactive session.

- On the command line we can type `make build` and `make interactive` in order to run these commands in an easier to use manner.

- While the above is interesting, we can layer dependencies and also create much more complex statements to make our lives easier. Consider the following `Makefile` which, while similar, has a number of additional features:

```makefile
IMAGE_NAME=class5

.PHONY: build notebook interactive

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

- This allows us to not have to remember to rebuild the container ourselves! Since the `docker build` command will only run if there are changes in the files, adding this will not re-build the image every time -- only if a file changes.

- We have also added `$(shell pwd)` rather than `$(pwd)` to the volume section of the file. One thing to note about Make syntax is that it is not exactly `bash` and we sometimes will have to do something different.

- In this case we use `$(shell pwd)` to tell make to run the `pwd` command in the shell/terminal. Doing this will return the current working directory and substitute it into that volume mount command.

- In this example there are three valid `make` commands: `notebook`, `build` and `interactive`. At the command line we can preface any of those with `make` and the commands defined in the Makefile will be run as expected.

### Passing Environment Variables 

- If we have an environment variable, such as an API key or other secret that we want to pass into the container we can pass them in through the Makefile by specifying it in the `docker run` command.
- For example, assume that the host machine has an environment variable called `API_KEY` and we wish to pass it to the container. If we model our code from the previous Makefile we could do something like this:

```makefile

...

interactive: build
	docker run -it \
	-v $(shell pwd):/app/src \
    -e API_KEY_IN_CONTAINER=$(API_KEY) \
	$(IMAGE_NAME) /bin/bash

...

```

Looking carefully at the example above we can see that we denote the `API_KEY` in the host using the dollar-sign parenthesis notation. This tells Make to look for this in the `bash` environment. 

- Inside the container the `-e` line would create an environment variable called `API_KEY_IN_CONTAINER` which would be equal to the value of `API_KEY` from the host environment.

- Consider the following Python function which we will put in our repo and work through:

```python
import os

if __name__ == "__main__":
    container_api_key = os.environ.get("API_KEY_IN_CONTAINER", None)
    if not container_api_key:
        raise KeyError("API key not found")
    print(f"API key found: {container_api_key}")

```

- Let's now update the `Makefile` to run this command so that we can test what it does:

```makefile
IMAGE_NAME=class5

.PHONY: build notebook interactive
COMMON_DOCKER_FLAGS= \
	-v $(shell pwd):/app/src \
	-e API_KEY_IN_CONTAINER=$(API_KEY) \

build:
	docker build . -t $(IMAGE_NAME)

interactive: build
	docker run -it \
	$(COMMON_DOCKER_FLAGS) \
	$(IMAGE_NAME) /bin/bash

notebook: build
	docker run -it -p 8888:8888 \
	$(COMMON_DOCKER_FLAGS) \
	$(IMAGE_NAME) \
	uv run jupyter notebook --allow-root --no-browser \
	--port 8888 --ip=0.0.0.0

run-env-cmd: build
	docker run  $(COMMON_DOCKER_FLAGS) -it $(IMAGE_NAME) \
	uv run python /app/src/env_var.py
```

- Before we begin we need to set an environment variable: how do we do that? We use:
```bash
export API_KEY=2
```

- Now when we run `make run-env-cmd` we will see our `API_KEY` printed to screen.
- Note that when we change the `API_KEY` in the external environment it gets passed through.
- This is how we can keep things in memory and then avoid having them appear in code. By putting them in the environment through a different secure process we can create a wall between our code and our secrets, thereby enhancing security.