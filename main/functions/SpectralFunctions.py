import numpy as np
from scipy import signal
from Utils import prctile


def vf_leak_function(sub_signal):
    length = len(sub_signal)
    sub_signal = np.array(sub_signal)
    numerator = np.sum(np.abs(sub_signal[1:]))
    denominator = np.sum(np.abs(sub_signal[1:] - sub_signal[0:length - 1]))
    n = np.floor(np.pi * numerator / denominator + 1 / 2).astype(int)

    a = np.sum(np.abs(sub_signal[n + 1:] + sub_signal[0: (length - n - 1)]))
    b = np.sum(np.abs(sub_signal[n + 1:]) + np.abs(sub_signal[0: (length - n - 1)]))
    return a / b


def bwt(sub_signal, frequency):
    sub_signal = np.array(sub_signal)
    window_length = 2 * frequency
    valPT = 47

    x_d = np.append(np.ones((1, window_length)) * sub_signal[0], sub_signal)
    x_d = np.append(x_d, np.ones((1, window_length)) * sub_signal[-1])

    Wn = 2 * [6.5 / frequency, 30 / frequency]
    b, a = signal.butter(5, Wn, btype="bandpass")
    x_d = signal.filtfilt(b, a, x_d)
    x_d = x_d[(window_length + 1): -(window_length - 1)]
    number_of_windows = round(len(x_d) / window_length)

    bWT = []
    for i in range(0, number_of_windows):
        window = x_d[i * window_length:(i + 1) * window_length]
        window = window / max(abs(window))
        bWT.append(prctile(window, 50 + valPT / 2) - prctile(window, 50 - valPT / 2))

    return max(bWT)
