from ._base import DescriptionMixin, GherkinString, LocationMixin
from .table_row import TableRow
from .tag import Tag


class Examples(LocationMixin, DescriptionMixin):
    keyword: GherkinString
    name: GherkinString
    tags: tuple[Tag, ...]
    table_body: tuple[TableRow, ...]
    table_header: TableRow | None = None

    def __iter__(self):
        yield from self.tags

        yield self

        if self.table_header is not None:
            yield self.table_header

        yield from self.table_body
