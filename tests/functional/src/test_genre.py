import pytest

from tests.functional.schemas.genre_schema import FilmGenreValidation

pytestmark = pytest.mark.asyncio


async def test_list_genre(genre_index, make_get_request):
    expected: dict = {}
    # Выполнение запроса
    response = await make_get_request(endpoint="genre/")
    print()
    print(response)
    print(response.body.get("total"))
    # Проверка результата
    assert response.status == 200


async def test_genre_by_id(genre_index, make_get_request):
    genre_id: str = "526769d7-df18-4661-9aa6-49ed24e9dfd8"
    expected: dict = {"uuid": genre_id, "name": "Thriller"}
    # Выполнение запроса
    response = await make_get_request(endpoint=f"genre/{genre_id}")
    # Проверка результата
    assert response.status == 200
    assert response.body == expected
    assert FilmGenreValidation(**response.body)
