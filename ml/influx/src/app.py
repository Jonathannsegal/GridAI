"""Imports"""
import os

from flask import Flask

app = Flask(__name__)


def func(value):
    """Add 2 to value"""
    return value + 2


@app.route("/")
def hello_world():
    """Hello World Endpoint"""
    name = os.environ.get("NAME", "World")
    return f"Grid AI: Influx, Hello {name}!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
