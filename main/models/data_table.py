from typing import List

from attr import attrib, dataclass

from .location import Location
from .table_row import TableRow


@dataclass(slots=True)
class DataTable:
    location: Location = attrib(cmp=False)
    rows: List[TableRow]
