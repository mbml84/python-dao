"""
Cache adapter module. Contains everything need to build a compatible cache adapter
"""
from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any


class CacheAdapter(ABC):
    """
    Base CacheAdapter class to use as a frontend to different cache backend
    """

    @abstractmethod
    def set(self, key: str | bytes, value: bytes, cache_time: int) -> None:
        """
        Set a value in cache

        Args:
            key (str | bytes): The cache key
            value (bytes): The value to cache
            cache_time (int): The cache duration in seconds

        """

    @abstractmethod
    def get(self, key: str | bytes) -> list[dict[str, Any]] | None:
        """
        Get from cache

        Args:
            key (str | bytes): The cache key

        Returns:
            dict | None: The result fetched from cache
        """


__all__ = [
    'CacheAdapter',
]
