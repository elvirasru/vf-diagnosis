import pandas as pd

from main.functions import TemporalFunctions as tf
from main.functions import ComplexFunctions as cf
from main.functions import SpectralFunctions as sf
from Reader import read_signal_annotations, get_users
from Transformer import to_segments
from Utils import add_variable

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 20)


def create_csv(db, frequency, seconds):
    users = get_users(db)

    complete_file = pd.DataFrame()
    for user in users:
        print("Read signal and annotations for user " + user)
        print("---------------------------------")
        signal_annotations_df = read_signal_annotations(user, db)
        print(signal_annotations_df)

        print("Calculate segments....")
        print("---------------------------------")
        segments_df = to_segments(signal_annotations_df, user, db, frequency, seconds)
        print(segments_df)

        complete_file = pd.concat([complete_file, segments_df])

    complete_file.reset_index(inplace=True)

    print("Calculate variables....")
    print("---------------------------------")
    add_variable(complete_file, lambda x: tf.count1_function(x, frequency, seconds), "count1")
    add_variable(complete_file, lambda x: tf.count2_function(x, frequency, seconds), "count2")
    add_variable(complete_file, lambda x: tf.count3_function(x, frequency, seconds), "count3")
    add_variable(complete_file, lambda x: tf.threshold_crossing_sample_count(x, frequency, seconds), "tcsc")
    add_variable(complete_file, lambda x: tf.standard_exponential(x, frequency), "exp")
    add_variable(complete_file, lambda x: tf.modified_exponential(x, frequency), "modExp")
    add_variable(complete_file, lambda x: tf.mean_absolute_value(x, frequency, seconds), "MAV")
    add_variable(complete_file, lambda x: tf.bcp(x, frequency), "bCP")
    add_variable(complete_file, lambda x: tf.x1(x, frequency), "x1")
    add_variable(complete_file, lambda x: cf.hilbert_function(x, frequency), "HILB")
    add_variable(complete_file, lambda x: cf.phase_space_reconstruction_function(x, frequency), "PSR")
    add_variable(complete_file, lambda x: cf.sample_entropy_function(x), "SampEn")
    add_variable(complete_file, lambda x: sf.vf_leak_function(x), "VFLEAK")
    add_variable(complete_file, lambda x: sf.bwt(x, frequency), "bWT")
    print(complete_file)

    complete_file.to_csv(db + '-' + str(seconds) + "s.csv", index=False, header=True)

# create_csv('cudb', 250, 4)
# create_csv('vfdb', 250, 4)