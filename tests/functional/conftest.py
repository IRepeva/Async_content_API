import asyncio
import http
import logging
import sys
from dataclasses import dataclass

import aiohttp
import aioredis
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch import helpers
from multidict import CIMultiDictProxy

sys.path.append('.')
from settings import test_settings
from testdata.indexes_data import INDEXES_DATA

logger = logging.getLogger(__name__)

SERVICE_URL = test_settings.SERVICE_URL
API_URL = SERVICE_URL + '/api/v1'


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=f'{test_settings.ELASTIC_URL}')
    yield client
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    pool = aioredis.ConnectionPool.from_url(
        test_settings.REDIS_URL,
        max_connections=20
    )
    client = aioredis.Redis(connection_pool=pool)
    yield client
    await client.close()


@pytest_asyncio.fixture
def make_get_request(session):
    async def inner(path: str, params: dict | None = None) -> HTTPResponse:
        params = params or {}
        url = API_URL + path
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


async def elastic_tear_down(es_client):
    await es_client.options(
        ignore_status=[http.HTTPStatus.BAD_REQUEST, http.HTTPStatus.NOT_FOUND]
    ).indices.delete(index="*")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def start_up_tear_down(redis_client, es_client):
    logger.info('Setting up')
    await redis_client.flushall()

    for index in INDEXES_DATA.values():
        index_name = index['name']
        if not await es_client.indices.exists(index=index_name):
            logger.info(
                f'Index "{index_name}" does not exist, '
                f'index creation was started'
            )
            await es_client.options(
                ignore_status=[http.HTTPStatus.BAD_REQUEST]
            ).indices.create(
                index=index_name,
                body={
                    'mappings': index['mappings'],
                    'settings': index['settings']
                }
            )
            logger.info(f'Index "{index_name}" was created')

        data = prepare_for_update(index['test_data'])
        await helpers.async_bulk(es_client, data, index=index['name'],
                                 refresh='wait_for')
    yield
    logger.info('Tearing down')
    await elastic_tear_down(es_client)


def prepare_for_update(data: list[dict]) -> list[dict]:
    prepared_data = [
        {
            "_op_type": 'update',
            "_id": str(item['id']),
            "doc": item,
            "doc_as_upsert": True
        } for item in data
    ]
    return prepared_data
