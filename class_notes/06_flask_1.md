# Flask

- During today's class we will build a simple `Flask` server.
- There are many different web server frameworks that we could use. In the Python world `Django` and `FastAPI` are two that currently have a lot of mind share. 
- `Flask` is a lightweight and relatively simple package in Python. While `Django` is much more full featured and `FastAPI` is more performant, `Flask` offers a nice goldilocks version of a web server. `FastAPI` uses the async library so leverages additional computer knowledge outside of this course.
- Importantly, the same concepts and abstractions that are used in `Flask` are used in the other systems listed.

## Basics of a web server

- There are four major components of our system:
    1. **Client:** This is the device or software which will ask things.
    2. **Server:** This is the device which will do things in our system.
    3. **Request:** This is the data object that is sent from the client to the server to ask the server to do something.
    4. **Response:** This is the data object that is sent from the server back to the client after the request is received.
- In the most common set up our Client is a web-browser, such as Safari or Chrome which is sending a request to a web server to get data to view on the client. The client will send a request which the server will receive and then respond with some HTML/CSS/JS for the browser to render.
- The protocol used for the request and response is HyperText Transfer Protocol (HTTP) is one of the most common protocols for sending and receiving responses over a network. HTTP is the basis for how the web works.
- There are other protocols, but for the purposes of this class we will focus on this one.

## Request Object
- An HTTP Request object consists of the following four components:
    1. **URL:** This is the server, port and path that the query is trying to get to. An example could be `http://www.google.com/`. The default port for an http request is 80 and the path is the root `/`. The server is `www.google.com`.
    2. **Query Parameters:** Web sites can attach a query parameter to a url in order to communicate additional information. Query parameters are designated by a question mark and an ampersand delimited list of key-value pairs. For example, if you go to google and then do a search in the web browser you will see something that looks like `?q=search_terms&src=...` These are query parameters and, while they are appended to the URL are parsed differently.
    3. **Request Body:** The client can add arbitrary data to the request in the body. The request body can contain text, or an image (such as when you upload an image to a web service) or any other data.
    4. **Request Header:** The request header is a list of information that is frequently expressed as a dictionary of information that the client sends. This information is usually considered `meta` information and contains things like the type of web browser or the size of the screen. Information in the header is supposed to help the server process the data in the rest of the request. Headers often contain information about any compression that is going on in the body of the request as well as authorization.
    5. **Request Type:** An HTTP request also has a request type which broadly denotes what the client is expecting the server to do. The most common request types are `GET` (have the server send information back), `POST` (add information to the server) and `PUT` (update information on the server). There are lots of other types, but these are the most prevalent. 

## Response Object
- Once a request is received, the server prepares a response. The response object contains the following components:
    1. **Response Body:** This is where the server puts any data for the client to process. In the case of a web page, the body is where the `html` will be.
    2. **Response Headers:** Just like the request, the response will also have headers. Just like the request, the response headers are designed to provide meta information about the response, such as compression, the type of data in the body, etc.
    3. **Status Code:** The status code of an http request helps the client understand how the server is responding. Status codes are three digit integers. For example, 200 denotes a successful response while 4xx and 5xx are used when an error occurs.

## Our Flask Web Server

In this section we are going to build a Flask based web app that will print (to the terminal) the header, body and query parameters of a request. We will also respond with an appropriate status code.

### Dependencies

We need to have `Flask` installed. In this example we also want to have access to Jupyter, so our `pyproject.toml` will look like:

```
jupyter==1.0.0
flask==3.1.2
```

### Makefile

We will build off the Makefile from our previous lecture

```makefile
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
	uv run jupyter notebook --allow-root --no-browser \
	--port 8888 --ip=0.0.0.0

flask: build
	docker run -p 4000:5000 \
	-v $(shell pwd):/app/src \
	$(IMAGE_NAME) \
	uv run python /src/app.py 
```

- We have added a few lines to our code:
  - The line `-p 4000:5000` maps the port inside the container (5000) to the host's 4000 port. This mapping is done on my computer because I have something already running on 5000. 

### Dockerfile

There are two lines that we will add to our standard Dockerfile:

```dockerfile
FROM astral/uv:python3.13-bookworm
WORKDIR /app

# Put the pyproject.toml & print_date.py file into the container
COPY pyproject.toml .

# Create a virtual environment and set the location to /app/.venv
RUN uv venv
RUN uv sync

```

- The line `ENV PYTHONUNBUFFERED=1` is a common parameter used to manage Python's output. When we run `Flask` inside a container we need to add this parameter to have terminal output printed in the manner we expect.

### Python File

- In our Makefile we specified that our `Flask` app location was `/app/src/app.py` so we will name this file `app.py`

```python
from flask import (
    Flask,
    Response
)

# Creating a Flask Application with default
# parameters and a name.
app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    return Response("Hello World", status=200,
                headers={'Content-type': 'text/html'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


```

- We import three objects from `flask` -- the server, the response object and the request object.
- The `app` is created in the global namespace on purpose. Since so much relies on the core app and we need access to the decorators that are used in the routes (the lines that begin with an `@` sign).
- In the `main` function we start our `flask` app on port 5000, so inside the container it is running on this port.
- The route that we have set up is `/test` and it will respond to a GET with a status 200 message of type `text/html` that says `Hello World`.
  - if you run this using `make flask` you should be able to go to your browser and type in `http://127.0.0.1:4000/test` and see this message!

### Printing the header query string and body

- The version of `app.py` below is a more complex version that handles printing the body, query parameters and headers. 

```python
from flask import (
    Flask,
    request,
    Response
)

# Creating a Flask Application with default
# parameters and a name.
app = Flask(__name__)


@app.route('/auth_route', methods=['GET'])
def secret_route():
    secret_password = "1235"
    # our logic: If there is a key/value pair 
    # in the header with "password" = secret_password
    # we will return status code 200 and a smiley face

    # If not:
    # we return 500

    secret = request.headers.get('Password', None)
    if secret == secret_password:
        return Response(":)", status=200,
                        headers={'Content-type': 'text/html'})

    else:
        return Response("You don't know the password", status=501,
                        headers={'Content-type': 'text/html'})


@app.route('/test', methods=['GET'])
def print_to_screen():
    print('\n')
    print('request received!!!!'.upper())

    # header printing
    print('\n')
    print("Header Info")
    print("---"*10)
    to_return_list = []
    for header, value in request.headers.items():
        header_item_info = f"{header}: {value}"
        print(header_item_info)

    # query parameter printing
    print('\n')
    print("Query Parameters Info")
    print("---"*10)
    to_return_list = []
    for header, value in request.args.items():
        header_item_info = f"{header}: {value}"
        print(header_item_info)
        to_return_list.append(header_item_info)

    # body printing
    print('\n')
    print("Body Info")
    print("---"*10)
    body = request.get_data(as_text=True)
    print(f"{body}")

    return Response('Here is my response', status=200,
                    headers={'Content-type': 'text/html'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

- The first function `secret_route` also demonstrates an authorization tactic for blocking users you do not want in the system.
- Specifically if the user does not provide, in the header, the password, they will receive a 500 response.

### Important notes on Headers

- Headers are handled inconsistently regarding case. While they should be case insensitive, some applications manipulate them in unexpected ways. Whenever you compare them it is best practice to handle case yourself.
- Underscores cannot be in headers -- use `-` instead if you want to separate words.