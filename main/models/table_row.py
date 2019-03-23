from typing import List

import attr

from .location import Location
from .table_cell import TableCell


@attr.s(slots=True, auto_attribs=True)
class TableRow:
    location: Location
    cells: List[TableCell]
