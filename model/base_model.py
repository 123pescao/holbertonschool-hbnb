#!/usr/bin/python3
print("Loading BaseModel from base_model.py")
from datetime import datetime
import uuid


class BaseModel:
    """
    BaseModel class that serves as a base for other models, providing unique ID
    creation timestamp, and update timestamp.
    """
    def __init__(self, id=None, created_at=None, updated_at=None):
        """
        Initialize a new instance of BaseModel.
        """
        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def save(self):
        self.updated_at = datetime.now()

    def to_dict(self):
        return self.__dict__
