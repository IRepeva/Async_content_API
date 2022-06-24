from functools import wraps

from fastapi import Depends, Request

from api.v1.utils.query_parser import QueryParser
from services.films import FilmService, get_film_service, BaseService


def arg_parser():
    def func_wrapper(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            print(f'!!!!!! input: {args}, {kwargs}')
            result_kwargs = kwargs.copy()
            for arg_name, arg in kwargs.items():
                if isinstance(arg, Request):
                    query_params = dict(arg.query_params)
                    parsed_params, paginator = QueryParser.parse_params(query_params)
                    print(f'!!!!! parsed_params: {parsed_params}')
                    result_kwargs.update(parsed_params)
                    result_kwargs.update({'paginator': paginator})
            print(f'dexorate: {args}, {result_kwargs}')
            return await func(*args, **result_kwargs)

        return wrapper
    return func_wrapper


#
# class Cache:
#     def __init__(self, func):
#         print(f'in init, {func}')
#         self.func = func
#
#     def __call__(self, *args, **kwargs):
#         print("Decorating", self.func.__name__, kwargs, args)
#         return self.func(*args, **kwargs)
class Cache:
    def __init__(self, *args, **kwargs):
        self.cache_args = args
        self.cache_kwargs = kwargs

    def __call__(self, function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            print("Decorating", function.__name__, kwargs, args)
            # cache_key = self.get_key()
            result = await function(*args, **kwargs)
            return result

        return wrapper


def cache_hits(*args, **kwargs):
    def _cache(function):
        return Cache(function, *args, **kwargs)

    return _cache


@Cache
async def film_details(
        film_id: str,
        film_service: FilmService = Depends(get_film_service)
):
    return
# film_details(6)
