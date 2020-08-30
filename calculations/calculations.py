import numpy as np


# This is the file that combines all calculations methods needed for the REST API point
# Note: in Java or C# I'll make it like a static class, but I see no point to do this in Python
# (though maybe there may be loading implications, like loading too much methods, the methods violation etc.
# since I know that Python is very flexible)

# Method that calculates spectrum
# Problems that I can not fix:
# 1. There is not used parameter 'units'
# 2. There not used 'duration'
# 3. Calculations that unnecessary (lines 2 and 3)
# 4. Method takes 'spectrum', reformat it and returns back the reformation - what is the purpose of the method?
def calc_spectrum(sampling_rate, units, dtype, spectrum_):
    spectrum = np.frombuffer(spectrum_, dtype=dtype).tolist()
    samples_per_signal = len(spectrum)  # why do we need this?
    duration = samples_per_signal / sampling_rate
    return spectrum


# Method that calculates mean
# Problems that I can not fix:
# 1. There is not used 'samples_per_signal'
def calculate_mean(spectrum, dtype):
    spectrum_ = np.frombuffer(spectrum, dtype=dtype).tolist()
    samples_per_signal = len(spectrum_)
    mean = np.mean(spectrum_)
    return mean


# Method that calculates mean
# Problems that I can not fix:
# 1. There is not used 'samples_per_signal'
def calculate_median(spectrum, dtype):
    spectrum_ = np.frombuffer(spectrum, dtype=dtype).tolist()
    samples_per_signal = len(spectrum)
    median = np.median(spectrum)
    return median
