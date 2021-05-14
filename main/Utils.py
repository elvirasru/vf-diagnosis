import numpy as np


def add_variable(data, function, var_name):
    data[var_name] = data['signal_prep'].apply(function)


def quantile(x, q):
    n = len(x)
    y = np.sort(x)
    return (np.interp(q, np.linspace(1 / (2 * n), (2 * n - 1) / (2 * n), n), y))


def prctile(x, p):
    return (quantile(x, np.array(p) / 100))
