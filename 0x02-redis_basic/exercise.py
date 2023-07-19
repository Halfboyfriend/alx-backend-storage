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
        Initialize and flushdb"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @functools.wraps
    def count_calls(fn: Callable) -> Callable:
        def wrapped(self, *args, **kwargs):
            key = fn.__qualname__
            self._redis.incr(key)
            return fn(self, *args, **kwargs)

        return wrapped

    @staticmethod
    def _get_key(method_name: str, suffix: str) -> str:
        return f"{method_name}:{suffix}"

    @staticmethod
    def _serialize_args(args: tuple) -> str:
        return str(args)

    @functools.wraps
    def call_history(method: Callable) -> Callable:
        def wrapped(self, *args, **kwargs):
            input_key = self._get_key(method.__qualname__, "inputs")
            output_key = self._get_key(method.__qualname__, "outputs")

            serialized_args = self._serialize_args(args)
            self._redis.rpush(input_key, serialized_args)

            result = method(self, *args, **kwargs)
            self._redis.rpush(output_key, str(result))

            return result

        return wrapped

    @count_calls
    @call_history
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
