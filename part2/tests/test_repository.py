import unittest
from app.persistence.repository import InMemoryRepository

class TestObject:
    def __init__(self, obj_id, name):
        self.id = obj_id
        self.name = name

class RepositoryTestCase(unittest.TestCase):
    def test_repository_methods(self):
        # Test add, get, update, delete for repository
        pass

if __name__ == "__main__":
    unittest.main()
