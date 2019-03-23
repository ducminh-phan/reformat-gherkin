import attr

from .location import Location


@attr.s(slots=True, auto_attribs=True)
class TableCell:
    location: Location
    value: str
