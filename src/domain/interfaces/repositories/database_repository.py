from abc import ABC, abstractmethod


class IDataBaseRepository(ABC):
    """
    Interface for a database repository that defines methods for setting up connections,
    storing, and retrieving data.
    """

    @classmethod
    @abstractmethod
    def setup_connection_strings(cls, **kwargs):
        """
        Configures the connection parameters for the database.

        :param kwargs: Additional parameters required for the connection setup.
        :raises NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError

    @classmethod
    def connect(cls):
        """
        Establishes a connection to the database.

        :return: The class instance with an active database connection.
        :raises NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def create(self, key: str, value: bytes | memoryview | str | int | float, expiration_time: int = None) -> None:
        """
        Stores a value in the database.

        :param key: The key under which the value will be stored.
        :param value: The value to be stored in the database.
        :param expiration_time: (Optional) Expiration time in seconds.
        :raises NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str):
        """
        Retrieves a value from the database by its key.

        :param id: The key to fetch from the database.
        :return: The value associated with the given key.
        :raises NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError