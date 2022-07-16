from typing import Optional

from ._base import prepare
from .data_table import DataTable
from .doc_string import DocString
from .location import LocationMixin


@prepare
class Step(LocationMixin):
    keyword: str
    text: str
    data_table: Optional[DataTable] = None
    doc_string: Optional[DocString] = None

    def __iter__(self):
        yield self

        if self.doc_string is not None:
            yield from self.doc_string

        if self.data_table is not None:
            yield from self.data_table
