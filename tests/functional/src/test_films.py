import pytest

from utils.data_preparation.data_preparer import (
    ElasticDataPreparer, RedisDataPreparer
)
from utils.data_preparation.indexes import INDEXES_DATA
from utils.errors import NotFoundDetail

pytestmark = pytest.mark.asyncio

INDEX = 'movies_index'
URL_PREFIX = '/films'


async def test_film_id_detailed(es_client, redis_client,
                                make_get_request):
    film_data = {
        'id': '666', 'title': 'Funny stories about satan',
        'description': 'Dive into the world of fascinating adventures!',
        'imdb_rating': 10.0, 'directors': [{'id': 'M', 'full_name': 'Martin'}],
        'writers': [{'id': 'L', 'full_name': 'Luther'}],
        'actors': [{'id': 'K', 'full_name': 'King'}],
        'genres': [{'id': 'A', 'name': 'Adventures'}]
    }
    url = URL_PREFIX + f"/{film_data['id']}"

    # film not found
    redis = RedisDataPreparer(redis_client)
    await redis.clear_all()

    response = await make_get_request(url)

    assert response.status == 404
    assert response.body['detail'] == NotFoundDetail.FILM

    # getting data from elastic
    elastic = ElasticDataPreparer(es_client)
    await elastic.load(index=INDEXES_DATA[INDEX], data=[film_data])

    response = await make_get_request(url)

    assert response.status == 200
    assert response.body == film_data

    # TODO uncomment when cache is ready
    # getting data from cache
    await elastic.clear_all()
    #
    # response = await make_get_request(url)
    #
    # assert response.status == 200
    # assert response.body == film_data


@pytest.mark.parametrize("url, query_params, expected_length, expected_body", (
        (  # Getting all films
            '/', None, 3,
            [
                {
                    'id': f'Bill_Gates_0',
                    'title': f'Walt Disney comedy stories start at 0',
                    'imdb_rating': 10.0,
                },
                {
                    'id': f'Bill_Gates_1',
                    'title': f'Walt Disney horror stories start at 1',
                    'imdb_rating': 9.0,
                },
                {
                    'id': f'Bill_Gates_2',
                    'title': f'Walt Disney horror stories start at 2',
                    'imdb_rating': 8.0,
                }
            ]
        ),
        (  # Getting all films sorted by rating asc
            '/', {'sort': 'imdb_rating'}, 3,
            [
                {
                    'id': f'Bill_Gates_2',
                    'title': f'Walt Disney horror stories start at 2',
                    'imdb_rating': 8.0,
                },
                {
                    'id': f'Bill_Gates_1',
                    'title': f'Walt Disney horror stories start at 1',
                    'imdb_rating': 9.0,
                },
                {
                    'id': f'Bill_Gates_0',
                    'title': f'Walt Disney comedy stories start at 0',
                    'imdb_rating': 10.0,
                }
            ]
        ),
        (  # Getting all movies with pagination (default page number)
            '/', {'page[size]': 2}, 2,
            [
                {
                    'id': f'Bill_Gates_0',
                    'title': f'Walt Disney comedy stories start at 0',
                    'imdb_rating': 10.0,
                },
                {
                    'id': f'Bill_Gates_1',
                    'title': f'Walt Disney horror stories start at 1',
                    'imdb_rating': 9.0,
                }
            ]
        ),
        (  # Getting all movies with pagination (custom page number)
            '/', {'page[size]': 2, 'page[number]': 2}, 1,
            [
                {
                    'id': f'Bill_Gates_2',
                    'title': f'Walt Disney horror stories start at 2',
                    'imdb_rating': 8.0,
                }
            ]
        ),
        (  # Getting movies of specific genre
            '/', {'filter[genre]': 'H'}, 2,
            [
                {
                    'id': f'Bill_Gates_1',
                    'title': f'Walt Disney horror stories start at 1',
                    'imdb_rating': 9.0,
                },
                {
                    'id': f'Bill_Gates_2',
                    'title': f'Walt Disney horror stories start at 2',
                    'imdb_rating': 8.0,
                }
            ]
        ),
        (  # Getting movies similar to specific film
            '/', {'similar_to': 'Bill_Gates_1'}, 1,
            [
                {
                    'id': f'Bill_Gates_2',
                    'title': f'Walt Disney horror stories start at 2',
                    'imdb_rating': 8.0,
                }
            ]
        ),
        (  # Getting movies with no query search
            '/search', None, 3,
            [
                {
                    'id': f'Bill_Gates_0',
                    'title': f'Walt Disney comedy stories start at 0',
                    'imdb_rating': 10.0,
                },
                {
                    'id': f'Bill_Gates_1',
                    'title': f'Walt Disney horror stories start at 1',
                    'imdb_rating': 9.0,
                },
                {
                    'id': f'Bill_Gates_2',
                    'title': f'Walt Disney horror stories start at 2',
                    'imdb_rating': 8.0,
                }
            ]
        ),
        (  # Getting movies with query in title
            '/search', {'query': 'horror'}, 2,
            [
                {
                    'id': f'Bill_Gates_1',
                    'title': f'Walt Disney horror stories start at 1',
                    'imdb_rating': 9.0,
                },
                {
                    'id': f'Bill_Gates_2',
                    'title': f'Walt Disney horror stories start at 2',
                    'imdb_rating': 8.0,
                }
            ]
        ),
        (  # Getting movies with query in title and description
            '/search', {'query': '2'}, 2,
            [
                {
                    'id': f'Bill_Gates_2',
                    'title': f'Walt Disney horror stories start at 2',
                    'imdb_rating': 8.0,
                },
                {
                    'id': f'Bill_Gates_0',
                    'title': f'Walt Disney comedy stories start at 0',
                    'imdb_rating': 10.0,
                }
            ]
        ),
))
async def test_films(url, query_params, expected_length, expected_body,
                     es_client, redis_client, make_get_request):
    genres = [('C', 'comedy'), ('H', 'horror'), ('H', 'horror')]
    films_data = [
        {
            'id': f'Bill_Gates_{i}',
            'title': f'Walt Disney {genre[1]} stories start at {i}',
            'description': 'Elon Musk approved!' if i > 0 else 'Jeff Bezos 2',
            'imdb_rating': 10.0 - i,
            'directors': [{'id': 'Steve', 'full_name': 'Vozniak'}],
            'writers': [{'id': 'Henry', 'full_name': 'Ford'}],
            'actors': [{'id': 'John', 'full_name': 'Rockefeller'}],
            'genres': [{'id': genre[0], 'name': genre[1]}]
        } for i, genre in enumerate(genres)
    ]

    # getting data from elastic
    url = URL_PREFIX + url if url else URL_PREFIX

    redis = RedisDataPreparer(redis_client)
    await redis.clear_all()

    elastic = ElasticDataPreparer(es_client)
    await elastic.load(index=INDEXES_DATA[INDEX], data=films_data)

    response = await make_get_request(url, query_params)

    assert response.status == 200
    assert len(response.body) == expected_length
    assert response.body == expected_body

    # TODO uncomment when cache is ready
    # getting data from cache
    await elastic.clear_all()
    #
    # response = await make_get_request(url, query_params)
    #
    # assert response.status == 200
    # assert len(response.body) == expected_length
    # assert response.body == expected_body


@pytest.mark.parametrize("url, query_params", (
        (  # Zero page size
                '/', {'page[size]': 0}
        ),
        (  # Page number greater than the last one
                '/', {'page[size]': 1, 'page[number]': 77}
        ),
        (  # Genre doesn't exist
                '/', {'filter[genre]': 'Its too serious to laugh'},
        ),
        (  # No search results
                '/search', {'query': 'Dont mess up with Feynman'},
        ),
))
async def test_films_not_found(url, query_params,
                               es_client, redis_client, make_get_request):
    films_data = [
        {
            'id': 'Dont believe these guys!', 'title': 'Physics is the best!',
            'description': 'Physicists never laugh',
            'imdb_rating': 100.0,
            'directors': [{'id': 'F', 'full_name': 'Faraday'}],
            'writers': [{'id': 'L', 'full_name': 'Lifschitz'}],
            'actors': [{'id': 'M', 'full_name': 'Maxwell'}],
            'genres': [{'id': 'PA', 'name': 'Physics Action'}]
        }
    ]

    url = URL_PREFIX + url

    redis = RedisDataPreparer(redis_client)
    await redis.clear_all()

    elastic = ElasticDataPreparer(es_client)
    await elastic.load(index=INDEXES_DATA[INDEX], data=films_data)

    response = await make_get_request(url, query_params)

    assert response.status == 404
    assert response.body['detail'] == NotFoundDetail.FILMS

    await elastic.clear_all()
