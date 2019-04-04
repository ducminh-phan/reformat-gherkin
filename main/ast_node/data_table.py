from typing import Tuple

from attr import attrib

from ._base import prepare
from .location import Location
from .table_row import TableRow


@prepare
class DataTable:
    location: Location = attrib(cmp=False, repr=False)
    rows: Tuple[TableRow, ...]

    def __iter__(self):
        yield self

        yield from self.rows
