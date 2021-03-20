import time
import flask
import neo4j
from neo4j import GraphDatabase, basic_auth
from flask import Flask,request,jsonify,render_template,redirect
from tensorflow import keras


driver=GraphDatabase.driver(uri="neo4j://neo4j:7687",auth=("neo4j","test"))
session=driver.session()
three_phase_model = keras.models.load_model('ThreePhaseModel/FuturePredictionsModelNoIndex/')
single_phase_model = keras.models.load_model('SinglePhaseModel/')
single_phase_CT_model = keras.models.load_model('SinglePhaseCTModel/')
single_phase_anomaly = keras.models.load_model('SPAnomaly/')
single_phase_CT_anomaly = keras.models.load_model('SPCTAnomaly/')
three_phase_anomaly = keras.models.load_model('ThreePhaseAnomaly/')

app = flask.Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route("/coordinates",methods=["GET","POST"])
def return_coords():
    q1="match (n) return n.BusID as BusID, n.X as X, n.Y as Y"
    output=session.run(q1)
    return(jsonify(output.data()))

@app.route("/allCurrentValues",methods=["GET","POST"])
def return_currValues():
    q1="match (n) return n.BusID as BusID, n.CurrVal as currentValue"
    output=session.run(q1)
    return(jsonify(output.data()))

@app.route("/threePhase",methods=["GET","POST"])
def return_threePhasePred():
    q1="match (n:`Three Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    output=session.run(q1).data()
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
    predictions = three_phase_model.predict(nodes).tolist()
    busPreds = []
    j = 0
    for i in output:
        busPreds.append(i['n.BusID'] + ': ' + str(predictions[j][0]))
        j+=1
    return {'predictions': busPreds}

@app.route("/singlePhase",methods=["GET","POST"])
def return_singlePhasePred():
    q1="match (n:`Single Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    output=session.run(q1).data()
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
    predictions = single_phase_model.predict(nodes).tolist()
    busPreds = []
    j = 0
    for i in output:
        busPreds.append(i['n.BusID'] + ': ' + str(predictions[j][0]))
        j+=1
    return {'predictions': busPreds}

@app.route("/singlePhaseCT",methods=["GET","POST"])
def return_singlePhaseCTPred():
    q1="match (n:`Single Phase CT`) return n.BusID, n.`Voltage rating of Winding 1 (kV)`,  n.` %R1`, n.` %R2`, n.` %R3`, n.` %X12`, n.` %X13`, n.` %X23`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    output=session.run(q1).data()
    nodes = []
    temp_node = []
    for i in output:
        temp_node.append(i['n.`Voltage rating of Winding 1 (kV)`'])
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
    predictions = single_phase_CT_model.predict(nodes).tolist()
    busPreds = []
    j = 0
    for i in output:
        busPreds.append(i['n.BusID'] + ': ' + str(predictions[j][0]))
        j+=1
    return {'predictions': busPreds}

@app.route("/singlePhaseAnom",methods=["GET","POST"])
def return_singlePhaseAnom():
    q1="match (n:`Single Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    output=session.run(q1).data()
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
        busPreds.append(i['n.BusID'] + ': ' + anomType)
        j+=1
    return {'predictions': busPreds}



@app.route("/singlePhaseCTAnom",methods=["GET","POST"])
def return_singlePhaseCTAnom():
    q1="match (n:`Single Phase CT`) return n.BusID, n.`Voltage rating of Winding 1 (kV)`,  n.` %R1`, n.` %R2`, n.` %R3`, n.` %X12`, n.` %X13`, n.` %X23`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    output=session.run(q1).data()
    nodes = []
    temp_node = []
    for i in output:
        temp_node.append(i['n.`Voltage rating of Winding 1 (kV)`'])
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
        busPreds.append(i['n.BusID'] + ': ' + anomType)
        j+=1
    return {'predictions': busPreds}

@app.route("/threePhaseAnom",methods=["GET","POST"])
def return_threePhaseAnom():
    q1="match (n:`Three Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    output=session.run(q1).data()
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
        busPreds.append(i['n.BusID'] + ': ' + anomType)
        j+=1
    return {'predictions': busPreds}

@app.route("/allPred",methods=["GET","POST"])
def return_allPred():
    q1="match (n:`Single Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    q2="match (n:`Three Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    q3="match (n:`Single Phase CT`) return n.BusID, n.`Voltage rating of Winding 1 (kV)`,  n.` %R1`, n.` %R2`, n.` %R3`, n.` %X12`, n.` %X13`, n.` %X23`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    #Single Phase Predictions
    output=session.run(q1).data()
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
    predictions = single_phase_model.predict(nodes).tolist()
    busPreds = []
    j = 0
    for i in output:
        busPreds.append(i['n.BusID'] + ': ' + str(predictions[j][0]))
        j+=1
    #Three Phase Prediction
    output=session.run(q2).data()
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
    predictions = single_phase_model.predict(nodes).tolist()
    j = 0
    for i in output:
        busPreds.append(i['n.BusID'] + ': ' + str(predictions[j][0]))
        j+=1
    #Single Phase CT Prediction
    output=session.run(q3).data()
    nodes = []
    temp_node = []
    for i in output:
        temp_node.append(i['n.`Voltage rating of Winding 1 (kV)`'])
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
    predictions = single_phase_CT_model.predict(nodes).tolist()
    j = 0
    for i in output:
        busPreds.append(i['n.BusID'] + ': ' + str(predictions[j][0]))
        j+=1
    return {'predictions': busPreds}

@app.route("/allAnom",methods=["GET","POST"])
def return_allAnom():
    q1="match (n:`Single Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    q2="match (n:`Three Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    q3="match (n:`Single Phase CT`) return n.BusID, n.`Voltage rating of Winding 1 (kV)`,  n.` %R1`, n.` %R2`, n.` %R3`, n.` %X12`, n.` %X13`, n.` %X23`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    #Single Phase Anomalies
    output=session.run(q1).data()
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
        busPreds.append(i['n.BusID'] + ': ' + anomType)
        j+=1
    #Three Phase Anomalies
    output=session.run(q2).data()
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
        busPreds.append(i['n.BusID'] + ': ' + anomType)
        j+=1

    #Single Phase CT Anomalies
    output=session.run(q3).data()
    nodes = []
    temp_node = []
    for i in output:
        temp_node.append(i['n.`Voltage rating of Winding 1 (kV)`'])
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
        busPreds.append(i['n.BusID'] + ': ' + anomType)
        j+=1
    return {'predictions': busPreds}


if __name__ == "__main__":
    app.run(host='0.0.0.0')

