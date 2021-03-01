from Reader import read_signal_annotations
from Transformer import to_4s_segments
from Functions import first_function
from Utils import add_variable

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

add_variable(segments, lambda x: first_function(x), "var1")
print("Segments with variable")
print("---------------------------------")
print(segments)
