import time
import mltest as ml
import flask
import neo4j
from neo4j import GraphDatabase, basic_auth
from flask import Flask,request,jsonify,render_template,redirect


driver=GraphDatabase.driver(uri="bolt://localhost:7687",auth=("neo4j","test"))
session=driver.session()

app = flask.Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/stock/<id>')
def get_pred(id):
    ml.ml_test(id)
    return flask.send_file('plot.png', mimetype='image/png')

@app.route("/coordinates",methods=["GET","POST"])
def return_nodes():
    q2="match (n) return n.BusID as BusID, n.X as X, n.Y as Y"
    output=session.run(q2)
    return(jsonify(output.data()))

if __name__ == "__main__":
    app.run(host='0.0.0.0')

