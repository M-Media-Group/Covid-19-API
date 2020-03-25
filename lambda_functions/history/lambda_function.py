import json
import csv
from requests import get  # to make GET request
from contextlib import closing
import codecs
import datetime
import os

country_array = {}
global_population = 0
countries_url ='https://raw.githubusercontent.com/M-Media-Group/country-json/master/src/countries-master.json'
latest_url ='https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_1.csv'

def proccessCountries():
	global global_population
	countries = None
	if not os.path.isfile('/tmp/countries.json'):
		with closing(get(countries_url, stream=True)) as r:
			countries = r.json()
			with open('/tmp/countries.json', 'a+') as file:
				file.write(json.dumps(countries))
	else:
		with open('/tmp/countries.json') as r:
			countries = json.load(r)

	for country in countries:
		# break
		if(country['population'] is not None):
			global_population = global_population + int(country['population'])

		if(country['country'] not in country_array):
			country_array[country['country']] = {}
			for (key, value) in country.items():
				country_array[country['country']][key] = value
	return country_array

def proccessMain(status):
	url ='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_'+status+'_global.csv'
	data = {}
	converted_dates = {}

	with closing(get(url, stream=True)) as r:
		reader = csv.DictReader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
		rows = list(reader)

	for row in rows:
		area_sum = 0

		if (row['Country/Region'] not in data):
			data[row['Country/Region']] = {}
			data[row['Country/Region']]['All'] = {}
			data[row['Country/Region']]['All']['dates'] = {}
			
            if(row['Country/Region'] in country_array):
				for key in country_array[row['Country/Region']]:
					data[row['Country/Region']]['All'][key] = country_array[row['Country/Region']][key]			

		if row['Province/State'] == '':
			row['Province/State'] = "All"

		if (row['Province/State'] not in data[row['Country/Region']]):
			data[row['Country/Region']][row['Province/State']] = {}

		if row['Province/State'] == row['Country/Region']:
			data[row['Country/Region']]['All']['lat'] = row['Lat']
			data[row['Country/Region']]['All']['long'] = row['Long']


		if ('dates' not in data[row['Country/Region']][row['Province/State']]):
			data[row['Country/Region']][row['Province/State']]['dates'] = {}

		for column in reversed(row):
			if column != 'Province/State' and column != 'Country/Region' and column != 'Lat' and column != 'Long':
				# total_collected_sum = total_collected_sum + int(row[column])
				original_column = column
				if(row[column] == ''):
					row[column] = 0

				if(column not in converted_dates):
					converted_dates[column] = datetime.datetime.strptime(column, '%m/%d/%y').strftime('%F')

				column = converted_dates[column]

				if (column not in data[row['Country/Region']]['All']['dates']):
					data[row['Country/Region']]['All']['dates'][column] = 0

				data[row['Country/Region']]['All']['dates'][column] = data[row['Country/Region']]['All']['dates'][column] + int(float(row[original_column]))

				if (column not in data[row['Country/Region']][row['Province/State']]['dates']):
					data[row['Country/Region']][row['Province/State']]['dates'][column] = 0

				data[row['Country/Region']][row['Province/State']]['dates'][column]  = int(row[original_column])

	global_array = {'All': {'population': global_population, 'dates': {}}}

	for (key, value) in data.items():

		for column in value['All']['dates']:
			if (column not in global_array['All']['dates']):
				global_array['All']['dates'][column] = 0
			global_array['All']['dates'][column] = global_array['All']['dates'][column] + value['All']['dates'][column]

	data['Global'] = global_array
	return data

def lambda_handler(event, context):
	proccessCountries()
	data = proccessMain(event['queryStringParameters']['status'].lower())

	try:
		return_data = data[event['queryStringParameters']['country']]

	except:
		return_data = data  # or whatever
	
	return {
		'statusCode': 200,
		'body': json.dumps(return_data)
	}
