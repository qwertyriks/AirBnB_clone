#!/usr/bin/python3
"""Writes the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """Represent a city.

    Attributes:
        state_id (str): The state sss id.
        name (str): The name sss of the city.
    """

    state_id = ""
    name = ""
