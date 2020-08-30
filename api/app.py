from flask import Flask, request

from base64 import b64decode
from calculations.calculations import calc_spectrum, calculate_mean, calculate_median

# To remind: I have only brief knowledge of Python, so after spending couple of hours trying to run your code,
# that does not compile on my machine, I've followed the example from the web and created a project that works,
# so that's why it looks a little different from yours

# What I did
# 1. Extracted calculation lines to separate package, so in future it can be used separately
# 2. Reduced the code duplication by extracting common lines to the separate methods

# TODO:
#  1. Use method for "if request.method == 'GET':" - need to find out how to do this gracefully in Python
#  2. Change the deserialize to more generic
#  3. Create an object for 'param'

app = Flask(__name__)


@app.route('/')
def routes():
    return {
        "spectrum": "/spectrum",
        "mean": "/mean",
        "median": "/median",
    }


# the spectrum endpoint
@app.route('/spectrum', methods=['POST', 'GET'])
def spectrum():
    if request.method == 'GET':
        return {'params': ['sampling_rate', 'units', 'dtype']}

    dtype, spectrum_input, sr, units = deserialize_spectrum_data()

    spectrum_result = calc_spectrum(sr, units, dtype, spectrum_input)
    return {'spectrum': spectrum_result}


# the mean endpoint
@app.route('/mean', methods=['POST', 'GET'])
def mean():
    if request.method == 'GET':
        return {'params': ['dtype']}

    dtype, req, spectrum_input = deserialize_basic_data()

    mean_result = calculate_mean(spectrum_input, dtype)
    return {'mean': mean_result}


# the median endpoint
@app.route('/median', methods=['POST', 'GET'])
def median():
    if request.method == 'GET':
        return {'params': ['dtype']}

    dtype, req, spectrum_input = deserialize_basic_data()
    median_result = calculate_median(spectrum_input, dtype)
    return {'median': median_result}


# Note: Use something like this for deserialization:
# https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
# def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
# def json2obj(data): return json.loads(data, object_hook=_json_object_hook)
#
# x = json2obj(data)

# Deserializes dtype and spectrum from input
def deserialize_basic_data():
    req = request.get_json()
    dtype = req['dtype'] if 'dtype' in req else "float64"
    spectrum_input = b64decode(req['spectrum'].encode('utf-8'))
    return dtype, req, spectrum_input


# Deserializes more spectrum from input
def deserialize_spectrum_data():
    dtype, req, spectrum_input = deserialize_basic_data()
    sr = float(req['sampling_rate'])
    units = req['units']
    return dtype, spectrum_input, sr, units


if __name__ == '__main__':
    app.run()
