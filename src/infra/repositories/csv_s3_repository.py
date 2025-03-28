from io import StringIO

import boto3
import pandas as pd

from src.domain.core.config import ENVIRONMENT
from src.domain.interfaces.repositories.csv_repository import ICsvRepository


class S3CSVRepository(ICsvRepository):
    def __init__(self, bucket_name: str):
        """
        Initializes the repository to fetch CSV files from S3.

        :param bucket_name: Name of the S3 bucket where the files are stored.
        """
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=ENVIRONMENT.aws_client_id.get_secret_value(),
            aws_secret_access_key=ENVIRONMENT.aws_secret_key.get_secret_value(),
            region_name=ENVIRONMENT.aws_region_name.get_secret_value()
        )
        self.bucket_name = bucket_name

    def fetch_csv_as_dataframe(self, file_key: str) -> pd.DataFrame:
        """
        Retrieves a CSV file from S3 and loads it as a Pandas DataFrame.

        :param file_key: Path to the file within the S3 bucket.
        :return: DataFrame containing the CSV data.
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
            csv_content = response["Body"].read().decode("utf-8")
            return pd.read_csv(StringIO(csv_content))
        except Exception as e:
            print(f"Error fetching file {file_key}: {str(e)}")
            return pd.DataFrame()