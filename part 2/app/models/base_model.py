#!/usr/bin/python3
"""Basemodel"""
import uuid
from datetime import datetime

class BaseModel:
    """Base model with common attributes"""
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, data):
        """Update object attributes and timestamp"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
