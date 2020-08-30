import base64
import numpy as np


def calc_spectrum(sampling_rate, units, dtype, spectrum_):
    spectrum = np.frombuffer(base64.b64decode(spectrum_.encode('utf-8')), dtype=dtype).tolist()
    samples_per_signal = len(spectrum)
    duration = samples_per_signal / sampling_rate
    return spectrum


def calculate_mean(spectrum):
    samples_per_signal = len(spectrum)
    mean = np.mean(spectrum)
    return mean


def calculate_median(spectrum):
    samples_per_signal = len(spectrum)
    median = np.median(spectrum)
    return median