from pyexpat import model
from django.db import models

# Create your models here.


class WeatherData(models.Model):
    class Meta:
        db_table = "weather_data"
        # unique_together = (("weather_station", "date"),)
        constraints = [
            models.UniqueConstraint(
                fields=["weather_station", "date"],
                name="unique_date_per_station",
            )
        ]

    weather_station = models.CharField(max_length=11)
    date = models.DateField()
    max_temp_of_day = models.IntegerField(null=True)
    min_temp_of_day = models.IntegerField(null=True)
    precipitation_of_day = models.IntegerField(null=True)


class YieldData(models.Model):
    class Meta:
        db_table = "yield_data"

    year = models.IntegerField(primary_key=True)
    total_harvested_grain = models.IntegerField()
