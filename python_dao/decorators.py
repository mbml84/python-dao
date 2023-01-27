"""
Decorators
"""
from __future__ import annotations

import json
from typing import Any
from typing import Callable

from python_dao.cache.adapters import CacheAdapter
from python_dao.cache.utils import create_key
from python_dao.exceptions import MultipleResultFound
from python_dao.exceptions import NoResultFound


def build_fetch_decorator(
        cache_adapter: CacheAdapter | None = None,
        result_formatter: Callable[[Any], dict[str, Any]] = dict,
) -> Callable[[Callable[[Any], object], bool, bool, bool, int], Callable]:
    """
    Create a decorator factory for fetching operation.

    Args:
        cache_adapter (CacheAdapter): The caching object if caching is needed.
            If None is passed, there will be no caching.
            Default : None
        result_formatter (Callable[[Any], dict[str, Any]]): A callable to format the raw output
            into a dictionary of attributes.
            Default : dict

    Returns:
        Callable[[Callable[[Any], object], bool, bool, bool, int], Callable]:
            A fetch decorator factory
    """

    def decorator_factory(
        cls: Callable[[Any], object],
        many: bool = True,
        raise_exception: bool = False,
        retrieve_from_cache: bool = True,
        cache_time: int = 0,
    ) -> Callable[[Callable], Callable]:
        """
        Create a decorator for fetching operation.

        Args:
            cls (Callable[[Any], object]): A callable that will create an object.
                This can be a class.
            many (bool): Indicates if many results will be returned.
                Default : True
            raise_exception (bool): Indicates if an exceptions must be raised
                when no results are found.
                Default : False
            retrieve_from_cache (bool): Indicates if results must be be fetch from cache.
                If they aren't found in the cache, they'll be fetch from the decorated function.
                Default : True
            cache_time (int): The cache duration in seconds
                Default : 0

        Returns:
            Callable[[Callable], Callable]: A decorator factory
        """

        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):

                results = (
                    cache_adapter.get(*args, **kwargs)
                    if cache_adapter and retrieve_from_cache
                    else None
                )

                if not results:
                    results = func(*args, **kwargs)

                    if not results and raise_exception:
                        raise NoResultFound()

                    if not many and len(results) > 1:
                        raise MultipleResultFound()

                    if cache_time:
                        cache_key = create_key(*args, **kwargs)
                        cache_adapter.set(
                            cache_key, json.dumps(results).encode(
                                'utf-8',
                            ), cache_time,
                        )

                    results = [cls(**result_formatter(result)) for result in results]

                    if not many:
                        results = results[0] if results else None

                return results

            return wrapper

        return decorator

    return decorator_factory


__all__ = [
    'build_fetch_decorator',
]
