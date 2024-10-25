import pandas as pd


def load_data():
    file_path = '/app/src/data/all_seasons.csv'
    df = pd.read_csv(file_path)
    df = df.loc[
        df.season == '2022-23',
        ['player_name', 'college', 'team_abbreviation']
    ]

    return df
