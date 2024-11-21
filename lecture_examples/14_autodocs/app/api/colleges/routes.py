"""College API route definitions and handlers.

This module provides Flask routes and handlers for listing colleges,
either all colleges or filtered by team.
"""

from flask import jsonify

from app.data_utils.sql_utils import list_college_sql
from app.route_utils.decorators import validate_team

BASE_URL = "/api/colleges"


def list_colleges():
    """Retrieve all colleges from the database.

    Returns:
        tuple: JSON response with college list and HTTP status code
    """
    try:
        college_list = list_college_sql()
        return jsonify({"colleges": college_list}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@validate_team
def list_colleges_per_team(team):
    """Retrieve colleges filtered by team. tre

    Args:
        team (str): Team identifier to filter colleges

    Returns:
        tuple: JSON response with filtered college list and HTTP status code

    Note:
        What a Great Function. So Glad I built it.

    Warning:
        BE CAREFUL WITH THIS. It is very powerful.

    """
    college_list = list_college_sql(team=team)
    return jsonify({"colleges": college_list}), 200


def register_college_routes(app):
    """Register college-related routes with the Flask application.

    Args:
        app: Flask application instance
    """

    @app.route(f"{BASE_URL}/list", methods=["GET"])
    def list_colleges_route():
        """Route handler for listing all colleges."""
        return list_colleges()

    @app.route(f"{BASE_URL}/<team>/list", methods=["GET"])
    def list_colleges_per_team_route(team):
        """Route handler for listing colleges by team."""
        return list_colleges_per_team(team)
