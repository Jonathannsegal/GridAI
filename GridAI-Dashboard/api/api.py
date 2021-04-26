import time
from datetime import datetime, timezone, timedelta
import pandas as pd
import flask
import neo4j
import sqlalchemy as db
from apscheduler.schedulers.background import BackgroundScheduler
from neo4j import GraphDatabase, basic_auth
from flask import Flask,request,jsonify,render_template,redirect
from tensorflow import keras

app = flask.Flask(__name__)

mysql_engine = db.create_engine('mysql+mysqldb://user:user@mysql:3306/db')
mysql_conn = mysql_engine.connect()
neo4j_driver=GraphDatabase.driver(uri="neo4j://neo4j:7687",auth=("neo4j","test"))
neo4j_session=neo4j_driver.session()
three_phase_model = keras.models.load_model('ThreePhaseModel/FuturePredictionsModelNoIndex/')
single_phase_model = keras.models.load_model('SinglePhaseModel/')
single_phase_CT_model = keras.models.load_model('SinglePhaseCTModel/')
single_phase_anomaly = keras.models.load_model('SPAnomaly/')
single_phase_CT_anomaly = keras.models.load_model('SPCTAnomaly/')
three_phase_anomaly = keras.models.load_model('ThreePhaseAnomaly/')

# meter_data = pd.read_csv('meter.csv')
# meter_data.set_index('Date', inplace=True)
# types = {'Date': db.types.DateTime()}
# for col in meter_data.columns:
#     types[col] = db.types.Float()
# meter_data.to_sql('smart_meter', con=mysql_conn, if_exists='replace', dtype=types)


def update_data():
    b = datetime.now(timezone(timedelta(hours=-5)))
    print(b, flush=True)
    sql_query=f"select * from smart_meter where date between '2017-{b:%m}-{b:%d} {b:%H}:00:00' and '2017-{b:%m}-{b:%d} {b:%H}:59:59'"
    result = mysql_conn.execute(sql_query)

    for row in result:
        for col in row._fields:
            if (str(col) != 'Date'):
                cypher_query = f"match (n {{BusID:\"T_{str(col)[-4:]}\"}}) return n.`Previous Bus` as PrevBus"
                test = neo4j_session.run(cypher_query)
                output = test.data()
                if output and output[0]['PrevBus'] != 0:
                    cypher_query = f"match (n {{BusID:\"T_{str(col)[-4:]}\"}}) \
                                set n.PrevVal = n.CurrVal, n.CurrVal = {row[col]}, n.`PrevNode Val` = {row['Bus ' + str(output[0]['PrevBus'])]}, \
                                n.Month = {b.month}, n.Day = {b.day}, n.Hour = {b.hour}"
                    neo4j_session.run(cypher_query)

    return

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/history/<bus>')
def get_table(bus):
    b = datetime.now(timezone(timedelta(hours=-5)))
    query=f"select date,`Bus {bus}` from smart_meter where date between date_sub('2017-{b:%m}-{b:%d} {b:%H}:00:00', interval 1 day) and '2017-{b:%m}-{b:%d} {b:%H}:59:59'"
    result = mysql_conn.execute(query)
    output = []
    for row in result:
        output.append(str(row[0]) + ': ' + str(row[1]))   
    return {'result': output}

@app.route("/coordinates",methods=["GET","POST"])
def return_coords():
    q1="match (n) return n.BusID as BusID, n.X as X, n.Y as Y"
    output=neo4j_session.run(q1)
    return(jsonify(output.data()))

@app.route("/allCurrentValues",methods=["GET","POST"])
def return_currValues():
    q1="match (n) return n.BusID as BusID, n.CurrVal as currentValue"
    output=neo4j_session.run(q1)
    return(jsonify(output.data()))

@app.route("/allCurrentValues/<bus>",methods=["GET","POST"])
def return_nodeValue(bus):
    q1="match (n {BusID:'"+bus+"'}) return n.BusID as BusID, n.CurrVal as currentValue"
    print("....."+str(q1))
    output=neo4j_session.run(q1)
    return(jsonify(output.data()))

@app.route("/threePhase",methods=["GET","POST"])
def return_threePhasePred():
    q1="match (n:`Three Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    output=neo4j_session.run(q1).data()
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
    output=neo4j_session.run(q1).data()
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
    output=neo4j_session.run(q1).data()
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
    output=neo4j_session.run(q1).data()
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
    output=neo4j_session.run(q1).data()
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
    output=neo4j_session.run(q1).data()
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
    output=neo4j_session.run(q1).data()
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
    output=neo4j_session.run(q2).data()
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
    output=neo4j_session.run(q3).data()
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
    output=neo4j_session.run(q1).data()
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
    output=neo4j_session.run(q2).data()
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
    output=neo4j_session.run(q3).data()
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


start_time = datetime.now().replace(minute=0, second=0, microsecond=0)
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_data, next_run_time=datetime.now(), trigger="cron", minute=0)
scheduler.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

