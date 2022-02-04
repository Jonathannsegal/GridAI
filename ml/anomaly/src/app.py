"""Imports"""
import os


import io
from posixpath import dirname
import tensorflow as tf
import numpy as np

from neo4j import GraphDatabase

from flask import Flask, request, jsonify


dir_name = os.path.dirname(__file__)

# ML models saved in dedicated folders
single_phase_anomaly = tf.keras.models.load_model(os.path.join(dir_name, 'SPAnomaly/'))
single_phase_CT_anomaly = tf.keras.models.load_model(os.path.join(dir_name, 'SinglePhaseCTAnomaly/'))
three_phase_anomaly = tf.keras.models.load_model(os.path.join(dir_name, 'ThreePhaseAnomaly/'))

neo4j_driver=GraphDatabase.driver(uri="neo4j://neo4j:7687",auth=("neo4j","test"))
neo4j_session_update=neo4j_driver.session()
neo4j_session_query=neo4j_driver.session()

app = Flask(__name__)


# Return anomaly classification of only Single Phase transformers. Returns string ('failure','normal','spike') and confidence percentage.
@app.route("/singlePhaseAnom",methods=["GET","POST"])
def return_singlePhaseAnom():
    q1="match (n:`Single Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    output=neo4j_session_query.run(q1).data()
    nodes = []
    temp_node = []
    for i in output:
        temp_node.append(i['n.`Primary voltage rating (kV)`'])
        temp_node.append(i['n.`Secondary voltage rating (kV)`'])
        temp_node.append(i['n.`kVA rating (kVA)`'])
        temp_node.append(i['n.` %R`'])
        temp_node.append(i['n.` %X`'])
        temp_node.append(i['n.Year'])
        temp_node.append(i['n.Month'])
        temp_node.append(i['n.Day'])
        temp_node.append(i['n.Hour'])
        temp_node.append(i['n.CurrVal'])
        temp_node.append(i['n.`PrevNode Val`'])
        temp_node.append(i['n.PrevVal'])
        nodes.append(temp_node)
        temp_node = []

    # Runs model prediction function
    predictions = single_phase_anomaly.predict(nodes).tolist()
    busPreds = []
    j = 0
    anomType = ''
    for i in output:
        max_val = max(predictions[j])
        anomIndex = predictions[j].index(max_val)
        if anomIndex == 0:
            anomType = 'normal'
        elif anomIndex == 1:
            anomType = 'failure'
        else:
            anomType = 'spike'
        busPreds.append(i['n.BusID'] + ': ' + anomType  + ': ' + str(max_val))
        j+=1
    return {'predictions': busPreds}

# Return anomaly classification of only Single Phase Center Tapped transformers. Returns string ('failure','normal','spike') and confidence percentage.
@app.route("/singlePhaseCTAnom",methods=["GET","POST"])
def return_singlePhaseCTAnom():
    q1="match (n:`Single Phase CT`) return n.BusID, n.`kVA rating of Winding 1 (kVA)`,  n.` %R1`, n.` %R2`, n.` %R3`, n.` %X12`, n.` %X13`, n.` %X23`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    output=neo4j_session_query.run(q1).data()
    nodes = []
    temp_node = []
    for i in output:
        temp_node.append(i['n.`kVA rating of Winding 1 (kVA)`'])
        temp_node.append(i['n.` %R1`'])
        temp_node.append(i['n.` %R2`'])
        temp_node.append(i['n.` %R3`'])
        temp_node.append(i['n.` %X12`'])
        temp_node.append(i['n.` %X13`'])
        temp_node.append(i['n.` %X23`'])
        temp_node.append(i['n.Year'])
        temp_node.append(i['n.Month'])
        temp_node.append(i['n.Day'])
        temp_node.append(i['n.Hour'])
        temp_node.append(i['n.CurrVal'])
        temp_node.append(i['n.`PrevNode Val`'])
        temp_node.append(i['n.PrevVal'])
        nodes.append(temp_node)
        temp_node = []

    # Runs model prediction function
    predictions = single_phase_CT_anomaly.predict(nodes).tolist()
    busPreds = []
    j = 0
    anomType = ''
    for i in output:
        max_val = max(predictions[j])
        anomIndex = predictions[j].index(max_val)
        if anomIndex == 0:
            anomType = 'normal'
        elif anomIndex == 1:
            anomType = 'failure'
        else:
            anomType = 'spike'
        busPreds.append(i['n.BusID'] + ': ' + anomType  + ': ' + str(max_val))
        j+=1
    return {'predictions': busPreds}

# Return anomaly classification of only Three Phase transformers. Returns string ('failure','normal','spike')  and confidence percentage.
@app.route("/threePhaseAnom",methods=["GET","POST"])
def return_threePhaseAnom():
    q1="match (n:`Three Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    output=neo4j_session_query.run(q1).data()
    nodes = []
    temp_node = []
    for i in output:
        temp_node.append(i['n.`Primary voltage rating (kV)`'])
        temp_node.append(i['n.`Secondary voltage rating (kV)`'])
        temp_node.append(i['n.`kVA rating (kVA)`'])
        temp_node.append(i['n.` %R`'])
        temp_node.append(i['n.` %X`'])
        temp_node.append(i['n.Year'])
        temp_node.append(i['n.Month'])
        temp_node.append(i['n.Day'])
        temp_node.append(i['n.Hour'])
        temp_node.append(i['n.CurrVal'])
        temp_node.append(i['n.`PrevNode Val`'])
        temp_node.append(i['n.PrevVal'])
        nodes.append(temp_node)
        temp_node = []

    # Runs model prediction function
    predictions = three_phase_anomaly.predict(nodes).tolist()
    busPreds = []
    j = 0
    anomType = ''
    for i in output:
        max_val = max(predictions[j])
        anomIndex = predictions[j].index(max_val)
        if anomIndex == 0:
            anomType = 'normal'
        elif anomIndex == 1:
            anomType = 'failure'
        else:
            anomType = 'spike'
        busPreds.append(i['n.BusID'] + ': ' + anomType  + ': ' + str(max_val))
        j+=1
    return {'predictions': busPreds}

# Return anomaly classification of all transformer types. Returns string ('failure','normal','spike') and confidence percentage
@app.route("/allAnom",methods=["GET","POST"])
def return_allAnom():
    q1="match (n:`Single Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    q2="match (n:`Three Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    q3="match (n:`Single Phase CT`) return n.BusID, n.`kVA rating of Winding 1 (kVA)`,  n.` %R1`, n.` %R2`, n.` %R3`, n.` %X12`, n.` %X13`, n.` %X23`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    #Single Phase Anomalies
    output=neo4j_session_query.run(q1).data()
    nodes = []
    temp_node = []
    for i in output:
        temp_node.append(i['n.`Primary voltage rating (kV)`'])
        temp_node.append(i['n.`Secondary voltage rating (kV)`'])
        temp_node.append(i['n.`kVA rating (kVA)`'])
        temp_node.append(i['n.` %R`'])
        temp_node.append(i['n.` %X`'])
        temp_node.append(i['n.Year'])
        temp_node.append(i['n.Month'])
        temp_node.append(i['n.Day'])
        temp_node.append(i['n.Hour'])
        temp_node.append(i['n.CurrVal'])
        temp_node.append(i['n.`PrevNode Val`'])
        temp_node.append(i['n.PrevVal'])
        nodes.append(temp_node)
        temp_node = []
    predictions = single_phase_anomaly.predict(nodes).tolist()
    busPreds = []
    j = 0
    anomType = ''
    for i in output:
        max_val = max(predictions[j])
        anomIndex = predictions[j].index(max_val)
        if anomIndex == 0:
            anomType = 'normal'
        elif anomIndex == 1:
            anomType = 'failure'
        else:
            anomType = 'spike'
        busPreds.append(i['n.BusID'] + ': ' + anomType  + ': ' + str(max_val))
        j+=1
    #Three Phase Anomalies
    output=neo4j_session_query.run(q2).data()
    nodes = []
    temp_node = []
    for i in output:
        temp_node.append(i['n.`Primary voltage rating (kV)`'])
        temp_node.append(i['n.`Secondary voltage rating (kV)`'])
        temp_node.append(i['n.`kVA rating (kVA)`'])
        temp_node.append(i['n.` %R`'])
        temp_node.append(i['n.` %X`'])
        temp_node.append(i['n.Year'])
        temp_node.append(i['n.Month'])
        temp_node.append(i['n.Day'])
        temp_node.append(i['n.Hour'])
        temp_node.append(i['n.CurrVal'])
        temp_node.append(i['n.`PrevNode Val`'])
        temp_node.append(i['n.PrevVal'])
        nodes.append(temp_node)
        temp_node = []
    predictions = three_phase_anomaly.predict(nodes).tolist()
    j = 0
    anomType = ''
    for i in output:
        max_val = max(predictions[j])
        anomIndex = predictions[j].index(max_val)
        if anomIndex == 0:
            anomType = 'normal'
        elif anomIndex == 1:
            anomType = 'failure'
        else:
            anomType = 'spike'
        busPreds.append(i['n.BusID'] + ': ' + anomType  + ': ' + str(max_val))
        j+=1

    #Single Phase CT Anomalies
    output=neo4j_session_query.run(q3).data()
    nodes = []
    temp_node = []
    for i in output:
        temp_node.append(i['n.`kVA rating of Winding 1 (kVA)`'])
        temp_node.append(i['n.` %R1`'])
        temp_node.append(i['n.` %R2`'])
        temp_node.append(i['n.` %R3`'])
        temp_node.append(i['n.` %X12`'])
        temp_node.append(i['n.` %X13`'])
        temp_node.append(i['n.` %X23`'])
        temp_node.append(i['n.Year'])
        temp_node.append(i['n.Month'])
        temp_node.append(i['n.Day'])
        temp_node.append(i['n.Hour'])
        temp_node.append(i['n.CurrVal'])
        temp_node.append(i['n.`PrevNode Val`'])
        temp_node.append(i['n.PrevVal'])
        nodes.append(temp_node)
        temp_node = []
    predictions = single_phase_CT_anomaly.predict(nodes).tolist()
    j = 0
    anomType = ''
    for i in output:
        max_val = max(predictions[j])
        anomIndex = predictions[j].index(max_val)
        if anomIndex == 0:
            anomType = 'normal'
        elif anomIndex == 1:
            anomType = 'failure'
        else:
            anomType = 'spike'
        busPreds.append(i['n.BusID'] + ': ' + anomType + ': ' + str(max_val))
        j+=1
    return {'predictions': busPreds}


@app.route("/", methods=["GET", "POST"])
def index():
    """Hello World Endpoint"""
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            # image_bytes = file.read()
            # pillow_img = Image.open(io.BytesIO(image_bytes)).convert('L')
            # tensor = transform_image(pillow_img)
            # prediction = predict(tensor)
            # data = {"prediction": int(prediction)}
            model = tf.keras.Sequential()
            data = {"NEVER GONNA GIVE YOU UP. NEVER GONNA LET YOU DOWN. NEVER GONNA RUN AROUND AND DESERT YOU."}
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
