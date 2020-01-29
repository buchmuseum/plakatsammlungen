import argparse

import pandas as pd

import plotly.express as px

parser = argparse.ArgumentParser(description="Create maps from data in a csv file.")
parser.add_argument('csv_file', help="name of the csv file serving as input")
parser.add_argument('-f', '--format', choices=['line', 'scatter', 'animation'],
                    default='line', help="format of the map")
parser.add_argument('map_file', help="name of the output html file")

args = parser.parse_args()

df = pd.read_csv(args.csv_file, parse_dates=True)

if args.format == 'line':
    fig = px.line_geo(df[df['stadt_latitude'] != None], lat='stadt_latitude', lon='stadt_longitude', scope='europe',
                      text='Stadt', hover_data=['Anzahl Stadt'])
elif args.format == 'scatter':
    fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', scope='europe',
                      text='Ort', hover_data=['Datum', 'Ereignis'])
#  elif args.format == 'bubble':
#      fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', scope='europe',
#                        text='Ort', hover_data=['Datum', 'Ereignis'], size='')
elif args.format == 'animation':
    fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', scope='europe',
                         text='Ort', hover_data=['Datum', 'Ereignis'],
                         animation_frame='Datum')

fig.write_html(args.map_file)
