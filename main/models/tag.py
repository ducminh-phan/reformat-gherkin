from attr import attrib, dataclass

from .location import Location


@dataclass(slots=True)
class Tag:
    location: Location = attrib(cmp=False)
    name: str
