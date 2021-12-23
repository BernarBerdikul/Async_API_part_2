from asyncio import sleep

from tests.functional.conftest import make_get_request


def wait_for_es(url: str = "http://127.0.0.1:9200"):
    """
    Дождаться пока по адресу url заработает сервер ElasticSearch
    """
    while True:
        response = await make_get_request(url)
        print(response)
        print("Соединения с Elastic нет, попробуем позже")
        sleep(5)
        if response.json().get("tagline", "").lower():
            print("Ответ Elastic не выглядит как надо, попробуем позже")
            sleep(5)
            continue
        return
