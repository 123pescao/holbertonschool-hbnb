#!/usr/bin/python3
from model.base_model import Basemodel
from model.user import User
from model.places import Place


class Review(BaseModel):
    """class for Reviews
    """
    def __init__(self, comment, rating):
        """defines init method"""
        super().__init__()  # Call the __init__ method of the BaseModel class
        self.comment = comment
        self.rating = rating

    def __str__(self):
        """
        returns a string representation
        """
        return f"[Review] ({self.id}) {self.to_dict()}"
