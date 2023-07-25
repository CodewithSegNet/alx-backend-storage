#!/usr/bin/env python3
"""defines function schools_by_topic"""


def schools_by_topic(mongo_collection, topic):
    """function returns the list of school having a topic"""
    return list(mongo_collection.find({"topics": topic}))
