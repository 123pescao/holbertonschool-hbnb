#!/usr/bin/python3
from model.city import City
from model.country import Country
from model.user import User
from model.amenity import Amenity
from modl.place import Place

class DataManager:
    def __init__(self):
        self.storage = {
            "User": {},
            "Country": {},
            "City": {},
            "Amenity": {},
            "Place": {}
        }

    def save(self, entity):
        if isinstance(entity, User):
            self.storage["User"][str(entity.id)] = entity
        elif isinstance(entity, Country):
            self.storage["Country"][entity.code] = entity
        elif isinstance(entity, City):
            self.storage["City"][str(entity.id)] = entity
        elif isinstance(entity, Amenity):
            self.storage["Amenity"][str(entity.id)] = entity
        elif isinstance(entity, Place):
            self.storage["Place"][str(entity.id)] = entity

    def get(self, entity_id, entity_type):
        return self.storage[entity_type].get(entity_id)

    def update(self, entity):
        if isinstance(entity, User):
            self.storage["User"][str(entity.id)] = entity
        elif isinstance(entity, Country):
            self.storage["Country"][entity.code] = entity
        elif isinstance(entity, City):
            self.storage["City"][str(entity.id)] = entity
        elif isinstance(entity, Amenity):
            self.storage["Amenity"][str(entity.id)] = entity
        elif isinstance(entity, Place):
            self.storage["Place"][str(entity.id)] = entity

    def delete(self, entity_id, entity_type):
        return self.storage[entity_type].pop(entity_id, None)
