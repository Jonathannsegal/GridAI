"""Imports"""
from flask import current_app
from neo4j.src.app import app
import pytest

@pytest.fixture
def client(mocker):
    with app.test_client() as client:
        with app.app_context():
            assert current_app.config["ENV"] == "production"
            mocker.patch("neo4j.src.app.graph.run", return_value=[{'n.name':'1'}, {'n.name':'2'}])
            yield client


def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert b'pong' in response.data


def test_add_node(client):
    response = client.post('/addNode?name=1')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Created node 1 successfully'


def test_get_nodes(client):
    response = client.get('/getNodes')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Node: 1\nNode: 2\n'
