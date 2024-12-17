#!/usr/bin/python3
"""Place Repository"""
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)
