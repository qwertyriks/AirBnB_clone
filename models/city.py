#!/usr/bin/python3
"""This module creates a User class"""

from models.base_model import BaseModel


class City(BaseModel):
    """Class for managing city objects state id and name."""

    state_id = ""
    name = ""
