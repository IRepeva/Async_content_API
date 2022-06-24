import logging
import os
import sys

from elasticsearch import Elasticsearch

from backoff import backoff

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base)
from settings import test_settings

logger = logging.getLogger(__name__)

elastic_host = f'{test_settings.ELASTIC_HOST}:{test_settings.ELASTIC_PORT}'
elastic = Elasticsearch(hosts=[elastic_host])


@backoff(start_sleep_time=1, factor=2, border_sleep_time=6, logger=logger)
def check_es_connection():
    while not elastic.ping():
        logger.info('Trying to connect to ElasticSearch...')
        raise ConnectionRefusedError
    logger.info(f'Connected to {elastic_host}')


check_es_connection()
