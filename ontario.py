import pandas as pd
import numpy as np

# Read in data.
df = pd.read_csv("./data/data-ontario.csv")
# pd.set_option('display.max_rows', None)

df["date"].replace(to_replace='T.*', value="", regex=True, inplace=True)
df["street"] = (df["street"]
    .str.replace(pat="  ", repl=" ")
    .str.replace(pat="Street", repl="St")
    .str.replace(pat="Road", repl="Rd")
    .str.replace(pat="Avenue", repl="Ave")
    .str.replace(pat="Highway", repl="Hwy")
    .str.replace(pat="Drive", repl="Dr")
    .str.replace(pat="Boulevard", repl="Blvd")
    .str.replace(pat="East", repl="E")
    .str.replace(pat="West", repl="W")
    .str.replace(pat="North", repl="N")
    .str.replace(pat="South", repl="S")
    .str.replace(pat="[.,']", repl="")
)
df["city"] = df["city"].str.replace(pat=" ,", repl=",")
df["date"] = pd.to_datetime(df["date"], errors='coerce')

df_max = df.groupby('street').min()

df_max.to_csv("./data-ontario-clean.csv")

df_pivot = pd.pivot_table(df_max, index= "date", aggfunc="count")
print(df_pivot)
