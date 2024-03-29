import http

import pytest

from api.v1.utils.errors import NotFoundDetail
from conftest import elastic_tear_down
from testdata.indexes_data import films_data
from testdata.test_data import films_data_result, not_existing_film

pytestmark = pytest.mark.asyncio

INDEX = 'movies_index'
URL_PREFIX = '/films'


async def test_film_id_detailed(es_client, make_get_request):

    # getting not existing ID
    url = URL_PREFIX + f'/{not_existing_film}'
    response = await make_get_request(url)

    assert response.status == http.HTTPStatus.NOT_FOUND
    assert response.body['detail'] == NotFoundDetail.FILM

    test_film = films_data[0]
    url = URL_PREFIX + f"/{test_film['id']}"

    # getting data from elastic
    response = await make_get_request(url)

    assert response.status == http.HTTPStatus.OK
    assert response.body == test_film

    # getting data from cache
    await elastic_tear_down(es_client)

    response = await make_get_request(url)

    assert response.status == http.HTTPStatus.OK
    assert response.body == test_film


@pytest.mark.parametrize("url, query_params, expected_body", (
        (  # Getting all films
            '/', None,
            films_data_result
        ),
        (  # Getting all films sorted by rating asc
            '/', {'sort': 'imdb_rating'},
            films_data_result[::-1]
        ),
        (  # Getting all movies with pagination (default page number)
            '/', {'page[size]': 2},
            films_data_result[:2]
        ),
        (  # Getting all movies with pagination (custom page number)
            '/', {'page[size]': 2, 'page[number]': 2},
            films_data_result[2:]
        ),
        (  # Getting movies of specific genre
            '/', {'filter[genre]': 'H'},
            films_data_result[1:]
        ),
        (  # Getting movies similar to specific film
            '/', {'similar_to': 'Bill_Gates_1'},
            films_data_result[2:]
        ),
        (  # Getting movies with no query search
            '/search', None,
            films_data_result
        ),
        (  # Getting movies with query in title
            '/search', {'query': 'horror'},
            films_data_result[1:]
        ),
        (  # Getting movies with query in title and description
            '/search', {'query': '2'},
            [films_data_result[2], films_data_result[0]]
        ),
))
async def test_films(url, query_params, expected_body,
                     es_client, make_get_request):

    # getting data from elastic
    url = URL_PREFIX + url

    response = await make_get_request(url, query_params)

    assert response.status == http.HTTPStatus.OK
    assert response.body == expected_body

    # getting data from cache
    await elastic_tear_down(es_client)

    response = await make_get_request(url, query_params)

    assert response.status == http.HTTPStatus.OK
    assert response.body == expected_body


@pytest.mark.parametrize("url, query_params", (
        (  # Zero page size
            '/', {'page[size]': 0}
        ),
        (  # Page number greater than the last one
            '/', {'page[size]': 1, 'page[number]': 77}
        ),
        (  # Genre doesn't exist
            '/', {'filter[genre]': 'Its too serious to laugh'}
        ),
        (  # No search results
            '/search', {'query': 'Dont mess up with Feynman'}
        ),
))
async def test_films_not_found(url, query_params, make_get_request):

    url = URL_PREFIX + url

    response = await make_get_request(url, query_params)

    assert response.status == http.HTTPStatus.NOT_FOUND
    assert response.body['detail'] == NotFoundDetail.FILMS
