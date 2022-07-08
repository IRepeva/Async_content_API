from typing import List

from models.genre import Genre
from models.mixin import MixinModel
from models.person import Person


class Film(MixinModel):
    title: str
    description: str | None = ''
    imdb_rating: float | None = 0
    genres: List[Genre] | None = []
    directors: List[Person] | None = []
    writers: List[Person] | None = []
    actors: List[Person] | None = []
