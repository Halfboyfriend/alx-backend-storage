#!/usr/bin/env python3
"""
Create a Cache class.
In the __init__ method, store an instance of the
Redis client as a private variable
named _redis (using redis.Redis()) and flush the instance using
"""
import functools

import redis
from typing import Union, Callable
import uuid


class Cache:
    """
    Create a Cache Class
    """
    def __init__(self):
        """
        Initialize and fluchdb"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @functools.wraps
    def count_calls(fn: Callable) -> Callable:
        def wrapped(self, *args, **kwargs):
            key = fn.__qualname__
            self._redis.incr(key)
            return fn(self, *args, **kwargs)

        return wrapped

    @count_calls
    def store(self, data: Union[str, float, int, bytes]) -> str:
        """

        :param data:
        :return:
        """
        randKey = str(uuid.uuid4())
        self._redis.set(randKey, data)
        return randKey

    def get(self, key: str, fn: Callable = None) -> \
            Union[str, bytes, int, float, None]:
        dt = self._redis.get(key)
        if dt is None:
            return None
        if fn is not None:
            return fn(dt)
        return dt

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=int)
