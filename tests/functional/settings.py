import warnings
from functools import lru_cache
from logging import config as logging_config

from elasticsearch import ElasticsearchDeprecationWarning
from pydantic import BaseSettings, Field

from logger import LOGGING

# LOGGING
logging_config.dictConfig(LOGGING)

# Unable Elasticsearch built-in security features are not enabled
warnings.filterwarnings('ignore', category=ElasticsearchDeprecationWarning)


class TestSettings(BaseSettings):
    # PROJECT
    PROJECT_NAME = Field('movies', env='PROJECT_NAME')

    # ELASTICSEARCH
    ELASTIC_URL: str = Field('http://127.0.0.1:9200', env='ES_URL')

    # REDIS
    REDIS_URL: str = Field('redis://127.0.0.1:6379', env='REDIS_URL')

    # API
    SERVICE_URL: str = Field('http://127.0.0.1:8000', env='API_URL')


@lru_cache
def get_settings() -> TestSettings:
    return TestSettings()


test_settings = get_settings()
