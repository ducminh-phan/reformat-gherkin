from typing import List

from .location import Location
from .table_cell import TableCell


class TableRow:
    def __init__(self, location: Location, cells: List[TableCell]):
        self.location: Location = location
        self.cells: List[TableCell] = cells
