import numpy as np
from scipy import signal


def first_function(array):
    return array[0]


def count1_function(sub_signal):
    b = [0.5, 0, -0.5]
    a = [8, -14, 7]
    signal_filt = signal.filtfilt(b, a, sub_signal)
    count = 0
    length_window = 4
    frequency = 250
    signal_abs = np.abs(signal_filt)
    for n in range(0, length_window):
        s = signal_abs[(n * frequency + 1):(n * frequency + frequency)]
        max_s = np.max(s)

        count += sum(s >= 0.5 * max_s)
    return count / length_window


def count2_function(sub_signal):
    b = [0.5, 0, -0.5]
    a = [8, -14, 7]
    signal_filt = signal.filtfilt(b, a, sub_signal)
    count = 0
    length_window = 4
    frequency = 250
    signal_abs = np.abs(signal_filt)
    for n in range(0, length_window):
        s = signal_abs[(n * frequency + 1):(n * frequency + frequency)]
        mean_s = np.mean(s)

        count += sum(s >= mean_s)
    return count / length_window


def count3_function(sub_signal):
    b = [0.5, 0, -0.5]
    a = [8, -14, 7]
    signal_filt = signal.filtfilt(b, a, sub_signal)
    count = 0
    length_window = 4
    frequency = 250
    signal_abs = np.abs(signal_filt)
    for n in range(0, length_window):
        s = signal_abs[(n * frequency + 1):(n * frequency + frequency)]
        mean_s = np.mean(s)
        md_s = np.mean(np.abs(s - np.repeat(mean_s, len(s))))

        count += sum((s >= (mean_s - md_s)) & (s <= (mean_s + md_s)))
    return count / length_window
