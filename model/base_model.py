#!/usr/bin/python3
import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    def save(self):
        self.updated_at = datetime.now()
