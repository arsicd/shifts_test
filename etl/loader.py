import os
from typing import List

from pymongo import MongoClient

from etl.shift_entry import ShiftEntry


class Loader:

    def __init__(self):
        self.db = self.get_db()

    @staticmethod
    def get_db():
        client = MongoClient(os.getenv('MONGO-URI'))
        return client.shifts

    def load_into_db(self, shift_entries: List[ShiftEntry]):
        for shift_entry in shift_entries:
            self.db.shifts.insert_one(shift_entry.shift)
            for break_entry in shift_entry.breaks:
                self.db.shift_breaks.insert_one(break_entry)
            for allowance_entry in shift_entry.allowances:
                self.db.shift_allowances.insert_one(allowance_entry)
            for award_interpretation_entry in shift_entry.award_interpretation:
                self.db.shift_award_interpretation.insert_one(
                    award_interpretation_entry
                )
