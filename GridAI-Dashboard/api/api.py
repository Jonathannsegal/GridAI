# Authors: Karthik Prakash
# Created: 1/25/2021
# Updated: 5/3/2021
# Copyrighted 2021 sdmay21-23@iastate.edu
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

# Database driver and connection instantiations
mysql_engine = db.create_engine('mysql+mysqldb://user:user@mysql:3306/db')
mysql_conn = mysql_engine.connect()
neo4j_driver=GraphDatabase.driver(uri="neo4j://neo4j:7687",auth=("neo4j","test"))
neo4j_session_update=neo4j_driver.session()
neo4j_session_query=neo4j_driver.session()

# ML models saved in dedicated folders 
three_phase_model = keras.models.load_model('ThreePhaseModel/FuturePredictionsModelNoIndex/')
single_phase_model = keras.models.load_model('SinglePhaseModel/')
single_phase_CT_model = keras.models.load_model('SinglePhaseCTFuture/')
single_phase_anomaly = keras.models.load_model('SPAnomaly/')
single_phase_CT_anomaly = keras.models.load_model('SinglePhaseCTAnomaly/')
three_phase_anomaly = keras.models.load_model('ThreePhaseAnomaly/')

# Start application in real-time mode
simulation = False
currTime = datetime.now(timezone(timedelta(hours=-5)))

# Inserts Smart Meter data into MySQL instance. Specify different .csv file to load other data. Make sure to keep .csv format consistent.
# meter_data = pd.read_csv('meter.csv')
# meter_data.set_index('Date', inplace=True)
# types = {'Date': db.types.DateTime()} # Ensures 'Date' column is loaded as datetime type
# for col in meter_data.columns:
#     types[col] = db.types.Float()
# meter_data.to_sql('smart_meter', con=mysql_conn, if_exists='replace', dtype=types)


# Provides real-time and simulated-time functionality by updating necessary ML features in Neo4j instance. \
# If NOT in simulation mode, actual current time is used for currTime. Time values will be the same as real-world time. \
# If in simulation mode, currTime is incremented by 1 hour each time function is run. Trigger frequency can be changed in '/sim' endpoint 
def update_data():
    global simulation
    global currTime
    # Real-time mode (data is updated every hour)
    if not simulation:
        currTime = datetime.now(timezone(timedelta(hours=-5))) #Change based on desired timezone conversion from UTC
        print(currTime, flush=True)
        # Get Smart Meter data of most recent hour for all transformers
        sql_query=f"select * from smart_meter where date between '2017-{currTime:%m}-{currTime:%d} {currTime:%H}:00:00' and '2017-{currTime:%m}-{currTime:%d} {currTime:%H}:59:59'"
        result = mysql_conn.execute(sql_query)

        # Update Neo4j node properties 
        for row in result:
            # For each Bus in Smart Meter
            for col in row._fields:
                if (str(col) != 'Date'):
                    # Get ID of Previous Bus in the grid network
                    cypher_query = f"match (n {{BusID:\"T_{str(col)[-4:]}\"}}) return n.`Previous Bus` as PrevBus"
                    test = neo4j_session_update.run(cypher_query)
                    prev_bus = test.data()
                    # If the transformer does have a Previous Bus instantiated and it is a valid Bus ID
                    if prev_bus and prev_bus[0]['PrevBus'] != 0:
                        # Update the transformer node properties \ 
                        # row[col] = kWh output of current transformer \
                        # row['Bus ' + str(prev_bus[0]['PrevBus'])] = kWh output of Previous Bus in grid network
                        cypher_query = f"match (n {{BusID:\"T_{str(col)[-4:]}\"}}) \
                                    set n.PrevVal = n.CurrVal, n.CurrVal = {row[col]}, n.`PrevNode Val` = {row['Bus ' + str(prev_bus[0]['PrevBus'])]}, \
                                    n.Month = {currTime.month}, n.Day = {currTime.day}, n.Hour = {currTime.hour}, n.Year = 2017"
                        neo4j_session_update.run(cypher_query)
    # Simulated-time mode (data is updated every 10 seconds [or the trigger you set in ])
    else:
        currTime = currTime + timedelta(hours=1) #Change based on desired timezone conversion from UTC
        print(currTime, flush=True)
        sql_query=f"select * from smart_meter where date between '2017-{currTime:%m}-{currTime:%d} {currTime:%H}:00:00' and '2017-{currTime:%m}-{currTime:%d} {currTime:%H}:59:59'"
        result = mysql_conn.execute(sql_query)

        # Update Neo4j nodes
        for row in result:
            for col in row._fields:
                if (str(col) != 'Date'):
                    cypher_query = f"match (n {{BusID:\"T_{str(col)[-4:]}\"}}) return n.`Previous Bus` as PrevBus"
                    test = neo4j_session_update.run(cypher_query)
                    output = test.data()
                    if output and output[0]['PrevBus'] != 0:
                        cypher_query = f"match (n {{BusID:\"T_{str(col)[-4:]}\"}}) \
                                    set n.PrevVal = n.CurrVal, n.CurrVal = {row[col]}, n.`PrevNode Val` = {row['Bus ' + str(output[0]['PrevBus'])]}, \
                                    n.Month = {currTime.month}, n.Day = {currTime.day}, n.Hour = {currTime.hour}, n.Year = 2017"
                        neo4j_session_update.run(cypher_query)
    

    return

# Test endpoint to verify that application is running
@app.route('/time')
def get_current_time():
    return {'time': time.time()}

# Switch between real-time and simulated-time modes. Switches trigger of scheduled job between hourly and every 10 seconds
@app.route('/sim')
def switch_data_mode():
    global simulation
    global currTime
    if simulation:
        simulation = False
        scheduler.reschedule_job(job_id='update', trigger='cron', minute=0)
        print('Switched to real-time mode', flush=True)
    else:
        simulation = True
        scheduler.reschedule_job(job_id='update', trigger='cron', second='*/10')
        currTime = datetime.now(timezone(timedelta(hours=-5)))
        print('Switched to simulated-time mode', flush=True)
    return {'simulation': simulation}


# Gets past 24 hours worth of kWh data for the transformer specified by <bus>, T_<bus>, from MySQL. <bus> need only be the numbers representing that transformer (i.e. the endpoint for 24 hours of T_2015 data would be '/history/2015')
@app.route('/history/<bus>')
def get_table(bus):
    global simulation
    global currTime
    # If in real-time mode then use actual current time, else use simulated time that is updated in update_data()
    if not simulation:
        currTime = datetime.now(timezone(timedelta(hours=-5)))
    query=f"select date,`Bus {bus}` from smart_meter where date between date_sub('2017-{currTime:%m}-{currTime:%d} {currTime:%H}:00:00', interval 1 day) and '2017-{currTime:%m}-{currTime:%d} {currTime:%H}:59:59'"
    result = mysql_conn.execute(query)
    output = []
    for row in result:
        output.append(str(row[0]) + ': ' + str(row[1]))   
    return {'result': output}

# Return x,y coordinates of all transformers from Neo4j
@app.route("/coordinates",methods=["GET","POST"])
def return_coords():
    q1="match (n) return n.BusID as BusID, n.X as X, n.Y as Y"
    output=neo4j_session_query.run(q1)
    return(jsonify(output.data()))

# Return current value of all transformers from Neo4j
@app.route("/allCurrentValues",methods=["GET","POST"])
def return_currValues():
    q1="match (n) return n.BusID as BusID, n.CurrVal as currentValue"
    output=neo4j_session_query.run(q1)
    return(jsonify(output.data()))

# Return current value of T_<bus> from Neo4j. <bus> need only be the numbers representing that transformer (i.e. the endpoint for current value of T_2015 data would be '/allCurrentValues/2015')
@app.route("/allCurrentValues/<bus>",methods=["GET","POST"])
def return_nodeValue(bus):
    q1="match (n {BusID:'"+bus+"'}) return n.BusID as BusID, n.CurrVal as currentValue"
    print("....."+str(q1))
    output=neo4j_session_query.run(q1)
    return(jsonify(output.data()))

#return static info of specified bus number (/busInfo/T_2087)
@app.route("/busInfo/<bus>",methods=["GET","POST"])
def return_busInfo(bus):
    q1="match (n {BusID:'"+bus+"'}) return n, labels(n) as busType"
    output=neo4j_session_query.run(q1)
    return(jsonify(output.data()))

#return link info of every bus
@app.route("/buslinks",methods=["GET","POST"])
def return_allBusLinks():
    q1="match (n) return n.BusID as BusID, n.`Previous Bus` as PrevBus"
    output=neo4j_session_query.run(q1)
    return(jsonify(output.data()))

# Return future hour prediction of only three-phase transformers
@app.route("/threePhase",methods=["GET","POST"])
def return_threePhasePred():
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
    predictions = three_phase_model.predict(nodes).tolist()
    busPreds = []
    j = 0
    for i in output:
        busPreds.append(i['n.BusID'] + ': ' + str(predictions[j][0]))
        j+=1
    return {'predictions': busPreds}

# Return future hour prediction of only Single Phase transformers
@app.route("/singlePhase",methods=["GET","POST"])
def return_singlePhasePred():
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
    predictions = single_phase_model.predict(nodes).tolist()
    busPreds = []
    j = 0
    for i in output:
        busPreds.append(i['n.BusID'] + ': ' + str(predictions[j][0]))
        j+=1
    return {'predictions': busPreds}

# Return future hour prediction of only Single Phase Center Tapped transformers
@app.route("/singlePhaseCT",methods=["GET","POST"])
def return_singlePhaseCTPred():
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
    predictions = single_phase_CT_model.predict(nodes).tolist()
    busPreds = []
    j = 0
    for i in output:
        busPreds.append(i['n.BusID'] + ': ' + str(predictions[j][0]))
        j+=1
    return {'predictions': busPreds}

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

# Return future hour prediction of all transformer types. Returns list of prediction values.
@app.route("/allPred",methods=["GET","POST"])
def return_allPred():
    q1="match (n:`Single Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    q2="match (n:`Three Phase`) return n.BusID, n.`Primary voltage rating (kV)`, n.`Secondary voltage rating (kV)`, n.`kVA rating (kVA)`, n.` %R`, n.` %X`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    q3="match (n:`Single Phase CT`) return n.BusID, n.`kVA rating of Winding 1 (kVA)`,  n.` %R1`, n.` %R2`, n.` %R3`, n.` %X12`, n.` %X13`, n.` %X23`, n.Year, n.Month, n.Day, n.Hour, n.CurrVal, n.`PrevNode Val`, n.PrevVal"
    #Single Phase Predictions
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
    predictions = single_phase_model.predict(nodes).tolist()
    busPreds = []
    j = 0
    for i in output:
        busPreds.append(i['n.BusID'] + ': ' + str(predictions[j][0]))
        j+=1
    #Three Phase Prediction
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
    predictions = three_phase_model.predict(nodes).tolist()
    j = 0
    for i in output:
        busPreds.append(i['n.BusID'] + ': ' + str(predictions[j][0]))
        j+=1
    #Single Phase CT Prediction
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
    predictions = single_phase_CT_model.predict(nodes).tolist()
    j = 0
    for i in output:
        busPreds.append(i['n.BusID'] + ': ' + str(predictions[j][0]))
        j+=1
    #predictions = return_singlePhaseCTPred()

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

# Initialization of scheduler. Starts application in real-time mode, so values are updated hourly. \
# Trigger is switched by sending request to '/sim' endpoint initialized above.
start_time = datetime.now().replace(minute=0, second=0, microsecond=0)
scheduler = BackgroundScheduler()
scheduler.add_job(id='update', func=update_data, next_run_time=datetime.now(), trigger="cron", minute=0)
scheduler.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

