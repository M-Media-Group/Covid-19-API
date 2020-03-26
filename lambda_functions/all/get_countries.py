import os
from contextlib import closing
from requests import get
import json


def proccessCountries():
    country_array = {}
    country_array['Global'] = {}
    country_array['Global']['population'] = 0

    countries = None
    countries_url = 'https://raw.githubusercontent.com/M-Media-Group/country-json/master/src/countries-master.json'

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
        if (country['population'] is not None):
            country_array['Global']['population'] = country_array['Global'][
                'population'] + int(country['population'])

        if (country['country'] not in country_array):
            country_array[country['country']] = {}
            for (key, value) in country.items():
                if (str(value).isdigit()):
                    country_array[country['country']][key] = int(value)
                else:
                    country_array[country['country']][key] = value
    return country_array
