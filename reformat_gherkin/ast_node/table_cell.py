from attr import attrib

from ._base import prepare
from .location import Location


@prepare
class TableCell:
    location: Location = attrib(cmp=False, repr=False)
    value: str
