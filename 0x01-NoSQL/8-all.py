#!/usr/bin/env python3
"""a function that lists all documents in a collection."""

def list_all(mongo_collection):
    """lists all docs in a collection"""
    documents = []

    for docs in mongo_collection.find():
        documents.append(docs)
    return documents
