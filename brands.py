import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)

# Read in data.
df = pd.read_csv("./data/data-ontario-clean.csv")

df[df["name"].str.contains("Walmart")] = "Walmart"

df[df["name"].str.contains("Rexall")] = "Rexall"

df[df["name"].str.contains("Shoppers")] = "Shoppers Drug Mart"

df[df["name"].str.contains("Sobeys")] = "Sobeys"

df[df["name"].str.contains("Guardian")] = "Guardian"

df[df["name"].str.contains("Costco|Costo", regex=True)] = "Costco"

df[df["name"].str.contains("Loblaw")] = "Loblaw"

df[df["name"].str.contains("IDA")] = "IDA"

df[df["name"].str.contains("Pharmasave")] = "Pharmasave"

df[df["name"].str.contains("Metro")] = "Metro"

df[~df["name"].str.contains("Walmart|Rexall|Shoppers Drug Mart|Sobeys|Guardian|Costco|Loblaw|IDA|Pharmasave|Metro", regex=True)] = "Independent"

pivot = pd.pivot_table(df, index="name", aggfunc="size")
print(pivot)

