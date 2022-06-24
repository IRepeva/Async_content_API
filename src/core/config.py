import os
from functools import lru_cache
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

# LOGGING
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    # PROJECT
    PROJECT_NAME = Field('movies', env='PROJECT_NAME')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # ELASTICSEARCH
    ELASTIC_HOST: str = Field('127.0.0.1', env='ES_HOST')
    ELASTIC_PORT: int = Field(9200, env='ES_PORT')

    # REDIS
    REDIS_URL: str = Field('redis://127.0.0.1:6379', env='REDIS_URL')


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
