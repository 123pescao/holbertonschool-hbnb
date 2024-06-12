#!/usr/bin/python3
print("Loading Place from places.py")
from model.base_model import BaseModel
from model.user import User


class Place(BaseModel):
    """
    Class for Place object
    """

    def __init__(self, place_id, name, description, address, number_rooms,
            reviews, bathrooms, price, max_guests):
        """ 
        Initialize Place object
        """
        super().__init__(**kwargs)
        if not isinstance(host, User):
            raise ValueError("Host must be a User")
        self.place_id = place_id
        self.name = name
        self.description = description
        self.address = address
        self.city = city
        self.host = host
        self.amenities = set()
        self.reviews = []
