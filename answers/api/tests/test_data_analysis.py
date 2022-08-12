from django.test import TestCase
from api.models import WeatherAnalysis
from django.core.management import call_command
from pathlib import Path
from os.path import dirname
import pandas as pd


class WeatherDataAnalysisTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ingest data from test path
        cls.col_names = [
            "date",
            "max_temp_of_day",
            "min_temp_of_day",
            "precipitation_of_day",
        ]
        stations = ["USC00110072", "USC00110187"]
        path = f"{dirname(Path(__file__))}/test_data/wx_test_data"
        for station in stations:
            file_path = f"{path}/{station}"
            df = pd.read_csv(file_path, sep="\t", header=None, names=cls.col_names)
        # df = self._add_additional_cols(df=df, file_path=file_path)
        pass

    def setUp(self):
        self.assertEqual(len(WeatherAnalysis.objects.all()), 0)

    def test_analyze_weather_stats_query(self):
        # call_command("analyze_weather")
        dirname(Path(__file__))
        pass
