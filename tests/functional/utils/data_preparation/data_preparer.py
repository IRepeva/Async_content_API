import abc
import logging
from dataclasses import dataclass

from elasticsearch import AsyncElasticsearch
from elasticsearch import helpers

from utils.backoff import backoff

logger = logging.getLogger(__name__)


class AbstractDataPreparer:
    @abc.abstractmethod
    async def load(self, key, data):
        ...

    @abc.abstractmethod
    async def clear(self, key, data):
        ...


@dataclass
class ElasticDataPreparer(AbstractDataPreparer):
    elastic: AsyncElasticsearch

    @backoff(logger=logger)
    async def load(self, index: dict[str, str], data: list[dict]):
        data = self.prepare_for_update(data)
        await self.check_existence_and_create(index)

        await helpers.async_bulk(self.elastic, data, index=index['name'],
                                 refresh='wait_for')

    @backoff(logger=logger)
    def create_index(self, index: dict[str, str],
                     settings: dict | None = None,
                     mappings: dict | None = None):
        if mappings is None:
            mappings = index['mappings']
        if settings is None:
            settings = index['settings']

        index_name = index['name']

        self.elastic.indices.create(index=index_name, ignore=400,
                                    body={
                                        'mappings': mappings,
                                        'settings': settings
                                    })
        logger.info(f'Index "{index_name}" was created')

    def prepare_for_update(self, data: list[dict]) -> list[dict]:
        prepared_data = [
            {
                "_op_type": 'update',
                "_id": str(item['id']),
                "doc": item,
                "doc_as_upsert": True
            } for item in data
        ]
        return prepared_data

    async def check_existence_and_create(self, index):
        index_name = index['name']
        if not await self.elastic.indices.exists(index=index_name):
            logger.info(
                f'Index "{index_name}" does not exist, '
                f'index creation was started'
            )
            self.create_index(index)

    async def clear(self, key, data):
        ...
