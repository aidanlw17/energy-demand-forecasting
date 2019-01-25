import pandas as pd
import numpy as np

import sys, os, subprocess
import wget
import datetime
import time

# Default Toronto
station_ID = 31688


def PullData(station_ID, year_start, year_end):
    # Get Datetimes
    # year_now = int(datetime.datetime.today().strftime('%Y'))-1

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
    year_static = list(range(year_start, year_end + 1))

    # Pull Statscan weather data
    print('Pulling Statscan Weather Data for Station {}...'.format(station_ID))

    for year in year_static:
        print(year)
        for month in range(1, 13):
            wget.download(
                "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={0}&Year={1}&Month={2}&Day=14&timeframe=1&submit=Download+Data".format(
                    station_ID, year, month), out='wget_data/Weather')

    print('Done.')

    # Clean, Convert CSV to Dataframes

    root = 'wget_data/Weather/'
    filenames = []

    for path, subdirs, files in os.walk(root):
        for name in files:
            filenames.append(os.path.join(path, name))

    print('Reading weather csvs to dataframe...')
    weather_data = pd.concat([pd.read_csv(f, skiprows=15) for f in filenames])
    print('Done.')

    return weather_data


if __name__ == "__main__":
    """weather_data = PullData(31688, 2011, 2013)

    print(weather_data.head())
    print(weather_data.tail())"""

    station_ID = input('Input Station ID: ')
    year_start = input('Input Start Year: ')
    year_end = input('Input End Year: ')
    print('Pulling weather data from {} to {}'.format(year_start, year_end))
    weather_data = PullData(station_ID, year_start, year_end)
    weather_data.to_csv('StatsCan Weather Data Station {} {}-{}'.format(station_ID, year_start, year_end))
