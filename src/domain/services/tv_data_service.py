import json
from collections import defaultdict
from typing import List
import pandas as pd
from src.domain.entities.open_tv import TVData
from src.infra.repositories.csv_s3_repository import S3CSVRepository
from src.infra.repositories.redis_repository import RedisRepository
import logging

logger = logging.getLogger(__name__)


class TvDataService:
    """
    Service responsible for processing TV audience and inventory data, storing it in Redis,
    and providing access to structured TV data.
    """
    redis_key: str = "tv_data"

    def __init__(self):
        """
        Initializes the service with the required repositories.
        """
        self.csv_repository = S3CSVRepository(bucket_name="globo-challange")
        self.database_repository = RedisRepository.setup_connection_strings().connect()

    def process_and_store_data(self, audience_csv_key: str, inventory_csv_key: str):
        """
        Fetches, validates, processes, and stores TV audience and inventory data.

        :param audience_csv_key: S3 key for the audience CSV file.
        :param inventory_csv_key: S3 key for the inventory CSV file.
        """
        audience_df, inventory_df = self._fetch_and_load_data(audience_csv_key, inventory_csv_key)
        audience_df = self._validate_audience_data(audience_df)
        inventory_df = self._validate_inventory_data(inventory_df)
        history = self._create_audience_history(audience_df)
        tv_data_list = self._generate_tv_data(inventory_df, history)
        self._store_in_redis(tv_data_list)

    def _fetch_and_load_data(self, audience_csv_key: str, inventory_csv_key: str):
        """
        Fetches CSV data from S3 and loads it into Pandas DataFrames.

        :param audience_csv_key: S3 key for the audience CSV file.
        :param inventory_csv_key: S3 key for the inventory CSV file.
        :return: Tuple containing audience and inventory DataFrames.
        """
        audience_df = self.csv_repository.fetch_csv_as_dataframe(audience_csv_key)
        inventory_df = self.csv_repository.fetch_csv_as_dataframe(inventory_csv_key)
        return audience_df, inventory_df

    def _validate_audience_data(self, audience_df):
        """
        Validates and processes audience data.

        :param audience_df: DataFrame containing audience data.
        :return: Processed audience DataFrame.
        """
        required_columns = ['signal', 'program_code', 'exhibition_date', 'average_audience']

        if not all(col in audience_df.columns for col in required_columns):
            raise KeyError(f"Missing required columns in audience data: {required_columns}")

        audience_df['exhibition_date'] = pd.to_datetime(audience_df['exhibition_date'], format="%Y-%m-%d",
                                                        errors='coerce')
        audience_df['weekday'] = audience_df['exhibition_date'].dt.day_name()

        logger.info("Audience data validation completed successfully!")
        return audience_df

    def _validate_inventory_data(self, inventory_df):
        """
        Validates and processes inventory data.

        :param inventory_df: DataFrame containing inventory data.
        :return: Processed inventory DataFrame.
        """
        required_columns = ['signal', 'program_code', 'date', 'available_time']

        if 'signal;program_code;date;available_time' in inventory_df.columns:
            logger.info("Detected invalid format in 'inventory_df'. Correcting...")
            inventory_df[['signal', 'program_code', 'date', 'available_time']] = inventory_df[
                'signal;program_code;date;available_time'].str.split(';', expand=True)
            inventory_df = inventory_df.drop(columns=['signal;program_code;date;available_time'])

        if not all(col in inventory_df.columns for col in required_columns):
            raise KeyError(f"Missing required columns in inventory data: {required_columns}")

        inventory_df['date'] = pd.to_datetime(inventory_df['date'], format="%d/%m/%Y", errors='coerce')
        inventory_df['weekday'] = inventory_df['date'].dt.day_name()

        logger.info("Inventory data validation and correction completed successfully!")
        return inventory_df

    def _create_audience_history(self, audience_df):
        """
        Creates an audience history for each program based on past records.

        :param audience_df: DataFrame containing audience data.
        :return: Dictionary mapping (signal, program_code, weekday) to past audience records.
        """
        history = defaultdict(list)
        logger.info("Creating audience history...")

        for _, row in audience_df.iterrows():
            weekday = row["weekday"] if pd.notna(row["weekday"]) else "Unknown"
            key = (row["signal"], row["program_code"], weekday)
            history[key].append(row["average_audience"])
            if len(history[key]) > 4:
                history[key].pop(0)

        logger.info(f"Audience history generated: {len(history)} records.")
        return history

    def _generate_tv_data(self, inventory_df, history):
        """
        Generates structured TV data by merging inventory data with audience history.

        :param inventory_df: DataFrame containing inventory data.
        :param history: Dictionary mapping (signal, program_code, weekday) to past audience records.
        :return: List of structured TV data.
        """
        tv_data_list = []

        for _, row in inventory_df.iterrows():
            key = (row["signal"], row["program_code"], row["weekday"])
            logger.info(f"Generating TV Data for key: {key}")

            median_audience = pd.Series(history[key]).median() if key in history and history[key] else None
            exhibition_date = row["date"].strftime("%Y-%m-%d")

            tv_data = TVData(
                signal=row["signal"],
                program_code=row["program_code"],
                weekday=row["weekday"],
                available_time=row["available_time"],
                predicted_audience=median_audience,
                exhibition_date=exhibition_date
            )

            tv_data_list.append(tv_data.model_dump_tv_data())

        return tv_data_list

    def _store_in_redis(self, tv_data_list):
        """
        Stores processed TV data in Redis.

        :param tv_data_list: List of structured TV data.
        """
        self.database_repository.create(self.redis_key, json.dumps(tv_data_list))

    def get_all_data(self) -> List[TVData]:
        """
        Retrieves all TV data stored in Redis.

        :return: List of TVData objects.
        """
        raw_data = self.database_repository.get(self.redis_key)
        return [] if not raw_data else [TVData(**item) for item in json.loads(raw_data)]
