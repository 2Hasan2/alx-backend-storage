#!/usr/bin/env python3
"""A module for using Redis data storage
"""
import redis
import uuid
from typing import Union


class Cache:
    """A class for storing data in Redis
    """
    def __init__(self) -> None:
        """Initialize the Redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, int, float, bytes]) -> str:
        """Store the input data in Redis and return a key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key