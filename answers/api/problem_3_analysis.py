from .models import WeatherData, WeatherAnalysis
from django.db.models import Sum, Avg, IntegerField
from django.db.models.functions import Round, ExtractYear, Cast
import logging

logger = logging.getLogger(__name__)

# TODO proper logging
def analyze_weather():
    logger.info("analyzing weather")
    rows = (
        WeatherData.objects.all()
        .values("weather_station")
        .annotate(
            year=Cast(ExtractYear("date"), output_field=IntegerField()),
            # divide by 10 to convert from 10ths of deg cel to deg cel
            avg_max_temp_of_year=Round(Avg("max_temp_of_day") / 10, precision=1),
            avg_min_temp_of_year=Round(Avg("min_temp_of_day") / 10, precision=1),
            # divide by 100 to convert from 10ths of mm to mm and then from mm to cm
            total_precipitation_of_year=Round(Sum("precipitation_of_day") / 100),
        )
        .order_by("weather_station", "year")
    )

    batch = [WeatherAnalysis(**row) for row in rows]

    WeatherAnalysis.objects.bulk_create(batch)
    logger.info("Num rows saved in WeatherAnalysis:", len(batch))
