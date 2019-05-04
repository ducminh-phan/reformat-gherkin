from typing import Optional, Tuple

from attr import attrib

from ._base import prepare
from .location import Location
from .table_row import TableRow
from .tag import Tag


@prepare
class Examples:
    location: Location = attrib(cmp=False, repr=False)
    keyword: str
    name: str
    tags: Tuple[Tag, ...]
    table_header: Optional[TableRow] = None
    table_body: Optional[Tuple[TableRow, ...]] = None
    description: Optional[str] = None

    def __iter__(self):
        yield from self.tags

        yield self

        if self.table_header is not None:
            yield self.table_header

        if self.table_body is not None:
            yield from self.table_body
