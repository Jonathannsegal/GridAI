"""Imports"""
import os

from flask import Flask, jsonify, request

app = Flask(__name__)


def process_text_query(text_query):
    """Process the text query and return an appropriate response"""

    # TODO

    return jsonify(text_query)


def voice_to_text(voice_file):
    """Converts voice file to a text string"""

    # TODO

    return f"Grid AI: ASSISTANT, PLACEHOLDER: {str(voice_file)}"


@app.route("/text", methods=["POST"])
def text_request():
    """Text Request Endpoint"""

    text_query = request.form.get('text')

    return process_text_query(text_query)


@app.route("/voice", methods=["POST"])
def voice_request():
    """Voice Request Endpoint"""

    voice_query = request.files.get('voice')
    text_query = voice_to_text(voice_query)

    return process_text_query(text_query)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
