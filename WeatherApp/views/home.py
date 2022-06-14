import logging

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from WeatherApp.apis import OpenWeatherMapAPI
from WeatherApp.models import City
from WeatherApp.views.utils import *


def home(request):
    # Main view of application
    # If city_id is given and unit info given, assign as variable
    context = {}
    if 'city_id' in request.GET.keys():
        city_id = request.GET['city_id']
        if 'unit' in request.GET.keys():
            unit = request.GET['unit']
        else:
            unit = 'standard'
    else:
        # Set city_id and unit as COOKIE
        city_id = request.COOKIES.get('weather_app_city_id')
        unit = request.COOKIES.get('weather_app_unit_type')

    if city_id is not None:
        # If city id is available, retrieve weather info as context
        context = get_weather_info(city_id, unit)

    # Rendering object will be returned after cookie set.
    response = render(request, 'pages/home.html', context)

    # If city_id is available, set city_id and unit as cookie for a week.
    if city_id is not None:
        set_cookie(response, 'weather_app_city_id', city_id, 7)
        set_cookie(response, 'weather_app_unit_type', unit, 7)

    return response


def get_weather_info(city_id, unit):
    # Check if city exist, else return error.
    # Error text will be displayed on view.
    try:
        city = City.objects.get(wid=int(city_id))
    except ObjectDoesNotExist:
        logging.error(f'City object does not exist! city_id = {city_id}, unit = {unit}')
        return {'error': True, 'error_text': f'City object with {city_id} ID, does not exist!'}

    # Retrieve current weather data via API
    current_weather_response = OpenWeatherMapAPI.get_current_weather_data(
        city.coord_lat,
        city.coord_lon,
        unit
    )

    # If error occurred return error object
    if 'error' in current_weather_response.keys():
        logging.error(f'Error occurred on Current Weather Response -> reason = {current_weather_response["error_text"]}')
        return {'error': True, 'error_text': current_weather_response['error_text']}

    # Retrieve weather forecast data via API
    forecast_weather_response = OpenWeatherMapAPI.get_forecast_data(
        city.coord_lat,
        city.coord_lon,
        unit
    )
    # If error occurred return error object
    if 'error' in forecast_weather_response.keys():
        logging.error(f'Error occurred on Forecast Weather Response -> reason = {forecast_weather_response["error_text"]}')
        return {'error': True, 'error_text': forecast_weather_response['error_text']}

    # Retrieve units data from API class
    units = OpenWeatherMapAPI.get_unit_params(unit)

    # Create context object
    result = {
        'current_weather': current_weather_response,
        'forecast_weather': forecast_weather_response,
        'city_name': city.name,
        'units': units,
        'unit': unit
    }

    return result
