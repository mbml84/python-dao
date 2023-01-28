from __future__ import annotations

import operator
from typing import Callable


class LazyObject:

    _wrapped = None
    _is_init = False

    def __init__(self, factory: Callable[..., object], **kwargs):
        """
        Constructor

        Args:
            factory (Callable[..., object]): Method to create the real object
            **kwargs: Arguments for factory method
        """
        self.__dict__['_factory'] = factory
        self.__dict__['_kwargs'] = kwargs

    def _setup(self):
        """
        Setup new object
        """
        factory = self.__dict__.pop('_factory')
        kwargs = self.__dict__.pop('_kwargs')
        self._wrapped = factory(**kwargs)
        self._is_init = True

    def new_method_proxy(func):
        """
        Util function to help us route functions
        to the nested object.
        """

        def inner(self, *args):
            if not self._is_init:
                self._setup()
            return func(self._wrapped, *args)
        return inner

    def __setattr__(self, name, value):
        if name in {'_is_init', '_wrapped'}:
            self.__dict__[name] = value
        else:
            if not self._is_init:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == '_wrapped':
            raise TypeError("can't delete _wrapped.")
        if not self._is_init:
            self._setup()
        delattr(self._wrapped, name)

    __getattr__ = new_method_proxy(getattr)
    __bytes__ = new_method_proxy(bytes)
    __str__ = new_method_proxy(str)
    __bool__ = new_method_proxy(bool)
    __dir__ = new_method_proxy(dir)
    __hash__ = new_method_proxy(hash)
    __class__ = property(new_method_proxy(operator.attrgetter('__class__')))
    __eq__ = new_method_proxy(operator.eq)
    __lt__ = new_method_proxy(operator.lt)
    __gt__ = new_method_proxy(operator.gt)
    __ne__ = new_method_proxy(operator.ne)
    __hash__ = new_method_proxy(hash)
    __getitem__ = new_method_proxy(operator.getitem)
    __setitem__ = new_method_proxy(operator.setitem)
    __delitem__ = new_method_proxy(operator.delitem)
    __iter__ = new_method_proxy(iter)
    __len__ = new_method_proxy(len)
    __contains__ = new_method_proxy(operator.contains)


__all__ = [
    'LazyObject',
]
