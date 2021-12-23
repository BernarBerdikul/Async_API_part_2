from .mixin import UUIDValidation, PaginationValidation


class FilmGenreValidation(UUIDValidation):

    name: str


class GenrePaginationValidation(PaginationValidation):
    genres: list[FilmGenreValidation] = []
