import wfdb
import pandas as pd
import numpy as np


def read_signal_annotations(user_id, db):
    s = read_signal(user_id, db)
    annotations = read_annotations(user_id, db)

    new_data = pd.merge(s, annotations, left_index=True, right_on="signalId", how='left')
    new_data.reset_index(inplace=True)
    new_data.drop('index', axis=1, inplace=True)
    new_data.annotation.fillna(method='ffill', inplace=True)
    return new_data


def get_users(db):
    return wfdb.get_record_list(db)


def read_signal(user_id, db):
    record = wfdb.rdrecord(user_id, pn_dir=db + '/1.0.0/')
    df = pd.DataFrame([s[0] for s in record.p_signal], columns=['signal'])
    return df


def read_annotations(user_id, db):
    annotation = wfdb.rdann(user_id, 'atr', pn_dir=db)
    symbols = annotation.symbol
    notes = annotation.aux_note

    count = 0
    annotations = []
    for note in notes:
        symbol = symbols[count]
        if symbol == '[':
            annotations.append('VF')
        elif symbol == ']':
            annotations.append("0")
        elif note != '':
            annotations.append(note)
        else:
            annotations.append(np.nan)
        count += 1

    return pd.DataFrame({'annotation': pd.Series(annotations), 'signalId': annotation.sample})
