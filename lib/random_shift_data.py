from datetime import datetime, date, time, timedelta
from typing import List
import random
import copy

import attr


class IdCreator:
    def __init__(self):
        self._id = 0

    def create_id(self):
        self._id += 1
        return self._id


class User:
    @staticmethod
    def get_all_users():
        return [{'id': x} for x in range(1, 16)]


@attr.dataclass
class Timesheet:
    user_id: int
    start: date
    finish: date

    id: int = attr.ib(init=False)
    shifts: List = attr.ib(init=False)

    _id_creator: IdCreator = IdCreator()

    def __attrs_post_init__(self):
        self.id = self._id_creator.create_id()

    def generate_random_shifts(self):
        number_of_shifts = self.get_random_number_of_shifts()
        shift_dates = self.get_random_shift_dates(number_of_shifts)
        self.shifts = []
        for shift_date in shift_dates:
            self.shifts.append(
                Shift.generate_random(self.id, self.user_id, shift_date)
            )

    @staticmethod
    def get_random_number_of_shifts():
        days = [0, 1, 2, 3, 4, 5]
        chances = [0.05, 0.01, 0.01, 0.03, 0.05, 0.85]
        assert sum(chances) == 1

        return random.choices(days, chances, k=1)[0]

    def get_random_shift_dates(self, number_of_shifts):
        days = random.sample(range(5), number_of_shifts)
        days.sort()

        dates = []
        for day in days:
            dates.append(self.start + timedelta(days=day))

        return dates


class Shift:
    _template = {
        'id': 1,
        'timesheet_id': 1,
        'user_id': 1,
        'date': '2020-12-04',
        'start': 1607103885,
        'break_start': 1607111085,
        'break_finish': 1607111445,
        'break_length': 6,
        'breaks': [],
        'finish': 1607125845,
        'status': 'PENDING',
        'allowances': [],
        'tag': 'Default Tag',
        'tag_id': 1,
        'sub_cost_centre': '1',
        'cost': 10.0,
        'award_interpretation': [],
        'department_id': 1,
        'metadata': 'Default metadata',
        'leave_request_id': 1,
        'record_id': 1,
        'approved_by': 1,
        'approved_at': '1607126145',
    }

    _id_creator: IdCreator = IdCreator()

    @classmethod
    def generate_random(
            cls, timesheet_id: int, user_id: int, shift_date: date
    ):
        shift = copy.deepcopy(cls._template)
        shift['id'] = cls._id_creator.create_id()
        shift['timesheet_id'] = timesheet_id
        shift['user_id'] = user_id

        shift['date'] = shift_date.strftime('%Y-%m-%d')

        nine_am = datetime.combine(shift_date, time(9, 0)).timestamp()
        time_offset = random.randrange(- 15 * 60, 15 * 60)
        shift['start'] = nine_am + time_offset

        five_pm = datetime.combine(shift_date, time(17, 0)).timestamp()
        time_offset = random.randrange(- 15 * 60, 15 * 60)
        shift['finish'] = five_pm + time_offset

        six_pm = datetime.combine(shift_date, time(18, 0)).timestamp()
        time_offset = random.randrange(- 15 * 60, 15 * 60)
        shift['approved_at'] = six_pm + time_offset

        a_break = Break.generate_random(shift['id'], shift_date)
        shift['breaks'] = [a_break]
        shift['break_start'] = a_break['start']
        shift['break_finish'] = a_break['finish']
        shift['break_length'] = a_break['length']

        shift['allowances'] = [Allowance.generate_random()]

        shift['award_interpretation'] = [
            AwardInterpretation.generate_random(
                shift['date'], shift['start'], shift['finish']
            )
        ]

        cls.sum_costs(shift)

        return shift

    @staticmethod
    def sum_costs(shift):
        allowance_sum = 0
        for allowance in shift['allowances']:
            allowance_sum += allowance['value'] * allowance['cost']

        award_interpretation_sum = 0
        for award_interpretation in shift['award_interpretation']:
            award_interpretation_sum += award_interpretation['cost']

        shift['cost'] = allowance_sum + award_interpretation_sum
        shift['cost_breakdown'] = {
            'award_cost': award_interpretation_sum,
            'allowance_cost': allowance_sum,
        }


class Break:
    _id_creator: IdCreator = IdCreator()

    @classmethod
    def generate_random(cls, shift_id, shift_date):
        one_pm = datetime.combine(shift_date, time(13, 0)).timestamp()
        time_offset = random.randrange(- 15 * 60, 15 * 60)
        break_length = random.randrange(15 * 60, 30 * 60)
        return {
            'id': cls._id_creator.create_id(),
            'shift_id': shift_id,
            'start': one_pm + time_offset,
            'finish': one_pm + time_offset + break_length,
            'length': round(break_length / 60),
            'paid': True
        }


class Allowance:
    _template = {
        'id': 1,
        'name': 'Default Allowance',
        'value': 1.0,
        'cost': 11.8
    }

    _id_creator: IdCreator = IdCreator()

    @classmethod
    def generate_random(cls):
        allowance = copy.deepcopy(cls._template)
        allowance['id'] = cls._id_creator.create_id()
        allowance['value'] = random.choice([0.5, 1.0])
        return allowance


class AwardInterpretation:
    _template = {
        'units': 6.45,
        'date': '2016-02-29',
        'export_name': 'ORD 1x',
        'secondary_export_name': 'LOAD',
        'ordinary_hours': True,
        'cost': 16.125,
        'from': 1456902000,
        'to': 1456916400
    }
    _id_creator: IdCreator = IdCreator()

    @classmethod
    def generate_random(cls, shift_date, start, finish):
        award = copy.deepcopy(cls._template)
        award['id'] = cls._id_creator.create_id()
        award['date'] = shift_date
        award['units'] = round((finish - start) / 60 / 60, 4)
        hour_cost = random.randrange(100, 200, 1) / 10
        award['cost'] = award['units'] * hour_cost

        return award
