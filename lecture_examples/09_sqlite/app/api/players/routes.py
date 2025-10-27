from app.data_utils.loading_utils import load_data, delete_player, add_player
from flask import jsonify, request

BASE_URL = "/api/players"


def list_players():
    try:
        df = load_data()
        players_list = df["player_name"].unique().tolist()
        return jsonify({"players": players_list}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def delete_player_route(player_name):
    try:
        delete_player(player_name)
        return jsonify({"message": f"Deleted player: {player_name}"}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def add_player_route():
    try:
        data = request.get_json()

        print(data)
        # This returns the information in the body of the request

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

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def register_player_routes(app):
    @app.route(f"{BASE_URL}/list", methods=["GET"])
    def list_players_route():
        return list_players()

    @app.route(f"{BASE_URL}/<player_name>", methods=["DELETE"])
    def delete_route(player_name):
        return delete_player_route(player_name)

    @app.route(f"{BASE_URL}", methods=["POST"])
    def add_route():
        return add_player_route()
