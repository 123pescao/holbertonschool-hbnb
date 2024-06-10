from model.base_model import BaseModel


class User(BaseModel):
    """
    User class that extends the BaseModel to include user-specific attributes.
    """

    def __init__(self, email, password, first_name="", last_name="", **kwargs):
        """
        Initialize a new User instance.

        """
        super().__init__(**kwargs)
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.places = []
        self.reviews = []

    def update_name(self, first_name="", last_name=""):
        """
        Update the user's first and last name.

        """
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        """
        Return a string representation of the User instance.

        Returns:
            str: A string representation of the user.
        """
        return f"[User] ({self.id}) {self.to_dict()}"
