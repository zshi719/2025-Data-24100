"""Database query utilities for managing basketball player and college data.

This module provides functions for querying and modifying player statistics
and college information in the SQLite database.
"""

from app.data_utils.loading_utils import (
    create_db_connection,
    execute_query_return_list_of_dicts_lm,
)


def list_college_sql(team=None):
    """Get list of colleges for all players or players from a specific team.

    Args:
        team (str, optional): Team abbreviation to filter by. Defaults to None.

    Returns:
        list: College names.
    """
    conn = create_db_connection()

    if team is None:
        list_colleges_query = (
            "SELECT distinct college from player_stats "
            " where season = '2022-23';"
        )
    else:
        list_colleges_query = (
            "SELECT distinct college from player_stats "
            f" where team_abbreviation = '{team}' and "
            " season = '2022-23';"
        )

    sql_results_dict = execute_query_return_list_of_dicts_lm(
        conn, list_colleges_query
    )

    return [x["college"] for x in sql_results_dict]


def list_players_per_team_sql(team=None):
    """Get list of players and their IDs for all teams or a specific team.

    Args:
        team (str, optional): Team abbreviation to filter by. Defaults to None.

    Returns:
        list: Dictionaries containing player names and IDs.
    """
    conn = create_db_connection()

    if team is None:
        list_query = (
            "SELECT distinct player_name, id from player_stats "
            " where season = '2022-23';"
        )
    else:
        list_query = (
            "SELECT distinct player_name, id from player_stats "
            f" where team_abbreviation = '{team}' and "
            " season = '2022-23';"
        )

    sql_results_dict = execute_query_return_list_of_dicts_lm(conn, list_query)

    return sql_results_dict


def add_player(player_info):
    """Add a new player to the database.

    Args:
        player_info (dict): Player information including name, team,
        and optional college.
    """
    conn = create_db_connection()
    query = """
    INSERT INTO player_stats
    (player_name, team_abbreviation, college, season)
    VALUES
    (?, ?, ?, '2022-23')
    """

    params = (
        player_info["player_name"],
        player_info["team"],
        player_info.get("college"),
    )

    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()


def delete_player(player_id):
    """Delete a player by ID and return their name.

    Args:
        player_id (int): ID of player to delete

    Returns:
        str: Name of deleted player

    Raises:
        ValueError: If no player found with given ID
    """
    conn = create_db_connection()

    # First get the player name
    name_query = """
    SELECT player_name
    FROM player_stats
    WHERE id = ?
    AND season = '2022-23'
    LIMIT 1
    """

    cursor = conn.cursor()
    cursor.execute(name_query, (player_id,))
    result = cursor.fetchone()

    if not result:
        raise ValueError(f"No player found with ID: {player_id}")

    player_name = result[0]

    # Then delete the player
    delete_query = """
    DELETE FROM player_stats
    WHERE id = ?
    AND season = '2022-23'
    """

    cursor.execute(delete_query, (player_id,))
    conn.commit()

    return player_name


def all_teams_sql():
    """Get a list of all teams in the table

    Args:
        None

    Returns:
        list: list containing the unique teams
    """
    conn = create_db_connection()

    team_query = (
        "select distinct team_abbreviation from player_stats "
        " where season = '2022-23'"
    )

    sql_results_dict = execute_query_return_list_of_dicts_lm(conn, team_query)
    team_list = [x["team_abbreviation"] for x in sql_results_dict]

    return team_list


def player_info_sql(player_id):
    """Get detailed information for a specific player.

    Args:
        player_id (int): Player's ID in database

    Returns:
        list: List containing dictionary with player information
    """
    conn = create_db_connection()

    player_query = (
        f"select * from player_stats where id = {player_id} "
        " and season = '2022-23'"
    )

    sql_results_dict = execute_query_return_list_of_dicts_lm(
        conn, player_query
    )

    return sql_results_dict
