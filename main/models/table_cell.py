from attr import attrib, dataclass

from .location import Location


@dataclass(slots=True)
class TableCell:
    location: Location = attrib(cmp=False)
    value: str
