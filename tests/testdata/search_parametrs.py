

films_params = [
    # получить фильмы с query
    ("film", {"query": "Star"}, 200, 10),
    # получить фильм без с query и с размером ответа
    ("film", {"query": "Star", "page_size": 1, "page": 1}, 200, 1),
    # получить данные 2 страницы
    ("film", {"page": 2}, 200, 10),
]
