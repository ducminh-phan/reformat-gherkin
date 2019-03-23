from typing import List

import attr

from .location import Location
from .table_row import TableRow


@attr.s(slots=True, auto_attribs=True)
class DataTable:
    location: Location
    rows: List[TableRow]
