from http import HTTPStatus
from typing import Optional

import aioredis
import pytest

from ..settings import Settings
from ..testdata.films_params import film_list_params, film_search_params
from ..utils.hash_key_creater import create_hash_key
from ..utils.status_films import check_films_result


@pytest.mark.parametrize(
    "endpoint, query, expected_status", [*film_search_params, *film_list_params]
)
@pytest.mark.asyncio
async def test_get_list_films(
    movies_index,
    make_get_request,
    redis_cache: aioredis,
    endpoint: str,
    query: dict,
    expected_status: int,
):
    response = await make_get_request(endpoint=f"{endpoint}", params=query)

    check_films_result(
        status=response.status,
        expected_status=expected_status,
        body=response.body,
        expected_query=query.get("query"),
        expected_page=query.get("page"),
        expected_page_size=query.get("page_size"),
    )
    # Проверка результата Redis
    page: int = response.body.get("page")
    page_size: int = response.body.get("page_size")
    total: int = response.body.get("total")
    sort: Optional[str] = query.get("sort")
    genre: Optional[str] = query.get("genre")
    search: Optional[str] = query.get("query")

    key: str = create_hash_key(
        index=Settings.MOVIES_INDEX,
        params=f"{total}{page}{sort}{page_size}{search}{genre}",
    )

    assert redis_cache.get(key=key) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=key) is None


@pytest.mark.asyncio
async def test_get_film(movies_index, make_get_request, redis_cache):
    expected_film_id: str = "201c0ec8-2add-4d55-90e9-6596afd6dfe9"
    expected_not_found_film_id: str = "201c0ec8-333-4d55-90e9-6596afd6dfe9"
    response = await make_get_request(endpoint=f"film/{expected_film_id}")
    # фильм найден
    assert expected_film_id == response.body.get("uuid")
    # запрос имеет статус 200
    assert HTTPStatus.OK == response.status
    # проверка на несуществующий id
    response = await make_get_request(endpoint=f"film/{expected_not_found_film_id}")
    assert HTTPStatus.NOT_FOUND == response.status

    assert redis_cache.get(key=expected_film_id) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=expected_film_id) is None
