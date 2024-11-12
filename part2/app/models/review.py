#!/usr/bin/python3
"""Review Class"""

from app.models.base_model import BaseModel

class Review(BaseModel):
    """Represents a review for a place in the HBnB application."""

    def __init__(self, text, rating, place_id, user_id):
        """Initialize a Review with content, rating, place, and user."""
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
