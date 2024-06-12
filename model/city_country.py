#!/usr/bin/python3
from model.base_model import BaseModel


class City(BaseModel):
    def __init__(self, city_name, country_code, **kwargs):
        super().__init__(**kwargs)
        self.city_name = city_name
        self.country_code = country_code
        self.places = []

    def add_city(self, city):
        self.city_name.append(city)
        self.places.append(city)



class Country(BaseModel):
    countries = []

    def __init__(self, name, code, **kwargs):
        super().__init__(**kwargs)
        self.name
        self.code = code
        Country.countries.append(self)
