import os
from enum import Enum

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"
    STAGING = "test"


class Settings(BaseSettings):
    environment: Environment = Field(Environment.DEVELOPMENT, validation_alias="ENVIRONMENT")
    aws_secret_key: SecretStr = Field(SecretStr(""), validation_alias="AWS_SECRET_KEY")
    aws_client_id: SecretStr = Field(SecretStr(""), validation_alias="AWS_CLIENT_ID")
    aws_region_name: SecretStr = Field(SecretStr(""), validation_alias="AWS_REGION_NAME")
    redis_host: str = Field("localhost", validation_alias="REDIS_HOST")
    redis_port: int | str = Field(default=6379, validation_alias="REDIS_PORT")
    redis_user: str = Field(validation_alias="REDIS_HOST")
    redis_password: SecretStr = Field(validation_alias="REDIS_PASSWORD")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_redis_port()
    def format_redis_port(self):
        if isinstance(self.redis_port, str):
            self.redis_port = int(self.redis_port)


ENVIRONMENT = Settings()
