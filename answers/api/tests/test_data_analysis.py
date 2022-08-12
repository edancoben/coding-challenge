from audioop import avg
from django.test import TestCase
from django.core.management import call_command
from pathlib import Path
from os.path import dirname
import pandas as pd
from api.models import WeatherData, WeatherAnalysis


class WeatherDataAnalysisTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.col_names = [
            "date",
            "max_temp_of_day",
            "min_temp_of_day",
            "precipitation_of_day",
            "weather_station",
        ]
        file_path = f"{dirname(Path(__file__))}/test_data/wx_test_data.csv"
        cls.df = pd.read_csv(file_path, sep=",", header=None, names=cls.col_names)

    def setUp(self):
        self.assertEqual(len(WeatherAnalysis.objects.all()), 0)

    def test_analyze_weather_stats_query(self):
        self.assertEqual(len(WeatherData.objects.all()), 0)
        rows = self.df.to_dict(orient="records")
        batch = [WeatherData(**row) for row in rows]
        WeatherData.objects.bulk_create(batch, batch_size=len(batch))
        self.assertEqual(len(WeatherData.objects.all()), len(self.df.index))
        # 2 weather stations each with data in a 2 year span in test data
        expected_values = self._cal_expected_stats()
        call_command("analyze_weather")
        self.assertEqual(len(WeatherAnalysis.objects.all()), len(expected_values))
        actual_values = list(
            WeatherAnalysis.objects.values(
                "weather_station",
                "year",
                "avg_max_temp_of_year",
                "avg_min_temp_of_year",
                "total_precipitation_of_year",
            )
        )
        self.assertEqual(actual_values, expected_values)

    def _cal_expected_stats(self):
        df = self.df

        df["year"] = pd.DatetimeIndex(df["date"]).year
        # to
        avg_df = df.groupby(["weather_station", "year"], as_index=False).mean().round(1)
        sum_df = df.groupby(["weather_station", "year"], as_index=False)[
            "precipitation_of_day"
        ].sum()
        avg_df["precipitation_of_day"] = sum_df["precipitation_of_day"]

        avg_df["max_temp_of_day"] = avg_df["max_temp_of_day"].div(10).round(1)
        avg_df["min_temp_of_day"] = avg_df["min_temp_of_day"].div(10).round(1)
        avg_df["precipitation_of_day"] = avg_df["precipitation_of_day"].div(100).round()
        avg_df.rename(
            columns={
                "max_temp_of_day": "avg_max_temp_of_year",
                "min_temp_of_day": "avg_min_temp_of_year",
                "precipitation_of_day": "total_precipitation_of_year",
            },
            inplace=True,
        )
        return avg_df.to_dict(orient="records")
