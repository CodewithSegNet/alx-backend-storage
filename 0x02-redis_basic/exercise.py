#!/usr/bin/env python3

"""
a class that stores an instance as a private var and flush the instance
"""
import redis
import uuid
from typing import Any, Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Tracks the call details of a method in a Cache class
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """returns the methods output after storing its inputs and output.
        """
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return wrapper
    

class Cache():
    def __init__(self):
        """ connect to the redis server and store \
                the instance in a private var """
        self._redis = redis.Redis()

        """ flush the instance flushdb """
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ generate a random UUID as the key """
        key = str(uuid.uuid4())

        """ Store the data in Redis using the generated key """
        self._redis.setex(key, 3600, data)

        """ Return the generated key """
        return key

    def get(self, key: str, fn: Callable = None)\
            -> Union[str, bytes, int, float]:
        """retrieve the data associated \
                with the given key from Redis"""
        data = self._redis.get(key)

        """ if the key doesnt exist in Redis, Return None """
        if data is None:
            return None

        """ if a conversion func(fn) is provided,\
                apply it to data and return result """

        if fn:
            return fn(data)

        """ otherwise, return the data as it is """
        return data

    def get_str(self, key: str) -> str:
        """ helper method to get the data as a utf-8 """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """ helper method to get the data as an int """
        return self.get(key, fn=int)
