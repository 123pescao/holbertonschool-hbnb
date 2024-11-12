import unittest
from app import create_app
from app.services.facade import HBnBFacade
from app.persistence.repository import InMemoryRepository

# Mock class to test repository methods
class TestObject:
    def __init__(self, obj_id, name):
        self.id = obj_id
        self.name = name

    def update(self, data):
        """Update attributes based on a dictionary of values."""
        for key, value in data.items():
            setattr(self, key, value)

class TestSetup(unittest.TestCase):

    def test_flask_app_initialization(self):
        app = create_app()
        self.assertIsNotNone(app)

    def test_facade_initialization(self):
        facade = HBnBFacade()
        self.assertIsInstance(facade, HBnBFacade)

    def test_repository_methods(self):
        repo = InMemoryRepository()
        test_obj = TestObject("1", "Test Object")

        # Test add and get
        repo.add(test_obj)
        self.assertEqual(repo.get("1").name, "Test Object")

        # Test update
        repo.update("1", {"name": "Updated Object"})
        self.assertEqual(repo.get("1").name, "Updated Object")

        # Test delete
        repo.delete("1")
        self.assertIsNone(repo.get("1"))

if __name__ == "__main__":
    unittest.main()
