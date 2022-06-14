from django.contrib import admin

from WeatherApp.models import City


class CityAdmin(admin.ModelAdmin):
    temp = []
    # Add each field into admin class
    for i in City._meta.fields:
        temp.append(i.__str__().split('.')[-1])
    list_display = tuple(temp)


admin.site.register(City, CityAdmin)