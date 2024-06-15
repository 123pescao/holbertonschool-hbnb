#!/usr/bin/python3
import os
import json
from models.ipersistence_manager import IPersistenceManager

class DataManager(IPersistenceManager):
    def __init__(self, storage_file='data.json'):
        self.storage_file = storage_file

    def _load_data(self):
        if not os.path.exists(self.storage_file):
            return {}
        with open(self.storage_file, 'r') as file:
            return json.load(file)

    def _save_data(self, data):
        with open(self.storage_file, 'w') as file:
            json.dump(data, file)

    def save(self, entity):
        data = self._load_data()
        entity_type = entity.__class__.__name__
        if entity_type not in data:
            data[entity_type] = {}
        data[entity_type][entity.id] = entity.to_dict()
        self._save_data(data)

    def get(self, entity_id, entity_type):
        data = self._load_data()
        if entity_type in data and entity_id in data[entity_type]:
            return data[entity_type][entity_id]
        return None

    def update(self, entity):
        self.save(entity)

    def delete(self, entity_id, entity_type):
        data = self._load_data()
        if entity_type in data and entity_id in data[entity_type]:
            del data[entity_type][entity_id]
            self._save_data(data)

    def get_all(self, entity_type):
        data = self._load_data()
        return list(data.get(entity_type, {}).values())
