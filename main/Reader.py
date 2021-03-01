import pandas as pd


def read_signal_annotations(user_id, db):
    signal = read_signal(user_id, db)
    annotations = read_annotations(user_id, db)

    new_data = pd.merge(signal, annotations, left_index=True, right_on="signalId", how='left')
    new_data.reset_index(inplace=True)
    new_data.drop('index', axis=1, inplace=True)
    new_data.an5.fillna(method='ffill', inplace=True)
    return new_data


def read_signal(user_id, db):
    column_names = ['signal']
    if db == 'vfdb':
        column_names.append("signal 2")
    return pd.read_csv("data/" + db + "/signal/" + user_id + ".csv", sep='\t', names=column_names, index_col=0)


def read_annotations(user_id, db):
    df = pd.read_csv("data/" + db + "/annotations/" + user_id + "n.csv", delimiter='\t', names=list('ab'))

    df = df.assign(date=df.a.str.split(expand=True)[0],
                   signalId=df.a.str.split(expand=True)[1].astype("int64"),
                   an5=df.b)
    df.drop(['a', 'b'], axis=1, inplace=True)
    return df
