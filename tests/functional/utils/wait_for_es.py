from time import sleep

import requests

from tests.functional.settings import Settings


def wait_for_es(url: str = f"http://{Settings.ELASTIC_URL}"):
    """Дождаться пока по адресу url заработает сервер ElasticSearch"""
    # Отправляем запрос в Elastic
    while True:
        response = requests.get(url=url)
        if response.json().get("tagline", "").lower() == "you know, for search":
            return
        else:
            # Ответ Elastic не корректный, попробуем позже
            sleep(5)
            continue


wait_for_es()
