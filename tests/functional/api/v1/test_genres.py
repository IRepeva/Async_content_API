import pytest

from api.v1.utils.errors import NotFoundDetail
from conftest import elastic_tear_down
from testdata.indexes_data import genres_data

pytestmark = pytest.mark.asyncio

INDEX = 'genres_index'
URL_PREFIX = '/genres'


async def test_genre_id_detailed(es_client, make_get_request):
    genre_num = 0
    url = URL_PREFIX + f"/{genres_data[genre_num]['id']}"

    # getting data from elastic
    response = await make_get_request(url)

    assert response.status == 200
    assert response.body == genres_data[genre_num]

    # getting data from cache
    await elastic_tear_down(es_client)

    response = await make_get_request(url)

    assert response.status == 200
    assert response.body == genres_data[genre_num]


async def test_genres(es_client, make_get_request):
    url = URL_PREFIX

    # getting data from elastic
    response = await make_get_request(url)

    assert response.status == 200
    assert response.body == genres_data

    # getting data from cache
    await elastic_tear_down(es_client)

    response = await make_get_request(url)

    assert response.status == 200
    assert response.body == genres_data


async def test_genre_not_found(make_get_request):
    url = URL_PREFIX + '/Faraday'

    response = await make_get_request(url)

    assert response.status == 404
    assert response.body['detail'] == NotFoundDetail.GENRE
