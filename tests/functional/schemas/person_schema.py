from typing import Optional
from uuid import UUID

from .mixin import UUIDValidation, PaginationValidation


class FilmPersonValidation(UUIDValidation):

    full_name: str


class DetailPersonValidation(FilmPersonValidation):

    role: str
    film_ids: Optional[list[UUID]] = []


class PersonPaginationValidation(PaginationValidation):
    persons: list[DetailPersonValidation] = []
