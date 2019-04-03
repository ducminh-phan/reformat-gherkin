from typing import List

from attr import attrib, dataclass

from .location import Location
from .table_cell import TableCell


@dataclass(slots=True)
class TableRow:
    location: Location = attrib(cmp=False, repr=False)
    cells: List[TableCell]

    def __iter__(self):
        yield self

        yield from self.cells

    def __len__(self):
        return len(self.cells)

    def __getitem__(self, item):
        return self.cells[item]
