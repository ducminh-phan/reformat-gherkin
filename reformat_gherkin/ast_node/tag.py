from attr import attrib

from ._base import prepare
from .location import Location


@prepare
class Tag:
    location: Location = attrib(eq=False, repr=False)
    name: str
