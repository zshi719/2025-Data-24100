from functools import wraps

from flask import jsonify

from app.data_utils.loading_utils import (
    load_data,
)


def validate_team(f):
    @wraps(f)
    def decorated_function(team, *args, **kwargs):
        df = load_data()
        if (
            team
            not in df.loc[
                :,
                "team_abbreviation",
            ].unique()
        ):
            return jsonify({"Error": f"Team {team} does not exist"}), 404
        return f(
            team,
            *args,
            **kwargs,
        )

    return decorated_function
