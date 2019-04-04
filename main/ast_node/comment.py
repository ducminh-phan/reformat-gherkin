from attr import attrib

from ._base import prepare
from .location import Location


@prepare
class Comment:
    location: Location = attrib(cmp=False, repr=False)
    text: str
