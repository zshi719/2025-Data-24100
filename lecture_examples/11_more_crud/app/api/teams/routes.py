from flask import jsonify

from app.data_utils.loading_utils import (
    load_data,
)
from app.route_utils.decorators import (
    validate_team,
)

BASE_URL = "/api/teams"


@validate_team
def list_players_per_team(
    team,
):
    df = load_data()

    players_list = (
        df.loc[
            (df.team_abbreviation == team),
            ["id", "player_name"],
        ]
        .drop_duplicates()
        .to_dict("records")
    )

    to_return = {team: players_list}
    return jsonify(to_return), 200


def register_team_routes(app):
    @app.route(
        f"{BASE_URL}/players/<team>/list",
        methods=["GET"],
    )
    def list_players_per_team_route(
        team,
    ):
        return list_players_per_team(team)
