from flask import Flask, request
from base64 import b64decode
from calculations.calculations import calc_spectrum, calculate_mean, calculate_median


# To remind: I have only brief knowledge of Python, so after spending couple of hours trying to run your code,
# that does not compile on my machine, I've followed the example from the web and created a project that run,
# so that's why it looks a little different from yours. And only then I've received your explanation on what
# exactly I need to do.

# What I did:
# 1. Extracted calculation lines to separate package, so in future it can be used separately
# 2. Reduced the code duplication by extracting common lines to the separate methods
# 3. I did not succeeded to run your tests (yet), but I've created Integration tests using PyCharm scratch option
# 4. I wrote some unit test using another library (it did worked perfectly from the first time)

# TODO:
#  1. Use method for "if request.method == 'GET':" - need to find out how to do this gracefully in Python,
#       in c# I'd use Reflection for that
#  2. Change the deserialize to more generic (see the example below)
#  3. Create an object for 'param'
#  4. Somehow reduce the amount of the string duplication, in c# I'd do the constant for it,
#           I not sure know how to do it in Python
#  5. There is a total mismatch in parameters, there several un necessary

def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    def routes():
        return {
            "spectrum": "/spectrum",
            "mean": "/mean",
            "median": "/median",
        }

    # the spectrum endpoint
    @app.route('/spectrum', methods=['POST', 'GET'])  # In the tests there are more commands to implement
    def spectrum():
        if request.method == 'GET':  # this code is ugly since it duplicated and uses string instead of
            return {'params': ['sampling_rate', 'units', 'dtype']}

        dtype, spectrum_input, sr, units = deserialize_spectrum_data()  # here I'd use at least C# tuple or class,
        # depends on the other usages

        spectrum_result = calc_spectrum(sr, units, dtype, spectrum_input)
        return {'spectrum': spectrum_result} # string should be const

    # the mean endpoint
    @app.route('/mean', methods=['POST', 'GET'])
    def mean():
        if request.method == 'GET':
            return {'params': ['dtype', 'spectrum']}

        dtype, spectrum_input, req = deserialize_basic_data()

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
        if req is None or req['spectrum'] is None:
            raise ValueError("Illegal parameter in deserialize_basic_data")

        dtype = req['dtype'] if 'dtype' in req else "float64"
        spectrum_input = b64decode(req['spectrum'].encode('utf-8'))  # why it is encoded? what does it mean by spectrum?
        return dtype, spectrum_input, req

    # Deserializes more spectrum from input
    def deserialize_spectrum_data():
        dtype, req, spectrum_input = deserialize_basic_data()

        if req is None or req['sampling_rate'] or req['units'] is None:
            raise ValueError("Illegal parameter in deserialize_spectrum_data")

        sr = float(req['sampling_rate'])
        units = req['units']
        return dtype, spectrum_input, sr, units

    return app


if __name__ == '__main__':
    create_app().app.run()
