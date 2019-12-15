from attr import attrib

from ._base import prepare
from .location import Location


@prepare
class DocString:
    location: Location = attrib(eq=False, repr=False)
    content: str

    def __iter__(self):
        yield self
