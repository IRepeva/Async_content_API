import asyncio
import sys
from dataclasses import dataclass

import aiohttp
import aioredis
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

sys.path.append('.')
from settings import test_settings

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
    client = AsyncElasticsearch(
        hosts=f'{test_settings.ELASTIC_HOST}:{test_settings.ELASTIC_PORT}'
    )
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
    async def inner(method: str, params: dict | None = None) -> HTTPResponse:
        params = params or {}
        url = API_URL + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
