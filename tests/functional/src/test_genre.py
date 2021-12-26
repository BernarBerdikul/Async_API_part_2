import asyncio

import pytest

from tests.functional.schemas.genre_schema import (
    FilmGenreValidation,
    GenrePaginationValidation
)
from tests.functional.settings import Settings
from tests.functional.utils.hash_key_creater import create_hash_key

pytestmark = pytest.mark.asyncio


async def test_list_genre(genre_index, make_get_request, redis_cache):
    await asyncio.sleep(3)
    expected: dict = {
        "total": 5,
        "page": 1,
        "page_size": 10,
        "next_page": None,
        "previous_page": None,
        "available_pages": 1,
        "genres": [
            {"uuid": "526769d7-df18-4661-9aa6-49ed24e9dfd8", "name": "Thriller"},
            {"uuid": "6a0a479b-cfec-41ac-b520-41b2b007b611", "name": "Animation"},
            {"uuid": "b92ef010-5e4c-4fd0-99d6-41b6456272cd", "name": "Fantasy"},
            {"uuid": "ca88141b-a6b4-450d-bbc3-efa940e4953f", "name": "Mystery"},
            {"uuid": "237fd1e4-c98e-454e-aa13-8a13fb7547b5", "name": "Romance"},
        ],
    }
    # Выполнение запроса
    response = await make_get_request(endpoint="genre/")
    response_body = response.body
    print()
    print(response)
    # Проверка результата
    assert response.status == 200
    assert response_body == expected
    assert GenrePaginationValidation(**response_body)
    # Проверка результата Redis
    page: int = response_body.get("page")
    page_size: int = response_body.get("page_size")
    total: int = response_body.get("total")
    key: str = create_hash_key(
        index=Settings.GENRE_INDEX, params=f"{total}{page}{page_size}"
    )
    assert await redis_cache.get(key=key) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=key) is None


async def test_genre_by_id(genre_index, make_get_request, redis_cache):
    genre_id: str = "526769d7-df18-4661-9aa6-49ed24e9dfd8"
    expected: dict = {"uuid": genre_id, "name": "Thriller"}
    # Выполнение запроса
    response = await make_get_request(endpoint=f"genre/{genre_id}")
    # Проверка результата Elastic
    assert response.status == 200
    assert response.body == expected
    assert FilmGenreValidation(**response.body)
    # Проверка результата Redis
    assert await redis_cache.get(key=genre_id) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=genre_id) is None
