#!/usr/bin/env python3

"""
a class that stores an instance as a private var and flush the instance
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


class Cache():
    def __init__(self):
        """ connect to the redis server and store \
                the instance in a private var """
        self._redis = redis.Redis()

        """ flush the instance flushdb """
        self._redis.flushdb()

    def count_calls(method: Callable) -> Callable:
        """ dictionary to store the call count for each method """
        method_call_count = {}

        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            """ get the qualified name of the method \
                    using __qualname__ dunder """
            method_name = method.__qualname__

            """ increment the call count for the method\
                    or initialize it to 1 """
            method_call_count[method_name] = method_call_count.get(
                method_name, 0) + 1

            """ calll the original method and return its result """
            return method(self, *args, **kwargs)

        """add a property to the wrapper to \
                get the call count for a method"""
        def get_call_count():
            method_name = method.__qualname__
            return method_call_count.get(method_name, 0)

        wrapper.get_call_count = get_call_count

        return wrapper

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ generate a random UUID as the key """
        key = str(uuid.uuid4())

        """ Store the data in Redis using the generated key """
        self._redis.set(key, data)

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
