#!/usr/bin/python3
print("Loading User from user.py")
from model.base_model import BaseModel


class User(BaseModel):
    users = []
    """
    User class that extends the BaseModel to include user-specific attributes.
    """

    def __init__(self, email, password, first_name="", last_name="", **kwargs):
        """
        Initialize a new User instance.

        """
        super().__init__(**kwargs)
        if email in [user.email for user in User.users]:
            raise ValueError("Email must be unique")
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.places = []
        self.reviews = []
        User.users.append(self)

    def update_name(self, first_name="", last_name=""):
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f"[User] ({self.id}) {self.to_dict()}"
