import unittest
from app import create_app
from app.services.facade import HBnBFacade

class TestAmenityEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.facade = HBnBFacade()

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            'name': 'Wi-Fi'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['name'], 'Wi-Fi')

    def test_get_all_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_amenity_by_id(self):
        # Create an amenity first
        response = self.client.post('/api/v1/amenities/', json={
            'name': 'Parking'
        })
        amenity_id = response.json['id']
        get_response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json['name'], 'Parking')

    def test_update_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            'name': 'Swimming Pool'
        })
        amenity_id = response.json['id']
        update_response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            'name': 'Updated Pool'
        })
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json['message'], 'Amenity updated successfully')

if __name__ == "__main__":
    unittest.main()
