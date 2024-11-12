import unittest
from app import create_app
from app.services.facade import HBnBFacade

class TestUserEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.facade = HBnBFacade()

    def test_create_user_valid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Invalid email format.")

    def test_create_user_missing_fields(self):
        response = self.client.post('/api/v1/users/', json={
        "email": "john.doe@example.com"
    })
        response_json = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response_json, f"Unexpected response format: {response_json}")
        self.assertIn("first_name", response_json["errors"])
        self.assertIn("last_name", response_json["errors"])

    def test_get_user(self):
        # Ensure user creation
        create_response = self.client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    })
        user_id = create_response.get_json()["id"]

        # Test fetching the created user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.get_json())


    def test_get_nonexistent_user(self):
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
