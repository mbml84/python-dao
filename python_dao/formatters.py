"""
Results formatters
"""
from __future__ import annotations

from typing import Any


class DictFormatter:
    """
    A default formatter
    """

    def __call__(
            self,
            results: list[dict[str, Any] | list[tuple[str, Any]]],
    ) -> list[dict[str, Any]]:
        return [dict(result) for result in results]


class ODBCFormatter:
    """
    Formatter for pyodbc cursors
    """

    def __call__(self, cursor) -> list[dict[str, Any]]:
        columns = [name for name, *_ in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


__all__ = [
    'DictFormatter',
    'ODBCFormatter',
]
