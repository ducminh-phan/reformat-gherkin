from typing import Tuple

from ._base import prepare
from .location import LocationMixin
from .table_cell import TableCell


@prepare
class TableRow(LocationMixin):
    cells: Tuple[TableCell, ...]

    def __len__(self):
        return len(self.cells)

    def __getitem__(self, item):
        return self.cells[item]
