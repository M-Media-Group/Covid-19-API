import os
from contextlib import closing
from requests import get
import json
from util.helpers.constants import COUNTRIES_URL


def get_countries() -> dict:
    """
    get countries data from url or from local folder
    """
    countries_array = {}
    countries_array["Global"] = {}
    countries_array["Global"]["population"] = 0

    if os.path.isfile("/tmp/countries.json"):
        with open("/tmp/countries.json") as file:
            countries_data = json.load(file)
    else:
        with closing(get(COUNTRIES_URL, stream=True)) as response:
            countries_data = response.json()

    for country_data in countries_data:
        if country_data["population"]:
            countries_array["Global"]["population"] = countries_array["Global"][
                "population"
            ] + int(country_data["population"])

        if country_data["country"] not in countries_array:
            countries_array[country_data["country"]] = {}
            for (key, value) in country_data.items():
                if str(value).isdigit():
                    countries_array[country_data["country"]][key] = int(value)
                else:
                    countries_array[country_data["country"]][key] = value

    return countries_array
