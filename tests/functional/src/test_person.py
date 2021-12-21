import pytest

pytestmark = pytest.mark.asyncio


async def test_search_person(person_index, make_get_request):
    # Выполнение запроса
    response = await make_get_request(
        endpoint="person/search", params={"query": "Jake"}
    )
    print()
    print(response)
    # Проверка результата
    assert response.status == 200


async def test_person_by_id(person_index, make_get_request):
    person_id: str = "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a"
    # Выполнение запроса
    # await insert_test_data_in_es(es_client=es_client)
    response = await make_get_request(endpoint=f"person/{person_id}")
    print()
    print(response)
    # Проверка результата
    assert response.status == 200


async def test_person_films(person_index, make_get_request):
    person_id: str = "c777f646-dae0-466f-867a-bc535a0b021b"
    # Выполнение запроса
    # await insert_test_data_in_es(es_client=es_client)
    response = await make_get_request(endpoint=f"person/{person_id}/films/")
    print()
    print(response)
    # Проверка результата
    assert response.status == 200
