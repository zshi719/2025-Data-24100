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


run-flask: build
	docker run -p 4000:5000 \
	$(COMMON_DOCKER_FLAGS) \
	$(IMAGE_NAME) \
	uv run python /app/src/app.py
