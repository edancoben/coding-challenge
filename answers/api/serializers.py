from .models import WeatherData, WeatherAnalysis, YieldData
from rest_framework import serializers


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = [
            "id",
            "weather_station",
            "date",
            "max_temp_of_day",
            "min_temp_of_day",
            "precipitation_of_day",
        ]


class YieldDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldData
        fields = [
            "year",
            "total_harvested_grain",
        ]


class WeatherAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherAnalysis
        fields = [
            "id",
            "weather_station",
            "year",
            "avg_max_temp_of_year",
            "avg_min_temp_of_year",
            "total_precipitation_of_year",
        ]
