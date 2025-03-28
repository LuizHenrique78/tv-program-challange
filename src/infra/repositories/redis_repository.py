import logging
import redis

from src.cross.errors import Forbidden, ValidationError
from src.domain.core.config import ENVIRONMENT
from src.domain.interfaces.repositories.database_repository import IDataBaseRepository

logger = logging.getLogger()


class RedisRepository(IDataBaseRepository):

    @classmethod
    def setup_connection_strings(cls):
        """
        Sets up the connection parameters for Redis.

        :return: The class instance with configured connection parameters.
        :raises ValueError: If there is an error while setting up the connection strings.
        """
        try:
            cls.redis_host = ENVIRONMENT.redis_host
            cls.redis_port = int(ENVIRONMENT.redis_port)
            cls.redis_password = ENVIRONMENT.redis_password

            return cls
        except Exception as e:
            logger.error(f"Error setting up connection strings - {e}")
            raise ValueError("Error setting up connection strings.")

    @classmethod
    def connect(cls):
        """
        Establishes a connection to the Redis cache.

        :return: The class instance with an active Redis connection.
        :raises Forbidden: If there is an error connecting to Redis.
        """
        try:
            cls.instance = redis.StrictRedis(
                host=cls.redis_host,
                port=cls.redis_port,
                password=cls.redis_password.get_secret_value(),
                decode_responses=True
            )

            return cls()
        except redis.ConnectionError as e:
            logger.critical(f"Error connecting to Redis - {e}")
            raise Forbidden("Error connecting to Redis.")

    def get(self, key: str):
        """
        Retrieves a value from the Redis cache.

        :param key: The key to fetch from Redis.
        :return: The value associated with the given key, or None if not found.
        :raises ValidationError: If there is an error retrieving the key.
        """
        try:
            return self.instance.get(key)
        except Exception as e:
            logger.error(f"Error getting key from cache - {e}")
            raise ValidationError("Error retrieving key from cache.")

    def create(self, key: str, value: bytes | memoryview | str | int | float, expiration_time: int = None) -> None:
        """
        Stores a value in the Redis cache with an optional expiration time.

        :param key: The key under which the value will be stored.
        :param value: The value to be stored in Redis.
        :param expiration_time: (Optional) Expiration time in seconds. Defaults to 3600 seconds if not provided.
        :raises ValidationError: If there is an error storing the key-value pair in Redis.
        """
        try:
            self.instance.set(key, value, ex=3600 if expiration_time is None else expiration_time)
        except Exception as e:
            logger.error(f"Error setting key in cache - {e}")
            raise ValidationError("Error storing key in cache.")