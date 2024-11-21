"""Player API route definitions and handlers.

This module provides Flask routes and handlers for managing players,
including listing, adding, deleting, and retrieving player information.
"""

from flask import jsonify, request

from app.data_utils.sql_utils import (
    add_player,
    delete_player,
    list_players_per_team_sql,
    player_info_sql,
)

BASE_URL = "/api/players"


def list_players_route():
    """Retrieve all players grouped by team.

    Returns:
        tuple: JSON response with players list and HTTP status code
    """
    try:
        players_list = list_players_per_team_sql()
        return jsonify({"players": players_list}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def delete_player_route(player_id):
    """Delete a player by their ID.

    Args:
        player_id (int): ID of player to delete

    Returns:
        tuple: Empty response with 204 status code on success, or error message
    """
    try:
        delete_player(player_id)
        return "", 204
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def add_player_route():
    """Add a new player to the database.

    Expects JSON with required fields: player_name, team
    Optional field: college

    Returns:
        tuple: JSON response with success message and player info, HTTP status
    """
    data = request.get_json()

    if not data.get("player_name"):
        return jsonify({"error": "player_name is required"}), 400
    if not data.get("team"):
        return jsonify({"error": "team is required"}), 400

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
    """Get detailed information for a specific player.

    Args:
        player_id (int): ID of player to retrieve

    Returns:
        tuple: JSON response with player info and HTTP status code
    """
    try:
        player_info = player_info_sql(player_id)
        if len(player_info) != 1:
            raise Exception("Player ID Unknown")
        return jsonify(player_info[0]), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def register_player_routes(app):
    """Register player-related routes with the Flask application.

    Args:
        app: Flask application instance
    """

    @app.route(f"{BASE_URL}", methods=["GET", "POST"])
    def base_url_handler():
        """Route handler for listing all players or adding a new player."""
        if request.method == "GET":
            return list_players_route()
        if request.method == "POST":
            return add_player_route()

    @app.route(f"{BASE_URL}/<int:player_id>", methods=["DELETE"])
    def delete_route(player_id):
        """Route handler for deleting a player."""
        return delete_player_route(player_id)

    @app.route(f"{BASE_URL}/<int:player_id>", methods=["GET"])
    def get_player_info(player_id):
        """Route handler for retrieving player information."""
        return get_player_info_route(player_id)
