from typing import List, Optional

from attr import dataclass

from .location import Location
from .table_row import TableRow
from .tag import Tag


@dataclass(slots=True)
class Examples:
    location: Location
    keyword: str
    name: str
    tags: List[Tag]
    table_header: Optional[TableRow] = None
    table_body: Optional[List[TableRow]] = None
    description: Optional[str] = None
