# Dear COVID-19,
# ....................../´¯/)
# ....................,/¯../
# .................../..../
# ............./´¯/'...'/´¯¯`·¸
# ........../'/.../..../......./¨¯\
# ........('(...´...´.... ¯~/'...')
# .........\.................'...../
# ..........''...\.......... _.·´
# ............\..............(
# ..............\.............\...

import json
import csv
from requests import get
from contextlib import closing
import codecs
import datetime
import os
from get_countries import proccessCountries

country_array = proccessCountries()

def getRowsFromCsv(url):
	# with open(get(url, stream=True)) as r:
	# 	reader = csv.DictReader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
	# 	rows = list(reader)
	with closing(get(url, stream=True)) as r:
		reader = csv.DictReader(codecs.iterdecode(r.iter_lines(), 'utf-8-sig'))
		rows = list(reader)
	return rows
	
def proccessMain(status):
	url ='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_'+status+'_global.csv'
	data = {}
	converted_dates = {}
	if not os.path.isfile('/tmp/history-'+status+'.json'):
		rows = getRowsFromCsv(url)
		for row in rows:
			area_sum = 0
	
			if (row['Country/Region'] not in data):
				data[row['Country/Region']] = {}
				data[row['Country/Region']]['All'] = {}
				if(row['Country/Region'] in country_array):
					for key in country_array[row['Country/Region']]:
						data[row['Country/Region']]['All'][key] = country_array[row['Country/Region']][key]
				
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
	
					data[row['Country/Region']][row['Province/State']]['dates'][column]  = int(float(row[original_column]))
	
		global_array = {'All': {'population': country_array['Global']['population'], 'dates': {}}}
	
		for (key, value) in data.items():
	
			for column in value['All']['dates']:
				if (column not in global_array['All']['dates']):
					global_array['All']['dates'][column] = 0
				global_array['All']['dates'][column] = global_array['All']['dates'][column] + value['All']['dates'][column]
	
		data['Global'] = global_array
		with open('/tmp/history-'+status+'.json', 'a+') as file:
				file.write(json.dumps(data))
	else:
		with open('/tmp/history-'+status+'.json') as r:
			data = json.load(r)
	return data

def proccessLatest():
	recent_data = {}
	latest_url ='https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_1.csv'
	country_array['Global']['confirmed'] = 0
	country_array['Global']['recovered'] = 0
	country_array['Global']['deaths'] = 0
	
	recent_rows = getRowsFromCsv(latest_url)

	for row in recent_rows:

		
		# yield [unicode(cell, 'utf-8') for cell in row]

		if ('Last_Update' not in row or row['Last_Update'] == ''):
			continue

		if (row['Country_Region'] not in recent_data):
			recent_data[row['Country_Region']] = {}
			recent_data[row['Country_Region']]['All'] = {}
			recent_data[row['Country_Region']]['All']['confirmed'] = 0
			recent_data[row['Country_Region']]['All']['recovered'] = 0
			recent_data[row['Country_Region']]['All']['deaths'] = 0
		
		country_array['Global']['confirmed'] = country_array['Global']['confirmed'] + int(row['Confirmed'])
		country_array['Global']['deaths'] = country_array['Global']['deaths'] + int(row['Deaths'])
		country_array['Global']['recovered'] = country_array['Global']['recovered'] + int(row['Recovered'])

		if(row['Country_Region'] in country_array):
			for key in country_array[row['Country_Region']]:
				recent_data[row['Country_Region']]['All'][key] = country_array[row['Country_Region']][key]
	
		if row['Province_State'] == '':
			row['Province_State'] = "All"
	
		if (row['Province_State'] not in recent_data[row['Country_Region']]):
			recent_data[row['Country_Region']][row['Province_State']] = {}
			
		if row['Province_State'] == row['Country_Region']:
			recent_data[row['Country_Region']]['All']['lat'] = row['Lat']
			recent_data[row['Country_Region']]['All']['long'] = row['Long_']
	
		recent_data[row['Country_Region']][row['Province_State']]['lat'] = row['Lat']
		recent_data[row['Country_Region']][row['Province_State']]['long'] = row['Long_']
	
		recent_data[row['Country_Region']][row['Province_State']]['confirmed'] = int(row['Confirmed'])
		recent_data[row['Country_Region']][row['Province_State']]['recovered'] = int(row['Recovered'])
		recent_data[row['Country_Region']][row['Province_State']]['deaths'] = int(row['Deaths'])
		recent_data[row['Country_Region']][row['Province_State']]['updated'] = row['Last_Update']
		# recent_data[row['Country_Region']][row['Province_State']]['updated'] = datetime.datetime.strptime(row['Last_Update'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%F')
	
		if(row['Province_State'] != 'All'):
			recent_data[row['Country_Region']]['All']['confirmed'] = int(recent_data[row['Country_Region']][row['Province_State']]['confirmed']) + int(recent_data[row['Country_Region']]['All']['confirmed'])
			recent_data[row['Country_Region']]['All']['recovered'] = int(recent_data[row['Country_Region']][row['Province_State']]['recovered']) + int(recent_data[row['Country_Region']]['All']['recovered'])
			recent_data[row['Country_Region']]['All']['deaths'] = int(recent_data[row['Country_Region']][row['Province_State']]['deaths']) + int(recent_data[row['Country_Region']]['All']['deaths'])
	
	global_array = {'All': {'population': country_array['Global']['population'], 'confirmed': country_array['Global']['confirmed'], 'recovered': country_array['Global']['recovered'], 'deaths': country_array['Global']['deaths']}}

	recent_data['Global'] = global_array
	
	return recent_data

def proccessVaccinated():
    vaccine_data = {}
    latest_url ='https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/vaccine_data_global.csv'
    country_array['Global']['administered'] = 0
    country_array['Global']['people_vaccinated'] = 0
    country_array['Global']['people_partially_vaccinated'] = 0
    if not os.path.isfile('/tmp/vaccines.json'):
        recent_rows = getRowsFromCsv(latest_url)

        for row in recent_rows:

            # yield [unicode(cell, 'utf-8') for cell in row]

            if ('Date' not in row or row['Date'] == ''):
                continue

            if (row['Country_Region'] not in vaccine_data):
                vaccine_data[row['Country_Region']] = {}
                vaccine_data[row['Country_Region']]['All'] = {}
                vaccine_data[row['Country_Region']]['All']['administered'] = 0
                vaccine_data[row['Country_Region']]['All']['people_vaccinated'] = 0
                vaccine_data[row['Country_Region']]['All']['people_partially_vaccinated'] = 0
            
            country_array['Global']['administered'] = (country_array['Global']['administered'] + int(float(row['Doses_admin']))) if row['Doses_admin'] else 0
            country_array['Global']['people_partially_vaccinated'] = country_array['Global']['people_partially_vaccinated'] + int(float(row['People_partially_vaccinated'])) if row['People_partially_vaccinated'].strip() != "" else 0
            country_array['Global']['people_vaccinated'] = country_array['Global']['people_vaccinated'] + int(float(row['People_fully_vaccinated'])) if row['People_fully_vaccinated'].strip() != "" else 0

            if(row['Country_Region'] in country_array):
                for key in country_array[row['Country_Region']]:
                    vaccine_data[row['Country_Region']]['All'][key] = country_array[row['Country_Region']][key]
        
            if row['Province_State'] == '':
            	row['Province_State'] = "All"
        
            if (row['Province_State'] not in vaccine_data[row['Country_Region']]):
                vaccine_data[row['Country_Region']][row['Province_State']] = {}
            
            vaccine_data[row['Country_Region']][row['Province_State']]['administered'] = int(float(row['Doses_admin'])) if row['Doses_admin'] else 0
            vaccine_data[row['Country_Region']][row['Province_State']]['people_vaccinated'] = int(float(row['People_fully_vaccinated'])) if row['People_fully_vaccinated'].strip() != "" else 0
            vaccine_data[row['Country_Region']][row['Province_State']]['people_partially_vaccinated'] = int(float(row['People_partially_vaccinated'])) if row['People_partially_vaccinated'].strip() != "" else 0
            #vaccine_data[row['Country_Region']][row['Province_State']]['updated'] = row['Date']
            vaccine_data[row['Country_Region']][row['Province_State']]['updated'] = datetime.datetime.strptime(row['Date'], '%Y-%m-%d').strftime('%Y/%m/%d %H:%M:%S+00')
        
        global_array = {'All': {'population': country_array['Global']['population'], 'administered': country_array['Global']['administered'], 'people_vaccinated': country_array['Global']['people_vaccinated'], 'people_partially_vaccinated': country_array['Global']['people_partially_vaccinated']}}

        vaccine_data['Global'] = global_array

    else:
        with open('/tmp/vaccines.json') as r:
            vaccine_data = json.load(r)
    return vaccine_data
    
def lambda_handler(event, context):
	
	return_data = None

	if(event['resource'] == '/history'):
		data = proccessMain(event['queryStringParameters']['status'].lower())

	elif(event['resource'] == '/cases'):
		data = proccessLatest()
	
	elif(event['resource'] == '/vaccines'):
		data = proccessVaccinated()
	
	try:
		if ('ab' in event['queryStringParameters']):
			return_data = list(filter(lambda x: 'abbreviation' in x['All'] and event['queryStringParameters']['ab'].upper() == x['All']['abbreviation'], data.values()))[0]
		elif ('continent' in event['queryStringParameters']):
			return_data = {k:v for k,v in data.items() if 'continent' in v['All'] and v['All']['continent'].upper() == event['queryStringParameters']['continent'].upper()}
		else:
			return_data = data[event['queryStringParameters']['country']]
	
	except:
		return_data = data
	
	return {
		'statusCode': 200,
		'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
		'body': json.dumps(return_data)
	}
