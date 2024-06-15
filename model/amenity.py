#!/usr/bin/python3
from datetime import datetime
import uuid

class Amenity:
    amenity_names = set()

    def __init__(self, name):
        if name in Amenity.amenity_names:
            raise ValueError("Amenity already exists")
        self.id = uuid.uuid4()
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        Amenity.amenity_names.add(name)

    def update(self, name=None):
        if name and name != self.name:
            if name in Amenity.amenity_names:
                raise ValueError("Amenity already exists")
            Amenity.amenity_names.remove(self.name)
            self.name = name
            Amenity.amenity_names.add(name)
        self.updated_at = datetime.now()
