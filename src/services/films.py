from functools import lru_cache

from elasticsearch import NotFoundError, AsyncElasticsearch
from elasticsearch_dsl import Q
from fastapi import Depends

from db.elastic import get_elastic
from models.film import Film
from services.base import BaseService


class FilmService(BaseService):
    INDEX = 'movies'
    MODEL = Film

    async def get_query(self, param, value):
        if param == 'similar_to':
            return (await getattr(self, param)(value)).to_dict()
        return await super().get_query(param, value)

    @property
    def query(self):
        return lambda query: Q("multi_match", query=query,
                               fields=["title^5", "description"])

    @property
    def genre(self):
        return lambda genre_id: Q("nested", path='genres',
                                  query=Q('match', genres__id=genre_id))

    @property
    def person(self):
        return lambda p_id: Q(
            'bool', should=[
                Q(
                    "nested", path=role,
                    query=Q('terms', **{f'{role}.id': [p_id]})
                )
                for role in ('actors', 'writers', 'directors')
            ]
        )

    async def similar_to(self, similar):
        try:
            doc = await self.es_manager.get_by_id(similar)
        except NotFoundError:
            return None

        genres = [genre.id for genre in doc.genres]
        return Q("nested", path='genres', query=Q('terms', genres__id=genres))


@lru_cache()
def get_film_service(
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> FilmService:
    return FilmService(elastic)
