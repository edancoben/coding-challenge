from pyexpat import model
from django.db import models

# Create your models here.

# unique constraint in place so we don't create duplicates
# weather station is expected to be 11 chars from all txt file names
# both date and weather station cannot be null
# max_temp, mmin_temp, total_prec are all ints
class WeatherData(models.Model):
    class Meta:
        db_table = "weather_data"
        constraints = [
            models.UniqueConstraint(
                fields=["weather_station", "date"], name="unique_date_per_station"
            )
        ]

    weather_station = models.CharField(max_length=11)
    date = models.DateField()
    max_temp_of_day = models.IntegerField(null=True)
    min_temp_of_day = models.IntegerField(null=True)
    precipitation_of_day = models.IntegerField(null=True)


# year is unique for as total exists for only one year
# total harvested grain is int like in file
class YieldData(models.Model):
    class Meta:
        db_table = "yield_data"

    year = models.IntegerField(unique=True)
    total_harvested_grain = models.IntegerField()


# for every year for every station is in constraint
# same concepts as WeatherData for station/year
# rest of the fields are Float types to have more data that seemed relevante
#   ie 20 deg celsius seemed like a significant amount less info thant 20.3 avg deg celsius
#   when comparing years
# also nullable for statistics that cannot be calculated
class WeatherAnalysis(models.Model):
    class Meta:
        db_table = "weather_analysis"
        constraints = [
            models.UniqueConstraint(
                fields=["weather_station", "year"], name="unique_year_per_station"
            )
        ]

    weather_station = models.CharField(max_length=11)
    year = models.IntegerField()
    avg_max_temp_of_year = models.FloatField(null=True)
    avg_min_temp_of_year = models.FloatField(null=True)
    total_precipitation_of_year = models.IntegerField(null=True)
