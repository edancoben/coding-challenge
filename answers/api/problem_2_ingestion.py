from os import listdir
from os.path import isfile, join, basename

from .models import WeatherData, YieldData
from pathlib import Path
import pandas as pd
from pandas import DataFrame


class IngestDataParent:
    def __init__(self) -> None:
        pass

    def run(self) -> None:
        file_paths = self._get_all_data_file_paths()
        for file_path in file_paths:
            df = self._load_data(file_path)
            df = self._clean_data(df)
            # print(df)
            # self._save_data_in_db(df)

            # print(df)
        print(df)
        # for file path in file paths
        # load into df
        # add any additional cols
        # clean change -9999 to null
        # save df into db one row at a time
        pass

    def _get_all_data_file_paths(self) -> list[str]:
        parent_path = Path(__file__).parents[2]
        data_path = join(parent_path, self.data_dir)
        file_paths = [
            join(data_path, f) for f in listdir(data_path) if isfile(join(data_path, f))
        ]
        return file_paths

    def _load_data(self, file_path: str) -> DataFrame:
        df = pd.read_csv(file_path, sep="\t", header=None, names=self.col_names)
        df = self._add_additional_cols(df=df, file_path=file_path)
        return df

    def _add_additional_cols(self, df: DataFrame, file_path: str = None) -> DataFrame:
        return df

    def _clean_data(self, df: DataFrame) -> DataFrame:
        return df


class IngestWeatherData(IngestDataParent):
    def __init__(self, data_dir: str) -> None:
        self.data_model = WeatherData
        self.data_dir = data_dir
        self.col_names = [
            "date",
            "max_temp_of_day",
            "min_temp_of_day",
            "precipitation_of_day",
        ]
        super().__init__()

    def _add_additional_cols(self, df: DataFrame, file_path: str) -> DataFrame:
        file_name = basename(file_path)
        weather_station = file_name.split(".txt")[0]
        return df.assign(weather_station=weather_station)

    def _clean_data(self, df: DataFrame) -> DataFrame:
        df["date"] = df["date"].apply(self._format_date)
        return df

    def _format_date(self, date: int) -> str:
        date = str(date)
        date = date[:4] + "-" + date[4:6] + "-" + date[6:]
        return date


class IngestYieldData(IngestDataParent):
    def __init__(self, data_dir: str) -> None:
        self.data_model = YieldData
        self.data_dir = data_dir
        self.col_names = ["year", "total_harvested_grain"]
        super().__init__()
