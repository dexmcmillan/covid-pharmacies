import pandas as pd
import numpy as np
import glob

# pd.set_option('display.max_rows', None)
pd.set_option('use_inf_as_na', True)

# Read in data.

frame = pd.read_csv('./data/clean/output-canada.csv', index_col=None, header=0)

ontario = frame[frame["province"] == "Ontario"]

print(ontario)



ontario.to_csv('./data/clean/output-ontario.csv')