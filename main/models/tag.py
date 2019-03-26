from attr import dataclass

from .location import Location


@dataclass(slots=True)
class Tag:
    location: Location
    name: str
