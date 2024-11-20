"""Player based routes"""

from flask import jsonify, request

from app.data_utils.loading_utils import add_player, delete_player, load_data

BASE_URL = "/api/players"


def list_players_route():
    try:
        df = load_data()
        players_list = (
            df.loc[:, ["id", "player_name"]]
            .drop_duplicates()
            .to_dict("records")
        )
        return jsonify({"players": players_list}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def delete_player_route(player_id):
    try:
        player_name = delete_player(player_id)
        return "", 204
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def add_player_route():
    data = request.get_json()

    # Validate required fields
    if not data.get("player_name"):
        return jsonify({"error": "player_name is required"}), 400
    if not data.get("team"):
        return jsonify({"error": "team is required"}), 400

    # Add player with optional college
    add_player(data)

    return jsonify(
        {
            "message": f"Successfully added player: {data['player_name']}",
            "player": {
                "name": data["player_name"],
                "team": data["team"],
                "college": data.get("college"),
            },
        }
    ), 201


def get_player_info_route(player_id):
    try:
        df = load_data()
        players_list = df.loc[(df.loc[:, "id"] == player_id), :].to_dict(
            "records"
        )
        # assert len(players_list) == 1, "Player ID Unknown"

        if len(players_list) != 1:
            raise Exception("Player ID Unknown")
        # Because we are filtering here we want to make a check that the
        # number of players being returned is actually 1.
        # We will talk more about assert / test later.
        return jsonify(players_list[0]), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def register_player_routes(app):
    @app.route(f"{BASE_URL}", methods=["GET", "POST"])
    def base_url_handler():
        if request.method == "GET":
            return list_players_route()
        if request.method == "POST":
            return add_player_route()

    @app.route(f"{BASE_URL}/<int:player_id>", methods=["DELETE"])
    def delete_route(player_id):
        return delete_player_route(player_id)

    @app.route(f"{BASE_URL}/<int:player_id>", methods=["GET"])
    def get_player_info(player_id):
        return get_player_info_route(player_id)
