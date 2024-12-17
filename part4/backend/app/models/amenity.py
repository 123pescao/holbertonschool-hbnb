#!/usr/bin/python3
"""Amenity Class"""
from app.models.base_model import BaseModel
from app import db

class Amenity(BaseModel):
    """Represents an amenity that a place can have."""
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = self._validate_name(name)

    def _validate_name(self, name):
        if len(name) == 0:
            raise ValueError("Name cannot be empty")
        if len(name) > 50:
            raise ValueError("Name must be less than 50 characters")
        return name
