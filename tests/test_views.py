"""Tests for API endpoints"""
import pytest
from flask.testing import FlaskClient
import xml.etree.ElementTree as ET


class TestReport:
    """
    Tests for [GET] "/api/v1/report/"
    """

    def test_response_status_code(self, client: FlaskClient):
        """Test status code.

        Args:
            client: Flask test client.
        """
        response = client.get("/api/v1/report/")
        assert response.status_code == 200

    @pytest.mark.parametrize("url, content_type", [("/api/v1/report/?format=json", "application/json"),
                                                   ("/api/v1/report/?format=xml", "application/xml")])
    def test_response_header(self, client: FlaskClient, url, content_type):
        """Test content type in the header.

        Args:
            client: Flask test client.
            url: request path with parameters.
            content_type: content type in response header.
        """
        response = client.get(url)
        assert content_type in response.headers["Content-Type"]

    @pytest.mark.parametrize("url, result", [("/api/v1/report/", "Sebastian"),
                                             ("/api/v1/report/?order=asc", "Sebastian"),
                                             ("/api/v1/report/?order=desc", "Lewis"),
                                             ("/api/v1/report/?order=desc&format=json", "Lewis")])
    def test_response_content_in_json(self, client: FlaskClient, url, result):
        """Test content in json format.

        Args:
            client: Flask test client.
            url: request path with parameters.
            result: name of the first driver in the json list.
        """
        response = client.get(url)
        drivers = response.get_json()
        assert drivers[0]["name"] == result

    @pytest.mark.parametrize("url, result", [("/api/v1/report/?format=xml", "Sebastian"),
                                             ("/api/v1/report/?order=asc&format=xml", "Sebastian"),
                                             ("/api/v1/report/?order=desc&format=xml", "Lewis")])
    def test_response_content_in_xml(self, client: FlaskClient, url, result):
        """Test content in xml format.

        Args:
            client: Flask test client.
            url: request path with parameters.
            result: name of the first driver in the xml tree.
        """
        response = client.get(url)
        response_xml = ET.fromstring(response.data)
        assert response_xml[0][0].text == result

    def test_response_length(self, client: FlaskClient):
        """Test index page content.

        Args:
            client: Flask test client.
        """
        response = client.get("/api/v1/report/")
        drivers = response.get_json()
        assert len(drivers) == 19


class TestDrivers:
    """
    Tests for [GET] "/api/v1/report/drivers/"
    """

    def test_response_status_code(self, client: FlaskClient):
        """Test status code.

        Args:
            client: Flask test client.
        """
        response = client.get("/api/v1/report/drivers/")
        assert response.status_code == 200

    @pytest.mark.parametrize("url, content_type", [("/api/v1/report/drivers/?format=json", "application/json"),
                                                   ("/api/v1/report/drivers/?format=xml", "application/xml")])
    def test_response_header(self, client: FlaskClient, url, content_type):
        """Test content type in the header.

        Args:
            client: Flask test client.
            url: request path with parameters.
            content_type: content type in response header.
        """
        response = client.get(url)
        assert content_type in response.headers["Content-Type"]

    @pytest.mark.parametrize("url, result", [("/api/v1/report/drivers/", "Brendon"),
                                             ("/api/v1/report/drivers/?order=asc", "Brendon"),
                                             ("/api/v1/report/drivers/?order=desc", "Valtteri"),
                                             ("/api/v1/report/drivers/?order=desc&format=json", "Valtteri")])
    def test_response_content_in_json(self, client: FlaskClient, url, result):
        """Test content in json format.

        Args:
            client: Flask test client.
            url: request path with parameters.
            result: name of the first driver in the json list.
        """
        response = client.get(url)
        drivers = response.get_json()
        assert drivers[0]["name"] == result

    @pytest.mark.parametrize("url, result", [("/api/v1/report/drivers/?format=xml", "Brendon"),
                                             ("/api/v1/report/drivers/?order=asc&format=xml", "Brendon"),
                                             ("/api/v1/report/drivers/?order=desc&format=xml", "Valtteri")])
    def test_response_content_in_xml(self, client: FlaskClient, url, result):
        """Test content in xml format.

        Args:
            client: Flask test client.
            url: request path with parameters.
            result: name of the first driver in the xml tree.
        """
        response = client.get(url)
        response_xml = ET.fromstring(response.data)
        assert response_xml[0][1].text == result

    def test_response_length(self, client: FlaskClient):
        """Test index page content.

        Args:
            client: Flask test client.
        """
        response = client.get("/api/v1/report/drivers/")
        drivers = response.get_json()
        assert len(drivers) == 19


class TestSingleDriver:
    """
    Tests for [GET] "/api/v1/report/drivers/{driver_id}"
    """

    def test_response_status_code(self, client: FlaskClient):
        """Test status code.

        Args:
            client: Flask test client.
        """
        response = client.get("/api/v1/report/drivers/BHS")
        assert response.status_code == 200

    @pytest.mark.parametrize("url, content_type", [("/api/v1/report/drivers/BHS?format=json", "application/json"),
                                                   ("/api/v1/report/drivers/BHS?format=xml", "application/xml")])
    def test_response_header(self, client: FlaskClient, url, content_type):
        """Test content type in the header.

        Args:
            client: Flask test client.
            url: request path with parameters.
            content_type: content type in response header.
        """
        response = client.get(url)
        assert content_type in response.headers["Content-Type"]

    @pytest.mark.parametrize("url, result", [("/api/v1/report/drivers/BHS", "Brendon"),
                                             ("/api/v1/report/drivers/BHS?format=json", "Brendon")])
    def test_response_content_in_json(self, client: FlaskClient, url, result):
        """Test content in json format.

        Args:
            client: Flask test client.
            url: request path with parameters.
            result: name of the first driver in the json list.
        """
        response = client.get(url)
        driver = response.get_json()
        assert driver["name"] == result

    def test_response_content_in_xml(self, client: FlaskClient):
        """Test content in xml format.

        Args:
            client: Flask test client.
        """
        response = client.get("/api/v1/report/drivers/BHS?format=xml")
        response_xml = ET.fromstring(response.data)
        assert response_xml[1].text == "Brendon"

    def test_response_length(self, client: FlaskClient):
        """Test index page content.

        Args:
            client: Flask test client.
        """
        response = client.get("/api/v1/report/drivers/BHS")
        driver = response.get_json()
        # Return dict with 5 key-value pairs
        assert len(driver) == 5


class TestErrorResponse:
    """
    Tests for errors.
    """

    @pytest.mark.parametrize("url, status_code", [("/api/v1/report/drivers/test", 200),
                                                  ("/api/v1/report/test/", 200)])
    def test_response_status_code(self, client: FlaskClient, url, status_code):
        """Test status code for page not found.

        Args:
            client: Flask test client.
        """
        response = client.get(url)
        assert response.status_code == status_code

    @pytest.mark.parametrize("url, content_type", [("/api/v1/report/drivers/test?format=json", "application/json"),
                                                   ("/api/v1/report/drivers/test?format=xml", "application/xml")])
    def test_response_header(self, client: FlaskClient, url, content_type):
        """Test content type in the header.

        Args:
            client: Flask test client.
            url: request path with parameters.
            content_type: content type in response header.
        """
        response = client.get(url)
        assert content_type in response.headers["Content-Type"]

    def test_response_content_in_json(self, client: FlaskClient):
        """Test content in json format.

        Args:
            client: Flask test client.
        """
        response = client.get("/api/v1/report/drivers/test?format=json")
        error = response.get_json()
        assert "404 Not Found" in error["error"]

    def test_response_content_in_xml(self, client: FlaskClient):
        """Test content in xml format.

        Args:
            client: Flask test client.
        """
        response = client.get("/api/v1/report/drivers/test?format=xml")
        response_xml = ET.fromstring(response.data)
        assert "404 Not Found" in response_xml.text
