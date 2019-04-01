from typing import List

from attr import attrib, dataclass

from .location import Location
from .table_cell import TableCell


@dataclass(slots=True)
class TableRow:
    location: Location = attrib(cmp=False)
    cells: List[TableCell]

    def __iter__(self):
        yield self

        yield from self.cells
