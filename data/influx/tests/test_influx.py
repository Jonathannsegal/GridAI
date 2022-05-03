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

def test_comparison(client):
    """Test comparison"""
    response = client.get('/comparison?comparison_type=1&comp_val=0')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '[]\n'


def test_write_voltage_with_id(client):
    """Test write to bucket"""
    response = client.post('/writeVoltageById?bus=1&voltage=2')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Created bus 1, voltage 2 successfully'

def delete_all(client):
    """Test delete all"""
    response = client.delete('/deleteAll')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'All Data Deleted'

def test_get_voltage_by_id(client):
    """test read from bucket"""
    response = client.get('/getVoltageById?busId=1')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '[]\n'

def test_get_extreme(client):
    """test extreme"""
    response = client.get('/getExtreme?extrema_type=MAX&count=10')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '[]\n'

def test_generic(client):
    """test generic"""
    req = '/generic?start=2022-04-21T22:00:00Z&'
    req += 'stop=2022-04-25T12:00:00Z&highest_value=3&extrema_type=MAX&count=2'
    response = client.get(req)
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '[["Time","Bus","Active Power"]]\n'

def test_get_all_voltage(client):
    """test read from bucket"""
    response = client.get('/getAllCurrentVoltageFrontend')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '[]\n'

def test_get_all_power(client):
    """test read from bucket"""
    response = client.get('/getAllCurrentGeneratedPower')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '[]\n'

def test_ping_influx(client):
    """test ping"""
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'pong'
    