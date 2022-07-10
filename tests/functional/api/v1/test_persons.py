import pytest

from api.v1.utils.errors import NotFoundDetail
from conftest import elastic_tear_down
from testdata.indexes_data import persons_data, persons_data_result, \
    films_data_result

pytestmark = pytest.mark.asyncio

INDEX = 'persons_index'
URL_PREFIX = '/persons'
person_num = 0
person_id = persons_data[person_num]['id']


async def test_person_id_detailed(es_client, make_get_request):

    url = URL_PREFIX + f"/{person_id}"

    # getting data from elastic
    response = await make_get_request(url)

    assert response.status == 200
    assert response.body == [persons_data_result[person_num]]

    # getting data from cache
    await elastic_tear_down(es_client)

    response = await make_get_request(url)

    assert response.status == 200
    assert response.body == [persons_data_result[person_num]]


@pytest.mark.parametrize("url, query_params, expected_body", (
        (  # Getting all persons
            '/search', {}, persons_data_result
        ),
        (  # Getting all persons with pagination (default page number)
            '/search', {'page[size]': 2}, persons_data_result[:2]
        ),
        (  # Getting all persons with pagination (custom page number)
            '/search', {'page[size]': 2, 'page[number]': 2},
            persons_data_result[2:]
        ),
        (  # Getting persons with query
            '/search', {'query': 'John'}, persons_data_result[2:]
        ),
        (  # Getting movies with query in title and description
            '/search', {'query': 'Henry'}, persons_data_result[:2]
        ),
        (  # Getting movies with query in title and description
            f'/{person_id}/film', {}, films_data_result[:2]
        ),
        (  # Getting movies with query in title and description
            f'/{person_id}/film', {}, films_data_result[:2]
        ),
))
async def test_persons(url, query_params, expected_body,
                       es_client, make_get_request):

    # getting data from elastic
    url = URL_PREFIX + url

    response = await make_get_request(url, query_params)

    assert response.status == 200
    assert response.body == expected_body

    # getting data from cache
    await elastic_tear_down(es_client)

    response = await make_get_request(url, query_params)

    assert response.status == 200
    assert response.body == expected_body


@pytest.mark.parametrize("url, query_params, not_found", (
        (  # Zero page size
            '/Maxwell', {},
            NotFoundDetail.PERSON
        ),
        (  # Zero page size
            '/search', {'page[size]': 0},
            NotFoundDetail.PERSONS
        ),
        (  # Page number greater than the last one
            '/search', {'page[size]': 1, 'page[number]': 77},
            NotFoundDetail.PERSONS
        ),
        (  # No search results
            '/search', {'query': 'Dont Be a Menace to South Central...'},
            NotFoundDetail.PERSONS
        ),
))
async def test_persons_not_found(url, query_params, not_found, make_get_request):

    url = URL_PREFIX + url

    response = await make_get_request(url, query_params)

    assert response.status == 404
    assert response.body['detail'] == not_found
