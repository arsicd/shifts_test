from pymongo import MongoClient


class Loader:

    def __init__(self):
        self.db = self.get_db()

    def get_db(self):
        client = MongoClient()
        return client.shifts

    def load_into_db(self, shifts):
        for shift in shifts:
            self.db.shifts.insert_one(shift)
