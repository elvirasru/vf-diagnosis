import numpy as np


def vf_leak_function(sub_signal):
    length = len(sub_signal)
    sub_signal = np.array(sub_signal)
    numerator = np.sum(np.abs(sub_signal[1:]))
    denominator = np.sum(np.abs(sub_signal[1:] - sub_signal[0:length -1]))
    n = np.floor(np.pi * numerator / denominator + 1 / 2).astype(int)

    a = np.sum(np.abs(sub_signal[n + 1:] + sub_signal[0: (length - n - 1)]))
    b = np.sum(np.abs(sub_signal[n + 1:]) + np.abs(sub_signal[0: (length - n - 1)]))
    return a / b
