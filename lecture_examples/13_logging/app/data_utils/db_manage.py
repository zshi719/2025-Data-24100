"""DB Management Accessor Function

This module contains the basic access method for the DB Management functions
"""

import argparse
import os

from loading_utils import (
    create_and_load_basketball_data,
    create_empty_sqlite_db,
    rm_db,
)

DATA_DIR = os.environ["DATA_DIR"]


if __name__ == "__main__":
    command_list = ["db_create", "db_load", "db_rm", "db_clean"]
    parser = argparse.ArgumentParser(description="Manage the SQLite database.")

    parser.add_argument(
        "command", choices=command_list, help="Command to execute"
    )

    args = parser.parse_args()
    csv_path = DATA_DIR + "/all_seasons.csv"
    table_name = "player_stats"

    if args.command == "db_create":
        create_empty_sqlite_db()
    if args.command == "db_load":
        create_and_load_basketball_data(csv_path, table_name)
    if args.command == "db_rm":
        rm_db()
    if args.command == "db_clean":
        rm_db()
        create_empty_sqlite_db()
        create_and_load_basketball_data(csv_path, table_name)
