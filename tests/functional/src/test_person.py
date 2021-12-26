import asyncio
from uuid import UUID

import pytest

from tests.functional.schemas.movie_schema import FilmPaginationValidation
from tests.functional.schemas.person_schema import (
    DetailPersonValidation,
    PersonPaginationValidation,
)
from tests.functional.settings import Settings
from tests.functional.utils.hash_key_creater import create_hash_key

pytestmark = pytest.mark.asyncio


async def test_person_by_id(person_index, make_get_request, redis_cache):
    person_id: str = "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a"
    expected: dict = {
        "uuid": person_id,
        "full_name": "George Lucas",
        "role": "actor",
        "film_ids": [
            "025c58cd-1b7e-43be-9ffb-8571a613579b",
            "0312ed51-8833-413f-bff5-0e139c11264a",
            "0659e0e6-504e-4482-8aa9-f7530f36cae2",
            "07f8bdbe-5246-4dfc-8d38-85043aeb307b",
            "118fd71b-93cd-4de5-95a4-e1485edad30e",
            "12a8279d-d851-4eb9-9d64-d690455277cc",
            "134989c3-3b20-4ae7-8092-3e8ad2333d59",
            "19babc93-62f5-481a-b6fe-9ebfef689cbc",
        ],
    }
    # Выполнение запроса
    response = await make_get_request(endpoint=f"person/{person_id}")
    response_body = response.body
    print()
    print(response)
    # Проверка результата
    assert response.status == 200
    assert response_body == expected
    assert DetailPersonValidation(**response.body)
    # Проверка результата Redis
    assert await redis_cache.get(key=person_id) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=person_id) is None


async def test_search_person(person_index, make_get_request, redis_cache):
    query: str = "Jake"
    await asyncio.sleep(3)
    expected: dict = {
        "total": 1,
        "page": 1,
        "page_size": 10,
        "next_page": None,
        "previous_page": None,
        "available_pages": 1,
        "persons": [
            {
                "uuid": "979996d5-ef97-427d-a0f5-d640cd1813a4",
                "full_name": "Jake Lloyd",
                "role": "actor",
                "film_ids": [
                    "08a588bd-5eeb-4cf3-8a42-f20195a02c25",
                    "17f634cd-9581-4ba1-b40b-89ee058c3f55",
                    "3b914679-1f5e-4cbd-8044-d13d35d5236c",
                    "569e23df-7e00-459d-b92a-6cb4653d36b8",
                    "7a87274a-541a-405c-b148-5946f6c707d4",
                    "c5653bd8-56b5-4530-90b2-34ce1a2ba6db",
                    "ec8bad1c-7643-49b3-93b5-cee9c8c1e602",
                ],
            }
        ],
    }
    # Выполнение запроса
    response = await make_get_request(endpoint="person/search", params={"query": query})
    response_body = response.body
    print()
    print(response)
    # Проверка результата
    assert response.status == 200
    assert response_body == expected
    assert PersonPaginationValidation(**response_body)
    # Проверка результата Redis
    page: int = response_body.get("page")
    page_size: int = response_body.get("page_size")
    total: int = response_body.get("total")
    key: str = create_hash_key(
        index=Settings.PERSON_INDEX, params=f"{total}{page}{page_size}{query}"
    )
    assert await redis_cache.get(key=key) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=key) is None


async def test_person_films(movies_index, person_index, make_get_request, redis_cache):
    person_id: str = "c777f646-dae0-466f-867a-bc535a0b021b"
    await asyncio.sleep(3)
    expected: dict = {
        "total": 3,
        "page": 1,
        "page_size": 10,
        "next_page": None,
        "previous_page": None,
        "available_pages": 1,
        "films": [
            {
                "uuid": "3b914679-1f5e-4cbd-8044-d13d35d5236c",
                "title": "Star Wars: Episode I - The Phantom Menace",
                "imdb_rating": 6.5,
            },
            {
                "uuid": "516f91da-bd70-4351-ba6d-25e16b7713b7",
                "title": "Star Wars: Episode III - Revenge of the Sith",
                "imdb_rating": 7.5,
            },
            {
                "uuid": "c4c5e3de-c0c9-4091-b242-ceb331004dfd",
                "title": "Star Wars: Episode II - Attack of the Clones",
                "imdb_rating": 6.5,
            },
        ],
    }
    # Выполнение запроса
    response = await make_get_request(endpoint=f"person/{person_id}/films/")
    response_body = response.body
    print()
    print(response)
    # Проверка результата Elastic
    assert response.status == 200
    assert response_body == expected
    assert FilmPaginationValidation(**response_body)
    # Проверка результата Redis
    page: int = response_body.get("page")
    page_size: int = response_body.get("page_size")
    total: int = response_body.get("total")
    film_ids: list[UUID] = [UUID(i.get("uuid")) for i in expected.get("films")]
    key: str = create_hash_key(
        index="person_films", params=f"{total}{page}{page_size}{film_ids}"
    )
    assert await redis_cache.get(key=key) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=key) is None
