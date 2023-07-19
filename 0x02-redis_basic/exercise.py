#!/usr/bin/env python3
"""
Create a Cache class.
In the __init__ method, store an instance of the
Redis client as a private variable
named _redis (using redis.Redis()) and flush the instance using
"""
import redis
from typing import Union
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

    def store(self, data: Union[str, float, int, bytes]) -> str:
        """

        :param data:
        :return:
        """
        randKey = str(uuid.uuid4())
        self._redis.set(randKey, data)
        return randKey
