#!/usr/bin/python3


import unittest
import json
from api.city_country import app

class TestCountriesCitiesAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_countries(self):
        response = self.app.get('/countries')
        self.assertEqual(response.status_code, 200)
        self.assertIn('code', response.json[0])
        self.assertIn('name', response.json[0])

    def test_get_country(self):
        response = self.app.get('/countries/US')
        self.assertEqual(response.status_code, 200)
        self.assertIn('code', response.json)
        self.assertIn('name', response.json)

    def test_get_cities_by_country(self):
        country_code = 'US'
        city_data = {"name": "New York", "country_code": country_code}
        self.app.post('/cities', data=json.dumps(city_data), content_type='application/json')

        response = self.app.get(f'/countries/{country_code}/cities')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.json[0])
        self.assertEqual(response.json[0]['country_code'], country_code)

    def test_create_city(self):
        city_data = {"name": "San Francisco", "country_code": "US"}
        response = self.app.post('/cities', data=json.dumps(city_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('name', response.json)
        self.assertIn('country_code', response.json)

    def test_update_city(self):
        city_data = {"name": "Los Angeles", "country_code": "US"}
        post_response = self.app.post('/cities', data=json.dumps(city_data), content_type='application/json')
        city_id = post_response.json['id']

        update_data = {"name": "Los Angeles Updated", "country_code": "US"}
        put_response = self.app.put(f'/cities/{city_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.json['name'], "Los Angeles Updated")

    def test_delete_city(self):
        city_data = {"name": "Chicago", "country_code": "US"}
        post_response = self.app.post('/cities', data=json.dumps(city_data), content_type='application/json')
        city_id = post_response.json['id']

        delete_response = self.app.delete(f'/cities/{city_id}')
        self.assertEqual(delete_response.status_code, 204)

        get_response = self.app.get(f'/cities/{city_id}')
        self.assertEqual(get_response.status_code, 404)

if __name__ == "__main__":
    unittest.main()