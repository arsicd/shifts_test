import os
import json
import unittest
from unittest.mock import patch

import mongomock

from etl.runner import Runner


class TestRunner(unittest.TestCase):

    @patch('etl.extractor.Extractor.extract_all_users')
    @patch('etl.extractor.Extractor.extract_user_shifts')
    @patch('etl.loader.Loader.get_db')
    def test_run(self, db_mock, shifts_mock, users_mock):

        path = os.path.join('tests/data', 'users_response.json')
        with open(path, 'r') as file:
            users_response = json.loads(file.read())

        path = os.path.join('tests/data', 'previous_week_shifts_response.json')
        with open(path, 'r') as file:
            previous_week_shifts_response = file.read()

        mock_db = mongomock.MongoClient().shifts

        db_mock.return_value = mock_db
        users_mock.return_value = users_response
        shifts_mock.return_value = previous_week_shifts_response

        Runner.run()

        all_shifts = list(mock_db.shifts.find())

        self.assertEqual(len(all_shifts), 5)
