#!/usr/bin/python3
from datetime import datetime
import uuid

class City:
    def __init__(self, name, country_code):
        self.id = uuid.uuid4()
        self.name = name
        self.country_code = country_code
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
