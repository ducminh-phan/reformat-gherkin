from attr import attrib

from ._base import prepare
from .location import Location


@prepare
class DocString:
    location: Location = attrib(cmp=False, repr=False)
    content: str

    def __iter__(self):
        yield self
