from typing import List

from attr import dataclass

from .location import Location
from .table_cell import TableCell


@dataclass(slots=True)
class TableRow:
    location: Location
    cells: List[TableCell]
