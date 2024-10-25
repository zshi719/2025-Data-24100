IMAGE_NAME=flask_app

.PHONY=build notebook interactive

build:
	docker build . -t $(IMAGE_NAME)

interactive: build
	docker run -it \
	-v $(shell pwd):/app/src \
	-e API_KEY_IN_CONT=$(APITEST) \
	$(IMAGE_NAME) /bin/bash

notebook: build
	docker run -it -p 8888:8888 \
	-v $(shell pwd):/app/src \
	$(IMAGE_NAME) \
	jupyter notebook --allow-root --no-browser \
	--port 8888 --ip=0.0.0.0

run: build
	docker run -p 4000:5000 \
	-v $(shell pwd):/app/src \
	-e FLASK_APP=src/app.py \
	-e FLASK_DEBUG=1 \
	-e FLASK_ENV=development \
	$(IMAGE_NAME)
