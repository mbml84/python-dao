"""
Decorators
"""
from __future__ import annotations

import pickle
from dataclasses import dataclass
from typing import Any
from typing import Callable

from python_dao.cache.adapters import CacheAdapter
from python_dao.cache.utils import create_key
from python_dao.exceptions import MultipleResultFound
from python_dao.exceptions import NoResultFound
from python_dao.formatters import DictFormatter


@dataclass(frozen=True)
class DecoratorFactory:
    """
    Create a decorator factory for fetching operation.

    Attributes:
        cache_adapter (CacheAdapter): The caching object if caching is needed.
            If None is passed, there will be no caching.
            Default : None
        result_formatter (Callable[[Any], list[dict[str, Any]]]): A callable to format
            the raw output into a dictionary of attributes.
            Default : DictFormatter
    """

    cache_adapter: CacheAdapter | None = None
    result_formatter: Callable[[Any], list[dict[str, Any]]] = DictFormatter()

    def __call__(
            self,
            cls: Callable[..., object],
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
            Callable[[Callable], Callable]: A decorator
        """

        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs) -> list[object] | object | None:

                objects = (
                    self.cache_adapter.get(create_key(*args, **kwargs))
                    if self.cache_adapter and retrieve_from_cache
                    else None
                )

                if not objects:
                    results = self.result_formatter(func(*args, **kwargs))

                    if not results and raise_exception:
                        raise NoResultFound(func)

                    if not many and len(results) > 1:
                        raise MultipleResultFound(func)

                    if cache_time and self.cache_adapter:
                        cache_key = create_key(*args, **kwargs)
                        self.cache_adapter.set(
                            cache_key, pickle.dumps(results), cache_time,
                        )

                    objects = [cls(**result) for result in results]

                    if not many:
                        objects = objects[0] if objects else None

                return objects

            return wrapper

        return decorator


__all__ = [
    'DecoratorFactory',
]
