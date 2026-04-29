from ._base import GherkinString, LocationMixin
from .data_table import DataTable
from .doc_string import DocString


class Step(LocationMixin):
    keyword: GherkinString
    text: GherkinString
    data_table: DataTable | None = None
    doc_string: DocString | None = None

    def __iter__(self):
        yield self

        if self.doc_string is not None:
            yield from self.doc_string

        if self.data_table is not None:
            yield from self.data_table
