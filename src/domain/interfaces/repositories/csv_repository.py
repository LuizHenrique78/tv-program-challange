from abc import ABC, abstractmethod
import pandas as pd


class ICsvRepository(ABC):
    """
    Interface for a CSV repository that defines methods for retrieving CSV files and loading them as Pandas DataFrames.
    """

    @abstractmethod
    def fetch_csv_as_dataframe(self, file_key: str) -> pd.DataFrame:
        """
        Retrieves a CSV file and loads it as a Pandas DataFrame.

        :param file_key: Path to the CSV file.
        :return: DataFrame containing the CSV data.
        :raises NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError