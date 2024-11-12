#!/usr/bin/python3
"""Amenity Class"""
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Represents an amenity that a place can have."""

    def __init__(self, name):
        """Initialize an Amenity with a name."""
        super().__init__()
        self.name = name