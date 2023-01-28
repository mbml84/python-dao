from __future__ import annotations

from dataclasses import dataclass

from python_dao.cache.adapters import CacheAdapter
from python_dao.decorators import DecoratorFactory


@dataclass
class DummyAdapter(CacheAdapter):
    cache: dict

    def set(self, key: str | bytes, value: bytes, cache_time: int) -> None:
        self.cache[key] = value

    def get(self, key: str | bytes) -> dict | None:
        return self.cache.get(key)


class DummyFormatter:

    def __call__(self, results):
        outs = []
        for result in results:
            params = {}
            for i in range(0, len(result), 2):
                params[result[i]] = result[i + 1]

            outs.append(params)
        return outs


simple_decorator = DecoratorFactory()
decorator_with_adapter = DecoratorFactory(cache_adapter=DummyAdapter(dict()))
decorator_with_formatter = DecoratorFactory(result_formatter=DummyFormatter())
full_param_decorator = DecoratorFactory(cache_adapter=DummyAdapter(dict()), result_formatter=DummyFormatter())


@dataclass
class Dummy:
    x: str
    y: int


def create_many(nb: int):
    return [
        {'x': 'test', 'y': nb},
        {'x': 'test2', 'y': nb},
    ]


def create_one(nb: int):
    return [
        {'x': 'test', 'y': nb},
    ]


def create_nothing(nb: int):
    return []


def create_many_non_formatted(nb: int):
    return [
        ['x', 'test', 'y', nb],
        ['x', 'test2', 'y', nb],
    ]


def create_one_non_formatted(nb: int):
    return [
        ['x', 'test', 'y', nb],
    ]


__all__ = [
    'Dummy',
    'DummyAdapter',
    'DummyFormatter',
    'create_many',
    'create_many_non_formatted',
    'create_nothing',
    'create_one',
    'create_one_non_formatted',
    'decorator_with_adapter',
    'decorator_with_formatter',
    'full_param_decorator',
    'simple_decorator',
]
