from typing import List, Optional

import attr

from .location import Location
from .table_row import TableRow
from .tag import Tag


@attr.s(slots=True, auto_attribs=True)
class Examples:
    location: Location
    keyword: str
    name: str
    tags: List[Tag]
    table_header: Optional[TableRow] = None
    table_body: Optional[List[TableRow]] = None
    description: Optional[str] = None
