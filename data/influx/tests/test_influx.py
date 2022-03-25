# pylint: disable=redefined-outer-name
# pylint: disable=no-self-argument
# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use
# pylint: disable=unused-argument
"""Imports"""
from flask import current_app
from influxdb_client.client.flux_table import FluxTable
from influx.src.app import app
import pytest

@pytest.fixture
def client(mocker):
    """Pytest client fixture"""
    with app.test_client() as client:
        with app.app_context():
            assert current_app.config["ENV"] == "production"

            class ClientMock():
                """Mock Function"""
                class QueryApi():
                    """Mock Function"""
                    def query(org, query):
                        """Mock query"""
                        return FluxTable()
                class WriteApiMock():
                    """Mock Function"""
                    def write(bucket, org, record):
                        """Mock query"""
                        return "hello"

            mocker.patch("influx.src.app.client", return_value=ClientMock)
            yield client


def test_root(client):
    """Test write to bucket"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, GridAI Influx' in response.data


def test_write_voltage_with_id(client):
    """Test write to bucket"""
    response = client.post('/writeVoltageById?bus=1&voltage=2')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Created bus 1, voltage 2 successfully'

# def test_upload_csv(client):
#     """Test write to bucket"""
#     response = client.post('/uploadCsv?url=http://test.com')
#     assert response.status_code == 200
#     assert response.data.decode('utf-8') == 'Uploaded data from http://test.com successfully'

def test_get_voltage_by_id(client):
    """test read from bucket"""
    response = client.get('/getVoltageById?busId=1')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '[]\n'

def test_get_all_voltage(client):
    """test read from bucket"""
    response = client.get('/getAllCurrentVoltage')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '[]\n'

def test_ping_influx(client):
    """test ping"""
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'pong'
    