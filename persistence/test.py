import unittest
from data_manager import DataManager
from entities import User, Place, City

class TestPersistence(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.user = User(id=1, name="John Doe")
        self.place = Place(id=1, location="123 Main St")
        self.city = City(id=1, name="Springfield")

    def test_save_and_get_user(self):
        self.data_manager.save(self.user)
        retrieved_user = self.data_manager.get(1, 'User')
        self.assertEqual(retrieved_user.name, "John Doe")

    def test_update_user(self):
        self.data_manager.save(self.user)
        self.user.name = "Jane Doe"
        self.data_manager.update(self.user)
        updated_user = self.data_manager.get(1, 'User')
        self.assertEqual(updated_user.name, "Jane Doe")

    def test_delete_user(self):
        self.data_manager.save(self.user)
        self.data_manager.delete(1, 'User')
        deleted_user = self.data_manager.get(1, 'User')
        self.assertIsNone(deleted_user)

    def test_save_and_get_place(self):
        self.data_manager.save(self.place)
        retrieved_place = self.data_manager.get(1, 'Place')
        self.assertEqual(retrieved_place.location, "123 Main St")

    def test_save_and_get_city(self):
        self.data_manager.save(self.city)
        retrieved_city = self.data_manager.get(1, 'City')
        self.assertEqual(retrieved_city.name, "Springfield")

if __name__ == '__main__':
    unittest.main()
