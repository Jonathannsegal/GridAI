# type: ignore
"""Imports"""
import os

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from flask import Flask, request, jsonify
from decouple import config

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


@app.route('/writeInflux', methods=['POST'])
def write_influx():
    """write to bucket"""
    bus_name = request.args["bus"]
    voltage = request.args["voltage"]
    write_api = client.write_api(write_options=SYNCHRONOUS)
    point = influxdb_client.Point(bus_name).field("voltage", voltage)
    write_api.write(bucket=bucket, org=org, record=point)
    return f"Created bus {bus_name}, voltage {voltage} successfully"


@app.route('/readInflux', methods=['GET'])
def read_influx():
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


@app.route("/ping")
def ping():
    """Ping the server"""
    return "pong"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
