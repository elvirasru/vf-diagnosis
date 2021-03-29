from scipy import stats
import pandas as pd
import numpy as np
from scipy import signal


def to_segments(data_set, user_id, db, signal_frequency, seconds):
    add_tags_by_group(data_set, seconds, signal_frequency, 'group')

    groups_with_nan = data_set[data_set['signal'].isna()]['group'].unique().tolist()
    data_set = data_set[~data_set['group'].isin(groups_with_nan)]
    data_set.reset_index(inplace=True)
    print("The following groups (containing NaN values) were excluded from " + user_id + ": " + str(groups_with_nan))

    data_set = data_set.assign(signal_prep=clean(data_set['signal'], signal_frequency))

    rest = add_tags_by_group(data_set, seconds, signal_frequency, 'new_group')
    data_set.drop(['signal', 'group'], axis=1, inplace=True)

    d1 = data_set.groupby('new_group')['annotation'].unique().reset_index()
    d1['annotation'] = d1['annotation'].apply(lambda y: stats.mode(y).mode[0])
    d1['annotation'] = d1['annotation'].apply(lambda x: str(x).replace("(", "", ))

    d2 = data_set.groupby('new_group')['signal_prep'].apply(list).reset_index()
    new_df = pd.merge(d1, d2, on="new_group")

    length = len(new_df)
    new_df['user_id'] = np.repeat(user_id, length)
    new_df['db'] = np.repeat(db, length)

    if rest > 0:
        # elimina el conjunto que no tiene 1000 muestras
        return new_df[:-1]
    return new_df


def add_tags_by_group(data_set, seconds, signal_frequency, col_name):
    total_rows = data_set.shape[0]
    num_of_obs_in_4s = signal_frequency * seconds
    rest = total_rows % num_of_obs_in_4s
    total_groups = total_rows // num_of_obs_in_4s
    p1 = np.repeat(np.linspace(1, total_groups, total_groups), num_of_obs_in_4s, axis=0)
    p2 = np.repeat(total_groups + 1, rest, axis=0)
    data_set.insert(0, col_name, pd.Series(np.concatenate((p1, p2))))
    return rest


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
