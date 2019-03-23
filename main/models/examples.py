from typing import List, Optional

from .location import Location
from .table_row import TableRow
from .tag import Tag


class Examples:
    def __init__(
        self,
        location: Location,
        keyword: str,
        name: str,
        tags: List[Tag],
        table_header: Optional[TableRow] = None,
        table_body: Optional[List[TableRow]] = None,
    ):
        self.location: Location = location
        self.keyword: str = keyword
        self.name: str = name
        self.tags: List[Tag] = tags
        self.table_header: Optional[TableRow] = table_header
        self.table_body: Optional[List[TableRow]] = table_body
