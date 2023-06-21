"""Module for constants"""
from symbol import test

# Constants for XML Response
# Root element in xml.
RESPONSE_TAG = "response"
# Driver element in xml.
DRIVER_TAG = "driver"
# Error element in xml.
ERROR_TAG = "error"
# Encoding for xml response.
ENCODING = "utf-8"
# Mimetype
APPLICATION_XML = "application/xml"

# Parameters in a request.
# Order parameter.
ORDER_PARAMETER = "order"
# Values of order parameter.
DESC_ORDER = "desc"
# Format parameter.
FORMAT_PARAMETER = "format"
# Value of format parameter.
XML_FORMAT = "xml"

# Path to API documentation.
REPORT_DOC = "./static/docs/report.yml"
DRIVERS_DOC = "./static/docs/drivers.yml"
SINGLE_DRIVER_DOC = "./static/docs/single_driver.yml"

# Path to log files.
ABBREVIATIONS = "data/abbreviations.txt"
START_LOG = "data/start.log"
END_LOG = "data/end.log"

# Column name in models.
START_TIME = "start_time"
END_TIME = "end_time"
LAP_TIME = "lap_time"
TEAM_ID = "team_id"
ID = "id"
NAME = "name"
SURNAME = "surname"

# Alias and additional columns.
PLACE = "place"
TEAM_ALIAS = "team"

# Reference in models
TEAM = "team"
DRIVER = "driver"
RESULT = "result"

# Datetime format string
DATETIME_STRING = "%Y-%m-%d_%H:%M:%S.%f"

# Error messages
DRIVER_NOT_FOUND = "A driver with the '%s' ID  was not found."
INTERNAL_ERROR = "There is an error in the application. Please contact the administrator."

# Logging
LOGGING_FORMAT = f"%(asctime)s %(levelname)s %(name)s : %(message)s"
LOGGING_FILE = {"development": "debug.log", "testing": "testing.log"}

# Configuration
TESTING = "testing"
DEVELOPMENT = "development"
DEFAULT = "default"
