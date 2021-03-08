from scipy import stats
import pandas as pd
import numpy as np


def to_4s_segments(data):
    # 4 seg son 1000 observaciones
    clean(data)

    signal_frequency = 250
    total_rows = data.size
    num_of_obs_in_4s = signal_frequency * 4
    rest = total_rows % num_of_obs_in_4s
    total_groups = total_rows // num_of_obs_in_4s
    p1 = np.repeat(np.linspace(1, total_groups, total_groups), num_of_obs_in_4s, axis=0)
    p2 = np.repeat(total_groups + 1, rest, axis=0)

    data['group'] = pd.Series(np.concatenate((p1, p2)))

    d1 = data.groupby('group')['an5'].unique().reset_index()
    d1['an5'] = d1['an5'].apply(lambda y: stats.mode(y).mode[0])
    d1['an5'] = d1['an5'].apply(lambda x: str(x).replace("(", "", ))

    d2 = data.groupby('group')['signal'].apply(list).reset_index()
    new_df = pd.merge(d1, d2, on="group")

    if rest > 0:
        # elimina el conjunto que no tiene 1000 muestras
        return new_df[:-1]
    return new_df


def clean(data):
    # TODO
    return data
