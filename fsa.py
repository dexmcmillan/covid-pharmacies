import pandas as pd
import numpy as np

# pd.set_option('display.max_rows', None)
pd.set_option('use_inf_as_na', True)

# Read in data.
df_covid = pd.read_csv("./data/data-ontario-geocoded.csv")
df_all = pd.read_csv("./data/data-ontario-pharmacies.csv")
df_ices = pd.read_csv("./data/ices-covid-data.csv")

df_covid["postal"] = df_covid["postal"].str.replace(" ", "")
df_covid["covid_site"] = "Yes"
df_covid["city"] = (df_covid["city"]
    .str.replace(", ON", "")
    .str.replace(pat=" ,", repl=",")
    )
df_covid["date"].replace(to_replace='T.*', value="", regex=True, inplace=True)
df_covid["street"] = (df_covid["street"]
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
df_covid["date"] = pd.to_datetime(df_covid["date"], errors='coerce')
df_covid["location_code"] = df_covid["Longitude"].astype('str') + df_covid["Latitude"].astype('str')

df_all["location_code"] = df_all["X"].astype('str') + df_all["Y"].astype('str')
df_all["covid_site"] = "No"
df_all.rename(columns={"EN_NAME": "name", "ADDRESS_1": "street", "POSTALCODE": "postal", "COMMUNITY": "city", "X": "Latitude", "Y": "Longitude"}, inplace=True)

df = df_covid.append(df_all)
df.drop_duplicates(subset="location_code", inplace=True)

df["type"] = "Other/Independent"
df["type"][df["name"].str.contains("Walmart|Wal-Mart")] = "Walmart"
df["type"][df["name"].str.contains("Rexall")] = "Rexall"
df["type"][df["name"].str.contains("Shoppers")] = "Shoppers Drug Mart"
df["type"][df["name"].str.contains("Sobeys")] = "Sobeys"
df["type"][df["name"].str.contains("Guardian")] = "Guardian"
df["type"][df["name"].str.contains("Costco|Costo", regex=True)] = "Costco"
df["type"][df["name"].str.contains("Loblaw")] = "Loblaw"
df["type"][df["name"].str.contains("IDA")] = "IDA"
df["type"][df["name"].str.contains("Pharmasave")] = "Pharmasave"
df["type"][df["name"].str.contains("Metro")] = "Metro"

df["fsa"] = df["postal"].str.slice(0, 3)
df["% positivity"] = df_ices["Overall - % positivity"].astype('int64')
data = df[["name", 'city', 'covid_site', "date", "Latitude", "Longitude", "postal", "fsa", "type", "% positivity"]]

pivot = pd.pivot_table(data, index="fsa", columns=["covid_site"], aggfunc="size").fillna(0).astype('int')
pivot["%"] = pivot["Yes"] / (pivot["Yes"] + pivot["No"])
pivot["%"].fillna(0, inplace=True)
pivot = pivot.merge(right=df_ices[["fsa", "Overall - % positivity"]], on="fsa")
pivot.sort_values("%", ascending=False, inplace=True)

pivot_brands = pd.pivot_table(data, index="type", columns="covid_site", aggfunc='size').fillna(0).astype('int64')
pivot_brands.rename({"city": "count"}, inplace=True)
pivot_brands["%"] = pivot_brands["Yes"] / (pivot_brands["Yes"] + pivot_brands["No"])
pivot_brands.sort_values("%", ascending=False)

with pd.ExcelWriter('./data/output-data.xlsx') as writer:
    data.to_excel(writer, sheet_name='Data')
    pivot.to_excel(writer, sheet_name='FSA Pivot')
    pivot_brands.to_excel(writer, sheet_name='Companies')


print(pivot)
print(pivot_brands)