from datetime import datetime

from django.test import TestCase

from WeatherApp.interface import open_weather_map_interface


class InterfaceTestCase(TestCase):

    def test_interface_for_digit(self):
        response = self.sample_response()
        self.assertIn('new_1', response.keys())

    def test_interface_for_timestamp(self):
        response = self.sample_response()
        self.assertIn('datetime', response.keys())

    @open_weather_map_interface
    def sample_response(self):
        return {
            '1': 'data',
            'dt': datetime.timestamp(datetime.now())
        }
