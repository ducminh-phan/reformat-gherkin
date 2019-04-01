from attr import attrib, dataclass

from .location import Location


@dataclass(slots=True)
class Tag:
    location: Location = attrib(cmp=False, repr=False)
    name: str
