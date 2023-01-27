"""
Exceptions for data fetching
"""
from __future__ import annotations


class NoResultFound(BaseException):
    """
    Exception for cases when no result are returned but at least one was expected
    """


class MultipleResultFound(BaseException):
    """
    Exception for cases when multiple results were returned but only one was expected
    """


__all__ = [
    'MultipleResultFound',
    'NoResultFound',
]
