from django.test import TestCase
from rest_framework.test import APIClient
from api.models import WeatherData, YieldData, WeatherAnalysis

# parent class to reuse as much code as possible
#   many of the get requests are checking the same things and edge cases
class ParentViewSetTests:
    def setUp(self):
        self.client = APIClient()

    def test_get_all_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], self.num_test_rows)

    def test_reject_unallowed_methods(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, 405)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 405)

    def test_check_station_filter(self):
        row = self.model(**self.test_row_data)
        row.save()
        self.test_row_data["id"] = row.id
        response = self.client.get(
            self.url, {"weather_station": self.test_row_data["weather_station"]}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0], self.test_row_data)

    def test_check_year_filter(self):
        row = self.model(**self.test_row_data)
        row.save()
        self.test_row_data["id"] = row.id
        response = self.client.get(self.url, {"year": self.test_row_data["year"]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0], self.test_row_data)


class WeatherDataViewSetTests(TestCase, ParentViewSetTests):
    @classmethod
    def setUpTestData(cls):
        cls.num_test_rows = 5
        cls.url = "/api/weather"
        cls.model = WeatherData
        cls.test_row_data = {
            "weather_station": "randome",
            "date": "2022-04-04",
            "max_temp_of_day": 222222222,
            "min_temp_of_day": 123456789,
            "precipitation_of_day": 444444444,
        }
        for i in range(1, cls.num_test_rows + 1):
            row = cls.model(weather_station=f"test{i}", date=f"1985-01-0{i}")
            row.save()

    def test_check_date_filter(self):
        row = self.model(**self.test_row_data)
        row.save()
        self.test_row_data["id"] = row.id
        response = self.client.get(self.url, {"date": self.test_row_data["date"]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0], self.test_row_data)

    def test_check_year_filter(self):
        pass


class YieldDataViewSetTests(TestCase, ParentViewSetTests):
    @classmethod
    def setUpTestData(cls):
        cls.num_test_rows = 5
        cls.url = "/api/yield"
        cls.model = YieldData
        cls.test_row_data = {
            "year": 2022,
            "total_harvested_grain": 222222222,
        }
        for i in range(1, cls.num_test_rows + 1):
            row = cls.model(year=f"201{i}", total_harvested_grain=12)
            row.save()

    def test_check_station_filter(self):
        pass


class WeatherAnalysisViewSetTests(TestCase, ParentViewSetTests):
    @classmethod
    def setUpTestData(cls):
        cls.num_test_rows = 5
        cls.url = "/api/weather/stats/"
        cls.model = WeatherAnalysis
        cls.test_row_data = {
            "weather_station": "random_asdfasdfklj",
            "year": 2021,
            "avg_max_temp_of_year": 222222222.0,
            "avg_min_temp_of_year": 123456789.0,
            "total_precipitation_of_year": 444444444,
        }
        for i in range(1, cls.num_test_rows + 1):
            row = cls.model(year=f"201{i}", weather_station=f"test{i}")
            row.save()
