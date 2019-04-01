from itertools import chain
from typing import List, Optional

from attr import attrib, dataclass

from .location import Location
from .table_row import TableRow
from .tag import Tag


@dataclass(slots=True)
class Examples:
    location: Location = attrib(cmp=False)
    keyword: str
    name: str
    tags: List[Tag]
    table_header: Optional[TableRow] = None
    table_body: Optional[List[TableRow]] = None
    description: Optional[str] = None

    def __iter__(self):
        yield from self.tags

        yield self

        if self.table_header is not None:
            yield from self.table_header

        if self.table_body is not None:
            yield from chain.from_iterable(self.table_body)
