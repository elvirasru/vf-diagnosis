import numpy as np
from scipy import signal


def count1_function(sub_signal, frequency, time_window):
    b = [0.5, 0, -0.5]
    a = [8, -14, 7]
    filtered_signal = signal.filtfilt(b, a, sub_signal)
    signal_abs = np.abs(filtered_signal)

    count = 0
    for n in range(0, time_window):
        s = signal_abs[(n * frequency):(n * frequency + frequency)]
        max_s = np.max(s)

        count += sum(s >= 0.5 * max_s)
    return count / time_window


def count2_function(sub_signal, frequency, time_window):
    b = [0.5, 0, -0.5]
    a = [8, -14, 7]
    filtered_signal = signal.filtfilt(b, a, sub_signal)
    signal_abs = np.abs(filtered_signal)

    count = 0
    for n in range(0, time_window):
        s = signal_abs[(n * frequency):(n * frequency + frequency)]

        count += sum(s >= np.mean(s))
    return count / time_window


def count3_function(sub_signal, frequency, time_window):
    b = [0.5, 0, -0.5]
    a = [8, -14, 7]
    filtered_signal = signal.filtfilt(b, a, sub_signal)
    signal_abs = np.abs(filtered_signal)

    count = 0
    for n in range(0, time_window):
        s = signal_abs[(n * frequency):(n * frequency + frequency)]
        mean_s = np.mean(s)
        md_s = np.mean(np.abs(s - mean_s))

        count += sum((s >= (mean_s - md_s)) & (s <= (mean_s + md_s)))
    return count / time_window


def threshold_crossing_sample_count(sub_signal, frequency, time_window):
    threshold = 0.2
    window_duration = 3
    window_size = window_duration * frequency
    tcsc = []
    for n in range(0, time_window - window_duration + 1):
        signal_window_3s = sub_signal[(n * frequency):((n + window_duration) * frequency)]
        signal_window_3s *= signal.tukey(window_size, alpha=(0.5 / window_duration))
        signal_window_3s = np.abs(signal_window_3s)
        signal_window_3s /= np.max(signal_window_3s)
        tcsc.append(np.sum(signal_window_3s > threshold) * 100 / window_size)
    return np.mean(tcsc)


def standard_exponential(sub_signal, frequency):
    tau = 3
    signal_size = len(sub_signal)
    max_time = np.argmax(sub_signal)
    max_value = sub_signal[max_time]
    f = lambda x: max_value * np.exp(-np.abs(x - max_time) / (tau * frequency))

    higher = True if sub_signal[0] > f(0) else False
    n_crosses = 0
    for t in range(1, signal_size):
        threshold = f(t)
        sample = sub_signal[t]
        if higher:
            if sample < threshold:
                higher = False
                n_crosses += 1
        else:
            if sample > threshold:
                higher = True
                n_crosses += 1
    return n_crosses / (signal_size / frequency)


def modified_exponential(sub_signal, frequency):
    tau = 0.2
    f = lambda x, y, z: x * np.exp(-np.abs(y - z) / (tau * frequency))

    signal_size = len(sub_signal)
    max_values_indexes = signal.argrelmax(np.array(sub_signal), order=round(0.05 * frequency))[0]

    local_max_index = max_values_indexes[0]
    local_max_value = sub_signal[max_values_indexes[0]]
    t = local_max_index + 1
    n_crosses = 0
    while t < signal_size:
        exp_value = f(local_max_value, t, local_max_index)
        if sub_signal[t] > exp_value:
            n_crosses += 1
            next_max_indexes = list(filter(lambda x: x > t, max_values_indexes))
            if len(next_max_indexes) == 0 or next_max_indexes[0] == signal_size:
                break

            local_max_index = next_max_indexes[0]
            local_max_value = sub_signal[local_max_index]
            t = local_max_index + 1
        else:
            t += 1
    return n_crosses / (signal_size / frequency)


def mean_absolute_value(sub_signal, frequency, time_window):
    window_duration = 2
    mav = []
    for n in range(0, time_window - window_duration + 1):
        signal_window_2s = sub_signal[(n * frequency):((n + window_duration) * frequency)]
        signal_window_2s = np.abs(signal_window_2s)
        signal_window_2s = signal_window_2s / np.max(signal_window_2s)
        mav.append(np.mean(signal_window_2s))
    return np.mean(mav)


def bcp(sub_signal, frequency):
    sub_signal = np.array(sub_signal)
    threshold = 0.0055
    window_length = 2 * frequency
    x_d = (sub_signal[1:] - sub_signal[0:len(sub_signal) - 1]) ** 2
    x_d = np.append(x_d, x_d[-1])
    number_of_windows = round(len(x_d) / window_length)

    bCP = []
    for i in range(0, number_of_windows):
        window = x_d[i * window_length:(i + 1) * window_length]
        normalized_window = window / max(window)
        bCP.append(sum(normalized_window < threshold) / window_length)

    return min(bCP)


def x1(sub_signal, frequency):
    sub_signal = np.array(sub_signal)
    window_length = 2 * frequency
    aMs = 100
    bP = np.ones(round(aMs * frequency / 1000))

    x_d = (sub_signal[1:] - sub_signal[0:len(sub_signal) - 1]) ** 2
    x_d = np.append(x_d, x_d[-1])

    x_d = np.append(np.ones((1, window_length)) * x_d[0], x_d)
    x_d = np.append(x_d, np.ones((1, window_length)) * x_d[-1])

    x_d = signal.filtfilt(bP, 1, x_d)
    x_d = x_d[(window_length + 1): -(window_length - 1)]

    return np.percentile(x_d, 10) / max(x_d)