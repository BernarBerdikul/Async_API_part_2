import pytest

from testdata.search_parametrs import films_params
from utils.checkpoints_status import check_results


@pytest.mark.parametrize(
    "path, query, status, page_size",
    [
        *films_params,
    ]
)
@pytest.mark.asyncio
async def test_get_films(
        make_get_request,
        path: str,
        query: dict,
        status: int,
        page_size: int):
    response = await make_get_request(f"/{path}", query)
    check_results(
        status=status,
        expected_status=response.status,
        body=response.body,
        expected_page_size=page_size
    )
