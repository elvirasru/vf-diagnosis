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


def bwt(sub_signal, frequency, time_window):
    sub_signal = np.array(sub_signal)
    length = len(sub_signal)
    window_duration = 2
    window_length = 2 * frequency
    valC = 0.0055
    valPT = 47

    x_d = np.ones(1, window_duration * frequency) * sub_signal[:], np.transpose(
        np.ones(1, window_duration * frequency) * sub_signal[-1])
    b, a = scipy.signal.butter(5, 2 * [6.5, 30] / frequency, 'bandpass')
    x_d = scipy.signal.filtfilt(b, a, x_d)
    x_d = x_d(window_duration * frequency + x_d[0:length - 1] - window_duration * frequency)
    number_of_windows = round(len(x_dl) / window_length)

    bWT = []
    for i in range(1, number_of_windows):
        window = x_d[i * window_length:(i + 1) * window_length]
        bWT.append((np.percentile(window, 50 + valPT / 2) - np.percentile(window, 50 - valPT / 2)) / max(abs(window)))
    return max(bWT)