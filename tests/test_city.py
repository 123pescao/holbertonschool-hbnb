import unittest
import os
import json
from datetime import datetime
from unittest.mock import patch, MagicMock
from model.city_country import City, data_manager

class TestCity(unittest.TestCase):

    @patch('your_module.DataManager')
    def setUp(self, MockDataManager):
        self.mock_data_manager = MockDataManager.return_value
        self.city = City(name="Test City", country_code="TC")

    def test_city_creation(self):
        self.assertEqual(self.city.name, "Test City")
        self.assertEqual(self.city.country_code, "TC")
        self.assertIsNotNone(self.city.id)
        self.assertIsInstance(self.city.created_at, datetime)
        self.assertIsInstance(self.city.updated_at, datetime)

    def test_city_to_dict(self):
        city_dict = self.city.to_dict()
        self.assertEqual(city_dict['name'], "Test City")
        self.assertEqual(city_dict['country_code'], "TC")
        self.assertEqual(city_dict['id'], self.city.id)
        self.assertEqual(city_dict['created_at'], self.city.created_at.isoformat())
        self.assertEqual(city_dict['updated_at'], self.city.updated_at.isoformat())

    @patch('your_module.data_manager')
    def test_save_city(self, mock_data_manager):
        self.city.save()
        mock_data_manager.save.assert_called_once_with(self.city)

    @patch('your_module.data_manager')
    def test_get_city(self, mock_data_manager):
        mock_city_data = {
            'id': '1234',
            'name': 'Test City',
            'country_code': 'TC',
            'created_at': '2023-01-01T00:00:00',
            'updated_at': '2023-01-01T00:00:00'
        }
        mock_data_manager.get.return_value = mock_city_data
        city = City.get('1234')
        self.assertIsNotNone(city)
        self.assertEqual(city.id, '1234')
        self.assertEqual(city.name, 'Test City')
        self.assertEqual(city.country_code, 'TC')

    @patch('your_module.os.listdir')
    @patch('your_module.open')
    def test_get_all_cities(self, mock_open, mock_listdir):
        mock_listdir.return_value = ['city1.json', 'city2.json']
        mock_open.side_effect = [
            MagicMock(read=lambda: json.dumps({
                'id': '1',
                'name': 'City One',
                'country_code': 'CO',
                'created_at': '2023-01-01T00:00:00',
                'updated_at': '2023-01-01T00:00:00'
            })),
            MagicMock(read=lambda: json.dumps({
                'id': '2',
                'name': 'City Two',
                'country_code': 'CT',
                'created_at': '2023-01-01T00:00:00',
                'updated_at': '2023-01-01T00:00:00'
            }))
        ]
        cities = City.get_all()
        self.assertEqual(len(cities), 2)
        self.assertEqual(cities[0].name, 'City One')
        self.assertEqual(cities[1].name, 'City Two')

    @patch('your_module.data_manager')
    def test_delete_city(self, mock_data_manager):
        City.delete('1234')
        mock_data_manager.delete.assert_called_once_with('1234', 'city')

if __name__ == '__main__':
    unittest.main()
