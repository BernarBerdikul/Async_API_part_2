import pytest

from ..testdata.films_params import film_search_params, film_list_params
from ..utils.status_films import check_films_result


@pytest.mark.parametrize(
    "endpoint, query, expected_status",
    [
        *film_search_params,
        *film_list_params
    ]

)
@pytest.mark.asyncio
async def test_get_list_films(
        movies_index,
        make_get_request,
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


@pytest.mark.asyncio
async def test_get_film(
        movies_index,
        make_get_request,
):
    expected_film_id: str = "201c0ec8-2add-4d55-90e9-6596afd6dfe9"
    expected_not_found_film_id: str = "201c0ec8-333-4d55-90e9-6596afd6dfe9"
    response = await make_get_request(endpoint=f"film/{expected_film_id}")
    print(response)
    # фильм найден
    assert expected_film_id == response.body.get('uuid')
    # запрос имеет статус 200
    assert 200 == response.status
    # проверка на несуществующий id
    response = await make_get_request(endpoint=f"film/{expected_not_found_film_id}")
    assert 404 == response.status
