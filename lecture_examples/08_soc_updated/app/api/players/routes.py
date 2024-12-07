from flask import jsonify
from app.data_utils.loading_utils import load_data

BASE_URL = "/api/players"


def list_players():
    try:
        df = load_data()
        players_list = df["player_name"].unique().tolist()
        return jsonify({"players": players_list}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def register_player_routes(app):
    @app.route(f"{BASE_URL}/list", methods=["GET"])
    def list_players_route():
        return list_players()
