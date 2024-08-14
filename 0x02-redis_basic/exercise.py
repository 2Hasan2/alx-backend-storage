#!/usr/bin/env python3
"""A module for using Redis data storage
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, any

def count_calls(method: Callable) -> Callable:
    """Tracks the number of calls made to a method in a Cache class.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> any:
        """Wrapper function
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
            return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """Tracks the history of inputs and outputs for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> any:
        """Wrapper function
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(method.__qualname__ + ":inputs", str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(method.__qualname__ + ":outputs", str(output))
            return output
    return wrapper


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

    def get(
            self,
            key:str,
            fn:Callable
            ) -> Union[str, bytes, int, float]:
        """Retrieves a value from a Redis data storage.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Retrieves a string value from a Redis data storage.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieves an integer value from a Redis data storage.
        """
        return self.get(key, lambda x: int(x))
