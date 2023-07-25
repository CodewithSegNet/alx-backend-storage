#!/usr/bin/env python3
"""define a function named insert_school"""


def insert_school(mongo_collection, **kwargs):
    """insert a new doc through kwargs"""
    inserted_document = mongo_collection.insert_one(kwargs)
    return inserted_document.inserted_id
