"""Module for Models"""
from typing import Optional

from peewee import AutoField, CharField, ForeignKeyField, DateTimeField

from app.extensions import db_wrapper, cache
from app.constants import DESC_ORDER, PLACE, TEAM_ALIAS, TEAM, RESULT, DRIVER


class Team(db_wrapper.Model):
    """Represents Team table in database"""
    id = AutoField(primary_key=True)
    name = CharField(null=False)


class Driver(db_wrapper.Model):
    """Represents Driver table in database"""
    id = CharField(primary_key=True)
    name = CharField(null=False)
    surname = CharField(null=False)
    team_id = ForeignKeyField(Team, backref=DRIVER)

    @classmethod
    @cache.cached(query_string=True)
    def get_drivers(cls, order: Optional[str]) -> list[dict]:
        """Gets drivers.

        Args:
            order: order in which drivers list should be return.

        Returns:
            list of drivers ordered by driver id in asc or desc order.

        Example:
            [{"id": "BHS", "name": "Brendon", "surname": "Hartley"}]
        """
        # Prepare query for selecting drivers.
        query = cls.select(cls.id,
                           cls.name,
                           cls.surname).order_by(cls.id).dicts()

        # Prepare list of drivers.
        drivers = [driver for driver in query]
        # Reverse list of drivers if order is desc.
        if order == DESC_ORDER:
            drivers.reverse()

        return drivers

    @classmethod
    @cache.cached(query_string=True)
    def get_single_driver(cls, driver_id: str) -> dict:
        """Gets drivers.

        Args:
            driver_id: driver's id.

        Returns:
            driver object.

        Exceptions:
            UserWarning: If driver with specific id doesn't exist.

        Example:
            {"id": "BHS",
             "name": "Brendon",
             "surname": "Hartley",
             "team": "FERRARI",
             "lap_time": "1:12:123}
        """
        # Prepare query for selecting information about driver.
        query = (cls
                 .select(cls.id,
                         cls.name,
                         cls.surname,
                         Team.name.alias(TEAM_ALIAS),
                         Result.lap_time)
                 .join(Team)
                 .where(cls.id == driver_id.upper())
                 .switch(cls)
                 .join(Result)
                 .order_by(Result.lap_time)).dicts()
        # Check driver with specific id exists.
        if not query.exists():
            raise UserWarning

        return query.get()


class Result(db_wrapper.Model):
    """Represents Result table in database"""
    id = AutoField(primary_key=True)
    lap_time = CharField(null=False)
    start_time = DateTimeField(null=False)
    end_time = DateTimeField(null=False)
    driver_id = ForeignKeyField(Driver, backref=RESULT)

    @classmethod
    @cache.cached(query_string=True)
    def get_report(cls, order: Optional[str]) -> list[dict]:
        """Gets drivers.

        Args:
            order: order in which results should be return.

        Returns:
            list of results ordered by place in asc or desc order.

        Example:
            [{"name": "Brendon",
              "surname": "Hartley",
              "team": "FERRARI",
              "lap_time": "1:12:123,
              "place": 1}]
        """
        # Prepare query for selecting results.
        query = (Driver
                 .select(Driver.name,
                         Driver.surname,
                         Team.name.alias(TEAM_ALIAS),
                         cls.lap_time)
                 .join_from(Driver, Team)  # Join driver with team.
                 .join_from(Driver, cls)  # Join driver with result.
                 .order_by(cls.lap_time)).dicts()

        results = []
        # Create report from query and adding drivers place.
        for place, driver in enumerate(query, start=1):
            driver[PLACE] = place
            results.append(driver)

        # Reverse list of results if order is desc.
        if order == DESC_ORDER:
            results.reverse()

        return results


def get_models():
    return {DRIVER: Driver, TEAM: Team, RESULT: Result}
