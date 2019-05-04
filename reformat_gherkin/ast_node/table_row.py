from typing import Tuple

from attr import attrib

from ._base import prepare
from .location import Location
from .table_cell import TableCell


@prepare
class TableRow:
    location: Location = attrib(cmp=False, repr=False)
    cells: Tuple[TableCell, ...]

    def __len__(self):
        return len(self.cells)

    def __getitem__(self, item):
        return self.cells[item]
