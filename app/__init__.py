"""Application factory module"""

from flask import Flask
from flask_cors import CORS

from app.db.scripts.db_scripts import create_tables
from app.utils import error_response
from config import config, CACHE_CONFIG
from app.extensions import db_wrapper, cache, swagger
from app.api import api_bp


def create_app(config_name) -> Flask:
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(config_name)

    # Register blueprint for api.
    app.register_blueprint(api_bp)

    db_wrapper.init_app(app)
    swagger.init_app(app)
    CORS(app)  # For handling Cross Origin Resource Sharing in Swagger UI
    cache.init_app(app, config=CACHE_CONFIG)

    register_error_handlers(app)

    # Create db and tables.
    create_tables()

    return app


def register_error_handlers(app: Flask):
    """Helper function for error handler registration

    Args:
        app: Flask instance
    """

    @app.errorhandler(404)
    def resource_not_found(e):
        """Page not found handler.

        Function will be called when an 404 error occurs in API endpoint or APP.

        Returns:
            Response in xml or json format.
        """
        return error_response(e)

    @app.errorhandler(500)
    def internal_server_error(e):
        """Internal server error handler.

        Function will be called when an 500 error occurs in API endpoint or APP.

        Returns:
            Response in xml or json format.
        """
        return error_response(e)
