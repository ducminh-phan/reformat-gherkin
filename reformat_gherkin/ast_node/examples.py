from typing import Optional

from ._base import GherkinString
from .location import LocationMixin
from .table_row import TableRow
from .tag import Tag


class Examples(LocationMixin):
    keyword: GherkinString
    name: GherkinString
    tags: tuple[Tag, ...]
    description: GherkinString
    table_body: tuple[TableRow, ...]
    table_header: Optional[TableRow] = None

    def __iter__(self):
        yield from self.tags

        yield self

        if self.table_header is not None:
            yield self.table_header

        yield from self.table_body
