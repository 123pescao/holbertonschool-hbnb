#!/usr/bin/python3


import unittest
from model.places import Place
from model.user import User
import uuid
from persistence.data_manager import DataManager


class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.data_manager = DataManager()

    def test_save_and_get_user(self):
        user = User(email="test@example.com", first_name="John", last_name="Doe")
        self.data_manager.save(user)
        retrieved_user = self.data_manager.get(user.id, "User")
        self.assertEqual(retrieved_user.email, "test@example.com")

    def test_update_user(self):
        user = User(email="test@example.com", first_name="John", last_name="Doe")
        self.data_manager.save(user)
        user.first_name = "Jane"
        self.data_manager.update(user)
        updated_user = self.data_manager.get(user.id, "User")
        self.assertEqual(updated_user.first_name, "Jane")

    def test_delete_user(self):
        user = User(email="test@example.com", first_name="John", last_name="Doe")
        self.data_manager.save(user)
        self.data_manager.delete(user.id, "User")
        deleted_user = self.data_manager.get(user.id, "User")
        self.assertIsNone(deleted_user)

    def test_save_and_get_place(self):
        place = Place(host_id=uuid.uuid4(), name="Lovely Apartment", description="A beautiful place", number_of_rooms=2, number_of_bathrooms=1, max_guests=4, price_per_night=150.0, latitude=40.7128, longitude=-74.0060, city_id=uuid.uuid4(), amenity_ids=[])
        self.data_manager.save(place)
        retrieved_place = self.data_manager.get(place.id, "Place")
        self.assertEqual(retrieved_place.name, "Lovely Apartment")

if __name__ == "__main__":
    unittest.main()