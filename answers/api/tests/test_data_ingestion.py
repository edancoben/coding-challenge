from django.test import TestCase
from api.models import WeatherData, YieldData
from api.problem_2_ingestion import IngestWeatherData, IngestYieldData
from pathlib import Path
from os.path import dirname, basename
import pandas as pd

# from os.path import isfile, join, basename

# Create your tests here.
class ParentDataIngestionTests:
    @classmethod
    def setUpTestData(cls):
        cls.test_path_dir = "test_dir"
        cls.model = WeatherData
        cls.ingestor = IngestWeatherData(cls.test_path_dir)

    def setUp(self):
        pass

    def test_get_all_data_file_paths(self):
        file_paths = self.ingestor._get_all_data_file_paths()
        expected_num_files = 2
        self.assertEqual(len(file_paths), expected_num_files)
        files = [basename(path) for path in file_paths]
        self.assertEqual(sorted(files), ["test1.txt", "test2.txt"])

    def test_clean_data(self):
        pass

    def test_save_data_in_db(self):
        pass


class IngestWeatherDataTests(TestCase, ParentDataIngestionTests):
    @classmethod
    def setUpTestData(cls):
        cls.test_path_dir = "answers/api/tests/test_data/test_dir"
        cls.test_data_file_path = "test_data/test_dir/test1.txt"
        cls.model = WeatherData
        cls.ingestor = IngestWeatherData(cls.test_path_dir)

    def test_load_data(self):
        dir = dirname(Path(__file__))
        path = f"{dir}/{self.test_data_file_path}"
        expected_df = pd.read_csv(
            path, sep="\t", header=None, names=self.ingestor.col_names
        )
        file_name = basename(path)
        weather_station = file_name.split(".txt")[0]
        expected_df = expected_df.assign(weather_station=weather_station)
        actual_df = self.ingestor._load_data(path)
        self.assertEqual(
            expected_df.to_dict(orient="records"), actual_df.to_dict(orient="records")
        )


class IngestYieldDataTests(TestCase, ParentDataIngestionTests):
    @classmethod
    def setUpTestData(cls):
        cls.test_path_dir = "answers/api/tests/test_data/test_dir"
        cls.test_data_file_path = "test_data/yld_test_data.txt"
        cls.model = YieldData
        cls.ingestor = IngestYieldData(cls.test_path_dir)

    def test_load_data(self):
        dir = dirname(Path(__file__))
        path = f"{dir}/{self.test_data_file_path}"
        expected_df = pd.read_csv(
            path, sep="\t", header=None, names=self.ingestor.col_names
        )
        actual_df = self.ingestor._load_data(path)
        self.assertEqual(
            expected_df.to_dict(orient="records"), actual_df.to_dict(orient="records")
        )
