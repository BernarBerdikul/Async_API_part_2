import asyncio
from dataclasses import dataclass

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from tests.functional import es_index, testdata
from tests.functional.settings import Settings
from tests.functional.testdata.data_inserter import es_index_loader


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


@pytest.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts="127.0.0.1:9200")
    yield client
    await client.close()


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
async def person_index(es_client):
    index: str = Settings.PERSON_INDEX
    await es_index_loader(
        es_client=es_client,
        index=index,
        index_body=es_index.PERSON_INDEX_BODY,
        row_data=testdata.person_data,
    )
    yield
    await es_client.indices.delete(index=index)


@pytest.fixture
async def genre_index(es_client):
    index: str = Settings.GENRE_INDEX
    await es_index_loader(
        es_client=es_client,
        index=index,
        index_body=es_index.GENRE_INDEX_BODY,
        row_data=testdata.genre_data,
    )
    yield
    await es_client.indices.delete(index=index)


@pytest.fixture
async def movies_index(es_client):
    index: str = Settings.MOVIES_INDEX
    await es_index_loader(
        es_client=es_client,
        index=index,
        index_body=es_index.FILM_WORK_INDEX_BODY,
        row_data=testdata.film_work_data,
    )
    yield
    await es_client.indices.delete(index=index)


@pytest.fixture
def make_get_request(session):
    async def inner(
        endpoint: str = None, params: dict = None, url: str = None
    ) -> HTTPResponse:
        """
        :param endpoint: str
            Путь до нашего конечного url
        :param params: Optional[dict]
            Параметры для запроса
        :param url: Optional[str]
            Готовый адрес конечного url
        :return:
        """
        params = params or {}
        if not url:
            url = f"{Settings.SERVICE_URL}/api/v1/{endpoint}"
        async with session.get(url=url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
