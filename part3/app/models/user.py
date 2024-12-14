#!/usr/bin/python3
"""User Class"""
import re
import uuid
from app import db, bcrypt
from app.models.base_model import BaseModel

#Validate email format
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


class User(BaseModel):
    """User model for storing user data"""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """Initialize a User with personal details and admin status."""
        super().__init__()
        self.first_name = self._validate_name(first_name, "First")
        self.last_name = self._validate_name(last_name, "Last")
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        self.hash_password(password)

    def _validate_email(self, email):
        if not re.fullmatch(regex, email):
            raise ValueError("Invalid email format")
        return email

    def _validate_name(self, name, field_name):
        if not 0 < len(name) <= 50:
            raise ValueError(f"{field_name} name must be between 1 and 50 characters")
        return name

    def hash_password(self, password):
        """Hashes the password before storing"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password"""
        return bcrypt.check_password_hash(self.password, password)
