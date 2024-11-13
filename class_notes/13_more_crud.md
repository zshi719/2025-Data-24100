# More CRUD

- Todays lecture will cover building endpoints with multiple functionalities
- We will also work through some additional abstraction levels
- We will begin a conversation around testing
- Note that the lecture material here was done by video, so the content format is slightly different.

## Expected Data

- In our previous lectures we had defined the parts of an http request and specifically mentioned a few places where we could pass data:

1. Through the url directly:
   1. Either the url itself (path parameter, URL Parameter)
   2. Query parameters
2. Through the body of the request (as we do in POST requests)
3. Through the header of the request (as we do with our authentication)

- When running an API we try to be consistent around what data paths are used for different request types. This makes our API easier to understand and debug. 
- While I've seen APIs do a lot of things, the following table shows some general rules around which data types should be used for which request type. 
- Much of the below is historical and revolves around how we develop our abstractions between our data and code.
- While there are examples of APIs that stray from the below, this is a pretty common starting point.


| Request Type | Usual Data Types |
| --- | --- |
| POST | <ul><li>**Body**: Complete new resource data</li><li>**Headers**: Authentication tokens</li><li>**Headers**: Content-Type specification (usually JSON)</li></ul> |
| GET | <ul><li>**URL**: Resource IDs</li><li>**Query**: Filtering/pagination parameters</li><li>**Headers**: Authentication tokens</li><li>**Body**: Generally none</li></ul> |
| PUT/PATCH | <ul><li>**URL**: Resource ID</li><li>**Body**: Updated fields (complete resource for PUT, partial for PATCH)</li><li>**Headers**: Authentication tokens</li><li>**Headers**: Content-Type specification</li></ul> |
| DELETE | <ul><li>**URL**: Resource ID</li><li>**Headers**: Authentication tokens</li><li>**Body**: Generally none</li><li>**Query**: Sometimes used for bulk operations</li></ul> |

## Accessing each data

- When we use flask we access data type differently. When using flask there are a few access patterns for each that we should know:

| Data object | Example | Accessor | Description | 
| --- | --- | --- | --- | 
| Query Parameters | `https://www.google.com/search?q=uchicago` | `requests.args` | This returns a dictionary like object. To convert it to an actual dictionary you can use `request.args.to_dict` though if there are multiply defined query parameters you will lose them. |
| URL Parameters | `https://github.com/NickRoss` | `https://github.com/<string:username>` | The parameter is then passed to the function inside the route handler. | 
| Body | Usually a JSON object | In flask there are accessor methods on the request that are specific to the data type. For json we can use either `request.get_json` or `request.json` | We use different methods depending on the context (e.g. uploading a file vs. simply sending some json data). There are lots of different ways to handle these things. | 
| Headers | Similar to the body it is usually described as dictionary like object | `requests.headers` is a dictionary like object for accessing the headers. | This is not a dictionary and there are some important differences. Headers are not case-sensitive, for example. | 

## Multiple request types 

- Flask allows us to easily track the request types and check for different data types in each. 
- One thing to keep in mind as you work through your own code is that it is very easy to violate the DRY principle when writing boilerplate code for routes abstraction.
- In the case of using multiple methods at a single endpoint there are a number of different methods for doing it, the key, like all code that we try to write is to keep it simple and consistent.

- Using the example from an updated version of our [basketball flask](../lecture_examples/11_more_crud/) lets take a look at how to do this:

```
from flask import jsonify, request

from app.data_utils.loading_utils import add_player, delete_player, load_data

BASE_URL = "/api/players"


def list_players_route():
    try:
        df = load_data()
        players_list = (df.loc[:, ["id", "player_name"]]
                        .drop_duplicates()
                        .to_dict("records")
                        )
        return jsonify({"players": players_list}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def delete_player_route(player_id):
    try:
        player_name = delete_player(player_id)
        return jsonify({
            "message": f"Deleted player: {player_name}",
            "id": player_id
        }), 204
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def add_player_route():
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get("player_name"):
            return jsonify({"error": "player_name is required"}), 400
        if not data.get("team"):
            return jsonify({"error": "team is required"}), 400

        # Add player with optional college
        add_player(
            data
        )

        return jsonify({
            "message": f"Successfully added player: {data['player_name']}",
            "player": {
                "name": data["player_name"],
                "team": data["team"],
                "college": data.get("college")
            }
        }), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def get_player_info_route(player_id):
    try:
        df = load_data()
        players_list = (df.loc[(df.loc[:, "id"] == player_id), :]
                        .to_dict("records")
                        )
        assert len(players_list) == 1
        return jsonify(players_list[0]), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def register_player_routes(app):
    @app.route(f"{BASE_URL}", methods=["GET"])
    def list_route():
        return list_players_route()

    @app.route(f"{BASE_URL}", methods=["POST"])
    def add_route():
        return add_player_route()

    @app.route(f"{BASE_URL}/<int:player_id>", methods=["DELETE"])
    def delete_route(player_id):
        return delete_player_route(player_id)

    @app.route(f"{BASE_URL}/<int:player_id>", methods=["GET"])
    def get_player_info(player_id):
        return get_player_info_route(player_id)
```

- Lets start from the _bottom_ and work our way through the code.
- In the `register_player_routes` function we have four functions, each one corresponding to a single route-request type combination. Each route function has a simple call and response.
- This is well organized and keeps a consistent abstraction level. 
- This is not the only way that we could have broken up the routes. We could, instead choose a different abstraction layer but forcing the decision point of the request further down. For example:

```
def register_player_routes(app):
    @app.route(f"{BASE_URL}", methods=["GET", "POST"])
    def base_routes():
        if request.method == 'GET':
            return list_players_route()

        if request.method == 'POST':
            return add_player_route()


    @app.route(f"{BASE_URL}/<int:player_id>", methods=["GET", "DELETE"])
    def base_player_route():
        if request.method == 'DELETE':
            return delete_player_route(player_id)

        if request.method == 'GET':
            return get_player_info_route(player_id)
```

- Looking at the methods above they functionally do the same thing, but they change where in the code the branching occurs for the method. 
- Is one better than the other? I'd make a slight argument that the first version is better, but both abstractions could be reasonably argued.
- The most important factor is that this abstraction is kept across the entire code base. 
