import TemporalFunctions as tf
import pandas as pd

from Reader import read_signal_annotations, get_users
from Transformer import to_segments
from Utils import add_variable

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 20)


def create_csv(db, seconds):
    users = get_users(db)

    complete_file = pd.DataFrame()
    for user in users:
        print("Read signal and annotations for user " + user)
        print("---------------------------------")
        signal_annotations_df = read_signal_annotations(user, db)
        print(signal_annotations_df)

        print("Calculate segments....")
        print("---------------------------------")
        segments_df = to_segments(signal_annotations_df, user, db, 250, seconds)
        print(segments_df)

        complete_file = pd.concat([complete_file, segments_df])

    print("Calculate variables....")
    print("---------------------------------")
    add_variable(complete_file, lambda x: tf.first_function(x), "var1")
    add_variable(complete_file, lambda x: tf.count1_function(x), "count1")
    add_variable(complete_file, lambda x: tf.count2_function(x), "count2")
    add_variable(complete_file, lambda x: tf.count3_function(x), "count3")
    print(complete_file)

    complete_file.to_csv(db + '-' + str(seconds) + "s.csv", index=False, header=True)


#create_csv('cudb', 4)
#create_csv('vfdb', 4)
