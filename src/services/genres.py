from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from models.genre import Genre
from services.base import BaseService
from utils.cache import ICache, get_cache_storage


class GenreService(BaseService):
    INDEX = 'genres'
    MODEL = Genre


@lru_cache
def get_genre_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
        cache_storage: ICache = Depends(get_cache_storage)
) -> GenreService:
    return GenreService(elastic, cache_storage)
