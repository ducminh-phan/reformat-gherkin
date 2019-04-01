from itertools import chain
from typing import List

from attr import attrib, dataclass

from .location import Location
from .table_row import TableRow


@dataclass(slots=True)
class DataTable:
    location: Location = attrib(cmp=False)
    rows: List[TableRow]

    def __iter__(self):
        yield self

        yield from chain.from_iterable(self.rows)
