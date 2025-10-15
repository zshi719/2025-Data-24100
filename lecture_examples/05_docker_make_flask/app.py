## Flask Server
from flask import (
    Flask,
    Response,
    request
)

# How you create the flask app.
# Required before defining routes.
app = Flask(__name__)

# define our routes
@app.route('/test_harriet', methods=['GET'])
def test():
    return Response("Hello world", status=200, 
                    headers={'Content-type': 'text/html'})

@app.route('/', methods=['GET'])
def test_home():
    return Response("Hello it's me. ", status=200, 
                    headers={'Content-type': 'text/html'})

@app.route('/auth_route', methods=['GET'])
def secret_route():
    secret_password = "12345"

    # If there is a key-value pair of secret password in the header 
    # then we will respond with a 200 and a smiley face

    # otherwise reject the request with a 501

    secret = request.headers.get('Password', None)

    if secret == secret_password:
        return Response(":)", status=200, headers={'Content-type': 'text/html'})
    else:
        return Response("You don't know the password", status=501,
                    headers={'Content-type': 'text/html'})


@app.route('/print', methods=['GET'])
def print_to_screen():
    print('\n')
    print('Requests Received')

    # Print Headers
    print ('\n')
    print("Header Info")
    print("---"*10)
    for header, value in request.headers.items():
        header_item_info = f"{header}: {value}"
        print(header_item_info)

    # Print Query Parameters
    print('\n')
    print("Query Params")
    print("---"*10)
    for query_key, query_value in request.args.items():
        query_item_info = f"{query_key}: {query_value}"
        print(query_item_info)


    # Print Query Parameters
    print('\n')
    print("Body")
    print("---"*10)
    body = request.get_data(as_text=True)
    print(f"{body}")

    return Response("Ha!", status = 200, headers={"Content-type": 'text/html'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)