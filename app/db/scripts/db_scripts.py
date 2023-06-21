"""Module contains scripts for creating database
 and filling it with data from log files."""

from datetime import datetime

from typing import Union

from app.extensions import db_wrapper
from app.constants import ABBREVIATIONS, START_LOG, END_LOG, LAP_TIME, END_TIME, \
    START_TIME, SURNAME, NAME, ID, TEAM_ID, DATETIME_STRING
from app.db.models import Team, Driver, Result, get_models

# Integers are used to format lap time string.
TRAILING_ZEROS = 3
LEADING_ZEROS = -3


def create_tables():
    """Create and prepare database.

    When application is lunched for the first time, database and tables should
    be created and filed with data from log files.
    """
    # Get models in dictionary.
    models = get_models()
    with db_wrapper.database.connection_context():
        tables = db_wrapper.database.get_tables()
        # Check if db has tables.
        if not tables:
            # Create tables from models.
            db_wrapper.database.create_tables(models.values())
            # Fill database with data from log files.
            fill_database_with_data()


def data_from_abbreviation(path: str):
    """Get data from abbreviations file.

    Read file and get driver's abbreviation, driver's full name and team name.

    Args:
        path: path to the abbreviation file.

    Returns:
        tuple[dict[str: int], list[dict[Union[str, int]]]:
            dictionary of teams where key is team name and value team id, and
            list of drivers, where drivers is dictionary with driver id, name,
            surname and team id.

    Example:
        ({"SCUDERIA TORO ROSSO HONDA": 7},
         [{"id": "BHS", "name": "Brendon", "surname": "Hartley", "team_id": 7})
    """
    teams = {}
    drivers = []

    with open(path, encoding="utf8") as file:
        # team_id is value in dictionary of teams, when key is team name.
        team_id = 1
        for line in file:
            line = line.strip()
            if line:
                # Data in line is split with underscore:
                # "abbreviation_driver_team".
                driver_id, fullname, team = line.split("_")

                # Add team if it is not in dictionary of teams.
                if team not in teams:
                    teams[team] = team_id
                    team_id += 1

                name, surname = fullname.split(" ")
                driver = {ID: driver_id,
                          NAME: name,
                          SURNAME: surname,
                          TEAM_ID: teams[team]}  # Add Foreign Key of team.
                # Add driver to dictionary of drivers.
                drivers.append(driver)
    return teams, drivers


def data_from_logs(start_log, end_log):
    """Get data from log files.

    Read files and get driver start and finish time.
    Also calculate driver lap time.

    Args:
        start_log: path to start log file.
        end_log: path to end log file.

    Returns:
        dict[str: dict[str: str]: dictionary where key is driver id and value is
        dictionary of result.

    Example:
        {"BHS": {"start_time": "2018-05-24 12:05:14.100",
                 "end_time": "2018-05-24 12:06:28.100",
                 "lap_time": 1:14:000"}}
    """
    results = {}
    # Open start log file.
    with open(start_log, encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if line:
                # First three chars in the line is abbreviation - key,
                # rest is 1st qualification start time or end time of the lap
                driver_id = line[:3]
                start_time = datetime.strptime(line[3:].strip(), "%Y-%m-%d_%H:%M:%S.%f")

                # Add new key-value pair to dictionary of results,
                # where key is driver id and value is dictionary with start time.
                results[driver_id] = {START_TIME: start_time}

    # Open end log file.
    with open(end_log, encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if line:
                # First three chars in the line is abbreviation - key,
                # rest is 1st qualification start time or end time of the lap
                driver_id = line[:3]
                end_time = datetime.strptime(line[3:].strip(), DATETIME_STRING)

                # Add end time to the dictionary of specific driver
                results[driver_id][END_TIME] = end_time
                # Count driver's lap time in string format. Example: 2:12:831
                lap_time = str(results[driver_id][END_TIME] - results[driver_id][START_TIME])[
                           TRAILING_ZEROS: LEADING_ZEROS]
                # Add lap time to the dictionary of specific driver
                results[driver_id][LAP_TIME] = lap_time

    return results


def add_data_to_team_table(teams: dict[str: int]):
    """Adds data to Team table

    Args:
        teams: data to fill in the table.
    """
    for team_name, team_id in teams.items():
        Team.create(id=team_id, name=team_name)


def add_data_to_driver_table(drivers: list[dict[Union[str, int]]]):
    """Adds data to Driver table

        Args:
            drivers: data to fill in the table.
        """
    for driver in drivers:
        Driver.create(id=driver[ID],
                      name=driver[NAME],
                      surname=driver[SURNAME],
                      team_id=driver[TEAM_ID])


def add_data_to_result_table(results: dict[str: dict[str: str]]):
    """Adds data to Result table

        Args:
            results: data to fill in the table.
        """
    for driver_id, result in results.items():
        Result.create(start_time=result[START_TIME],
                      end_time=result[END_TIME],
                      lap_time=result[LAP_TIME],
                      driver_id=driver_id)


def fill_database_with_data():
    """Data-to-Database control function.

    This function calls other functions responsible for getting
    data from log files and adding them to the database.
    """
    # Get data from abbreviation file.
    teams, drivers = data_from_abbreviation(ABBREVIATIONS)
    # Add data to the tables
    add_data_to_team_table(teams)
    add_data_to_driver_table(drivers)

    # Get data from log files.
    results = data_from_logs(start_log=START_LOG, end_log=END_LOG)
    # Add data to the table.
    add_data_to_result_table(results)
