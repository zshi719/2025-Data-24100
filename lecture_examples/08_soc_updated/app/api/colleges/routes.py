from flask import jsonify
import pandas as pd
from app.data_utils.loading_utils import load_data
from app.route_utils.decorators import validate_team

BASE_URL = '/api/colleges'


def list_colleges():
    try:
        df = load_data()

        college_list = (
            df.loc[~(df.college.isna()), 'college'].unique().tolist()
        )

        return jsonify({'colleges': college_list}), 200

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@validate_team
def list_colleges_per_team(team):
    df = load_data()

    team_data = df.loc[
        (df.team_abbreviation == team), ['player_name', 'college']
    ]
    
    list_of_players_and_colleges = [
        {
            'player_name': row['player_name'], 
            'college': None if pd.isna(row['college']) else row['college']
        } 
        for _, row in team_data.iterrows()
    ]

    to_return = {team: list_of_players_and_colleges}
    return jsonify(to_return), 200


def register_college_routes(app):
    @app.route(f'{BASE_URL}/list', methods=['GET'])
    def list_colleges_route():
        return list_colleges()

    @app.route(f'{BASE_URL}/<team>/list', methods=['GET'])
    def list_colleges_per_team_route(team):
        return list_colleges_per_team(team)
