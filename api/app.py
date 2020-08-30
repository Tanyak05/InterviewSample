from flask import Flask, request
import base64
import numpy as np

from calculations.calculations import calc_spectrum, calculate_mean, calculate_median

app = Flask(__name__)


@app.route('/')
def routes():
    return {
        "spectrum": "/spectrum",
        "mean": "/mean",
        "median": "/median",
    }


@app.route('/spectrum', methods=['POST', 'GET'])
def spectrum():
    if request.method == 'GET':
        return {'params': ['sampling_rate', 'units', 'dtype']}

    req = request.get_json()
    sr = float(req['sampling_rate'])
    units = req["units"]
    dtype = req['dtype'] if 'dtype' in req else "float64"

    spectrum_ = calc_spectrum(sr, units, dtype )
    return {'spectrum': spectrum_}


@app.route('/mean', methods=['POST', 'GET'])
def mean():
    if request.method == 'GET':
        return {'params': ['dtype']}

    req = request.get_json()
    dtype = req['dtype'] if 'dtype' in req else "float64"
    spectrum = np.frombuffer(base64.b64decode(req["spectrum"].encode('utf-8')), dtype=dtype).tolist()
    mean = calculate_mean(spectrum)
    return {'mean': mean}


@app.route('/median', methods=['POST', 'GET'])
def median():
    if request.method == 'GET':
        return {'params': ['dtype']}

    req = request.get_json()
    dtype = req['dtype'] if 'dtype' in req else "float64"
    spectrum = np.frombuffer(base64.b64decode(req["spectrum"].encode('utf-8')), dtype=dtype).tolist()
    median = calculate_median(spectrum)
    return {'median': median}


if __name__ == '__main__':
    app.run()
