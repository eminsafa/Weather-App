import json
import logging

import requests

from WeatherApp.interface import open_weather_map_interface
from django.conf import settings


class OpenWeatherMapAPI:
    """
    This class stores api connection methods for OpenWeatherMap.Org
    Functions are developed as class methods.
    """

    API_KEY = settings.OPEN_WEATHER_MAP_API_KEY
    HOST = 'https://api.openweathermap.org/data/2.5/'
    # These units are used in the templates section.
    UNITS = {
        'standard': {
            'temp': ['Kelvin', 'K'],
            'humidity': ['Percent', '%'],
            'pressure': ['hPa', 'hPa'],
            'speed': ['meter/sec', 'm/s']
        },
        'metric': {
            'temp': ['Celsius', '°C'],
            'humidity': ['Percent', '%'],
            'pressure': ['hPa', 'hPa'],
            'speed': ['meter/sec', 'm/s']
        },
        'imperial': {
            'temp': ['Fahrenheit', '°F'],
            'humidity': ['Percent', '%'],
            'pressure': ['hPa', 'hPa'],
            'speed': ['miles/hour', 'mph']
        }
    }

    @classmethod
    def get_unit_params(cls, unit_name) -> dict:
        # If the unit name is invalid, the default unit (standard) is returned.
        if unit_name in cls.UNITS.keys():
            return cls.UNITS[unit_name]
        return cls.UNITS['standard']

    @classmethod
    @open_weather_map_interface
    def get_current_weather_data(cls, lat: float, lon: float, units: str = 'standard') -> dict:
        # Current Weather API
        # Details available on https://openweathermap.org/current
        # Response will be modified by @open_weather_map_interface
        params = f'lat={lat}&lon={lon}&units={units}&appid={cls.API_KEY}'
        return cls.request_and_parse(cls.HOST + 'weather?' + params)

    @classmethod
    @open_weather_map_interface
    def get_forecast_data(cls, lat: float, lon: float, units: str = 'standard') -> dict:
        # 5-Day Weather Forecast API
        # Details available on https://openweathermap.org/forecast5
        # Response will be modified by @open_weather_map_interface
        params = f'lat={lat}&lon={lon}&units={units}&appid={cls.API_KEY}'
        return cls.request_and_parse(cls.HOST + 'forecast?' + params)

    @classmethod
    def request_and_parse(cls, path) -> dict:
        try:
            raw_response = requests.get(path)
            response_text = raw_response.text
        except Exception as e:
            logging.error(f'Request error on path: {path}, response: {e}')
            return {'error': True, 'error_text': 'Request error'}

        # Check status code if success
        if raw_response.status_code != 200:
            logging.error(f'Request error on path: {path}, response: {response_text}')
            return {'error': True, 'error_text': f'Request code error.'}

        try:
            # Response string to dictionary
            response = json.loads(raw_response.text)
        except ValueError:
            logging.error(f'JSON decode error on path: {path}')
            return {'error': True, 'error_text': 'JSON decode error'}
        else:
            return response
