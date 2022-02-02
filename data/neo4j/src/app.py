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
    """default"""
    return "Hello, GridAI Neo4j"


@app.route("/ping")
def ping():
    """Ping"""
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
    query = ("MATCH (n:Node) RETURN n.name LIMIT 25")
    result = ""
    for record in graph.run(query):
        result += "Node: " + record["n.name"] + "\n"
    return result


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
