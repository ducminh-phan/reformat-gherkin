from typing import List

from .location import Location
from .table_row import TableRow


class DataTable:
    def __init__(self, location: Location, rows: List[TableRow]):
        self.location: Location = location
        self.rows: List[TableRow] = rows
