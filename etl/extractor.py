import os
from urllib.parse import urljoin

import requests


class Extractor:
    API_URL = os.getenv('SHIFTS-API-URL')

    def extract_all_users(self):
        response = requests.get(urljoin(self.API_URL, 'users'))
        return response.json()

    def extract_user_shifts(self, users):
        return requests.get(
            urljoin(self.API_URL, 'previous_week_shifts'),
            params=','.join([str(user['id']) for user in users])
        ).text
