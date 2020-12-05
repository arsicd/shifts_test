import json
from datetime import datetime

import pytz

from etl.shift_entry import ShiftEntry


class Transformer:
    @classmethod
    def transform(cls, raw_data):
        shift_data = json.loads(raw_data)
        shift_entries = []
        for entry in shift_data:
            shift_entry = ShiftEntry(entry)
            for field in ['breaks', 'allowances', 'award_interpretation']:
                if field in entry:
                    for field_entry in entry[field]:
                        field_entry['shift_id'] = entry['id']
                        field_entry['shift_date'] = entry['date']
                        field_entry['sheet_id'] = entry['timesheet_id']
                    setattr(shift_entry, field, entry[field])
                    del shift_entry.shift[field]

            cls.convert_timezones(shift_entry)

            shift_entries.append(shift_entry)
        return shift_entries

    @staticmethod
    def convert_timezones(shift_entry):
        ts_fields = [
            'start',
            'finish',
            'approved_at',
            'break_start',
            'break_finish'
        ]
        for field in ts_fields:
            if field in shift_entry.shift:
                shift_entry.shift[field] = datetime.fromtimestamp(
                    shift_entry.shift[field],
                    pytz.timezone('EST')
                )

        breaks_ts_fields = [
            'start',
            'finish',
        ]
        for break_entry in shift_entry.breaks:
            for field in breaks_ts_fields:
                if field in break_entry:
                    break_entry[field] = datetime.fromtimestamp(
                        break_entry[field],
                        pytz.timezone('EST')
                    )

        award_interpretation_ts_fields = [
            'from',
            'to',
        ]
        for award_interpretation_entry in shift_entry.award_interpretation:
            for field in award_interpretation_ts_fields:
                if field in award_interpretation_entry:
                    award_interpretation_entry[field] = datetime.fromtimestamp(
                        award_interpretation_entry[field],
                        pytz.timezone('EST')
                    )
