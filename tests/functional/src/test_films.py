import pytest

from utils.data_preparation.data_preparer import ElasticDataPreparer
from utils.data_preparation.indexes import INDEXES_DATA

pytestmark = pytest.mark.asyncio

INDEX = 'movies_index'
URL_PREFIX = '/films'


@pytest.mark.parametrize("expected", (
        (  # success action
                True
        ),
))
async def test_film_id_detailed(expected, es_client, make_get_request):
    # Заполнение данных для теста
    film_data = {
        'id': '666', 'title': 'Funny stories about satan',
        'description': 'Dive into the world of fascinating adventures!',
        'imdb_rating': 10.0, 'directors': [{'id': 'M', 'full_name': 'Martin'}],
        'writers': [{'id': 'L', 'full_name': 'Luther'}],
        'actors': [{'id': 'K', 'full_name': 'King'}],
        # 'actors_names': ['King'], 'writers_names': ['Luther'],
        'genres': [{'id': 'A', 'name': 'Adventures'}]
    }
    data_preparer = ElasticDataPreparer(es_client)
    await data_preparer.load(index=INDEXES_DATA[INDEX], data=[film_data])

    # Выполнение запроса
    url = URL_PREFIX + f"/{film_data['id']}"
    print(f'url: {url}')
    response = await make_get_request(url)

    # Проверка результата
    assert response.status == 200
    # assert len(response.body) == 1

    assert response.body == film_data

#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("expected", (
#         (  # success action
#                 True
#         ),
# ))
# async def test_search_detailed(expected, es_client, make_get_request):
#     # Заполнение данных для теста
#     data_preparer = ElasticDataPreparer(es_client)
#     await data_preparer.load(index=INDEXES_DATA[INDEX], data=[{}])
#
#     # Выполнение запроса
#     url = URL_PREFIX + '/search'
#     response = await make_get_request(url, {'search': 'Star Wars'})
#
#     # Проверка результата
#     assert response.status == 200
#     assert len(response.body) == 1
#
#     assert response.body == expected
