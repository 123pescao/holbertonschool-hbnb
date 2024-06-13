from persistence_interface import IPersistenceManager

class DataManager(IPersistenceManager):
    def __init__(self):
        self.storage = {
            'User': {},
            'Place': {},
            'City': {}
        }

    def save(self, entity):
        entity_type = type(entity).__name__
        entity_id = getattr(entity, 'id')
        self.storage[entity_type][entity_id] = entity

    def get(self, entity_id, entity_type):
        return self.storage.get(entity_type, {}).get(entity_id)

    def update(self, entity):
        entity_type = type(entity).__name__
        entity_id = getattr(entity, 'id')
        if entity_id in self.storage[entity_type]:
            self.storage[entity_type][entity_id] = entity

    def delete(self, entity_id, entity_type):
        if entity_id in self.storage.get(entity_type, {}):
            del self.storage[entity_type][entity_id]
