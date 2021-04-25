import pandas as pd
import numpy as np
import glob

# pd.set_option('display.max_rows', None)
pd.set_option('use_inf_as_na', True)

df = pd.read_csv('./data/data-ontario-pharmacies.csv')
df.rename(columns={"POSTALCODE": "postal", "EN_NAME": "name", "COMMUNITY": "city", "ADDRESS_1": "street"}, inplace=True)

df["postal"] = df["postal"].str.replace(" ", "")
df["city"] = (df["city"]
    .str.replace(", ON", "")
    .str.replace(pat=" ,", repl=",")
    )

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


df["type"] = "Other/Independent"
df.loc[df["name"].str.contains("Walmart|Wal-Mart", na=False, regex=True), 'type'] = "Walmart"
df.loc[df["name"].str.contains("Rexall", na=False, regex=True), 'type'] = "Rexall"
df.loc[df["name"].str.contains("Shoppers Drug", na=False, regex=True), 'type'] = "Shoppers Drug Mart"
df.loc[df["name"].str.contains("Sobeys|FreshCo", na=False, regex=True), 'type'] = "Sobeys"
df.loc[df["name"].str.contains("Guardian", na=False, regex=True), 'type'] = "Guardian"
df.loc[df["name"].str.contains("Costco|Costo", na=False, regex=True), 'type'] = "Costco"
df.loc[df["name"].str.contains("Loblaw|Zehr|Drugstore|Drug Store Pharmacy|Superstore|nofrills", na=False, regex=True), 'type'] = "Loblaw"
df.loc[df["name"].str.contains("Pharmasave", na=False, regex=True), 'type'] = "Pharmasave"
df.loc[df["name"].str.contains("Metro", na=False, regex=True), 'type'] = "Metro"
df.loc[df["name"].str.contains("IDA", na=False, regex=True), 'type'] = "IDA"

df["location_code"] = df["X"].astype(str) + df["Y"].astype(str) + df["type"]
# df.drop_duplicates(subset="location_code", inplace=True)

df["fsa"] = df["postal"].str.slice(0, 3)

# df_pharmacies.rename(columns={"POSTALCODE": "postal", "EN_NAME": "name", "COMMUNITY": "city"}, inplace=True)
# combined = df.append(df_pharmacies)

data = df[["name", 'city', "street", "X", "Y", "postal", "fsa", "location_code", "type"]]
toprint = data.groupby("location_code").min()
print(toprint)

# toprint[toprint["province"] == "Ontario"][toprint["date"] == "2021-04-13"].to_csv('./data/new-additions.csv')
# with pd.ExcelWriter('./data/output-data.xlsx') as writer:
#     data.to_excel(writer, sheet_name='Data')
toprint.to_csv('./data/clean/output-all.csv')