import unittest
from app import create_app
from app.services.facade import HBnBFacade

class TestPlaceEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.facade = HBnBFacade()

    def test_create_place_valid_data(self):
        user = self.facade.create_user({
            "first_name": "Owner",
            "last_name": "Smith",
            "email": "owner.smith@example.com"
        })
        response = self.client.post('/api/v1/places/', json={
            "title": "Mountain Cabin",
            "description": "A cozy cabin in the mountains.",
            "price": 120.0,
            "latitude": 35.6528,
            "longitude": -117.2834,
            "owner_id": user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_create_place_invalid_price(self):
        user = self.facade.create_user({
            "first_name": "Owner",
            "last_name": "Smith",
            "email": "owner.smith@example.com"
        })
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "price": -50.0,
            "latitude": 34.0,
            "longitude": -118.0,
            "owner_id": user.id
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Price must be a positive number.")

    def test_create_place_invalid_latitude(self):
        user = self.facade.create_user({
            "first_name": "Owner",
            "last_name": "Smith",
            "email": "owner.smith@example.com"
        })
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "price": 150.0,
            "latitude": 100.0,
            "longitude": -118.0,
            "owner_id": user.id
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Latitude must be between -90 and 90.")

    def test_get_place(self):
        user = self.facade.create_user({
            "first_name": "Owner",
            "last_name": "Smith",
            "email": "owner.smith@example.com"
        })
        place = self.facade.create_place({
            "title": "Beach House",
            "description": "A house by the beach.",
            "price": 200.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": user.id
        })
        response = self.client.get(f'/api/v1/places/{place.id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
