from django.test import TestCase
from WeatherApp.models import City
from WeatherApp.apis import OpenWeatherMapAPI


class APITestCase(TestCase):

    def setUp(self) -> None:
        self.city = City.objects.create(name='Test', coord_lat=34.50, coord_lon=45, wid=1, state='OK', country='CA')

    def test_current_weather_response(self):
        resp = OpenWeatherMapAPI.get_current_weather_data(self.city.coord_lat, self.city.coord_lon, 'not_standard')
        self.assertIn('temp', resp['main'].keys())

    def test_forecast_weather_response(self):
        resp = OpenWeatherMapAPI.get_forecast_data(self.city.coord_lat, self.city.coord_lon, 'not_standard')
        self.assertIn('temp', resp['list'][10]['main'])

    def test_api_wrong_city(self):
        resp = OpenWeatherMapAPI.get_current_weather_data(None, None, None)
        self.assertIn('error', resp.keys())
