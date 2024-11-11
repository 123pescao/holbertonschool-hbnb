import unittest
from app import create_app
from app.services.facade import HBnBFacade

class TestReviewEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.facade = HBnBFacade()

    def test_create_review_valid_data(self):
        user = self.facade.create_user({
            "first_name": "Reviewer",
            "last_name": "Jones",
            "email": "reviewer.jones@example.com"
        })
        place = self.facade.create_place({
            "title": "Lakeside Cottage",
            "description": "A serene place by the lake.",
            "price": 100.0,
            "latitude": 34.0,
            "longitude": -118.0,
            "owner_id": user.id
        })
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing experience!",
            "rating": 5,
            "user_id": user.id,
            "place_id": place.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_create_review_invalid_rating(self):
        user = self.facade.create_user({
            "first_name": "Reviewer",
            "last_name": "Jones",
            "email": "reviewer.jones@example.com"
        })
        place = self.facade.create_place({
            "title": "Lakeside Cottage",
            "description": "A serene place by the lake.",
            "price": 100.0,
            "latitude": 34.0,
            "longitude": -118.0,
            "owner_id": user.id
        })
        response = self.client.post('/api/v1/reviews/', json={
            "text": "It was okay.",
            "rating": 6,
            "user_id": user.id,
            "place_id": place.id
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Rating must be between 1 and 5.")

    def test_get_review(self):
        user = self.facade.create_user({
            "first_name": "Reviewer",
            "last_name": "Jones",
            "email": "reviewer.jones@example.com"
        })
        place = self.facade.create_place({
            "title": "Lakeside Cottage",
            "description": "A serene place by the lake.",
            "price": 100.0,
            "latitude": 34.0,
            "longitude": -118.0,
            "owner_id": user.id
        })
        review = self.facade.create_review({
            "text": "Loved the stay!",
            "rating": 5,
            "user_id": user.id,
            "place_id": place.id
        })
        response = self.client.get(f'/api/v1/reviews/{review.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['text'], "Loved the stay!")

if __name__ == '__main__':
    unittest.main()
