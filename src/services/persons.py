from functools import lru_cache
from pprint import pprint

from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Q
from fastapi import Depends

from db.elastic import get_elastic
from models.person import Person
from services.base import BaseService
from utils.cache import ICache, get_cache_storage


class PersonService(BaseService):
    INDEX = 'persons'
    MODEL = Person

    @property
    def query(self):
        return lambda query: Q('match', full_name={'query': query})

    async def get_persons(self, person_id):

        from services.films import FilmService

        person = await self.get_by_id(person_id)

        film_service = FilmService(self.elastic, self.cache_storage)
        try:
            films = await film_service.get_list(
                person=person_id,
                fields=['id', 'title', 'directors', 'writers', 'actors'])
        except NotFoundError:
            return None

        if not films:
            return [person]

        print('films:')
        pprint(films)
        persons_films = []
        self._set_films_for_person(persons_films, person_id,
                                   person.full_name, films)

        if not persons_films:
            return [person]

        return persons_films

    def _set_films_for_person(
            self,
            persons_films: list,
            person_id: str,
            person_name: str,
            films: dict
    ) -> None:
        """
        Parse films ids by roles for person id and add them to general list
        of persons films
        """

        roles = {
            ('directors', 'director'): [],
            ('writers', 'writer'): [],
            ('actors', 'actor'): []
        }

        def cond_func(item):
            return item.id == person_id

        for film in films:
            for role in roles:
                if list(filter(cond_func, getattr(film, role[0]))):
                    roles[role].append(film.id)

        for role in roles:
            if roles[role]:
                persons_films.append(
                    Person(id=person_id, full_name=person_name,
                           role=role[1], film_ids=roles[role])
                )


@lru_cache()
def get_person_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
        cache_storage: ICache = Depends(get_cache_storage)
) -> PersonService:
    return PersonService(elastic, cache_storage)
