from django.shortcuts import render
from rest_framework import viewsets
from .models import WeatherData, WeatherAnalysis, YieldData
from rest_framework.response import Response

# TODO data should be paginated
class WeatherViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = WeatherData

    def get_queryset(self):
        query_params = self.request.query_params
        date = query_params.get("date")
        weather_station = query_params.get("weather_station")

        kwargs = {}
        if date:
            kwargs["date"] = date
        if weather_station:
            kwargs["weather_station"] = weather_station

        queryset = WeatherData.objects.filter(**kwargs)
