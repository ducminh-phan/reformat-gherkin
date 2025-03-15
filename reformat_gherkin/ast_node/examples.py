from typing import Optional

from ._base import prepare
from .location import LocationMixin
from .table_row import TableRow
from .tag import Tag


@prepare
class Examples(LocationMixin):
    keyword: str
    name: str
    tags: tuple[Tag, ...]
    description: str
    table_body: tuple[TableRow, ...]
    table_header: Optional[TableRow] = None

    def __iter__(self):
        yield from self.tags

        yield self

        if self.table_header is not None:
            yield self.table_header

        yield from self.table_body
