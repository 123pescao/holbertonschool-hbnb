#!/usr/bin/python3
from model.base_model import BaseModel

class Amenities(BaseModel):
    amenities = []

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        if name in [amenity.name for amenity in Amenities.amenities]:
            raise ValueError("Amenity name must be unique")
        self.name = name
        Amenities.amenities.append(self)
