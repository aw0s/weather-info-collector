#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import loads
from os import getenv

from dotenv import load_dotenv
from pony import orm as ponyorm
from requests import get

from utils import kelvin_to_celsius


load_dotenv()
API_KEY = getenv('API_KEY')


def get_api_dict(api_call: str) -> dict:
    api_dict = dict(loads(get(api_call).text))

    return api_dict


class Weather:
    def __init__(self, city: str) -> None:
        self.city = city

        self.api_call = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={API_KEY}'
        self.api_dict = get_api_dict(self.api_call)

        self.country_name = self.api_dict.get('sys').get('country')
        self.weather_description = self.api_dict.get('weather')[0].get('description')

        api_dict_main = self.api_dict.get('main')
        temperature_k = api_dict_main.get('temp')
        self.temperature_c = kelvin_to_celsius(temperature_k)
        self.min_temperature = api_dict_main.get('temp_min')
        self.max_temperature = api_dict_main.get('temp_max')

        self.pressure = api_dict_main.get('pressure')
        self.humidity = api_dict_main.get('humidity')

        self.database = ponyorm.Database()