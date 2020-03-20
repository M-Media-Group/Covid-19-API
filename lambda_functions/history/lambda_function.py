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

countries_url ='https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json'

with closing(get(countries_url, stream=True)) as r:
	countries = r.json()

for country in countries:
	# break
	if(country['population'] is not None):
		global_population = global_population + int(country['population'])
	
	if(country['country'] not in country_array):
		country_array[country['country']] = country['population']

latest_url ='https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_1.csv'

with closing(get(latest_url, stream=True)) as r:
	reader = csv.DictReader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
	recent_rows = list(reader)

for row in recent_rows:
	if (row['Country_Region'] not in recent_data):
		recent_data[row['Country_Region']] = {}
		recent_data[row['Country_Region']]['All'] = {}
		recent_data[row['Country_Region']]['All']['dates'] = {}

	if row['Province_State'] == '':
		row['Province_State'] = "All"

	if (row['Province_State'] not in recent_data[row['Country_Region']]):
		recent_data[row['Country_Region']][row['Province_State']] = {}

	recent_data[row['Country_Region']][row['Province_State']]['confirmed'] = int(row['Confirmed'])
	recent_data[row['Country_Region']][row['Province_State']]['recovered'] = int(row['Recovered'])
	recent_data[row['Country_Region']][row['Province_State']]['deaths'] = int(row['Deaths'])
	recent_data[row['Country_Region']][row['Province_State']]['Last_Update'] = datetime.datetime.strptime(row['Last_Update'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%F')


def lambda_handler(event, context):
	data = {}

	url ='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-'+event['queryStringParameters']['status'].capitalize()+'.csv'

	with closing(get(url, stream=True)) as r:
		reader = csv.DictReader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
		rows = list(reader)
	
	for row in rows:
		area_sum = 0
		# total_collected_sum = 0
	
		if (row['Country/Region'] not in data):
			data[row['Country/Region']] = {}
			data[row['Country/Region']]['All'] = {}
			if(row['Country/Region'] in country_array):
				data[row['Country/Region']]['All']['population'] = int(country_array[row['Country/Region']])
			data[row['Country/Region']]['All']['dates'] = {}
	
		if row['Province/State'] == '':
			row['Province/State'] = "All"
	
		if (row['Province/State'] not in data[row['Country/Region']]):
			data[row['Country/Region']][row['Province/State']] = {}
		
		if row['Province/State'] == row['Country/Region']:
			data[row['Country/Region']]['All']['lat'] = row['Lat']
			data[row['Country/Region']]['All']['long'] = row['Long']
	
	
		if ('dates' not in data[row['Country/Region']][row['Province/State']]):
			data[row['Country/Region']][row['Province/State']]['dates'] = {}
		
		if (row['Country/Region'] in recent_data and row['Province/State'] in recent_data[row['Country/Region']]):
			data[row['Country/Region']][row['Province/State']]['lat'] = row['Lat']
			data[row['Country/Region']][row['Province/State']]['long'] = row['Long']
			if ('confirmed' not in data[row['Country/Region']]['All']):
				data[row['Country/Region']]['All']['confirmed'] = 0
				data[row['Country/Region']]['All']['recovered'] = 0
				data[row['Country/Region']]['All']['deaths'] = 0
	
			data[row['Country/Region']]['All']['confirmed'] = int(recent_data[row['Country/Region']][row['Province/State']]['confirmed']) + int(data[row['Country/Region']]['All']['confirmed'])
			data[row['Country/Region']]['All']['recovered'] = int(recent_data[row['Country/Region']][row['Province/State']]['recovered']) + int(data[row['Country/Region']]['All']['recovered'])
			data[row['Country/Region']]['All']['deaths'] = int(recent_data[row['Country/Region']][row['Province/State']]['deaths']) + int(data[row['Country/Region']]['All']['deaths'])
			
		if ('confirmed' not in data[row['Country/Region']][row['Province/State']]):
			if (row['Country/Region'] in recent_data and row['Province/State'] in recent_data[row['Country/Region']]):
				data[row['Country/Region']][row['Province/State']]['confirmed'] = recent_data[row['Country/Region']][row['Province/State']]['confirmed']
				data[row['Country/Region']][row['Province/State']]['recovered'] = recent_data[row['Country/Region']][row['Province/State']]['recovered']
				data[row['Country/Region']][row['Province/State']]['deaths'] = recent_data[row['Country/Region']][row['Province/State']]['deaths']
				data[row['Country/Region']][row['Province/State']]['last_update'] = recent_data[row['Country/Region']][row['Province/State']]['Last_Update']
	
			else:
				data[row['Country/Region']][row['Province/State']]['confirmed'] = 00
				data[row['Country/Region']][row['Province/State']]['recovered'] = 00
				data[row['Country/Region']][row['Province/State']]['deaths'] = 00
				data[row['Country/Region']][row['Province/State']]['last_update'] = "N/A"
	
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
	
		# data[row['Country/Region']]['total'] = area_sum
		# if total_collected_sum is 0:
		# 	continue
	global_array = {'All': {'population': global_population, 'deaths': 0, 'recovered': 0,'confirmed': 0, 'dates': {}}}

	for (key, value) in data.items():
		global_array['All']['confirmed'] = global_array['All']['confirmed'] + value['All']['confirmed']
		global_array['All']['recovered'] = global_array['All']['recovered'] + value['All']['recovered']
		global_array['All']['deaths'] = global_array['All']['deaths'] + value['All']['deaths']
		# if('population' in value['All']):
		# 	global_array['All']['population'] = global_array['All']['population'] + value['All']['population']

		for column in value['All']['dates']:
			if (column not in global_array['All']['dates']):
				global_array['All']['dates'][column] = 0
			global_array['All']['dates'][column] = global_array['All']['dates'][column] + value['All']['dates'][column]
	
	data['Global'] = global_array

	try:
		return_data = data[event['queryStringParameters']['country']]

	except:
		return_data = data  # or whatever

	return {
		'statusCode': 200,
		'body': json.dumps(return_data)
	}
