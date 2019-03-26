from attr import dataclass

from .location import Location


@dataclass(slots=True)
class TableCell:
    location: Location
    value: str
