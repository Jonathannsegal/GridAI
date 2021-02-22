import time
import mltest as ml
import flask

app = flask.Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': 'hello'}

@app.route('/stock/<id>')
def get_pred(id):
    ml.ml_test(id)
    return flask.send_file('plot.png', mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
