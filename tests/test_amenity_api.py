#!/usr/bin/python3


import unittest
import json
from api.amenities import app

class TestAmenitiesAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_amenity(self):
        amenity_data = {"name": "WiFi"}
        response = self.app.post('/amenities', data=json.dumps(amenity_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('name', response.json)

    def test_get_amenities(self):
        response = self.app.get('/amenities')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_amenity(self):
        amenity_data = {"name": "Pool"}
        post_response = self.app.post('/amenities', data=json.dumps(amenity_data), content_type='application/json')
        amenity_id = post_response.json['id']

        get_response = self.app.get(f'/amenities/{amenity_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertIn('name', get_response.json)

    def test_update_amenity(self):
        amenity_data = {"name": "Gym"}
        post_response = self.app.post('/amenities', data=json.dumps(amenity_data), content_type='application/json')
        amenity_id = post_response.json['id']

        update_data = {"name": "Fitness Center"}
        put_response = self.app.put(f'/amenities/{amenity_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.json['name'], "Fitness Center")

    def test_delete_amenity(self):
        amenity_data = {"name": "Parking"}
        post_response = self.app.post('/amenities', data=json.dumps(amenity_data), content_type='application/json')
        amenity_id = post_response.json['id']

        delete_response = self.app.delete(f'/amenities/{amenity_id}')
        self.assertEqual(delete_response.status_code, 204)

        get_response = self.app.get(f'/amenities/{amenity_id}')
        self.assertEqual(get_response.status_code, 404)

if __name__ == "__main__":
    unittest.main()