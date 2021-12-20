import pytest

from tests.functional.settings import PERSON_INDEX
from tests.functional.testdata.data_inserter import insert_data_in_es
from tests.functional.testdata.person import person_data
from tests.functional.testdata.person_schema import PERSON_INDEX_BODY

pytestmark = pytest.mark.asyncio


# async def test_search_person(es_client, make_get_request):
#     # Выполнение запроса
#     response = await make_get_request(
#         endpoint='person/search', params={'query': 'Jake'}
#     )
#     print(response)
#     # Проверка результата
#     assert response.status == 200


async def test_person_by_id(es_client, make_get_request):
    person_id: str = "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a"
    # Заполнение данных для теста
    await es_client.indices.create(
        index=PERSON_INDEX, body=PERSON_INDEX_BODY, ignore=400
    )
    await insert_data_in_es(client=es_client, index=PERSON_INDEX, row_data=person_data)
    # Выполнение запроса
    response = await make_get_request(endpoint=f"person/{person_id}")
    print(response)
    # Проверка результата
    assert response.status == 200
