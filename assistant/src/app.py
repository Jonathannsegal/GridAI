"""Imports"""
import os

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

from assistant.src.assistant_service import AssistantService
from assistant.src.command_handler import CommandHandler
from assistant.src.speech_to_text import speech_text

VOICE_UPLOAD_FOLDER = '/tmp/voicefiles'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'raw'}  # add file formats as needed

app = Flask(__name__)
app.config['VOICE_UPLOAD_FOLDER'] = VOICE_UPLOAD_FOLDER


def process_text_query(text_query):
    """Process the text query and return an appropriate response"""

    service = AssistantService()
    handler, input_args = service.process_query(text_query)

    response = None if handler is None else \
        CommandHandler().handle_command(handler, input_args)

    return jsonify(response)


def voice_to_text(voice_file):
    """Converts voice file to a text string"""

    response = speech_text(voice_file, False)

    return response


def allowed_file(filename):
    """Limits to whitelisted file extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/text", methods=["POST"])
def text_request():
    """Text Request Endpoint"""

    request_json = request.get_json()

    t_request = request_json['text']

    return process_text_query(t_request)


@app.route("/voice", methods=["POST"])
def voice_request():
    """Voice Request Endpoint set paramater "transcipt to any
    value to return a transcript of the speech"""
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
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getcwd() + \
        "/assistant/client_secret/speechtotext-331119-820cdd23000d.json"
    return os.environ['GOOGLE_APPLICATION_CREDENTIALS']


@app.route("/ping")
def ping_pong():
    """Ping Pong"""
    return 'pong'


@app.route("/res", methods=["POST"])
def gen_response():
    """generate response"""
    request_json = request.get_json()
    return jsonify(request_json)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
