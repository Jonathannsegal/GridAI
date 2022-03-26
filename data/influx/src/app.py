# type: ignore
"""Imports"""
import os

from datetime import datetime

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from flask import Flask, request, jsonify
from decouple import config

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
    point = influxdb_client.Point(bus_name).field("voltage", voltage)
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


@app.route('/getAllCurrentVoltage', methods=['GET'])
def get_all_current_voltage():
    """read from bucket"""
    query_api = client.query_api()
    query = f""" from(bucket:"{bucket}")\
    |> range(start: -30d)\
    |> last()"""
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_time(), record.get_measurement(), record.get_value()))
    return jsonify(results)


@app.route("/uploadCsv", methods=['POST'])
def upload_csv():
    """Uploads csv to influx db"""
    csv_url = request.args["url"]
    data = pd.read_csv(csv_url)
    for i in range(data.shape[0]):
        # pylint: disable=maybe-no-member
        point = influxdb_client.Point(data.iat[i, 0]) \
            .field('voltage', data.at[i, 'kw']) \
            .time(data.at[i, 'date'])
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=point)
    return f"Uploaded data from {csv_url} successfully"


@app.route("/uploadTestCsv", methods=['POST'])
def upload_test_csv():
    """Uploads Test csv to influx db"""
    csv_url = """https://firebasestorage.googleapis.com/v0/b/influx-csv.appspot.com
    /o/updated.csv?alt=media&token=9cf9d70e-d5c2-4629-b259-a65f533cf0b2"""
    data = pd.read_csv(csv_url)
    for i in range(data.shape[0]):
        # pylint: disable=maybe-no-member
        relative_time = datetime.strptime(data.at[i, 'date'], "%Y-%m-%d %H:%M:%S")
        date = datetime.today().replace(hour=relative_time.hour,
                                        minute=relative_time.minute, second=relative_time.second, microsecond=0)
        point = influxdb_client.Point(data.iat[i, 0]) \
            .field('voltage', data.at[i, 'kw']) \
            .time(str(date))
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=point)  #
    return "Uploaded test data successfully"


@app.route("/ping")
def ping():
    """Ping the server"""
    return "pong"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
