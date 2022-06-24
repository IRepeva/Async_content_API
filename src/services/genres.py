from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from models.genre import Genre
from services.base import BaseService


class GenreService(BaseService):
    INDEX = 'genres'
    MODEL = Genre


@lru_cache
def get_genre_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(elastic)
