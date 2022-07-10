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