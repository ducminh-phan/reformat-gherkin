from typing import Optional

from attr import attrib

from ._base import prepare
from .data_table import DataTable
from .location import Location


@prepare
class Step:
    location: Location = attrib(cmp=False, repr=False)
    keyword: str
    text: str
    argument: Optional[DataTable] = None

    def __iter__(self):
        yield self

        if self.argument is not None:
            yield from self.argument
