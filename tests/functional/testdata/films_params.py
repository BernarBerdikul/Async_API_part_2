film_search_params = [
    # параметры с query
    ("film", {"query": "Star"}, 200),
    # параметры с query и страницей
    ("film", {"query": "Star", "page": 2}, 200),
    # параметры с query и и страницей и количеством фильмов в ответе
    ("film", {"query": "Star", "page": 2, "page_size": 3}, 200),
    # проверяем сортировку по возрастанию без параметра query
    ("film", {"query": "Star", "sort": "imdb_rating"}, 200),
    # проверяем сортировку по убыванию без параметра query
    ("film", {"query": "Star", "sort": "-imdb_rating"}, 200),
    # сортировка по несуществующему полю
    ("film", {"query": "Star", "sort": "test"}, 422),
    # поиск фильма с лучшим рейтингом и в жанре Drama
    ("film", {"query": "Bright", "page": 1, "page_size": 10, "sort": "-imdb_rating", "genre": "Drama"}, 200),
]

film_list_params = [
    # параметры без query
    ("film", {}, 200),
    # параметры со страницами
    ("film", {"page": 2, "page_size": 1}, 200),
    # проверяем сортировку по возрастанию без параметра query
    ("film", {"sort": "imdb_rating"}, 200),
    # проверяем сортировку по убыванию без параметра query
    ("film", {"sort": "-imdb_rating"}, 200),
    # сортировка по несуществующему полю
    ("film", {"sort": "test"}, 422),
    # фильтрация по жанру
    ("film", {"genre": "Drama"}, 200),

]
