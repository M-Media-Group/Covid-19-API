import json
import csv
from requests import get  # to make GET request
from contextlib import closing
import codecs
import datetime

converted_dates = {}
recent_data = {}
country_array = {}
global_population = 0

countries_url = 'https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json'

with closing(get(countries_url, stream=True)) as r:
    countries = r.json()

for country in countries:
    # break
    if (country['population'] is not None):
        global_population = global_population + int(country['population'])

    if (country['country'] not in country_array):
        country_array[country['country']] = country['population']

latest_url = 'https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_1.csv'

with closing(get(latest_url, stream=True)) as r:
    reader = csv.DictReader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
    recent_rows = list(reader)

for row in recent_rows:
    if (row['Country_Region'] not in recent_data):
        recent_data[row['Country_Region']] = {}
        recent_data[row['Country_Region']]['All'] = {}
        recent_data[row['Country_Region']]['All']['confirmed'] = 0
        recent_data[row['Country_Region']]['All']['recovered'] = 0
        recent_data[row['Country_Region']]['All']['deaths'] = 0
        if (row['Country_Region'] in country_array):
            recent_data[row['Country_Region']]['All']['population'] = int(
                country_array[row['Country_Region']])

    if row['Province_State'] == '':
        row['Province_State'] = "All"

    if (row['Province_State'] not in recent_data[row['Country_Region']]):
        recent_data[row['Country_Region']][row['Province_State']] = {}

    if row['Province_State'] == row['Country_Region']:
        recent_data[row['Country_Region']]['All']['lat'] = row['Lat']
        recent_data[row['Country_Region']]['All']['long'] = row['Long_']

    recent_data[row['Country_Region']][
        row['Province_State']]['lat'] = row['Lat']
    recent_data[row['Country_Region']][
        row['Province_State']]['long'] = row['Long_']

    recent_data[row['Country_Region']][
        row['Province_State']]['confirmed'] = int(row['Confirmed'])
    recent_data[row['Country_Region']][
        row['Province_State']]['recovered'] = int(row['Recovered'])
    recent_data[row['Country_Region']][row['Province_State']]['deaths'] = int(
        row['Deaths'])
    recent_data[row['Country_Region']][
        row['Province_State']]['updated'] = datetime.datetime.strptime(
            row['Last_Update'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%F')

    # print(recent_data['Iraq']['All']['confirmed'])
    if (row['Province_State'] != 'All'):
        recent_data[row['Country_Region']]['All']['confirmed'] = int(
            recent_data[row['Country_Region']][
                row['Province_State']]['confirmed']) + int(
                    recent_data[row['Country_Region']]['All']['confirmed'])
        recent_data[row['Country_Region']]['All']['recovered'] = int(
            recent_data[row['Country_Region']][
                row['Province_State']]['recovered']) + int(
                    recent_data[row['Country_Region']]['All']['recovered'])
        recent_data[row['Country_Region']]['All']['deaths'] = int(recent_data[
            row['Country_Region']][row['Province_State']]['deaths']) + int(
                recent_data[row['Country_Region']]['All']['deaths'])

global_array = {
    'All': {
        'population': global_population,
        'deaths': 0,
        'recovered': 0,
        'confirmed': 0
    }
}
for (key, value) in recent_data.items():
    if ('All' in value):
        global_array['All']['confirmed'] = global_array['All'][
            'confirmed'] + value['All']['confirmed']
        global_array['All']['recovered'] = global_array['All'][
            'recovered'] + value['All']['recovered']
        global_array['All'][
            'deaths'] = global_array['All']['deaths'] + value['All']['deaths']

recent_data['Global'] = global_array


def lambda_handler(event, context):

    try:
        return_data = recent_data[event['queryStringParameters']['country']]

    except:
        return_data = recent_data  # or whatever
    return {'statusCode': 200, 'body': json.dumps(return_data)}
