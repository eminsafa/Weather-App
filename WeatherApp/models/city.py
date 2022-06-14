from django.db import models


class City(models.Model):
    wid = models.IntegerField(unique=True)  # Unique ID on OpenWeatherMap.Org cities list
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=2)
    coord_lat = models.FloatField(null=False)
    coord_lon = models.FloatField(null=False)

    def __str__(self):
        return self.name

