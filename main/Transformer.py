from scipy import stats
import pandas as pd
import numpy as np
from scipy import signal


def to_segments(data_set, user_id, db, signal_frequency, seconds):
    data_cleaned = clean(data_set['signal'], signal_frequency)

    total_rows = data_cleaned.size
    num_of_obs_in_4s = signal_frequency * seconds
    rest = total_rows % num_of_obs_in_4s
    total_groups = total_rows // num_of_obs_in_4s

    p1 = np.repeat(np.linspace(1, total_groups, total_groups), num_of_obs_in_4s, axis=0)
    p2 = np.repeat(total_groups + 1, rest, axis=0)

    data_set['signal_prep'] = data_cleaned
    data_set.drop('signal', axis=1, inplace=True)
    data_set['group'] = pd.Series(np.concatenate((p1, p2)))

    d1 = data_set.groupby('group')['annotation'].unique().reset_index()
    d1['annotation'] = d1['annotation'].apply(lambda y: stats.mode(y).mode[0])
    d1['annotation'] = d1['annotation'].apply(lambda x: str(x).replace("(", "", ))

    d2 = data_set.groupby('group')['signal_prep'].apply(list).reset_index()
    new_df = pd.merge(d1, d2, on="group")

    length = len(new_df)
    new_df['user_id'] = np.repeat(user_id, length)
    new_df['db'] = np.repeat(db, length)

    if rest > 0:
        # elimina el conjunto que no tiene 1000 muestras
        return new_df[:-1]
    return new_df


def clean(data, signal_frequency):
    data_without_mean = signal.detrend(data, type == 'constant')
    data_ma_filter = moving_average(data_without_mean, 5)
    data_hp = high_pass_filter(data_ma_filter, 1, signal_frequency)
    return low_pass_filter(data_hp, 30, signal_frequency)


def moving_average(x, n):
    b = (np.ones(n)) / n
    return signal.lfilter(b, 1, x)


def low_pass_filter(data, hz, signal_frequency):
    b, a = signal.butter(1, hz, 'lowpass', fs=signal_frequency)
    return signal.filtfilt(b, a, data)


def high_pass_filter(data, hz, signal_frequency):
    b, a = signal.butter(1, hz, 'highpass', fs=signal_frequency)
    return signal.filtfilt(b, a, data)
