# type: ignore
"""Imports"""
import os

from datetime import datetime

import re

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from flask import Flask, request, jsonify
from decouple import config
from numpy import Infinity

import pandas as pd


app = Flask(__name__)

# You can generate a Token from the "Tokens Tab" in the UI
token = config('DATABASE_TOKEN', default='token')
org = config('DATABASE_ORG', default='org')
bucket = config('DATABASE_BUCKET', default='bucket')
url = config('DATABASE_URL', default='url')

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)


@app.route("/")
def index():
    """Root Directory"""
    return "Hello, GridAI Influx"


@app.route('/writeVoltageById', methods=['POST'])
def write_influx():
    """write to bucket"""
    bus_name = request.args["bus"]
    voltage = request.args["voltage"]
    write_api = client.write_api(write_options=SYNCHRONOUS)
    point = influxdb_client.Point(bus_name).field("voltage", float(voltage))
    write_api.write(bucket=bucket, org=org, record=point)
    return f"Created bus {bus_name}, voltage {voltage} successfully"


@app.route('/getVoltageById', methods=['GET'])
def get_current_voltage():
    """read from bucket"""
    bus_name = request.args["busId"]
    query_api = client.query_api()
    query = f""" from(bucket:"{bucket}")\
    |> range(start: -30d)
    |> filter(fn:(r) => r._measurement == "{bus_name}" )\
    |> last()"""
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_time(), record.get_measurement(), record.get_value()))
    return jsonify(results)


@app.route('/comparison', methods=['GET'])
def comparison():
    """compare with given values"""
    start = "-30d"
    stop = "0d"
    if "start" in request.args:
        start = request.args["start"]
    if "stop" in request.args:
        stop = request.args["stop"]
    query = f""" from(bucket:"{bucket}")\n\
    |> range(start: {start}, stop: {stop})\n"""
    if "busId" in request.args:
        bus_name = request.args["busId"]
        query += f"""|> filter(fn:(r) => r._measurement == "{bus_name}" )\n"""
    field = "activePower"
    if "curr_flg" in request.args:
        query += """|> last()\n"""
    if "power_type" in request.args:
        field = request.args["power_type"]
    comp_str = "=="
    if request.args["comparison_type"] == "1":
        comp_str = "<"
    elif request.args["comparison_type"] == "2":
        comp_str = ">"
    comp_val = request.args["comp_val"]
    query_api = client.query_api()
    query += f"""|> filter(fn:(r) => r._field == "{field}" and r._value {comp_str}  {comp_val} )\n"""
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_time(), record.get_measurement(), record.get_value()))
    return jsonify(results)


@app.route('/generic', methods=['GET'])
def generic():  # noqa: C901; pylint: disable=R0912
    """generic query for voice assistant"""
    start = "-30d"
    stop = "0d"
    if "start" in request.args:
        start = request.args["start"]
    if "stop" in request.args:
        stop = request.args["stop"]
    query = f""" from(bucket:"{bucket}")\n\
    |> range(start: {start}, stop: {stop})\n"""
    if "busId" in request.args:
        bus_name = request.args["busId"]
        query += f"""|> filter(fn:(r) => r._measurement == "{bus_name}" )\n"""
    field = "activePower"
    if "power_type" in request.args:
        field = request.args["power_type"]
    lowest_value = 0
    highest_value = Infinity
    if "lowest_value" in request.args:
        lowest_value = request.args["lowest_value"]
    if "highest_value" in request.args:
        highest_value = request.args["highest_value"]
    query += f"""|> filter(fn:(r) => r._field == "{field}" and r._value > {lowest_value} """
    if float(highest_value) < Infinity:
        query += f""" and r._value < {highest_value}"""
    query += ")\n|> group()\n"
    if "extrema_type" in request.args:
        count = 20
        if "count" in request.args:
            count = request.args["count"]
        if request.args["extrema_type"] == "MAX":
            query += f"""|> top(n:{count})"""
        elif request.args["extrema_type"] == "MIN":
            query += f"""|> bottom(n:{count})"""
    query_api = client.query_api()
    result = query_api.query(org=org, query=query)
    results = []
    results.append(("Time", "Bus",
                    ' '.join(re.findall('[A-Z][^A-Z]*', field[0].upper() + field[1:]))))
    for table in result:
        for record in table.records:
            results.append((record.get_time(), record.get_measurement(), record.get_value()))
    return jsonify(results)


@app.route('/getAllCurrentVoltageFrontend', methods=['GET'])
def get_all_current_voltage_frontend():
    """read from bucket"""
    query_api = client.query_api()
    query = f""" from(bucket:"{bucket}")\
    |> range(start: -30d)\
    |> last()\
    |> pivot(rowKey: ["_time","_measurement"], columnKey: ["_field"], valueColumn: "_value")"""
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            print(record)
            results += [{
                "date": record.get_time(),
                "id": record.get_measurement(),
                "active": record["activePower"],
                "reactive": record["reactivePower"]
                }]

    return jsonify(results)


@app.route('/getAllCurrentGeneratedPower', methods=['GET'])
def get_all_current_generated_power():
    """read from bucket"""
    query_api = client.query_api()
    query = f""" from(bucket:"{bucket}")\
    |> range(start: -30d)\
    |> filter(fn:(r) => r._field == "activeGeneratedPower")\
    |> last()\
    |> pivot(rowKey: ["_time","_measurement"], columnKey: ["_field"], valueColumn: "_value")"""
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            print(record)
            results += [{
                "date": record.get_time(),
                "id": record.get_measurement(),
                "generated": record["activeGeneratedPower"]
                }]

    return jsonify(results)


@app.route("/uploadCsv", methods=['POST'])
def upload_csv():
    """Uploads csv to influx db"""
    csv_url = request.args["url"]
    data = pd.read_csv(csv_url)
    new_data = data.set_index('_time', inplace=False)
    write_api = client.write_api()
    dfs = dict(tuple(new_data.groupby('_measurement')))

    for measurements in dfs:
        result = dfs[measurements].drop('_measurement', 1)
        write_api.write(bucket, org, record=result, data_frame_measurement_name=measurements)
    return f"Uploaded data from {csv_url} successfully"


@app.route("/deleteAll", methods=['DELETE'])
def delete_all():
    """Delete all"""
    delete_api = client.delete_api()
    delete_api.delete(datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
                      datetime.strptime("2030-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"), "", bucket, org)
    return "All Data Deleted"


@app.route("/getExtreme", methods=['GET'])
def get_extreme():
    """Get extremes"""
    start = "-30d"
    stop = "0d"
    if "start" in request.args:
        start = request.args["start"]
    if "stop" in request.args:
        stop = request.args["stop"]
    query = f""" from(bucket:"{bucket}")\n\
    |> range(start: {start}, stop: {stop})\n"""
    field = "activePower"
    if "power_type" in request.args:
        field = request.args["power_type"]
    query += f"""|> filter(fn:(r) => r._field == "{field}")\n"""
    query += "|> group()\n"
    if request.args["extrema_type"] == "MAX":
        query += f"""|> top(n:{request.args["count"]})"""
    elif request.args["extrema_type"] == "MIN":
        query += f"""|> bottom(n:{request.args["count"]})"""
    else:
        raise Exception()
    query_api = client.query_api()
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_time(), record.get_measurement(), record.get_value()))
    return jsonify(results)


@app.route("/uploadTestCsv", methods=['POST'])
def upload_test_csv():
    """Uploads Test csv to influx db"""
    csv_urls = ["", ""]
    csv_urls[0] = "https://firebasestorage.googleapis.com/v0/b/influx-csv.appspot.com/o/"
    csv_urls[0] += "out.csv?alt=media&token=aa6015a9-a582-47d7-81f3-0f8018378842"
    csv_urls[1] = "https://firebasestorage.googleapis.com/v0/b/influx-csv.appspot.com/o/"
    csv_urls[1] += "generatedPower.csv?alt=media&token=6fbf89cf-79a2-493e-94f2-a451e83af539"
    today = datetime.today()
    for csv_url in csv_urls:
        data = pd.read_csv(csv_url)
        data['_time'] = pd.to_datetime(data['_time'], format="%Y-%m-%d %H:%M")
        data['_time'] = data['_time'].apply(lambda t: t.replace(day=today.day - 1, month=today.month, year=today.year))
        new_data = data.set_index('_time', inplace=False)
        write_api = client.write_api()
        dfs = dict(tuple(new_data.groupby('_measurement')))

        for measurements in dfs:
            result = dfs[measurements].drop('_measurement', 1)
            write_api.write(bucket, org, record=result, data_frame_measurement_name=measurements)

    return "Uploaded test data successfully"


@app.route("/ping")
def ping():
    """Ping the server"""
    return "pong"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
