# type: ignore
"""Imports"""
import os
from py2neo import Graph
from flask import Flask, request
from decouple import config


app = Flask(__name__)
user = config('DATABASE_USERNAME', default='username')
password = config('DATABASE_PASSWORD', default='password')
url = config('DATABASE_URL', default='url')
graph = Graph(url, auth=(user, password))


@app.route("/")
def index():
    """Root Directory"""
    return "Hello, GridAI Neo4j"


@app.route("/ping")
def ping():
    """Ping the server"""
    return "pong"


@app.route('/addNode', methods=['POST'])
def add_node():
    """Create node"""
    name = request.args['name']
    query = ("CREATE (p1:Node { name: $node_name })")
    graph.run(query, node_name=name)
    return f"Created node {name} successfully"


@app.route('/getNodes', methods=['GET'])
def get_nodes():
    """Get all nodes"""
    query = ("MATCH (n:Node) RETURN n.NodeId")
    result = ""
    for record in graph.run(query):
        result += "Node: " + record["n.NodeId"] + "\n"
    return result


@app.route('/uploadFile', methods=['POST'])
def upload_file():
    """upload a csv file to import data"""
    csv_url = request.args['url']
    query = ("""LOAD CSV WITH HEADERS FROM $url_name AS row MERGE
    (n:Node {NodeId: row.busID, longitude: row.longitude, latitude: row.latitude})""")
    graph.run(query, url_name=csv_url)
    return "success"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
