#!/usr/bin/python3

"""This __init__ is for models directory"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
