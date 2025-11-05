"""All Decorator Functions"""

import time
from functools import wraps

from flask import jsonify, request

from app.data_utils.sql_utils import (
    all_teams_sql,
)
from app.logger_utils.custom_logger import custom_logger


def validate_team(f):
    """Wrapper to validate team and return 404 if does not exist"""

    @wraps(f)
    def decorated_function(team, *args, **kwargs):
        all_teams = all_teams_sql()
        if team not in all_teams:
            return jsonify({"Error": f"Team {team} does not exist"}), 404
        return f(
            team,
            *args,
            **kwargs,
        )

    return decorated_function


def log_request_response(f):
    """Wrapper to log all requests and responses"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        custom_logger.debug(
            "Request received: " f"{request.method} {request.path}"
        )

        response = f(*args, **kwargs)

        custom_logger.debug(f"Response: {response[1]} - {request.path}")
        return response

    return decorated_function


def log_request_response_time(f):
    """Wrapper to log all requests times"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        custom_logger.info(
            f"Request received: {request.method} {request.path}"
        )

        response = f(*args, **kwargs)
        # Convert to milliseconds
        execution_time = (time.time() - start_time) * 1000
        custom_logger.info(
            f"Response: {response[1]} - {request.path} "
            f"- Execution time: {execution_time:.2f}ms"
        )
        return response

    return decorated_function
