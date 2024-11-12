import unittest
from app import create_app
from app.services.facade import HBnBFacade


class TestUserEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.facade = HBnBFacade()

    def test_create_valid_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email format", response.get_json()["error"])

    def test_create_user_missing_fields(self):
        response = self.client.post('/api/v1/users/', json={
        "email": "john.doe@example.com"
    })
        response_json = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response_json, f"Unexpected response format: {response_json}")
        self.assertIn("first_name", response_json["errors"], f"Unexpected response format: {response_json}")
        self.assertIn("last_name", response_json["errors"], f"Unexpected response format: {response_json}")
        self.assertIn("first_name", response_json["errors"], f"Missing 'first_name' error in response.")
        self.assertIn("last_name", response_json["errors"], f"Missing 'last_name' error in response.")



class TestPlaceEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.facade = HBnBFacade()
        # Create a user to act as the owner for places
        owner_response = cls.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Smith",
            "email": "owner.smith@example.com"
        })
        cls.owner_id = owner_response.get_json()["id"]

    def test_create_valid_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "description": "Lovely beach house.",
            "price": 200.00,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_missing_title(self):
        response = self.client.post('/api/v1/places/', json={
            "description": "Lovely beach house.",
            "price": 200.00,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("'title' cannot be empty", response.get_json()["error"])

    def test_create_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Mountain Cabin",
            "description": "Cozy cabin.",
            "price": -50.00,
            "latitude": 35.6528,
            "longitude": -117.2834,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Price must be a positive number.", response.get_json()["error"])

    def test_create_place_invalid_latitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Desert Camp",
            "description": "Desert camp.",
            "price": 100.00,
            "latitude": 95.0000,
            "longitude": -117.2834,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Latitude must be between -90 and 90.", response.get_json()["error"])

    def test_create_place_invalid_longitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Desert Camp",
            "description": "Desert camp.",
            "price": 100.00,
            "latitude": 35.6528,
            "longitude": 200.0000,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Longitude must be between -180 and 180.", response.get_json()["error"])


class TestReviewEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.facade = HBnBFacade()
        # Create a user and a place to act as references for reviews
        user_response = cls.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "Jones",
            "email": "reviewer.jones@example.com"
        })
        cls.user_id = user_response.get_json()["id"]
        place_response = cls.client.post('/api/v1/places/', json={
            "title": "Lake House",
            "description": "A house by the lake.",
            "price": 300.00,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": cls.user_id
        })
        cls.place_id = place_response.get_json()["id"]

    def test_create_valid_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_missing_text(self):
        response = self.client.post('/api/v1/reviews/', json={
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("'text' cannot be empty.", response.get_json()["error"])

    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great experience!",
            "rating": 6,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Rating must be between 1 and 5.", response.get_json()["error"])

    def test_create_review_invalid_user_id(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Lovely stay!",
            "rating": 4,
            "user_id": "invalid-user-id",
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid user_id: User does not exist.", response.get_json()["error"])

    def test_create_review_invalid_place_id(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Lovely stay!",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": "invalid-place-id"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid place_id: Place does not exist.", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main()
