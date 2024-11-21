"""Team API route definitions and handlers.

This module provides Flask routes and handlers for team-related operations,
specifically listing players by team.
"""

from flask import jsonify

from app.data_utils.sql_utils import list_players_per_team_sql
from app.route_utils.decorators import (
    log_request_response,
    log_request_response_time,
    validate_team,
)

BASE_URL = "/api/teams"


@validate_team
@log_request_response
@log_request_response_time
def list_players_per_team(team):
    """List all players for a specific team.

    Args:
        team (str): Team identifier to filter players

    Returns:
        tuple: JSON response containing team's players and HTTP status code
    """
    list_of_players = list_players_per_team_sql(team)
    to_return = {team: list_of_players}
    return jsonify(to_return), 200


def register_team_routes(app):
    """Register team-related routes with the Flask application.

    Args:
        app: Flask application instance
    """

    @app.route(f"{BASE_URL}/players/<team>/list", methods=["GET"])
    def list_players_per_team_route(team):
        """Route handler for listing players by team."""
        return list_players_per_team(team)
