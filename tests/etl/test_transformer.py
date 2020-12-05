import json
import unittest
from datetime import datetime

import pytz

from etl.transformer import Transformer


class TestTransformer(unittest.TestCase):
    def test_transform_arrays(self):
        transformer = Transformer()
        shift_data = [
            {
                'id': 2,
                'date': '2020-11-23',
                'timesheet_id': 1,
                'breaks': [
                    {
                        'id': 5,
                    }
                ],
            }
        ]

        transformed_data = transformer.transform(json.dumps(shift_data))

        self.assertEqual(len(transformed_data), 1)
        self.assertEqual(len(transformed_data[0].breaks), 1)

    def test_transform_timezone(self):
        transformer = Transformer()
        shift_data = [
            {
                'id': 2,
                'date': '2020-11-23',
                'timesheet_id': 1,
                'start': 1606118459,
                'breaks': [
                    {
                        'id': 5,
                        'start': 1606132166
                    }
                ]
            }
        ]

        transformed_data = transformer.transform(json.dumps(shift_data))

        expected = datetime(2020, 11, 23, 3, 0, 59, 0, pytz.timezone('EST'))
        self.assertEqual(transformed_data[0].shift['start'], expected)
        expected = datetime(2020, 11, 23, 6, 49, 26, 0, pytz.timezone('EST'))
        self.assertEqual(transformed_data[0].breaks[0]['start'], expected)


if __name__ == '__main__':
    unittest.main()
