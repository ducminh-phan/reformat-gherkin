from .location import LocationMixin
from .table_row import TableRow


class DataTable(LocationMixin):
    rows: tuple[TableRow, ...]

    def __iter__(self):
        yield self

        yield from self.rows
