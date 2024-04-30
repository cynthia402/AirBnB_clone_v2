#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os

env_db = os.environ.get('HBNB_TYPE_STORAGE')

if env_db != 'db':
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
else:
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
storage.reload()
