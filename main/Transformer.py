from scipy import stats
import pandas as pd
import numpy as np


def to_4s_segments(data):
    # (solo funciona para cudb)
    # para cudb 4 seg son 1000 observaciones
    clean(data)

    data['group'] = pd.Series(np.repeat(np.linspace(1, 128, 128), 994, axis=0))

    d1 = data.groupby('group')['an5'].unique().reset_index()
    d1['an5'] = d1['an5'].apply(lambda y: stats.mode(y).mode[0])
    d1['an5'] = d1['an5'].apply(lambda x: str(x).replace("(", "", ))

    d2 = data.groupby('group')['signal'].apply(list).reset_index()
    return pd.merge(d1, d2, on="group")


def clean(data):
    # TODO
    return data
