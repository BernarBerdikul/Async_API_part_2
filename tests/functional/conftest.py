from dataclasses import dataclass

import aiohttp
import aioredis
import pytest
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from tests.functional.settings import SERVICE_URL


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
async def get_redis() -> Redis:
    redis = await aioredis.create_redis_pool(
        ("127.0.0.1", "6379"), minsize=10, maxsize=20
    )
    yield redis
    await redis.close()


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
def make_get_request(session):
    async def inner(endpoint: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        # в боевых системах старайтесь так не делать!
        url: str = f"{SERVICE_URL}/api/v1/{endpoint}"
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
