import Functions as f

from Reader import read_signal_annotations
from Transformer import to_4s_segments
from Utils import add_variable

import pandas as pd

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 20)

# prueba
user_id = "cu01"
database = "cudb"

complete_file = read_signal_annotations(user_id, database)
print("These are the signal and annotations for user" + user_id + " and database" + database)
print("---------------------------------")
print(complete_file)

segments = to_4s_segments(complete_file)
print("Segments")
print("---------------------------------")
print(segments)

add_variable(segments, lambda x: f.first_function(x), "var1")
add_variable(segments, lambda x: f.count1_function(x), "count1")
add_variable(segments, lambda x: f.count2_function(x), "count2")
add_variable(segments, lambda x: f.count3_function(x), "count3")
print("Segments with variables")
print("---------------------------------")
print(segments)
