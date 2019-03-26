from typing import List

from attr import dataclass

from .location import Location
from .table_row import TableRow


@dataclass(slots=True)
class DataTable:
    location: Location
    rows: List[TableRow]
