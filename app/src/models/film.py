from typing import Optional

from models.genre import FilmGenre
from models.mixin import BaseModelMixin, PaginationMixin
from models.person import FilmPerson
from pydantic import BaseModel


class ESFilm(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    imdb_rating: Optional[float] = None
    genre: Optional[list[dict[str, str]]] = None
    actors: Optional[list[dict[str, str]]] = None
    writers: Optional[list[dict[str, str]]] = None
    directors: Optional[list[dict[str, str]]] = None


class ListResponseFilm(BaseModelMixin):
    """Schema for Film work list"""

    title: str
    imdb_rating: Optional[float] = None


class DetailResponseFilm(ListResponseFilm):
    """Schema for Film work detail"""

    description: Optional[str] = None
    genre: Optional[list[FilmGenre]] = []
    actors: Optional[list[FilmPerson]] = []
    writers: Optional[list[FilmPerson]] = []
    directors: Optional[list[FilmPerson]] = []


class FilmPagination(PaginationMixin):
    films: list[ListResponseFilm] = []
