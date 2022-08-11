from urllib import response
from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient
from api.views import WeatherDataViewSet, WeatherAnalysisViewSet, YieldDataViewSet
from api.serializers import (
    WeatherAnalysisSerializer,
    WeatherDataSerializer,
    YieldDataSerializer,
)
from api.models import WeatherData


class WeatherDataViewSetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = "/api/weather/"
        # cls.view_set = WeatherDataViewSet
        # cls.expected_serializer = WeatherDataSerializer

    def setUp(self):
        self.client = APIClient()
        # self.client.force_authenticate()

    def test_get_data(self):
        row = WeatherData(weather_station="test", date="1985-01-01")
        row.save()
        row = WeatherData(weather_station="test2", date="1986-01-01")
        row.save()
        response = self.client.get(
            self.url, {"weather_station": "test", "date": "1985-01-01"}
        )
        # response = self.client.get(self.url)
        print(response.json())

    def test_reject_unallowed_methods(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, 405)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 405)
