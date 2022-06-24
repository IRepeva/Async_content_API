from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.models_api.film import FilmDetails, Film
from api.v1.utils.errors import NotFoundDetail
from services.films import FilmService, get_film_service

router = APIRouter()


async def common_parameters(
        sort: str | None = None,
        page: int | None = Query(default=1, alias='page[number]'),
        page_size: int | None = Query(default=50, alias='page[size]')
):
    return {'sort': sort, 'page': page, 'page_size': page_size}


@router.get('/search', response_model=List[Film], summary='Get search results')
async def films_search(
        query: str | None = None,
        common_params: dict = Depends(common_parameters),
        film_service: FilmService = Depends(get_film_service)
) -> List[Film]:
    """
    Search for a movie matching the query parameter 'query'.

    Pagination settings can be passed using 'page[size]' and 'page[number]'
    parameters, default settings are: page size=50, page number=1

    If 'query' is omitted than all movies with pagination settings will be retrieved

    Movie information:
    - **id**: each film has a unique id
    - **title**: film title
    - **imdb_rating**: rating of the movie
    """
    films_list = await film_service.get_list(query=query, **common_params)
    if not films_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=NotFoundDetail.FILMS
        )

    return [Film(**film.dict()) for film in films_list]


@router.get('/{film_id}', response_model=FilmDetails, summary="Get film by id")
async def film_details(
        film_id: str,
        film_service: FilmService = Depends(get_film_service)
) -> FilmDetails:
    """
    Get all film information:

    - **id**: each film has a unique id
    - **title**: film title
    - **description**: short film description
    - **imdb_rating**: rating of the movie
    - **genres**: list of film genres
    - **directors**: list of film directors
    - **writers**: list of film writers
    - **actors**: list of film actors
    """
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=NotFoundDetail.FILM
        )

    return FilmDetails(**film.dict())


@router.get('/', response_model=List[Film], summary='Get all movies')
async def films(
        similar_to: str | None = None,
        genre: str | None = Query(default=None, alias='filter[genre]'),
        common_params: dict = Depends(common_parameters),
        film_service: FilmService = Depends(get_film_service)
) -> List[Film]:
    """
    Get all movies with pagination settings.

    Pagination settings can be passed using 'page[size]' and 'page[number]'
    parameters, default settings are: page size=50, page number=1

    Movie information:
    - **id**: each film has a unique id
    - **title**: film title
    - **imdb_rating**: rating of the movie
    """
    films_list = await film_service.get_list(genre=genre, similar_to=similar_to,
                                             **common_params)
    if not films_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=NotFoundDetail.FILMS
        )
    return [Film(**film.dict()) for film in films_list]
