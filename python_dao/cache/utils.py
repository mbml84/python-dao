"""
Utils for caching
"""
from __future__ import annotations

import hashlib
import pickle


def create_key(*args, **kwargs) -> str:
    """
    Create a cache keys from arguments.

    Args:
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        str: A cache key

    Notes:
        All args an kwargs must be serializable with pickle

    """

    key = hashlib.sha256(pickle.dumps(args))
    key.update(pickle.dumps(kwargs))

    return key.hexdigest()


__all__ = [
    'create_key',
]
