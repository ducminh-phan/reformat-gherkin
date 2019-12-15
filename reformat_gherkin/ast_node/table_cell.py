from attr import attrib

from ._base import prepare
from .location import Location


@prepare
class TableCell:
    location: Location = attrib(eq=False, repr=False)
    value: str
