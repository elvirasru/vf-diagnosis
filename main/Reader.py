import pandas as pd

csv = pd.read_csv("data/vfdb/signal/418.csv", sep='\t', header=None, index_col=0)

print(csv.head())
