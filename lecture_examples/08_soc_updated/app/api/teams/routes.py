from flask import jsonify
from app.data_utils.loading_utils import load_data
from app.route_utils.decorators import validate_team

BASE_URL = '/api/teams'


@validate_team
def list_players_per_team(team):
    df = load_data()

    list_of_players = (df
                       .loc[(df.team_abbreviation == team), 'player_name']
                       .to_list()
                       )

    to_return = {team: list_of_players}
    return jsonify(to_return), 200


def register_team_routes(app):
    @app.route(f'{BASE_URL}/players/<team>/list', methods=['GET'])
    def list_players_per_team_route(team):
        return list_players_per_team(team)
