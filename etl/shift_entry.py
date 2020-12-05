from typing import Dict, List

import attr


@attr.dataclass
class ShiftEntry:
    shift: Dict
    breaks: List[Dict] = attr.Factory(list)
    allowances: List[Dict] = attr.Factory(list)
    award_interpretation: List[Dict] = attr.Factory(list)
