"""Imports"""
from flask import current_app
from neo4j.src.app import app
import pytest

@pytest.fixture
def client(mocker):
    with app.test_client() as client:
        with app.app_context():
            assert current_app.config["ENV"] == "production"
            mocker.patch("neo4j.src.app.graph.run", return_value=[{'n.NodeId':'1', 'n.longitude':'1', 'n.latitude':'1'}, {'n.NodeId':'2', 'n.longitude':'2', 'n.latitude':'2'}])
            yield client


def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, GridAI Neo4j' in response.data


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


def test_get_all_coordinates(client):
    response = client.get('/getCoords')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Node: 1 1 1\nNode: 2 2 2\n'


def test_upload_file(client):
    response = client.post('/uploadFile?url=1')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'success'
