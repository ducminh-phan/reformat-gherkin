from attr import attrib

from ._base import prepare


@prepare(eq=True)
class Location:
    line: int
    column: int


@prepare
class LocationMixin:
    location: Location = attrib(eq=False, repr=False)
