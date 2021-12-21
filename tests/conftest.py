import asyncio

import aiohttp
import pytest

from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch

from settings import Settings


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='127.0.0.1:9200')
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def create_index_es(es_client, index_name: str = 'test'):
    await es_client.indices.create(index=index_name)
    await es_client.indices.exists(index=index_name)
    await es_client.indices.delete(index=index_name)


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(path: str, params: dict = None) -> HTTPResponse:
        """
        :param path: Путь до нашего конечного url
        :param params: Параметры для запроса
        :return:
        """
        params = params or {}
        url = f'{Settings.SERVICE_URL}/api/v1{path}'
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
