#!/usr/bin/python3
"""Place Class"""
from app.models.base_model import BaseModel

class Place(BaseModel):
    """Represents a property listing in the HBnB application."""

    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=[]):
        """Initialize a Place with details, location, and ownership."""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price must be a non-negative number.")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        self._longitude = value
