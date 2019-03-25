from typing import Optional

import attr

from .data_table import DataTable
from .location import Location


@attr.s(slots=True, auto_attribs=True)
class Step:
    location: Location
    keyword: str
    text: str
    argument: Optional[DataTable] = None
