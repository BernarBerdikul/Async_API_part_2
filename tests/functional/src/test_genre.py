import pytest

pytestmark = pytest.mark.asyncio


async def test_list_genre(genre_index, make_get_request):
    # Выполнение запроса
    response = await make_get_request(endpoint="genre/")
    print()
    print(response)
    # Проверка результата
    assert response.status == 200


async def test_genre_by_id(genre_index, make_get_request):
    genre_id: str = "526769d7-df18-4661-9aa6-49ed24e9dfd8"
    # Выполнение запроса
    # await insert_test_data_in_es(es_client=es_client)
    response = await make_get_request(endpoint=f"genre/{genre_id}")
    print()
    print(response)
    # Проверка результата
    assert response.status == 200
    assert response.body.get("name") == "Thriller"
