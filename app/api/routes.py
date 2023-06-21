"""Module for API"""
from flask import request, Response, abort, current_app
from flask_restful import Resource
from flasgger import swag_from

from app.utils import create_response
from app.api import api
from app.constants import RESPONSE_TAG, DRIVER_TAG, ORDER_PARAMETER, FORMAT_PARAMETER, \
    REPORT_DOC, DRIVERS_DOC, SINGLE_DRIVER_DOC, DRIVER_NOT_FOUND
from app.db.models import Driver, Result


class Report(Resource):
    """Class for actions with report"""
    @swag_from(REPORT_DOC)
    def get(self) -> Response:
        """Returns race report in json or xml format.

        Returns:
            Response object in json or xml format.
        """
        # Get report from database
        report = Result.get_report(request.args.get(ORDER_PARAMETER))
        # return json or xml response
        return create_response(response_format=request.args.get(FORMAT_PARAMETER),
                               data=report,
                               root=RESPONSE_TAG)


class Drivers(Resource):
    """Class for actions with drivers"""
    @swag_from(DRIVERS_DOC)
    def get(self) -> Response:
        """Returns list of drivers in json or xml format

        Returns:
            Response object in json or xml.
        """
        # Get drivers from database
        drivers = Driver.get_drivers(order=request.args.get(ORDER_PARAMETER))
        # return json or xml response
        return create_response(response_format=request.args.get(FORMAT_PARAMETER),
                               data=drivers,
                               root="response")


class SingleDriver(Resource):
    """Class for actions with specific driver"""
    @swag_from(SINGLE_DRIVER_DOC)
    def get(self, driver_id: str) -> Response:
        """Return driver object in json or xml format.

        Args:
            driver_id: driver abbreviation.

        Returns:
            If converts to xml format, return Response object with xml
            else returns driver object.
        """
        try:
            # Get driver from database
            driver = Driver.get_single_driver(driver_id)
        except UserWarning:
            # Driver not found.
            current_app.logger.info(DRIVER_NOT_FOUND, driver_id)
            abort(404, description=f"A driver with the '{driver_id}' ID  was not found.")
        # return json or xml response
        return create_response(response_format=request.args.get(FORMAT_PARAMETER),
                               data=driver,
                               root=DRIVER_TAG)


# Add a resource to the api.
api.add_resource(Report, "/report/")
api.add_resource(Drivers, "/report/drivers/")
api.add_resource(SingleDriver, "/report/drivers/<string:driver_id>")
