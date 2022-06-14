from django.test import RequestFactory, TestCase

from WeatherApp.models import City
from WeatherApp.views import home, city_search


class ViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_wrong_city_id(self):
        request = self.factory.get('')
        # Request not existing city
        request.GET = {'city_id': -1}
        response = home(request)
        # Should display error
        self.assertIn(b'ERROR: City object with -1 ID, does not exist!', response.content)

    def test_search_view(self):
        # Create sample city
        city = City.objects.create(name='Sample City Name', coord_lat=34.50, coord_lon=45, wid=1, state='OK', country='CA')
        request = self.factory.get('')
        # Call search endpoint with a few letter of city name
        request.GET = {'search_query': city.name[:2]}
        response = city_search(request)
        # Check if city name exist in the content
        self.assertIn(city.name.encode(), response.content)
