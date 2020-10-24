import time
import mltest as ml
from flask import Flask

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.strftime('%a, %B %d, %Y %I:%M:%S')}

#@app.route('/stock/<id>')
#def get_pred(id):
#    ml.ml_test(id)
#    return send_file('plot.png', mimetype='image/png')
