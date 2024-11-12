#!/usr/bin/python3
"""User Class"""
from app.models.base_model import BaseModel

class User(BaseModel):
    """Initialize User object"""
    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialize a User with personal details and admin status."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
