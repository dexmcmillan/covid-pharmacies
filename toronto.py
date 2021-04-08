import pandas as pd
import numpy as np

# Read in the full dataset downloaded from the proximity measures database from StatsCan.
# Data is not included in this repo as it's too large. Please download from
# https://www150.statcan.gc.ca/n1/pub/17-26-0002/172600022020001-eng.htm
df = pd.read_csv("./PMD-en.csv")
df.replace(to_replace=",", value="", inplace=True)

toronto = df[(df["CSDNAME"] == "Toronto")]

toronto.to_csv(r'./data-toronto.csv', index=True, header=True)