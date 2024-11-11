import unittest
from app import create_app
from app.services.facade import HBnBFacade

class TestUserEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.facade = HBnBFacade()

    def test_create_user(self):
        """Test user creation with valid data."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_create_user_missing_fields(self):
        """Test user creation with missing required fields."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John'
            # Missing 'last_name' and 'email'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json)  # Check for 'errors' key
        self.assertIn('email', response.json['errors'])  # Check specific field error
        self.assertIn('last_name', response.json['errors'])

    def test_get_user_list(self):
        """Test retrieval of all users."""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_user_by_id(self):
        """Test retrieval of a user by ID."""
        # Create a user to retrieve
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com'
        })
        user_id = response.json['id']
        get_response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json['email'], 'jane.smith@example.com')

    def test_update_user(self):
        """Test updating a user with valid data."""
        # Create a user to update
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'Mike',
            'last_name': 'Brown',
            'email': 'mike.brown@example.com'
        })
        user_id = response.json['id']
        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            'first_name': 'Michael',
            'last_name': 'Brown',
            'email': 'michael.brown@example.com'
        })
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json['first_name'], 'Michael')

    def test_update_user_invalid_data(self):
        """Test updating a user with invalid data."""
        # Create a user to update with invalid data
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'Alice',
            'last_name': 'Green',
            'email': 'alice.green@example.com'
        })
        user_id = response.json['id']
        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            'first_name': 'Alice',
            'last_name': 'Green',
            'email': 123  # Invalid email type
        })
        self.assertEqual(update_response.status_code, 400)
        self.assertIn('errors', update_response.json)  # Check for 'errors' key
        self.assertIn('email', update_response.json['errors'])  # Check specific field error

if __name__ == "__main__":
    unittest.main()
