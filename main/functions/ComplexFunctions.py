import antropy as ant
import numpy as np
from scipy import signal


def hilbert_function(sub_signal, frequency):
    duration = len(sub_signal) / frequency

    down_sampled_signal = signal.resample(sub_signal, int(duration * 50))
    analytic_signal = signal.hilbert(down_sampled_signal)
    imaginary_signal = np.imag(analytic_signal)

    down_sampled_signal_40_grid = normalize_to_40(down_sampled_signal)
    imaginary_signal_40_grid = normalize_to_40(imaginary_signal)

    grid = np.zeros((40, 40), dtype=np.int32)
    grid[down_sampled_signal_40_grid, imaginary_signal_40_grid] = 1
    return np.sum(grid) / 1600


def phase_space_reconstruction_function(sub_signal, frequency):
    tau = 0.5
    new_frequency = 50
    duration = len(sub_signal) / frequency

    down_sampled_signal = signal.resample(sub_signal, int(duration * new_frequency))

    down_sampled_signal_40_grid = normalize_to_40(down_sampled_signal)

    len_signal_40_grid = len(down_sampled_signal_40_grid)

    num_samples = int(tau * new_frequency)
    xt = down_sampled_signal_40_grid[0: (len_signal_40_grid - num_samples)]
    xt_tau = down_sampled_signal_40_grid[num_samples:]

    grid = np.zeros((40, 40), dtype=np.int32)
    grid[xt, xt_tau] = 1
    return np.sum(grid) / 1600


def sample_entropy_function(sub_signal):
    return ant.sample_entropy(sub_signal)


def normalize_to_40(array):
    array = array - np.min(array)
    max_array = np.max(array)
    return ((array * 39) / max_array).astype(int)


