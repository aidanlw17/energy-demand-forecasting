import pandas as pd
import numpy as np

import sys, os, subprocess
import wget
import datetime
import time
import csv

# Default Toronto
station_ID = 31688


def pull_data(station_name, station_ID, year_start, year_end):
    # Get Datetimes

    # Check directory
    print('Clean old files...')

    # clean weather direc
    root_weather = 'wget_data/Weather'
    filenames_weather = []

    for path, subdirs, files in os.walk(root_weather):
        for name in files:
            filenames_weather.append(os.path.join(path, name))

    for i in range(len(filenames_weather)):
        os.remove(filenames_weather[i])

    print('Done.')

    # Compare with required
    year_static = list(range(int(year_start), int(year_end) + 1))

    # Pull Statscan weather data
    print('Pulling Statscan Weather Data for Station {}...'.format(station_ID))

    for year in year_static:
        print(year)
        for month in range(1, 13):
            wget.download(
                "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={0}&Year={1}&Month={2}&Day=14&timeframe=1&submit=Download+Data".format(
                    station_ID, year, month), out='../data/Weather Data/'+ str(station_name) + str(year) + str(month) + '.csv')
            df = pd.read_csv('../data/Weather Data/'+ str(station_name) + str(year) + str(month) + '.csv', skiprows=15)
            df['DateTime'] = pd.to_datetime(df[df.columns[0]])
            df.set_index('DateTime', inplace=True, drop=True)
            df.to_csv('../data/Weather Data/'+ str(station_name) + str(year) + str(month) + '.csv')

    print('Done.')

if __name__ == "__main__":
    """weather_data = PullData(31688, 2011, 2013)

    print(weather_data.head())
    print(weather_data.tail())"""

    station_name = input('Input Station Name: ')
    station_ID = input('Input Station ID: ')
    year_start = input('Input Start Year: ')
    year_end = input('Input End Year: ')
    
    print('Pulling weather data from {} to {}'.format(year_start, year_end))
    weather_data = pull_data(station_name, station_ID, year_start, year_end)
