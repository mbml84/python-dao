"""
Exceptions for data fetching
"""
from __future__ import annotations

from typing import Callable


class NoResultFound(BaseException):
    """
    Exception for cases when no result are returned but at least one was expected
    """

    def __init__(self, func: Callable):
        super().__init__(f'No result found found for {func.__name__}')


class MultipleResultFound(BaseException):
    """
    Exception for cases when multiple results were returned but only one was expected
    """

    def __init__(self, func: Callable):
        super().__init__(f'Multiple results returned for {func.__name__}')


__all__ = [
    'MultipleResultFound',
    'NoResultFound',
]
