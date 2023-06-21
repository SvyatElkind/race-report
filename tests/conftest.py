import pytest
from flask.testing import FlaskClient

from app import create_app
from app.constants import TESTING


@pytest.fixture(scope="session")
def client() -> FlaskClient:
    """Create test client

    Returns:
        Flask Client for test purpose.
    """
    app = create_app(TESTING)
    return app.test_client()

