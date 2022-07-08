import sys

import pytest

from testdata.indexes_data import films_data, INDEXES_DATA
from utils.data_preparation.data_preparer import (
    ElasticDataPreparer, RedisDataPreparer
)


sys.path.append('/app/api/v1/utils/cache')
sys.path.append('/api/v1/utils/cache')
sys.path.append('.')
print(sys.path)
from api.v1.utils.errors import NotFoundDetail
from app.api.v1.utils.cache import get_cache_key

pytestmark = pytest.mark.asyncio

INDEX = 'movies_index'
URL_PREFIX = '/films'


async def test_film_id_detailed(es_client, redis_client,
                                make_get_request):
    film_num = 0
    url = URL_PREFIX + f"/{films_data[film_num]['id']}"

    redis_client.flushall()

    # # film not found
    # redis = RedisDataPreparer(redis_client)
    # await redis.clear_all()
    #
    # response = await make_get_request(url)
    #
    # assert response.status == 404
    # assert response.body['detail'] == NotFoundDetail.FILM

    # getting data from elastic
    response = await make_get_request(url)

    assert response.status == 200
    assert response.body == films_data[film_num]

    # getting data from cache
    # await elastic.clear_all()
    #
    # response = await make_get_request(url)
    cache_key = get_cache_key({'film_id': films_data[film_num]['id']})
    cache_result = redis_client.get(cache_key)

    assert cache_result == films_data[film_num]


# @pytest.mark.parametrize("url, query_params, expected_length, expected_body", (
#         (  # Getting all films
#             '/', None, 3,
#             [
#                 {
#                     'id': f'Bill_Gates_0',
#                     'title': f'Walt Disney comedy stories start at 0',
#                     'imdb_rating': 10.0,
#                 },
#                 {
#                     'id': f'Bill_Gates_1',
#                     'title': f'Walt Disney horror stories start at 1',
#                     'imdb_rating': 9.0,
#                 },
#                 {
#                     'id': f'Bill_Gates_2',
#                     'title': f'Walt Disney horror stories start at 2',
#                     'imdb_rating': 8.0,
#                 }
#             ]
#         ),
#         (  # Getting all films sorted by rating asc
#             '/', {'sort': 'imdb_rating'}, 3,
#             [
#                 {
#                     'id': f'Bill_Gates_2',
#                     'title': f'Walt Disney horror stories start at 2',
#                     'imdb_rating': 8.0,
#                 },
#                 {
#                     'id': f'Bill_Gates_1',
#                     'title': f'Walt Disney horror stories start at 1',
#                     'imdb_rating': 9.0,
#                 },
#                 {
#                     'id': f'Bill_Gates_0',
#                     'title': f'Walt Disney comedy stories start at 0',
#                     'imdb_rating': 10.0,
#                 }
#             ]
#         ),
#         (  # Getting all movies with pagination (default page number)
#             '/', {'page[size]': 2}, 2,
#             [
#                 {
#                     'id': f'Bill_Gates_0',
#                     'title': f'Walt Disney comedy stories start at 0',
#                     'imdb_rating': 10.0,
#                 },
#                 {
#                     'id': f'Bill_Gates_1',
#                     'title': f'Walt Disney horror stories start at 1',
#                     'imdb_rating': 9.0,
#                 }
#             ]
#         ),
#         (  # Getting all movies with pagination (custom page number)
#             '/', {'page[size]': 2, 'page[number]': 2}, 1,
#             [
#                 {
#                     'id': f'Bill_Gates_2',
#                     'title': f'Walt Disney horror stories start at 2',
#                     'imdb_rating': 8.0,
#                 }
#             ]
#         ),
#         (  # Getting movies of specific genre
#             '/', {'filter[genre]': 'H'}, 2,
#             [
#                 {
#                     'id': f'Bill_Gates_1',
#                     'title': f'Walt Disney horror stories start at 1',
#                     'imdb_rating': 9.0,
#                 },
#                 {
#                     'id': f'Bill_Gates_2',
#                     'title': f'Walt Disney horror stories start at 2',
#                     'imdb_rating': 8.0,
#                 }
#             ]
#         ),
#         (  # Getting movies similar to specific film
#             '/', {'similar_to': 'Bill_Gates_1'}, 1,
#             [
#                 {
#                     'id': f'Bill_Gates_2',
#                     'title': f'Walt Disney horror stories start at 2',
#                     'imdb_rating': 8.0,
#                 }
#             ]
#         ),
#         (  # Getting movies with no query search
#             '/search', None, 3,
#             [
#                 {
#                     'id': f'Bill_Gates_0',
#                     'title': f'Walt Disney comedy stories start at 0',
#                     'imdb_rating': 10.0,
#                 },
#                 {
#                     'id': f'Bill_Gates_1',
#                     'title': f'Walt Disney horror stories start at 1',
#                     'imdb_rating': 9.0,
#                 },
#                 {
#                     'id': f'Bill_Gates_2',
#                     'title': f'Walt Disney horror stories start at 2',
#                     'imdb_rating': 8.0,
#                 }
#             ]
#         ),
#         (  # Getting movies with query in title
#             '/search', {'query': 'horror'}, 2,
#             [
#                 {
#                     'id': f'Bill_Gates_1',
#                     'title': f'Walt Disney horror stories start at 1',
#                     'imdb_rating': 9.0,
#                 },
#                 {
#                     'id': f'Bill_Gates_2',
#                     'title': f'Walt Disney horror stories start at 2',
#                     'imdb_rating': 8.0,
#                 }
#             ]
#         ),
#         (  # Getting movies with query in title and description
#             '/search', {'query': '2'}, 2,
#             [
#                 {
#                     'id': f'Bill_Gates_2',
#                     'title': f'Walt Disney horror stories start at 2',
#                     'imdb_rating': 8.0,
#                 },
#                 {
#                     'id': f'Bill_Gates_0',
#                     'title': f'Walt Disney comedy stories start at 0',
#                     'imdb_rating': 10.0,
#                 }
#             ]
#         ),
# ))
# async def test_films(url, query_params, expected_length, expected_body,
#                      es_client, redis_client, make_get_request):
#
#     # getting data from elastic
#     url = URL_PREFIX + url if url else URL_PREFIX
#
#     # redis = RedisDataPreparer(redis_client)
#     await redis_client.flushall()
#
#     # elastic = ElasticDataPreparer(es_client)
#     # await elastic.load(index=INDEXES_DATA[INDEX], data=films_data)
#
#     response = await make_get_request(url, query_params)
#
#     assert response.status == 200
#     assert len(response.body) == expected_length
#     assert response.body == expected_body
#
#     # getting data from cache
#
#     cache_key = get_cache_key(**query_params)
#     cache_result = redis_client.get(cache_key)
#
#     assert len(cache_result) == expected_length
#     assert cache_result == expected_body
#
#     # await elastic.clear_all()
#     #
#     # response = await make_get_request(url, query_params)
#     #
#     # assert response.status == 200
#     # assert len(response.body) == expected_length
#     # assert response.body == expected_body
#
#
# @pytest.mark.parametrize("url, query_params", (
#         (  # Zero page size
#             '/Lifschitz', {}
#         ),
#         (  # Zero page size
#             '/', {'page[size]': 0}
#         ),
#         (  # Page number greater than the last one
#             '/', {'page[size]': 1, 'page[number]': 77}
#         ),
#         (  # Genre doesn't exist
#             '/', {'filter[genre]': 'Its too serious to laugh'},
#         ),
#         (  # No search results
#             '/search', {'query': 'Dont mess up with Feynman'},
#         ),
# ))
# async def test_films_not_found(url, query_params,
#                                es_client, redis_client, make_get_request):
#
#     url = URL_PREFIX + url
#
#     redis = RedisDataPreparer(redis_client)
#     await redis.clear_all()
#
#     elastic = ElasticDataPreparer(es_client)
#     await elastic.load(index=INDEXES_DATA[INDEX], data=films_data)
#
#     response = await make_get_request(url, query_params)
#
#     assert response.status == 404
#     assert response.body['detail'] == NotFoundDetail.FILMS
#
#     await elastic.clear_all()
