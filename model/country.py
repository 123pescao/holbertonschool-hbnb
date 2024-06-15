#!/usr/bin/python3
class Country:
    def __init__(self, code, name):
        self.code = code
        self.name = name

from datetime import datetime
import uuid

class City:
    city_names = {}

    def __init__(self, name, country_code):
        self.id = uuid.uuid4()
        self.name = name
        self.country_code = country_code
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if country_code not in City.city_names:
            City.city_names[country_code] = set()
        if name in City.city_names[country_code]:
            raise ValueError("City name must be unique within the country")
        City.city_names[country_code].add(name)

    def update(self, name=None, country_code=None):
        if name and name != self.name:
            if country_code not in City.city_names:
                City.city_names[country_code] = set()
            if name in City.city_names[country_code]:
                raise ValueError("City name must be unique within the country")
            City.city_names[self.country_code].remove(self.name)
            self.name = name
            City.city_names[self.country_code].add(name)
        if country_code and country_code != self.country_code:
            City.city_names[self.country_code].remove(self.name)
            self.country_code = country_code
            if name in City.city_names[country_code]:
                raise ValueError("City name must be unique within the country")
            City.city_names[country_code].add(self.name)
        self.updated_at = datetime.now()
