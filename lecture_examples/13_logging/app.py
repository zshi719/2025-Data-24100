"""Flask application setup and initialization.

This module configures and creates the Flask application instance,
sets up logging, and registers API route blueprints.
"""

import logging

from flask import Flask

from app.api.colleges.routes import (
    register_college_routes,
)
from app.api.players.routes import (
    register_player_routes,
)
from app.api.teams.routes import (
    register_team_routes,
)
from app.logger_utils.custom_logger import custom_logger


def create_app():
    """Create and configure the Flask application instance.

    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)

    # Logging Level to use (default DEBUG for now)
    logging_level = logging.DEBUG
    # Initialize logger
    app.logger = custom_logger  # Attach logger to Flask app
    app.logger.setLevel(logging_level)
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(logging_level)
    werkzeug_logger.handlers = []
    werkzeug_logger.addHandler(app.logger.handlers[0])

    register_player_routes(app)
    register_team_routes(app)
    register_college_routes(app)
    app.logger.info("Application initialized successfully")
    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
