from typing import Optional


def check_results(
        status: int,
        expected_status: int,
        body: dict,
        expected_page_size: Optional[int]
) -> None:
    """
    Сверяем ожидаемые значения с результатом запросов.
    """

    assert status == expected_status

    if expected_page_size is not None:
        assert body.get('total') == expected_page_size

