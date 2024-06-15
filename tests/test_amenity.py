#!/usr/bin/python3
import unittest
import json
from api import app


class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.amenity_data = {
            'name': 'Test Amenity'
        }

    def tearDown(self):
        # Clean up test data
        import shutil
        shutil.rmtree('data/amenities', ignore_errors=True)

    def test_create_amenity(self):
        response = self.client.post(
            '/amenities', data=json.dumps(self.amenity_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_amenities(self):
        self.client.post(
            '/amenities', data=json.dumps(self.amenity_data), content_type='application/json')
        response = self.client.get('/amenities')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_amenity(self):
        post_response = self.client.post(
            '/amenities', data=json.dumps(self.amenity_data), content_type='application/json')
        amenity_id = post_response.json['id']
        get_response = self.client.get(f'/amenities/{amenity_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json['name'], self.amenity_data['name'])

    def test_update_amenity(self):
        post_response = self.client.post(
            '/amenities', data=json.dumps(self.amenity_data), content_type='application/json')
        amenity_id = post_response.json['id']
        updated_data = {
            'name': 'Updated Amenity'
        }
        put_response = self.client.put(
            f'/amenities/{amenity_id}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.json['name'], 'Updated Amenity')

    def test_delete_amenity(self):
        post_response = self.client.post(
            '/amenities', data=json.dumps(self.amenity_data), content_type='application/json')
        amenity_id = post_response.json['id']
        delete_response = self.client.delete(f'/amenities/{amenity_id}')
        self.assertEqual(delete_response.status_code, 204)
        get_response = self.client.get(f'/amenities/{amenity_id}')
        self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()