"""Imports"""
import os

from warnings import warn
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

from assistant.src.assistant_service import AssistantService
from assistant.src.command_handler import CommandHandler
from assistant.src.speech_to_text import speech_text

VOICE_UPLOAD_FOLDER = '/tmp/voicefiles'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'raw'}  # add file formats as needed

app = Flask(__name__)
app.config['VOICE_UPLOAD_FOLDER'] = VOICE_UPLOAD_FOLDER


@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle webhook requests from Dialogflow."""
    # Get WebhookRequest object
    request_json = request.get_json(force=True)

    # Handle request)
    prompt = CommandHandler.handle_webhook(request_json)

    webhook_response = {
        "prompt": prompt,
    }

    # Copy metadata from request to response
    copy_list = ("session", "scene", "user")
    for copy_name in copy_list:
        if hasattr(request_json, copy_name):
            webhook_response[copy_name] = request_json[copy_name]  # type: ignore

    return jsonify(webhook_response)


def process_text_query(text_query):
    """Process the text query and return an appropriate response"""
    warn("process_text_query function is now deprecated.")

    service = AssistantService()
    handler, input_args = service.process_query(text_query)

    response = None if handler is None else \
        CommandHandler.handle_command(handler, input_args)

    return jsonify(response)


def voice_to_text(voice_file):
    """Converts voice file to a text string"""
    warn("voice_to_text function is now deprecated.")

    response = speech_text(voice_file, False)

    return response


def allowed_file(filename):
    """Limits to whitelisted file extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/text", methods=["POST"])
def text_request():
    """Text Request Endpoint"""
    warn("text_request function is now deprecated.")

    request_json = request.get_json()

    t_request = request_json['text']

    return process_text_query(t_request)


@app.route("/voice", methods=["POST"])
def voice_request():
    """Voice Request Endpoint set paramater "transcipt to any
    value to return a transcript of the speech"""
    warn("voice_request function is now deprecated.")

    voice_query = request.files.get('voice')
    transcript_mode = request.args.get("transcript", default=False, type=bool)
    tmpdir = False
    if not os.path.isdir(app.config['VOICE_UPLOAD_FOLDER']):
        os.mkdir(app.config['VOICE_UPLOAD_FOLDER'])
        tmpdir = True
    if voice_query.name == '':
        return 'No File'
    if voice_query and allowed_file(voice_query.filename):
        file_path = os.path.join(app.config['VOICE_UPLOAD_FOLDER'],
                                 secure_filename(voice_query.filename))
        voice_query.save(file_path)
        text_query = voice_to_text(file_path)
        # remove temporary file
        os.remove(file_path)
        if transcript_mode:
            return text_query
        return process_text_query(text_query)
    if tmpdir:
        os.rmdir(app.config['VOICE_UPLOAD_FOLDER'])

    return 'File extension not allowed'


@app.route("/setCred")
def set_cred():
    """sets google application crednentials. for debug use only"""
    warn("set_cred function is now deprecated.")

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getcwd() + \
        "/assistant/client_secret/speechtotext-331119-820cdd23000d.json"
    return os.environ['GOOGLE_APPLICATION_CREDENTIALS']


@app.route("/ping")
def ping():
    """Ping the server"""
    return "pong"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
