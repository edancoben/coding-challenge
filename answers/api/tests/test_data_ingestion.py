from django.test import TestCase
from api.models import WeatherData, YieldData

# Create your tests here.
class ParentDataIngestionTests:
    def setUp(self):
        pass


class IngestWeatherDataTests(TestCase, ParentDataIngestionTests):
    @classmethod
    def setUpTestData(cls):
        cls.model = WeatherData


class IngestYieldDataTests(TestCase, ParentDataIngestionTests):
    @classmethod
    def setUpTestData(cls):
        cls.model = YieldData
