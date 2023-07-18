#!/usr/bin/env python3
"""
 function that inserts a new document in a collection based on kwargs"""
import pymongo



def insert_school(mongo_collection, **kwargs):
    """
    function that inserts new documents
    """
    if not mongo_collection:
        return []
    dt = mongo_collection.insert_one(kwargs)
    return dt.inserted_id
