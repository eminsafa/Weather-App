import json
import logging

import requests

from WeatherApp.interface import open_weather_map_interface


class OpenWeatherMapAPI:
    """
    This class stores api connection methods for OpenWeatherMap.Org
    Functions are developed as class methods.
    """

    API_KEY = 'efa58fb098b2a9f881069b410ca23df3'
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
        raw_response = requests.get(path)

        # Check status code if success
        if raw_response.status_code != 200:
            logging.error(f'Request error on path: {path}')
            return {'error': True, 'error_text': 'Request error'}

        try:
            # Response string to dictionary
            response = json.loads(raw_response.text)
        except ValueError:
            logging.error(f'JSON decode error on path: {path}')
            return {'error': True, 'error_text': 'JSON decode error'}
        else:
            return response
