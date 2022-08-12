from os import listdir
from os.path import isfile, join, basename

from .models import WeatherData, YieldData
from pathlib import Path
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine
import logging
import time

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class IngestDataParent:
    # skeleton incase I wanna add on later
    def __init__(self) -> None:
        pass

    # main controller
    def run(self) -> None:
        logger.info(f"Starting Data Ingestor {type(self).__name__}")
        start = time.time()
        total_rows_saved = 0
        # returns list of file paths
        file_paths = self._get_all_data_file_paths()
        for file_path in file_paths:
            df = self._load_data(file_path)
            df = self._clean_data(df)
            num_rows_saved = self._save_data_in_db(df)
            total_rows_saved += num_rows_saved
        logger.info(f"total_rows_saved: {total_rows_saved} in model {self.data_model}")
        end = time.time()
        logger.info(f"Process Runtime: {end - start} seconds")

    def _get_all_data_file_paths(self) -> list[str]:
        # parents[2] so I can grab directories but also be similar to template
        parent_path = Path(__file__).parents[2]
        data_path = join(parent_path, self.data_dir)
        # check to make sure every file I grab is a file and not a directory
        file_paths = [
            join(data_path, f) for f in listdir(data_path) if isfile(join(data_path, f))
        ]
        return file_paths

    def _load_data(self, file_path: str) -> DataFrame:
        df = pd.read_csv(file_path, sep="\t", header=None, names=self.col_names)
        df = self._add_additional_cols(df=df, file_path=file_path)
        return df

    # not needed for yield data so just returning
    def _add_additional_cols(self, df: DataFrame, file_path: str = None) -> DataFrame:
        return df

    # not needed for yield data so just returning
    def _clean_data(self, df: DataFrame) -> DataFrame:
        return df

    # using create engine with sql lite sped up code immensly
    def _save_data_in_db(self, df: DataFrame) -> int:
        num_rows_saved = 0
        model = self.data_model
        engine = create_engine("sqlite:///db.sqlite3")
        try:
            df.to_sql(model._meta.db_table, con=engine, if_exists="append", index=False)
            num_rows_saved = len(df.index)
        except Exception as e:
            # passing because logs are blowing up my console
            pass
            # logger.exception(e)
        return num_rows_saved

    # older method but was having issue with saving nan valus and df.to_sql is ~5 times faster
    # def _old_save_in_db(self, df: DataFrame) -> int:
    #     num_rows_saved = 0
    #     model = self.data_model

    #     batch = df.to_dict(orient="records")
    #     batch = [model(**row) for row in batch]

    #     try:
    #         model.objects.bulk_create(batch, batch_size=len(batch))
    #         num_rows_saved = len(batch)
    #     except Exception as e:
    #         logger.exception(e)
    #     return num_rows_saved


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

    # formate date properly
    # make sure all -9999 become null
    def _clean_data(self, df: DataFrame) -> DataFrame:
        df["date"] = df["date"].apply(self._format_date)
        df["max_temp_of_day"] = df["max_temp_of_day"].apply(self._convert_null_vals)
        df["min_temp_of_day"] = df["min_temp_of_day"].apply(self._convert_null_vals)
        df["precipitation_of_day"] = df["precipitation_of_day"].apply(
            self._convert_null_vals
        )
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
