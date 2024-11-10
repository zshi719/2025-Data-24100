## Quiz 2 AK

There were a few common errors / changes:

1. When starting with relatives paths it is unnecessary to add  `./` at the start. Just provide the  path (e.g. `rm ./docs/image2.jpg` vs. `rm docs/image2.jpg`)
2. Not creating the directory to put the `jpg` files in for problem 2.


---

1. Move `requirements.txt` to the correct location. Assume your current working directory is `/users/nick` and use a single command with relative paths to move the `requirements.txt`` file to the correct location. 

`mv old_project/requirements.txt project`

2. There are a number of `*.jpg` files in the `old\_project/jpgs`. Using absolute paths, write a set of commands that will allow the `COPY` command in the Dockerfile to run properly.

There are two parts of this: (1) creating the directory and then moving or copying the files:

```
mkdir /users/nick/project/jpgdir
cp /users/nick/old_project/jpgs/*.jpg /users/nick/project/jpgdir

```

3. The environment variable `MY\_NAME` will be printed on the terminal at build, however it is not currently set in the Dockerfile. Please write a line of code to be added to the Dockerfile to have it print ``NICK" when building.

```
ENV MY_NAME=NICK
```

4. We run the container using `docker run -it quiz\_image /bin/bash`. Please modify this so that an environment variable (`MY\_VAR`) is set inside the container, with a value of `1234`. Write the entire `docker run` command.

```
docker run -it -e MY_VAR=1234 quiz_image /bin/bash
```