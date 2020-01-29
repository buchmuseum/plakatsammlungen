import argparse

import pandas as pd
import geopy.geocoders as geo
from geopy.extra.rate_limiter import RateLimiter
import numpy as np

parser = argparse.ArgumentParser(description="Geolocates places in a Excel file.")
parser.add_argument('excel_file', help="name of the Excel file serving as input")
# parser.add_argument('-c', '--column', default='Region', help="column of the table containing places")
parser.add_argument('csv_file', help="name of the output CSV file")

args = parser.parse_args()

geolocator = geo.Nominatim(user_agent='Itinerar')
geo.options.default_timeout = 10

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=5)

print("Lade die Datei {}...".format(args.excel_file))
df = pd.read_excel(args.excel_file, parse_dates=True)


print("Erstelle die Geodaten")

geo_stadt = []
geo_region = []
geo_land = []

for cnt, row in df.iterrows():
    print("processing row ", cnt)

    if not pd.isna(row['Stadt']):
       geo_stadt.append(geocode(row['Stadt'] + ', ' + str(row['Land'])))
    else:
       geo_stadt.append(np.nan)

    if not pd.isna(row['Region']):
        geo_region.append(geocode(row['Region'] + ', ' + str(row['Land'])))
    else:
        geo_region.append(np.nan)

    if not pd.isna(row['Land']):
        geo_land.append(geocode(row['Land']))
    else:
        geo_land.append(np.nan)


df['stadt_geo'] = pd.Series(geo_stadt)
df['region_geo'] = pd.Series(geo_region)
df['land_geo'] = pd.Series(geo_land)

df['stadt_latitude'] = df['stadt_geo'].apply(lambda x: x.latitude if pd.notna(x) else None)
df['stadt_longitude'] = df['stadt_geo'].apply(lambda x: x.longitude if pd.notna(x) else None)
df['region_latitude'] = df['region_geo'].apply(lambda x: x.latitude if pd.notna(x) else None)
df['region_longitude'] = df['region_geo'].apply(lambda x: x.longitude if pd.notna(x) else None)
df['land_latitude'] = df['land_geo'].apply(lambda x: x.latitude if pd.notna(x) else None)
df['land_longitude'] = df['land_geo'].apply(lambda x: x.longitude if pd.notna(x) else None)

print("Speichere die CSV-Datei {}...".format(args.csv_file))
df.to_csv(args.csv_file)
