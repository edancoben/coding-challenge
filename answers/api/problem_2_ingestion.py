from os import listdir
from os.path import isfile, join, basename

from .models import WeatherData, YieldData
from pathlib import Path
import pandas as pd
from pandas import DataFrame
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine


class IngestDataParent:
    def __init__(self) -> None:
        pass

    def run(self) -> None:
        total_rows_saved = 0
        file_paths = self._get_all_data_file_paths()
        for file_path in file_paths:
            df = self._load_data(file_path)
            df = self._clean_data(df)
            num_rows_saved = self._save_data_in_db(df)
            total_rows_saved += num_rows_saved
            # print(df)
        # print(df)
        print("total_rows_saved:", total_rows_saved)

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

    def _save_data_in_db(self, df: DataFrame) -> int:
        num_rows_saved = 0
        model = self.data_model
        engine = create_engine("sqlite:///db.sqlite3")
        # TODO find a shorter way to get table name
        try:
            df.to_sql(model._meta.db_table, con=engine, if_exists="append", index=False)
            # print("num rows saved:", len(df.index))
            num_rows_saved = len(df.index)
        # except IntegrityError:
        #     print("integrity error")
        except Exception as e:
            # print(e)
            pass
        return num_rows_saved


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
        df["max_temp_of_day"] = df["max_temp_of_day"].apply(self._convert_null_vals)
        df["min_temp_of_day"] = df["min_temp_of_day"].apply(self._convert_null_vals)
        df["precipitation_of_day"] = df["precipitation_of_day"].apply(
            self._convert_null_vals
        )
        # df.set_index(["weather_station", "date"], inplace=True)
        return df

    def _format_date(self, date: int) -> str:
        date = str(date)
        date = date[:4] + "-" + date[4:6] + "-" + date[6:]
        return date

    def _convert_null_vals(self, value: int):
        if value == -9999:
            return None
        return value


class IngestYieldData(IngestDataParent):
    def __init__(self, data_dir: str) -> None:
        self.data_model = YieldData
        self.data_dir = data_dir
        self.col_names = ["year", "total_harvested_grain"]
        super().__init__()

    def _clean_data(self, df: DataFrame) -> DataFrame:
        df.set_index(["year"], inplace=True)
        return df
