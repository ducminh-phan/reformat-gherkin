from attr import dataclass

from .location import Location


@dataclass(slots=True)
class Comment:
    location: Location
    text: str
