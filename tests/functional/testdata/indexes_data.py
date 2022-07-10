RU_EN_SETTINGS = {
    'refresh_interval': '1s',
    'analysis': {
        'filter': {
            'english_stop': {
                'type': 'stop',
                'stopwords': '_english_'
            },
            'english_stemmer': {
                'type': 'stemmer',
                'language': 'english'
            },
            'english_possessive_stemmer': {
                'type': 'stemmer',
                'language': 'possessive_english'
            },
            'russian_stop': {
                'type': 'stop',
                'stopwords': '_russian_'
            },
            'russian_stemmer': {
                'type': 'stemmer',
                'language': 'russian'
            }
        },
        'analyzer': {
            'ru_en': {
                'tokenizer': 'standard',
                'filter': [
                    'lowercase',
                    'english_stop',
                    'english_stemmer',
                    'english_possessive_stemmer',
                    'russian_stop',
                    'russian_stemmer'
                ]
            }
        }
    }
}
MOVIES_MAPPING = {
    'dynamic': 'strict',
    'properties': {
        'id': {
            'type': 'keyword'
        },
        'imdb_rating': {
            'type': 'float'
        },
        'genres': {
            'type': 'nested',
            'dynamic': 'strict',
            'properties': {
                'id': {
                    'type': 'keyword'
                },
                'name': {
                    'type': 'text',
                    'analyzer': 'ru_en'
                }
            }
        },
        'title': {
            'type': 'text',
            'analyzer': 'ru_en',
            'fields': {
                'raw': {
                    'type': 'keyword'
                }
            }
        },
        'description': {
            'type': 'text',
            'analyzer': 'ru_en'
        },
        'directors': {
            'type': 'nested',
            'dynamic': 'strict',
            'properties': {
                'id': {
                    'type': 'keyword'
                },
                'full_name': {
                    'type': 'text',
                    'analyzer': 'ru_en'
                }
            }
        },
        'actors_names': {
            'type': 'text',
            'analyzer': 'ru_en'
        },
        'writers_names': {
            'type': 'text',
            'analyzer': 'ru_en'
        },
        'actors': {
            'type': 'nested',
            'dynamic': 'strict',
            'properties': {
                'id': {
                    'type': 'keyword'
                },
                'full_name': {
                    'type': 'text',
                    'analyzer': 'ru_en'
                }
            }
        },
        'writers': {
            'type': 'nested',
            'dynamic': 'strict',
            'properties': {
                'id': {
                    'type': 'keyword'
                },
                'full_name': {
                    'type': 'text',
                    'analyzer': 'ru_en'
                }
            }
        }
    }
}
GENRES_MAPPING = {
    'dynamic': 'strict',
    'properties': {
        'id': {
            'type': 'keyword'
        },
        'name': {
            'type': 'text',
            'analyzer': 'ru_en',
        },
    }
}
PERSONS_MAPPING = {
    'dynamic': 'strict',
    'properties': {
        'id': {
            'type': 'keyword'
        },
        'full_name': {
            'type': 'text',
            'analyzer': 'ru_en',
        },
    }
}

films_data = [
    {
        'id': f'Bill_Gates_{i}',
        'title': f'Walt Disney {genre[1]} stories start at {i}',
        'description': 'Elon Musk approved!' if i > 0 else 'Jeff Bezos 2',
        'imdb_rating': 10.0 - i,
        'directors': [{'id': 'Henry', 'full_name': 'Henry Sage'}] if i < 2 else [],
        'writers': [
            {'id': 'Henry2', 'full_name': 'Henry Ford'},
            {'id': 'John', 'full_name': 'John Rockefeller'}
        ] if i == 0 else [],
        'actors': [{'id': 'John', 'full_name': 'John Rockefeller'}],
        'genres': [{'id': genre[0], 'name': genre[1]}]
    } for i, genre in
    enumerate([('C', 'comedy'), ('H', 'horror'), ('H', 'horror')])
]

genres_data = [{'id': f'{i}', 'name': f'Murdock_{i}'} for i in range(2)]

persons_data = [
    {'id': 'Henry', 'full_name': 'Henry Sage'},
    {'id': 'Henry2', 'full_name': 'Henry Ford'},
    {'id': 'John', 'full_name': 'John Rockefeller'}
]

INDEXES_DATA = {
    'movies_index': {
        'name': 'movies',
        'mappings': MOVIES_MAPPING,
        'settings': RU_EN_SETTINGS,
        'test_data': films_data
    },
    'genres_index': {
        'name': 'genres',
        'mappings': GENRES_MAPPING,
        'settings': RU_EN_SETTINGS,
        'test_data': genres_data
    },
    'persons_index': {
        'name': 'persons',
        'mappings': PERSONS_MAPPING,
        'settings': RU_EN_SETTINGS,
        'test_data': persons_data
    }
}

films_data_result = [
    {
        'id': f'Bill_Gates_{i}',
        'title': f'Walt Disney {genre[1]} stories start at {i}',
        'imdb_rating': 10.0 - i,
    } for i, genre in
    enumerate([('C', 'comedy'), ('H', 'horror'), ('H', 'horror')])
]
persons_data_result = [
    {
        'id': 'Henry', 'full_name': 'Henry Sage',
        'role': 'director', 'film_ids': ['Bill_Gates_0', 'Bill_Gates_1']
    },
    {
        'id': 'Henry2', 'full_name': 'Henry Ford',
        'role': 'writer', 'film_ids': ['Bill_Gates_0']
    },
    {
        'id': 'John', 'full_name': 'John Rockefeller',
        'role': 'writer', 'film_ids': ['Bill_Gates_0']
    },
    {
        'id': 'John', 'full_name': 'John Rockefeller',
        'role': 'actor',
        'film_ids': ['Bill_Gates_0', 'Bill_Gates_1', 'Bill_Gates_2']
    }
]
