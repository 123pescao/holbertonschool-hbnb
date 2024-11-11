#!/usr/bin/python3
"""CRUD Methods"""
from models.user import User


class UserManager:
    def __init__(self, repository):
        """Initialize UserManager with a Repository"""
        self.repository = repository

    def create_user(self, id, name, email):
        """Create new User object and add to repository"""
        new_user = User(id, name, email)
        self.repository.add(new_user)
        return new_user

    def get_user(self, user_id):
        """Retrieve user from repository"""
        return self.repository.get(user_id)

    def update_user(self, user_id, new_name=None, new_email=None):
        """Update existe User object"""
        user = self.get_user(user_id)
        if user:
            if new_name:
                user.name = new_name
            if new_email:
                user.email = new_email
            self.repository.add(user)
            return user
        return None

    def delete_user(self, user_id):
        """Delete a user from repository by ID"""
        user = self.get_user(user_id)
        if user:
            self.repository.delete(user_id)
            return True
        return False
