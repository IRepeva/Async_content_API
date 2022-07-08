# import pytest
#
# from testdata.indexes_data import INDEXES_DATA
# from utils.data_preparation.data_preparer import (
#     ElasticDataPreparer, RedisDataPreparer
# )
# from utils.errors import NotFoundDetail
#
# pytestmark = pytest.mark.asyncio
#
# INDEX = 'genres_index'
# URL_PREFIX = '/genres'
#
#
# async def test_genre_id_detailed(es_client, redis_client,
#                                  make_get_request):
#     id_ = 0
#     url = URL_PREFIX + f"/{id_}"
#
#     # genre not found
#     redis = RedisDataPreparer(redis_client)
#     await redis.clear_all()
#
#     response = await make_get_request(url)
#
#     assert response.status == 404
#     assert response.body['detail'] == NotFoundDetail.GENRE
#
#     # getting data from elastic
#     elastic = ElasticDataPreparer(es_client)
#     await elastic.load(index=INDEXES_DATA[INDEX], data=genres_data)
#
#     response = await make_get_request(url)
#
#     assert response.status == 200
#     assert response.body == genres_data[id_]
#
#     # getting data from cache
#     await elastic.clear_all()
#
#     response = await make_get_request(url)
#
#     assert response.status == 200
#     assert response.body == genres_data[id_]
#
#
# @pytest.mark.parametrize("expected_length, expected_body", (
#         (  # Getting all genres
#                 2, [{'id': '0', 'name': f'100'}, {'id': '1', 'title': f'101'}]
#         ),
# ))
# async def test_films(expected_length, expected_body,
#                      es_client, redis_client, make_get_request):
#     # getting data from elastic
#     url = URL_PREFIX
#
#     redis = RedisDataPreparer(redis_client)
#     await redis.clear_all()
#
#     elastic = ElasticDataPreparer(es_client)
#     await elastic.load(index=INDEXES_DATA[INDEX], data=genres_data)
#
#     response = await make_get_request(url)
#
#     assert response.status == 200
#     assert len(response.body) == expected_length
#     assert response.body == expected_body
#
#     # getting data from cache
#     await elastic.clear_all()
#
#     response = await make_get_request(url)
#
#     assert response.status == 200
#     assert len(response.body) == expected_length
#     assert response.body == expected_body
