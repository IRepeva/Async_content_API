from typing import List

from api.v1.models_api.genre import Genre
from api.v1.models_api.mixin import MixinModel
from api.v1.models_api.person import PersonBase


class Film(MixinModel):
    title: str
    imdb_rating: float | None = 0


class FilmDetails(Film):
    description: str | None = ''
    genres: List[Genre] | None = []
    directors: List[PersonBase] | None = []
    writers: List[PersonBase] | None = []
    actors: List[PersonBase] | None = []
