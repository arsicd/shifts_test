import json

from etl.shift_entry import ShiftEntry


class Transformer:
    @staticmethod
    def transform(raw_data):
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
            shift_entries.append(shift_entry)
        return shift_entries
