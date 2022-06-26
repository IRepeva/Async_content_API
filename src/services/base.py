from dataclasses import dataclass
import json
from pprint import pprint
from typing import Any

from elasticsearch import AsyncElasticsearch, NotFoundError

from utils.cache import ICache

CACHE_EXPIRY_TIME = 60 * 5

@dataclass
class ElasticSearchManager:
    model: Any

    async def get_list(self, sort: str | None = None, page: int | None = 1,
                       page_size: int | None = 50, **kwargs):

        from api.v1.utils.query_parser import QueryParser
        try:
            doc = await self.model.elastic.search(
                index=self.model.INDEX,
                body=await QueryParser.parse_params(self.model, **kwargs),
                from_=page_size * (page - 1),
                size=page_size,
                _source = kwargs.get('fields', None),
                sort=QueryParser.parse_sort(sort) if sort else None
            )
        except NotFoundError:
            return None

        return [self.model.MODEL(**item['_source']) for item in
                doc['hits']['hits']]

    async def get_by_id(self, _id):
        try:
            doc = await self.model.elastic.get(self.model.INDEX, _id)
        except NotFoundError:
            return None
        return self.model.MODEL(**doc['_source'])


class BaseService:
    INDEX = None
    MODEL = None

    def __init__(self, elastic: AsyncElasticsearch,
                 cache_storage: ICache | None = None) -> None:
        self.elastic = elastic
        self.cache_storage = cache_storage

    async def get_query(self, param, value):
        return getattr(self, param)(value).to_dict()

    @property
    def es_manager(self):
        return ElasticSearchManager(self)

    async def get_by_id(self, _id):

        value = await self._get_from_cache(_id)
        if value:
            return value

        value = await self.es_manager.get_by_id(_id)
        if value:
            await self._set_to_cache(_id, value)
        return value

    async def get_list(self, **kwargs):
        value = await self._get_from_cache(kwargs)
        if value:
            return value

        value = await self.es_manager.get_list(**kwargs)
        if value:
            await self._set_to_cache(kwargs, value)

        return value

    async def _get_from_cache(self, key: str | dict) -> Any:
        if not self.cache_storage:
            return None
        
        if not isinstance(key, str):
            key = self._get_key_from_dict(key)

        data = await self.cache_storage.get(key)
        if not data:
            return None

        data = json.loads(data)

        if isinstance(data, list):
            return [self.MODEL.parse_raw(item) for item in data]
        
        return self.MODEL.parse_obj(data)
    
    async def _set_to_cache(self, key: str | dict, value):
        if not self.cache_storage:
            return
        
        if not isinstance(key, str):
            key = self._get_key_from_dict(key)

        if isinstance(value, list):
            value = [self.MODEL.json(item) for item in value]
            value = json.dumps(value)
        else:
            value = self.MODEL.json(value)

        await self.cache_storage.set(key, value, CACHE_EXPIRY_TIME)

    def _get_key_from_dict(self, params):
        return json.dumps(params)
    