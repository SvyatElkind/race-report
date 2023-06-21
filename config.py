"""Module contains configurations"""
import logging

from app.constants import LOGGING_FILE, LOGGING_FORMAT, DEVELOPMENT, TESTING, DEFAULT

# Cache configuration dictionary
CACHE_CONFIG = {"CACHE_TYPE": "SimpleCache",
                "CACHE_DEFAULT_TIMEOUT": 300}


class Config:
    """Base configuration class.

    Contains default configuration."""
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False

    @staticmethod
    def init_app(config_name: str):
        """Method allows additional application configuration.

        Args:
            config_name: name of configuration
                allowed values are development, testing, production.
        """

        logging.basicConfig(filename=LOGGING_FILE[config_name],
                            level=logging.DEBUG,
                            format=LOGGING_FORMAT)


class DevelopmentConfig(Config):
    """Configuration for development"""
    DEBUG = True
    DATABASE = {
        "name": "dev.db",
        "engine": "peewee.SqliteDatabase"
    }


class TestingConfig(Config):
    """Configuration for testing"""
    TESTING = True
    DATABASE = {
        "name": "test.db",
        "engine": "peewee.SqliteDatabase"
    }


config = {
    DEVELOPMENT: DevelopmentConfig,
    TESTING: TestingConfig,
    DEFAULT: DevelopmentConfig
}
