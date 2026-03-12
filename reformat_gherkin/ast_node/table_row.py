from ._base import LocationMixin
from .table_cell import TableCell


class TableRow(LocationMixin):
    cells: tuple[TableCell, ...]

    def __len__(self):
        return len(self.cells)

    def __getitem__(self, item):
        return self.cells[item]
