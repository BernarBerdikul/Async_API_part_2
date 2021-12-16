import aiohttp
import pytest

from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import SERVICE_URL, PERSON_INDEX

pytestmark = pytest.mark.asyncio


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='127.0.0.1:9200')
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = {}) -> HTTPResponse:
        params = params or {}
        url = f'{SERVICE_URL}/api/v1{method}'  # в боевых системах старайтесь так не делать!
        print(url)
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner


async def test_search_person(es_client, make_get_request):
    # Заполнение данных для теста
    await es_client.bulk()
    # Выполнение запроса
    response = await make_get_request(
        method='/person/search', params={'query': 'John'}
    )
    print(response)
    # Проверка результата
    assert response.status == 200


async def test_person_by_id(es_client, make_get_request):
    # Заполнение данных для теста
    person_id: str = "2"
    test_person = {
        "id": person_id,
        "full_name": "Bernar",
        "roles": ["actor"],
        "film_ids": [
            "118fd71b-93cd-4de5-95a4-e1485edad30e"
        ]
    }
    test_data = [
        {"create": {"_index": PERSON_INDEX, "_id": test_person["id"]}},
        test_person
    ]
    await es_client.bulk(index=PERSON_INDEX, body=test_data, refresh=True)
    # Выполнение запроса
    response = await make_get_request(method=f'/person/{person_id}')
    print(response)
    # Проверка результата
    assert response.status == 200
