import numpy as np
from scipy import signal
from scipy.fft import fft


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
        bWT.append(np.percentile(window, 50 + valPT / 2) - np.percentile(window, 50 - valPT / 2))

    return max(bWT)


def x3(sub_signal, frequency, time_window):
    sub_signal = np.array(sub_signal)
    n_fft = 2048
    fft_signal = fft(sub_signal * np.hamming(time_window * frequency), n_fft)
    fft_signal = np.fft.fftshift(fft_signal)

    ff = np.linspace(-frequency / 2, frequency / 2, n_fft)
    Pss = abs(fft_signal) ** 2

    dif = ff[1] - ff[0]
    area = sum(Pss * dif) / 2
    Pss = Pss / area

    indexes_1_30 = np.argwhere((ff > 0) & (ff < 30))
    f = ff[indexes_1_30][:, 0]
    Pss = Pss[indexes_1_30][:, 0]

    indexes = np.argwhere((f >= 1) & (f <= 10))
    argmax = np.argmax(Pss[indexes])

    return f[indexes[argmax]][0]


def x4(sub_signal, frequency, time_window):
    sub_signal = np.array(sub_signal)
    n_fft = 2048
    fft_signal = fft(sub_signal * np.hamming(time_window * frequency), n_fft)
    fft_signal = np.fft.fftshift(fft_signal)

    ff = np.linspace(-frequency / 2, frequency / 2, n_fft)
    Pss = abs(fft_signal) ** 2

    dif = ff[1] - ff[0]
    area = sum(Pss * dif) / 2
    Pss = Pss / area

    indexes_1_30 = np.argwhere((ff > 0) & (ff < 30))
    f = ff[indexes_1_30]
    Pss = Pss[indexes_1_30]

    return sum(Pss[(f >= 2.5) & (f <= 7.5)] * dif)


def x5(sub_signal, frequency, time_window):
    sub_signal = np.array(sub_signal)
    n_fft = 2048
    fft_signal = fft(sub_signal * np.hamming(time_window * frequency), n_fft)
    fft_signal = np.fft.fftshift(fft_signal)

    ff = np.linspace(-frequency / 2, frequency / 2, n_fft)
    Pss = abs(fft_signal) ** 2

    dif = ff[1] - ff[0]
    area = sum(Pss * dif) / 2
    Pss = Pss / area

    indexes_1_30 = np.argwhere((ff > 0) & (ff < 30))
    f = ff[indexes_1_30]
    Pss = Pss[indexes_1_30]

    return sum(Pss[(f >= 12) & (f <= 30)] * dif)

