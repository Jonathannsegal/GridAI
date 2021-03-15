import time
import flask

app = flask.Flask(__name__)

@app.route('/time')
def get_current_time():
    return str(time.strftime('%a, %B %d, %Y %I:%M:%S'))

@app.route('/')
def home():
    return 'Hello World!'
