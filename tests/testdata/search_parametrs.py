

film_search_params = [
    # совпадения по заголовку фильма и описанию с параметрами страницы
    ("film", {"query": "Star"}, 200, 10),
    ("film", {"query": "Star", "page_size": 1, "page": 1}, 200, 1),
]