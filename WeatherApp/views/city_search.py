import logging

from django.core.serializers import serialize
from django.shortcuts import HttpResponse

from WeatherApp.models import City


def city_search(request):
    result = "[]"
    if 'search_query' in request.GET:
        search_query = request.GET['search_query']
        if len(search_query) > 1:
            # Search for cities where the entered phrase occurs. Limited to 10 entities.
            cities = City.objects.filter(name__contains=search_query).order_by('name')[:10]
            # Serialize with just wid and name info. Coordinates and other information are hidden.
            result = serialize('json', cities, fields=['wid', 'name'])
    else:
        # If search_query not in GET objects, warn.
        logging.warning('Search Query not in request.GET')

    return HttpResponse(result, content_type='application/json')
