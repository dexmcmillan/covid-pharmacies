import pandas as pd
import numpy as np
import glob

# pd.set_option('display.max_rows', None)
pd.set_option('use_inf_as_na', True)

# Read in data.

covid_pharmacies = pd.read_csv('./data/clean/output-canada.csv', index_col=None, header=0)
covid_pharmacies = covid_pharmacies[covid_pharmacies["province"] == "Ontario"]

flu = pd.read_csv('./data/data-flu.csv', index_col=None, header=0)

flu["street"] = (flu["street"]
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

flu["type"] = "Other/Independent"
flu.loc[flu["name"].str.contains("Walmart|Wal-Mart", na=False, regex=True), 'type'] = "Walmart"
flu.loc[flu["name"].str.contains("Rexall", na=False, regex=True), 'type'] = "Rexall"
flu.loc[flu["name"].str.contains("Shoppers", na=False, regex=True), 'type'] = "Shoppers Drug Mart"
flu.loc[flu["name"].str.contains("Sobeys|FreshCo", na=False, regex=True), 'type'] = "Sobeys"
flu.loc[flu["name"].str.contains("Guardian", na=False, regex=True), 'type'] = "Guardian"
flu.loc[flu["name"].str.contains("Costco|Costo", na=False, regex=True), 'type'] = "Costco"
flu.loc[flu["name"].str.contains("Loblaw||Zehr|Drugstore|Drug Store Pharmacy|Superstore|nofrills", na=False, regex=True), 'type'] = "Loblaw"
flu.loc[flu["name"].str.contains("Pharmasave", na=False, regex=True), 'type'] = "Pharmasave"
flu.loc[flu["name"].str.contains("Metro", na=False, regex=True), 'type'] = "Metro"
flu.loc[flu["name"].str.contains("IDA", na=False, regex=True), 'type'] = "IDA"

flu["location_code"] = flu["X"].astype(str) + flu["Y"].astype(str) + flu["type"]

export = covid_pharmacies[~covid_pharmacies["street"].isin(flu["street"])]

print(export)



export.to_csv('./data/clean/output-flu.csv')