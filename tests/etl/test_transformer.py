import json
import unittest

from etl.transformer import Transformer


class TestTransformer(unittest.TestCase):
    def test_transform(self):
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


if __name__ == '__main__':
    unittest.main()
