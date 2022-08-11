from api.serializers import (
    WeatherDataSerializer,
    YieldDataSerializer,
    WeatherAnalysisSerializer,
)
from rest_framework import viewsets
from .models import WeatherData, WeatherAnalysis, YieldData


class WeatherDataViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = WeatherDataSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        date = query_params.get("date")
        weather_station = query_params.get("weather_station")

        kwargs = {}
        if date:
            kwargs["date"] = date
        if weather_station:
            kwargs["weather_station"] = weather_station

        queryset = WeatherData.objects.filter(**kwargs).order_by("id")

        return queryset


class YieldDataViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = YieldDataSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        year = query_params.get("year")

        kwargs = {}
        if year:
            kwargs["year"] = year

        queryset = YieldData.objects.filter(**kwargs).order_by("id")

        return queryset


class WeatherAnalysisViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = WeatherAnalysisSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        year = query_params.get("year")
        weather_station = query_params.get("weather_station")

        kwargs = {}
        if year:
            kwargs["year"] = year
        if weather_station:
            kwargs["weather_station"] = weather_station

        queryset = WeatherAnalysis.objects.filter(**kwargs).order_by("id")

        return queryset
