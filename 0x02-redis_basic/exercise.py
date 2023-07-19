#!/usr/bin/env python3
"""
Create a Cache class.
In the __init__ method, store an instance of the Redis client as a private variable 
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
        self.__redis = redis.Redis()
        self.__redis.flushdb()

    def store(self, data: Union[str, float, int, bytes]) -> str:
        """
        Create a store method that takes a data argument and 
        returns a string
        """
        k = str(uuid.uuid4())
        self.__redis.set(k, data)
        return k
