import unittest
import json
import xml.etree.ElementTree as ET
from unittest.mock import patch
from app import app
from tests.mock_data import start_data, end_data, abbreviations_data


class TestApp(unittest.TestCase):
    def setUp(self):
        self.mock_connect_db = patch('app.sqlite3.connect').start()
        self.mock_cursor = self.mock_connect_db().cursor()
        self.mock_read_log_file = patch('f1_report.log_reader.read_log_file', side_effect=[
            start_data.splitlines(),
            end_data.splitlines(),
            abbreviations_data.splitlines()
        ]).start()
        self.addCleanup(self.mock_read_log_file.stop)
        self.addCleanup(self.mock_connect_db.stop)
        self.app = app.test_client()

    def test_get_report_json(self):
        self.mock_cursor.fetchall.return_value = [
            ('Driver 1', 'Team 1', 100.0),
            ('Driver 2', 'Team 2', 110.0)
        ]

        response = self.app.get('/api/v1/report/?format=json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('best_laps', data)
        self.assertIn('invalid_laps', data)

    def test_get_report_xml(self):
        self.mock_cursor.fetchall.return_value = [
            ('Driver 1', 'Team 1', 100.0),
            ('Driver 2', 'Team 2', 110.0)
        ]

        response = self.app.get('/api/v1/report/?format=xml')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/xml')
        root = ET.fromstring(response.data)
        self.assertEqual(root.tag, 'report')

    def test_get_report_invalid_format(self):
        response = self.app.get('/api/v1/report/?format=csv')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
