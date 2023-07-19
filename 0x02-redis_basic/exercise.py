#!/usr/bin/env python3

"""
a class that stores an instance as a private var and flush the instance
"""
import redis
import uuid
from typing import Union

r = redis.Redis()


class Cache():
    def __init__(self):
        """ connect to the redis server and store \
                the instance in a private var """
        self._redis = r

        """ flush the instance flushdb """
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int]) -> str:
        """ generate a random UUID as the key """
        key = str(uuid.uuid4())

        """ Store the data in Redis using the generated key """
        self._redis.set(key, data)

        """ Return the generated key """
        return key
