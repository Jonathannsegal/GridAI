# type: ignore
# pylint: disable=line-too-long
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


@app.route('/getCoords', methods=['GET'])
def get_all_coordinates():
    """Get all node coordinates"""
    query = ("MATCH (n:Node) RETURN n.NodeId,n.latitude,n.longitude")
    result = ""
    for record in graph.run(query):
        result += "Node: " + record["n.NodeId"] + " " + record["n.longitude"] + " " + record["n.latitude"] + "\n"
    return result


@app.route('/uploadFile', methods=['POST'])
def upload_file():
    """upload a csv file to import data"""
    csv_url = request.args['url']
    query = ("""LOAD CSV WITH HEADERS FROM $url_name AS row MERGE
    (n:Node {NodeId: row.busID, longitude: row.longitude, latitude: row.latitude})""")
    graph.run(query, url_name=csv_url)
    return "success"


@app.route('/uploadFileConnections', methods=['POST'])
def upload_connections():
    """upload a file and get connections from it"""
    file = request.files['file']
    lines = file.readlines()
    query = ("""MATCH (a:Node), (b:Node) WHERE a.NodeId = $node1id AND b.NodeId = $node2id
     CREATE (a)-[r:connected {name: a.NodeId + '<->' + b.NodeId}]->(b)""")
    for line in lines:
        my_str = line.decode('utf-8').split()
        if (my_str[0] == "New" or my_str[0] == "Edit"):
            bus1 = my_str[2].split("=")
            bus2 = my_str[3].split("=")
            bus1id = bus1[1].split(".")[0]
            bus2id = bus2[1].split(".")[0]
            graph.run(query, node1id=bus1id, node2id=bus2id)
    return "success"


@app.route('/getConnections', methods=['GET'])
def get_connections():
    """get connections between nodes"""
    query = ("MATCH p=(n:Node)-->(m:Node) RETURN n.latitude,n.longitude,m.latitude,m.longitude")
    result = ""
    for record in graph.run(query):
        result += record["n.longitude"] + "," + record["n.latitude"] + "_"
        result += record["m.longitude"] + "," + record["m.latitude"] + "\n"
    return result


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
