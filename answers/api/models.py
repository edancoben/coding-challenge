from pyexpat import model
from django.db import models

# Create your models here.


class WeatherData(models.Model):
    class Meta:
        db_table = "weather_data"
        unique_together = (("weather_station", "date"),)

    weather_station = models.CharField(max_length=11, primary_key=True)
    date = models.DateField()
    max_temp_of_day = models.IntegerField(null=True)
    min_temp_of_day = models.IntegerField(null=True)
    precipitation_of_day = models.IntegerField(null=True)


class YieldData(models.Model):
    class Meta:
        db_table = "yield_data"

    year = models.IntegerField(primary_key=True)
    total_harvested_grain = models.IntegerField()
