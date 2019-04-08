from typing import Optional, Union

from attr import attrib

from ._base import prepare
from .data_table import DataTable
from .doc_string import DocString
from .location import Location


@prepare
class Step:
    location: Location = attrib(cmp=False, repr=False)
    keyword: str
    text: str
    argument: Optional[Union[DataTable, DocString]] = None

    def __iter__(self):
        yield self

        if self.argument is not None:
            yield from self.argument
