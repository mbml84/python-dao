from typing import Callable
import json
from python_dao.cache.utils import create_key
from python_dao.cache.adapters import CacheAdapter
from python_dao.exceptions import NoResultFound, MultipleResultFound
import os


def base_decorator(
        cache_adapter: CacheAdapter,
        result_formatter: Callable = None
):
    def fetch(
            cls,
            many: bool = True,
            raise_exception: bool = False,
            retrieve_from_cache: bool = True,
            cache_time: int = None
    ):
        if cache_time is None:
            cache_time = os.getenv('DAO_CACHE_TIME', 0)

        def decorator(func: Callable):
            def wrapper(*args, **kwargs):

                results = cache_adapter.get(*args, **kwargs) if cache_adapter and retrieve_from_cache else None

                if not results:
                    results = func(*args, **kwargs)
                    if result_formatter:
                        results = result_formatter(results)

                    if not results and raise_exception:
                        raise NoResultFound()

                    if not many and len(results) > 1:
                        raise MultipleResultFound()

                    if cache_time:
                        cache_key = create_key(*args, **kwargs)
                        cache_adapter.set(
                            cache_key,
                            json.dumps(results).encode('utf-8'),
                            cache_time
                        )

                    results = [cls(**attributes) for attributes in results]

                    if not many:
                        results = results[0] if results else None

                return results

            return wrapper

        return decorator

    return fetch
