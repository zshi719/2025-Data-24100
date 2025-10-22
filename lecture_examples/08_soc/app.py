from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)


@app.route('/list_players', methods=['GET'])
def list_players_route():
    df = pd.read_csv('/app/src/all_seasons.csv')
    df = df.loc[
        (df.season == '2022-23'),
        ['player_name', 'college', 'team_abbreviation'],
    ]

    players_list = df['player_name'].unique().tolist()

    to_return = {'players': players_list}
    return jsonify(to_return), 200


@app.route('/list_colleges', methods=['GET'])
def list_colleges_route():
    df = pd.read_csv('/app/src/all_seasons.csv')
    df = df.loc[
        (df.season == '2022-23'),
        ['player_name', 'college', 'team_abbreviation'],
    ]

    df = df.loc[~(df.college.isna()), :]
    college_list = df['college'].unique().tolist()

    to_return = {'college': college_list}
    return jsonify(to_return), 200


@app.route('/colleges_team/<team>')
def list_colleges_per_team(team):
    df = pd.read_csv('/app/src/all_seasons.csv')
    df = df.loc[
        (df.season == '2022-23'),
        ['player_name', 'college', 'team_abbreviation'],
    ]

    if team not in df.loc[:, 'team_abbreviation'].unique():
        return jsonify({'Error': f'Team {team} does not exist'})

    college_list = df.loc[
        (df.team_abbreviation == team) & ~(df.college.isna()), 'college'
    ].unique().tolist()

    to_return = {team: college_list}
    return jsonify(to_return), 200


@app.route('/players_team/<team>')
def list_players_and_colleges_per_team(team):
    df = pd.read_csv('/app/src/all_seasons.csv')
    df = df.loc[
        (df.season == '2022-23'),
        ['player_name', 'college', 'team_abbreviation'],
    ]

    if team not in df.loc[:, 'team_abbreviation'].unique():
        return jsonify({'Error': f'Team {team} does not exist'}), 500

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
