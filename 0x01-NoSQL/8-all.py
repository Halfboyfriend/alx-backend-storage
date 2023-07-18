#!/usr/bin/env python3
"""
 lists all documents in a collection:"""
import pymongo



def list_all(mongo_collection):
    """
    function that list all documents
    """
    if not mongo_collection:
        return []
    doc = mongo_collection.find()
    return [l for l in doc]
