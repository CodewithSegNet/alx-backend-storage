#!/usr/bin/env python3

"""
a class that stores an instance as a private var and flush the instance
"""
import redis
import uuid
from typing import Union, Callable


class Cache():
    def __init__(self):
        """ connect to the redis server and store \
                the instance in a private var """
        self._redis = redis.Redis()

        """ flush the instance flushdb """
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int]) -> str:
        """ generate a random UUID as the key """
        key = str(uuid.uuid4())

        """ Store the data in Redis using the generated key """
        self._redis.set(key, data)

        """ Return the generated key """
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """retrieve the data associated with the given key from Redis"""
        data = self.redis.get(key)

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
